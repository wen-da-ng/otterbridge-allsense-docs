"""MkDocs hook: the docs for AI assistants, from the same pages as the site.

- llms.txt: an index (llmstxt.org): each page's title, link and one-line description.
- llms-full.txt: every page in nav order, as Markdown.
- <page>/index.md next to each page's index.html: that page as plain Markdown.

Snippets (--8<-- "path/to/example.py") are expanded, so the AI sees the same tested examples
as people do. A page's description is its `description:` front matter, else its first paragraph.
"""

from __future__ import annotations

import re
from pathlib import Path

_SNIPPET = re.compile(r'^(?P<indent>[ \t]*)--8<--[ \t]+"(?P<path>[^"]+)"[ \t]*$', re.M)
# Diagrams are inline SVG for people; an AI gets the caption instead.
_FIGURE = re.compile(r'<figure class="ob-diagram"[^>]*>.*?<figcaption[^>]*>(?P<caption>.*?)</figcaption>\s*</figure>', re.S)
_pages: dict[str, tuple[str, str, str]] = {}  # src_uri -> (title, description, markdown)
_nav = None


def _expand(markdown: str, root: Path) -> str:
    def one(m: re.Match) -> str:
        path, _, lines = m["path"].partition(":")
        text = (root / path).read_text(encoding="utf-8").splitlines()
        if lines:
            start, _, end = lines.partition(":")
            text = text[int(start or 1) - 1:int(end) if end else None]
        return "\n".join(m["indent"] + line if line else line for line in text)

    return _SNIPPET.sub(one, markdown)


def _description(page, markdown: str) -> str:
    if page.meta.get("description"):
        return page.meta["description"]
    for block in re.split(r"\n\s*\n", markdown):
        block = block.strip()
        if block and not block.startswith(("#", "!", "<", "|", "```", "-", "*", "[")):
            return " ".join(re.sub(r"\{[^}]*\}", "", block).split())
    return ""


def on_nav(nav, config, files):
    global _nav
    _nav = nav
    _pages.clear()


def on_page_markdown(markdown, page, config, files):
    root = Path(config["config_file_path"]).parent
    full = _FIGURE.sub(lambda m: f"*Diagram: {' '.join(m['caption'].split())}*", _expand(markdown, root))
    _pages[page.file.src_uri] = (page.title or "", _description(page, full), full)
    return markdown


def on_page_context(context, page, config, nav):
    # For the "Copy page" button (docs/overrides/partials/actions.html).
    context["page_md"] = _pages.get(page.file.src_uri, ("", "", ""))[2]
    return context


def on_post_build(config):
    site = Path(config["site_dir"])
    index = [f"# {config['site_name']}", "", f"> {config['site_description']}", ""]
    full = [f"# {config['site_name']}", "", f"> {config['site_description']}", ""]
    section = None
    for page in _nav.pages:
        if page.file.src_uri not in _pages:
            continue
        title, description, markdown = _pages[page.file.src_uri]
        top = page.parent.title if page.parent else "Home"
        if top != section:
            section = top
            index += ["", f"## {section}", ""]
        md_path = page.url + "index.md" if page.url.endswith("/") or page.url == "" else page.url.removesuffix(".html") + ".md"
        index.append(f"- [{title}]({md_path}): {description}" if description else f"- [{title}]({md_path})")
        full += ["", "---", "", f"<!-- {page.file.src_uri} -->", "", markdown.strip(), ""]
        out = site / md_path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
    (site / "llms.txt").write_text("\n".join(index) + "\n", encoding="utf-8")
    (site / "llms-full.txt").write_text("\n".join(full) + "\n", encoding="utf-8")
