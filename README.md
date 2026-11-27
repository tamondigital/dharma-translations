# dharma-translations

Provisional English of Chinese Buddhist texts, published at **https://tiedy.com/dharma-translations/**.
The translations are made and certified in mani (`reference/translation/provisional/`, runbook `docs/SYSTEM.md` §4.6);
this repo only snapshots and renders them. The repo name is the URL path: renaming the repo moves every URL.

## Publish

```bash
npm install                 # once
npm run export              # mani → content/: only texts whose every line is certified (and unchanged since)
npm run build               # → dist/, to check locally
git add content && git commit -m "export: <T-id>" -- content
git push
gh workflow run deploy.yml  # a manual redeploy; every push to main deploys on its own
```

Publishing is the owner's decision, and every push to `main` deploys, so push only what the owner has approved.
A text reaches `content/` only once every line is cleared in mani: certified by the owner in the webui 譯經 tab
(`review/<T-id>/certification.json`), passed by the AI reviewers (both, once a text has a second review), or its
flags answered in writing (`review/<T-id>/resolutions.json`) — and unchanged since. A text also needs an entry in
`site.config.json` → `texts` (URL slug, English title, pinyin, author).

## Preview (local only)

```bash
npm run export:preview      # every text, certified or not → content-preview/ (gitignored)
npm run preview:dev         # http://localhost:4321/dharma-translations/ with a "local preview" bar, noindex
```

## Pages

- `/` texts · `/method/` mani's METHOD.md (links into the private mani repo become plain text)
- `/<slug>/` one text in three views (`?view=read|bilingual|how`, remembered per browser): Read = the English alone with the reading guide and term notes (a marked term opens its note; the glossary closes the page); Side by side = Chinese beside English per line; a line the Chinese allows to be read another way carries an "another reading" mark that opens it; How it was made = side by side plus *Why this reading*: the teacher's reading,
  each `NN 行a–b` linked to that line of the lecture transcript on dharma-notes, and the flags
- `/files/<T-id>.tsv` the source file, CC BY-NC-SA 4.0

Links to dharma-notes are by URL only (`dharma_notes` in `site.config.json`); no code is shared between the sites.

## Look and layout

The site follows the shared **tiedy theme** (`../tamondigital.github.io/theme/`, see its README): the same header,
phone menu, text size and light/dark controls as 講經筆記. On a wide screen a text page has the 目次 rail on the left;
on a phone the same list opens from the 目次 button in the toolbar above the text, and a term's note opens as a
bottom sheet. After the theme changes: `npm run theme`, then rebuild.
