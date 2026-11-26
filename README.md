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
gh workflow run deploy.yml  # manual until the first public deploy is approved; then deploys run on push
```

Publishing is the owner's decision: a text reaches `content/` only once every line is marked certified in the
mani webui 譯經 tab and `review/<T-id>/certification.json` is committed there. A text also needs an entry in
`site.config.json` → `texts` (URL slug, English title, pinyin, author).

## Preview (local only)

```bash
npm run export:preview      # every text, certified or not → content-preview/ (gitignored)
npm run preview:dev         # http://localhost:4321/dharma-translations/ with a "local preview" bar, noindex
```

## Pages

- `/` texts · `/method/` mani's METHOD.md (links into the private mani repo become plain text)
- `/<slug>/` one text: Chinese beside English per line; *Why this reading* shows the teacher's reading,
  each `NN 行a–b` linked to that line of the lecture transcript on dharma-notes, and the flags
- `/files/<T-id>.tsv` the source file, CC BY-NC-SA 4.0

Links to dharma-notes are by URL only (`dharma_notes` in `site.config.json`); no code is shared between the sites.
