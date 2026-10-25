# CLAUDE.md

The AllSense docs site (https://docs.allsense.otterbridge.org/): MkDocs Material, Markdown in `docs/`, theme overrides in `docs/overrides/`, styles in `docs/stylesheets/extra.css`, the `tools/mkdocs_llms.py` hook (llms.txt, llms-full.txt, a `.md` per page, the "Copy page" menu). Hosted on GitHub Pages: `.github/workflows/ci.yml` builds on every push and pull request and publishes pushes to main (custom domain in Settings → Pages; Squarespace DNS CNAME docs.allsense → wen-da-ng.github.io). Netlify was dropped 2026-10-24 (out of credit). Public, MIT (names, logo and screenshots excluded).

## Working here

- **The user makes every commit and push.** Edit files and build, then hand over: what changed, the build result, and a one-line commit message suggestion. Never run `git commit`, `git push`, tags or releases; add no Co-Authored-By line unless asked.
- **Public repository and public site:** never write the user's serials, IPs, Wi-Fi details, home location, tokens or file paths into it. Screenshots: never of a connect guide or Settings → Server (they show the pairing token); Location shots only with coordinates hidden. Machine facts go in `CLAUDE.local.md` (git-ignored).
- **Copies:** `docs/{PROTOCOL,TEMPLATES,RECORDING,MQTT}.md` come from the protocol repo's `spec/`, `examples/` from the library repos. Never edit them here: change the source repo, then `python tools/sync.py`.

## Build

```bash
.venv/Scripts/mkdocs build --strict     # must pass: broken links, missing pages and missing snippet files fail it
python tools/sync.py --check            # copies match the sibling repos
```

Setup: `python -m venv .venv && .venv/Scripts/pip install --require-hashes -r tools/docs-requirements.txt`. The user previews with `mkdocs serve`.
Dependencies: `tools/docs-requirements.in` holds the two top-level pins; `tools/docs-requirements.txt` is the hash-locked list CI installs (`--require-hashes`). After changing the `.in`, regenerate: `uv pip compile tools/docs-requirements.in --universal --python-version 3.12 --generate-hashes -o tools/docs-requirements.txt`, then check a fresh venv installs it and `mkdocs build --strict` passes. Workflow actions are pinned to commit SHAs (version in a trailing comment); Dependabot (`.github/dependabot.yml`) proposes weekly updates for both.

## Style

- Page layout: title → one-line lead (`{ .lead }`) → time/needs chips (`ob-meta`) → `!!! robot "For example"` card → **The shortest way** as numbered steps (`<div class="steps" markdown>`) → Details → Reference table. Short sentences; every page has `description:` front matter (it feeds llms.txt).
- Say what a feature is *for* (a concrete robot example) before how it works. App places by their UI names: Home, Sensors → <page>, Robot → <card>, Connect → <guide>, Settings.
- The app is closed source: no app code paths or build steps here; installing means the APK from the home repo's releases.

## Still to do

- Reference pages for the Python API, the ROS bridge and the Arduino library.
- Retake the Location and Hardware screenshots (they predate the redesign); screenshots are taken with the app repo's tools (`phone_ui.py`, `clean_shot.py`, `hide_coords.py`).
