#!/usr/bin/env python3
"""Snapshot mani's provisional canon translations into this site.

Reads (never writes) <mani>/reference/translation/provisional/:
  <T-id>.tsv                         seg · zh · en · basis · flags
  <T-id>.meta.json                   lectures + sections
  <T-id>.glossary.tsv                the reader's guide and term notes (id · kind · zh · term · sense · defined ·
                                     teacher · cite · flags); a row is certified under its id, h = sha1 of
                                     term..flags joined by tabs
  review/<T-id>/certification.json   {seg: {status, note, h, at}}, h = sha1(en)[:10]
  METHOD.md

  review/<T-id>/ai-review.json       {id: {verdict: pass|flag, reason, h, model, at}}, the AI reviewer's

A line or glossary row is cleared for the site when the owner certified it, or, with no owner's mark, the AI
reviewer passed it; either mark must hold the hash of the current text (a changed line is not cleared).
Writes content/ (committed, deployed): a text only when every line is cleared, and only its cleared glossary rows.
Each exported row carries `review`: "owner" | "ai" | "draft" (draft only under --preview).
The teacher's evidence per line (his transcript lines and study-note rows) comes from mani's
pipelines/knowledgebase/src/provisional_evidence.py, imported read-only.
--preview writes every text to content-preview/ (gitignored) for `npm run preview:dev`; it never touches content/.
A text needs an entry in site.config.json `texts` (slug, English title) to be exported at all.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
MANI = (ROOT / CFG["mani"]).resolve()
PROV = MANI / "reference" / "translation" / "provisional"
sys.path.insert(0, str(MANI / "pipelines" / "knowledgebase"))
from src import provisional_evidence as pe  # noqa: E402
CITE = re.compile(r"(?<![\d–-])(\d{2}) 行(\d+(?:[–-]\d+)?(?:, \d+(?:[–-]\d+)?)*)")
LESSON_NO = re.compile(r"(\d{2})\D*學習筆記\.md$")
TID = re.compile(r"^T\d{4}[A-Za-z]?$")
GLOSSARY_COLS = ["id", "kind", "zh", "term", "sense", "defined", "teacher", "cite", "flags"]


def review_of(rid: str, h: str, ah: str, certs: dict, ai: dict) -> str:
    """"owner" | "ai" | "draft": the owner's mark (hash h) outranks the AI reviewer's (hash ah); a mark on other text
    does not count."""
    c = certs.get(rid)
    if c and c.get("h") == h:
        return "owner" if c.get("status") == "certified" else "draft"
    v = ai.get(rid)
    return "ai" if v and v.get("h") == ah and v.get("verdict") == "pass" else "draft"


def read_tsv(p: Path) -> tuple[list[str], list[dict]]:
    head, segs = [], []
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            head.append(line.lstrip("# "))
            continue
        c = line.split("\t")
        if len(c) < 3 or c[0] == "seg":
            continue
        c += [""] * (5 - len(c))
        segs.append({"id": c[0], "zh": c[1], "en": c[2], "basis": c[3], "flags": c[4]})
    return head, segs


def noted_lessons(lecture: dict) -> set[str]:
    d = MANI / "notes" / lecture["channel"] / lecture["playlist"]
    return {m.group(1) for f in d.glob("*學習筆記.md") if (m := LESSON_NO.search(f.name))} if d.is_dir() else set()


def basis_parts(basis: str, lecture: dict | None, noted: set[str]) -> list[dict]:
    """A basis or flags text as [{t}, {t, href}]: each `NN 行a–b` becomes 'lecture NN, lines a–b' with every range
    linked to that line of the lecture's transcript on dharma-notes, when the lecture has a note."""
    out, i = [], 0
    for m in CITE.finditer(basis):
        if m.start() > i:
            out.append({"t": basis[i:m.start()]})
        no = m.group(1)
        out.append({"t": f"lecture {no}, lines "})
        for k, rng in enumerate(m.group(2).split(", ")):
            if k:
                out.append({"t": ", "})
            first = re.split(r"[–-]", rng)[0]
            if lecture and no in noted:
                href = f"{CFG['dharma_notes']}/{lecture['channel']}/{lecture['playlist']}/{no}/transcript/#L{first}"
                out.append({"t": rng.replace("-", "–"), "href": href})
            else:
                out.append({"t": rng})
        i = m.end()
    if i < len(basis):
        out.append({"t": basis[i:]})
    return out


def attach_terms(segs: list[dict], terms: list[dict]) -> None:
    """Each segment gets en_parts [{t}, {t, term: id}]: a term's phrase is marked at its first occurrence in reading
    order (a phrase already inside another term's mark is not marked again); the term records that segment."""
    marks = {}
    for g in terms:
        for s in segs:
            i = s["en"].find(g["term"])
            taken = marks.get(s["id"], [])
            if i >= 0 and all(i + len(g["term"]) <= a or i >= b for a, b, _ in taken):
                marks.setdefault(s["id"], []).append((i, i + len(g["term"]), g["id"]))
                g["first_seg"] = s["id"]
                break
    for s in segs:
        parts, pos = [], 0
        for a, b, gid in sorted(marks.get(s["id"], [])):
            if a > pos:
                parts.append({"t": s["en"][pos:a]})
            parts.append({"t": s["en"][a:b], "term": gid})
            pos = b
        if pos < len(s["en"]):
            parts.append({"t": s["en"][pos:]})
        s["en_parts"] = parts


def method_md(published: dict[str, str]) -> str:
    """METHOD.md with its repo-relative links resolved: a published text's .tsv → its page; anything else
    inside mani (private) → plain text."""
    md = (PROV / "METHOD.md").read_text(encoding="utf-8")

    def link(m: re.Match) -> str:
        label, target = m.group(1), m.group(2)
        if re.match(r"https?://", target):
            return m.group(0)
        tid = Path(target).stem
        if target.endswith(".tsv") and tid in published:
            return f"[{label}](../{published[tid]}/)"
        return label

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, md)


def export(preview: bool) -> int:
    out = ROOT / ("content-preview" if preview else "content")
    if out.exists():
        shutil.rmtree(out)
    (out / "texts").mkdir(parents=True)
    index, published = [], {}
    for tsv in sorted(p for p in PROV.glob("T*.tsv") if TID.match(p.stem)):
        tid = tsv.stem
        site = CFG["texts"].get(tid)
        if not site:
            print(f"{tid}: no entry in site.config.json texts — skipped")
            continue
        head, segs = read_tsv(tsv)
        meta = json.loads((PROV / f"{tid}.meta.json").read_text(encoding="utf-8"))
        rev = PROV / "review" / tid
        load = lambda f: json.loads((rev / f).read_text(encoding="utf-8")) if (rev / f).is_file() else {}
        certs, ai = load("certification.json"), load("ai-review.json")
        for s in segs:
            s["review"] = review_of(s["id"], pe.en_hash(s["en"]), pe.line_hash(s["en"], s["basis"], s["flags"]), certs, ai)
        n_cert = sum(s["review"] != "draft" for s in segs)
        n_owner = sum(s["review"] == "owner" for s in segs)
        complete = n_cert == len(segs) and segs
        print(f"{tid}: {n_cert}/{len(segs)} lines cleared ({n_owner} by the owner, {n_cert - n_owner} by the AI reviewer)"
              + ("" if complete else " — not published"))
        if not complete and not preview:
            continue
        lecture = (meta.get("lectures") or [None])[0]
        noted = noted_lessons(lecture) if lecture else set()
        ev = pe.segment_evidence(segs, lecture, MANI / "notes") if lecture else {}
        tx = lambda les, a: f"{CFG['dharma_notes']}/{lecture['channel']}/{lecture['playlist']}/{les}/transcript/#L{a}"
        for s in segs:
            e = ev.get(s["id"], {"basis": [], "notes": []})
            s["words"] = [dict(w, href=tx(w["lesson"], w["a"])) for w in e["basis"] if w["lines"]]
            s["notes"] = [dict(n, href=tx(n["lesson"], n["a"]) if n["a"] else None) for n in e["notes"]]
            s["basis_parts"] = basis_parts(s["basis"], lecture, noted)
            s["flags_parts"] = basis_parts(s["flags"], lecture, noted)
        rows = pe.read_glossary(PROV / f"{tid}.glossary.tsv")
        for g in rows:
            g["review"] = review_of(g["id"], g["h"], g["h"], certs, ai)
            g["words"] = [dict(w, href=tx(w["lesson"], w["a"])) for w in pe.cited_words(lecture, g["cite"]) if w["lines"]] \
                if lecture else []
            g["teacher"] = [x.strip() for x in g["teacher"].split("¶") if x.strip()]
            g["cite_parts"] = basis_parts(g["cite"], lecture, noted)
            g["flags_parts"] = basis_parts(g["flags"], lecture, noted)
            g["defined_first"] = (re.findall(r"[A-Z]\d{2}", g["defined"]) or [None])[0]
        rows = [g for g in rows if g["review"] != "draft" or preview]
        print(f"{tid}: {sum(g['review'] != 'draft' for g in rows)} cleared glossary/guide row(s) exported"
              + (f", {sum(g['review'] == 'draft' for g in rows)} draft (preview)" if preview else ""))
        terms = [g for g in rows if g["kind"] == "term"]
        attach_terms(segs, terms)
        sections, by_start, cur = [], {x["start"]: x for x in meta.get("sections", [])}, None
        for s in segs:
            if s["id"] in by_start or cur is None:
                cur = dict(by_start.get(s["id"], {"en": "Text", "zh": ""}), segs=[])
                sections.append(cur)
            cur["segs"].append(s)
        title_zh = re.sub(r"^T\d+\w? | \(.*\)$", "", head[0].split(" — ")[0]) if head else tid
        dates = [c["at"] for c in list(certs.values()) + list(ai.values()) if c.get("at")]
        text = {
            "id": tid, **site, "title_zh": title_zh, "lectures": meta.get("lectures", []),
            "certified": bool(complete), "certified_at": max(dates)[:10] if complete and dates else None,
            "n_segs": len(segs), "n_certified": n_cert, "n_owner": n_owner, "sections": sections,
            "guide": [g for g in rows if g["kind"] == "guide"], "glossary": terms,
            "tsv": tsv.read_text(encoding="utf-8"),
        }
        (out / "texts" / f"{tid}.json").write_text(json.dumps(text, ensure_ascii=False, indent=1), encoding="utf-8")
        published[tid] = site["slug"]
        index.append({k: text[k] for k in ("id", "slug", "title_en", "title_zh", "title_pinyin", "author_en",
                                            "teacher_en", "certified", "certified_at", "n_segs", "n_certified", "n_owner")})
    (out / "index.json").write_text(json.dumps({"preview": preview, "texts": index}, ensure_ascii=False, indent=1),
                                    encoding="utf-8")
    (out / "method.md").write_text(method_md(published), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}/: {len(index)} text(s)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--preview", action="store_true", help="every text, certified or not, to content-preview/")
    if not PROV.is_dir():
        sys.exit(f"no mani checkout at {MANI}")
    sys.exit(export(ap.parse_args().preview))
