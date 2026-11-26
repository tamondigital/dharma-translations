# CLAUDE.md

A static site (Astro) that renders mani's provisional canon translations. Human overview and commands: README.md.

## Model routing

No job in this repo calls a model. `scripts/export.py` and the build are deterministic. Do not add a model call or an agent here without a human decision: the translations are certified upstream and must stay as exported.

## Rules

- `export.py` reads `../../mani` and never writes there. Translation fixes happen in mani, never in `content/`.
- `content/` holds only fully certified texts; never commit `content-preview/` or hand-edit `content/`.
- Committing a new export to `content/` and deploying is a publish decision: the owner's, not the agent's.
- Every page keeps the AI-generated label and the link to the method page.
- Links to dharma-notes are URLs only; never import code or data from that repo.
