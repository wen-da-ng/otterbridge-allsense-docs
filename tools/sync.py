"""Copies what the site shows from the other AllSense repos, cloned next to this one:

- the spec pages: docs/{PROTOCOL,TEMPLATES,RECORDING,MQTT}.md from ../otterbridge-allsense-protocol/spec/
- the code examples the pages include (--8<-- "examples/<lib>/<path>") from ../otterbridge-allsense-<lib>/<path>

    python tools/sync.py           # copy
    python tools/sync.py --check   # only list copies that differ (exit 1)

Edit those files in their own repo, never here. The copies keep the site buildable without access to the
other repos while they're private; once they're public, the build can fetch them from release tags instead.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPECS = ["PROTOCOL", "TEMPLATES", "RECORDING", "MQTT"]
SNIPPET = re.compile(r'--8<-- "examples/([a-z0-9]+)/([^"]+)"')


def wanted():
    """(copy here, source in a sibling repo) pairs."""
    pairs = [(ROOT / "docs" / f"{s}.md", ROOT.parent / "otterbridge-allsense-protocol" / "spec" / f"{s}.md") for s in SPECS]
    examples = {m.groups() for md in (ROOT / "docs").rglob("*.md") for m in SNIPPET.finditer(md.read_text(encoding="utf-8"))}
    pairs += [(ROOT / "examples" / lib / path, ROOT.parent / f"otterbridge-allsense-{lib}" / path) for lib, path in sorted(examples)]
    return pairs


def main():
    check = "--check" in sys.argv
    pairs = wanted()
    stale = 0
    for copy, source in pairs:
        if not source.exists():
            sys.exit(f"missing: {source}")
        if copy.exists() and copy.read_bytes() == source.read_bytes():
            continue
        stale += 1
        print(("differs: " if check else "copied: ") + copy.relative_to(ROOT).as_posix())
        if not check:
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_bytes(source.read_bytes())
    print(f"{len(pairs)} files, {stale} {'differ' if check else 'updated'}")
    sys.exit(1 if check and stale else 0)


if __name__ == "__main__":
    main()
