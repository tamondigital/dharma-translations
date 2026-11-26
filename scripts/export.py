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

Writes content/ (committed, deployed). A text is exported only when every segment is certified and every
mark's hash matches the current English: an uncertified or changed line keeps the whole text off the site.
A glossary or guide row is exported only when it is certified and unchanged; the rest are left out.
--preview writes every text to content-preview/ (gitignored) for `npm run preview:dev`; it never touches content/.
A text needs an entry in site.config.json `texts` (slug, English title) to be exported at all.
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
MANI = (ROOT / CFG["mani"]).resolve()
PROV = MANI / "reference" / "translation" / "provisional"
CITE = re.compile(r"(?<![\d–-])(\d{2}) 行(\d+(?:[–-]\d+)?(?:, \d+(?:[–-]\d+)?)*)")
LESSON_NO = re.compile(r"(\d{2})\D*學習筆記\.md$")
TID = re.compile(r"^T\d{4}[A-Za-z]?$")
GLOSSARY_COLS = ["id", "kind", "zh", "term", "sense", "defined", "teacher", "cite", "flags"]


def en_hash(en: str) -> str:
    return hashlib.sha1(en.encode("utf-8")).hexdigest()[:10]


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


def read_glossary(tid: str) -> list[dict]:
    p = PROV / f"{tid}.glossary.tsv"
    out = []
    for line in (p.read_text(encoding="utf-8").splitlines() if p.is_file() else []):
        if line.startswith("#") or line.startswith("id\t") or not line.strip():
            continue
        c = line.split("\t")
        c += [""] * (len(GLOSSARY_COLS) - len(c))
        out.append(dict(zip(GLOSSARY_COLS, c), h=en_hash("\t".join(c[3:9]))))
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
        cert_p = PROV / "review" / tid / "certification.json"
        certs = json.loads(cert_p.read_text(encoding="utf-8")) if cert_p.is_file() else {}
        n_cert = 0
        for s in segs:
            c = certs.get(s["id"])
            s["certified"] = bool(c and c.get("status") == "certified" and c.get("h") == en_hash(s["en"]))
            n_cert += s["certified"]
        complete = n_cert == len(segs) and segs
        print(f"{tid}: {n_cert}/{len(segs)} lines certified" + ("" if complete else " — not published"))
        if not complete and not preview:
            continue
        lecture = (meta.get("lectures") or [None])[0]
        noted = noted_lessons(lecture) if lecture else set()
        for s in segs:
            s["basis_parts"] = basis_parts(s["basis"], lecture, noted)
            s["flags_parts"] = basis_parts(s["flags"], lecture, noted)
        rows = read_glossary(tid)
        for g in rows:
            c = certs.get(g["id"])
            g["certified"] = bool(c and c.get("status") == "certified" and c.get("h") == g["h"])
            g["teacher"] = [x.strip() for x in g["teacher"].split("¶") if x.strip()]
            g["cite_parts"] = basis_parts(g["cite"], lecture, noted)
            g["flags_parts"] = basis_parts(g["flags"], lecture, noted)
            g["defined_first"] = (re.findall(r"[A-Z]\d{2}", g["defined"]) or [None])[0]
        rows = [g for g in rows if g["certified"] or preview]
        print(f"{tid}: {sum(g['certified'] for g in rows)} certified glossary/guide row(s) exported"
              + (f", {sum(not g['certified'] for g in rows)} uncertified (preview)" if preview else ""))
        terms = [g for g in rows if g["kind"] == "term"]
        attach_terms(segs, terms)
        sections, by_start, cur = [], {x["start"]: x for x in meta.get("sections", [])}, None
        for s in segs:
            if s["id"] in by_start or cur is None:
                cur = dict(by_start.get(s["id"], {"en": "Text", "zh": ""}), segs=[])
                sections.append(cur)
            cur["segs"].append(s)
        title_zh = re.sub(r"^T\d+\w? | \(.*\)$", "", head[0].split(" — ")[0]) if head else tid
        dates = [c["at"] for c in certs.values() if c.get("at")]
        text = {
            "id": tid, **site, "title_zh": title_zh, "lectures": meta.get("lectures", []),
            "certified": bool(complete), "certified_at": max(dates)[:10] if complete and dates else None,
            "n_segs": len(segs), "n_certified": n_cert, "sections": sections,
            "guide": [g for g in rows if g["kind"] == "guide"], "glossary": terms,
            "tsv": tsv.read_text(encoding="utf-8"),
        }
        (out / "texts" / f"{tid}.json").write_text(json.dumps(text, ensure_ascii=False, indent=1), encoding="utf-8")
        published[tid] = site["slug"]
        index.append({k: text[k] for k in ("id", "slug", "title_en", "title_zh", "title_pinyin", "author_en",
                                            "teacher_en", "certified", "certified_at", "n_segs", "n_certified")})
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
