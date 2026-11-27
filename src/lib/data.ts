import { readFileSync, readdirSync, existsSync } from "node:fs";

// PREVIEW=1 reads content-preview/ (every text, certified or not; never deployed). The deploy builds content/,
// which scripts/export.py fills with fully certified texts only.
const DIR = new URL(process.env.PREVIEW ? "../../content-preview/" : "../../content/", import.meta.url);
const cfg = JSON.parse(readFileSync(new URL("../../site.config.json", import.meta.url), "utf-8"));

export const site = { title: cfg.title as string, tagline: cfg.tagline as string, notes: cfg.dharma_notes as string };
export const base = import.meta.env.BASE_URL.replace(/\/$/, "");
export const url = (p: string) => `${base}/${p.replace(/^\//, "")}`;

export interface Part { t: string; href?: string; term?: string }
export type Review = "owner" | "ai" | "ai-resolved" | "draft";
export interface Words { lesson: string; a: number; b: number; lines: { n: number; text: string }[]; href: string }
export interface NoteRow { lesson: string; quote: string; explanation: string; a: number; b: number; words: { n: number; text: string }[]; href: string | null }
export interface Seg { id: string; zh: string; en: string; basis: string; flags: string; review: Review; basis_parts: Part[]; flags_parts: Part[]; en_parts: Part[]; words: Words[]; notes: NoteRow[]; resolution: string | null; reviewers: string[] }
export interface Gloss {
  id: string; kind: "guide" | "term"; zh: string; term: string; sense: string; defined: string; defined_first: string | null;
  teacher: string[]; cite: string; cite_parts: Part[]; flags: string; flags_parts: Part[]; review: Review; first_seg?: string; words: Words[]; resolution: string | null; reviewers: string[];
}
export interface Section { start: string; en: string; zh: string; segs: Seg[] }
export interface Lecture { teacher: string; channel: string; playlist: string }
export interface Text {
  id: string; slug: string; title_en: string; title_zh: string; title_pinyin: string; author_en: string; teacher_en: string;
  lectures: Lecture[]; certified: boolean; certified_at: string | null; n_segs: number; n_certified: number; n_owner: number; reviewers: string[];
  sections: Section[]; tsv: string; guide: Gloss[]; glossary: Gloss[];
}

const read = (p: string) => JSON.parse(readFileSync(new URL(p, DIR), "utf-8"));
export const index: { preview: boolean; texts: Omit<Text, "sections" | "lectures" | "tsv" | "guide" | "glossary">[] } =
  existsSync(new URL("index.json", DIR)) ? read("index.json") : { preview: false, texts: [] };
export const preview = index.preview;
export const texts: Text[] = existsSync(new URL("texts/", DIR))
  ? readdirSync(new URL("texts/", DIR)).filter((f) => f.endsWith(".json")).sort().map((f) => read(`texts/${f}`))
  : [];
export const methodMd: string = existsSync(new URL("method.md", DIR)) ? readFileSync(new URL("method.md", DIR), "utf-8") : "";
