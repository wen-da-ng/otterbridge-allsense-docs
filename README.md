# AllSense docs

The documentation site for **AllSense by OtterBridge**, the app that turns an Android phone into a sensor hub for robots: **https://docs.allsense.otterbridge.org/**

Markdown in `docs/`, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). Every page is also published as plain Markdown (`<page>/index.md`), with `llms.txt` and `llms-full.txt` for AI assistants.

## Build it

```bash
python -m venv .venv
.venv/Scripts/pip install --require-hashes -r tools/docs-requirements.txt  # .venv/bin/pip on Linux and macOS
.venv/Scripts/mkdocs serve                                                  # preview at http://127.0.0.1:8000
.venv/Scripts/mkdocs build --strict                                         # what CI runs
```

`tools/docs-requirements.txt` pins every package with its hashes (CI installs it with `--require-hashes`). To change a version, edit the two top-level pins in `tools/docs-requirements.in` and regenerate the locked list with [uv](https://docs.astral.sh/uv/):

```bash
uv pip compile tools/docs-requirements.in --universal --python-version 3.12 --generate-hashes -o tools/docs-requirements.txt
```

Dependabot proposes updates to it and to the pinned actions every week.

Every push to `main` publishes the site to GitHub Pages (`.github/workflows/ci.yml`); pull requests only build it.

## Where things come from

- **Pages:** `docs/` (Home, Get started, Guides, How it works, Contributing, Modules). Page layout: title, a one-line lead, then the shortest way as numbered steps, then details and a reference table.
- **Spec pages** (`docs/PROTOCOL.md`, `TEMPLATES.md`, `RECORDING.md`, `MQTT.md`): copies from [otterbridge-allsense-protocol](https://github.com/wen-da-ng/otterbridge-allsense-protocol)'s `spec/`. Change them there.
- **Code examples** (`examples/`): copies of the libraries' own examples, which their CI runs. Change them in the library's repo.
- `python tools/sync.py` refreshes both from the repos cloned next to this one; `--check` lists stale copies.
- **Diagrams:** `python tools/make_diagrams.py` writes `docs/diagrams/*.svg`.

## Licence

Code and text: MIT. The OtterBridge and AllSense names, the otter logo and the app screenshots are not covered (see [LICENSE](LICENSE)).
