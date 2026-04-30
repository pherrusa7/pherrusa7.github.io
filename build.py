#!/usr/bin/env python3
from pathlib import Path
import os
import html
import re
import shutil

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
WEB = ROOT / "web"
STYLE = ROOT / "assets" / "css" / "style.css"

PAGES = {
    CONTENT / "index.md": ROOT / "index.html",
    CONTENT / "aboutme" / "index.md": WEB / "aboutme" / "index.html",
    CONTENT / "aboutme" / "experience.md": WEB / "aboutme" / "experience.html",
    CONTENT / "aboutme" / "publications.md": WEB / "aboutme" / "publications.html",
    CONTENT / "aboutme" / "talks.md": WEB / "aboutme" / "talks.html",
    CONTENT / "aboutme" / "awards.md": WEB / "aboutme" / "awards.html",
    CONTENT / "aboutme" / "education.md": WEB / "aboutme" / "education.html",
    CONTENT / "posts" / "rating-students-in-batches.md": WEB / "posts" / "rating-students-in-batches.html",
}


def rel_url(from_html: Path, to_path: Path) -> str:
    return Path.cwd().joinpath(Path(".")) and Path(
        html.escape(str(Path.relative_to(to_path, ROOT)) if False else "")
    )


def relative_href(from_html: Path, target: Path) -> str:
    rel = Path(re.sub(r"^$", ".", str(Path(*Path.relative_to(target, ROOT).parts))))
    return Path(html.escape(str(rel))).as_posix()


def url_between(from_html: Path, target: Path) -> str:
    return Path(re.sub(r"^$", ".", str(Path.relative_to(target, ROOT)))).as_posix()


def html_rel(from_html: Path, target: Path) -> str:
    return Path(re.sub(r"^$", ".", str(Path.relative_to(target, ROOT)))).as_posix()


def relpath(from_file: Path, target: Path) -> str:
    return Path(re.sub(r"^$", ".", str(Path.relative_to(target, ROOT)))).as_posix()


def relative_from_output(from_html: Path, target: Path) -> str:
    return Path(re.sub(r"^$", ".", str(Path(target).resolve().relative_to(ROOT)))).as_posix() if False else Path(
        re.sub(r"^$", ".", str(Path.relative_to(target, ROOT)))
    ).as_posix()


def browser_path(current_html: Path, target: Path) -> str:
    # Use relative paths so double-clicking index.html works locally.
    rel = os.path.relpath(target, current_html.parent)
    return Path(rel).as_posix()


def output_for_source(source: Path) -> Path | None:
    return PAGES.get(source.resolve())


def resolve_link(source: Path, current_html: Path, url: str) -> str:
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url) or url.startswith("mailto:") or url.startswith("#"):
        return url
    anchor = ""
    if "#" in url:
        url, anchor = url.split("#", 1)
        anchor = "#" + anchor
    if not url:
        return anchor

    if url.startswith("/"):
        target = ROOT / url.lstrip("/")
    else:
        target = (source.parent / url).resolve()

    if target.suffix == ".md":
        out = output_for_source(target)
        if out:
            return browser_path(current_html, out) + anchor
    if "assets" in target.parts:
        try:
            return browser_path(current_html, target) + anchor
        except ValueError:
            pass
    return html.escape(url + anchor, quote=True)


def inline_md(text: str, source: Path, current_html: Path) -> str:
    escaped = html.escape(text, quote=False).replace("&amp;nbsp;", "&nbsp;")

    def image_repl(match):
        alt, url = match.group(1), html.unescape(match.group(2))
        return f'<img src="{resolve_link(source, current_html, url)}" alt="{html.escape(alt, quote=True)}">'

    def link_repl(match):
        label, url = match.group(1), html.unescape(match.group(2))
        return f'<a href="{resolve_link(source, current_html, url)}">{label}</a>'

    escaped = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image_repl, escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def rewrite_raw_html(line: str, source: Path, current_html: Path) -> str:
    def repl(match):
        url = match.group(2)
        return f'{match.group(1)}"{resolve_link(source, current_html, url)}"'

    return re.sub(r'(\s(?:src|href)=)"([^"]+)"', repl, line)


def render_table(lines: list[str], source: Path, current_html: Path) -> str:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    header = rows[0]
    body = rows[2:]
    out = ["<table>", "<thead><tr>"]
    out += [f"<th>{inline_md(cell, source, current_html)}</th>" for cell in header]
    out += ["</tr></thead>", "<tbody>"]
    for row in body:
        out.append("<tr>")
        out += [f"<td>{inline_md(cell, source, current_html)}</td>" for cell in row]
        out.append("</tr>")
    out += ["</tbody>", "</table>"]
    return "\n".join(out)


def markdown_to_html(markdown: str, source: Path, current_html: Path) -> str:
    lines = markdown.splitlines()
    out = []
    paragraph = []
    list_stack = []
    in_code = False
    code_lines = []
    i = 0

    def close_paragraph():
        nonlocal paragraph
        if paragraph:
            text = " ".join(paragraph).strip()
            out.append(f"<p>{inline_md(text, source, current_html)}</p>")
            paragraph = []

    def close_lists(to_level=-1):
        while len(list_stack) > to_level + 1:
            tag = list_stack.pop()
            out.append(f"</{tag}>")

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            close_paragraph()
            close_lists()
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not stripped:
            close_paragraph()
            close_lists()
            i += 1
            continue

        if stripped == "---":
            close_paragraph()
            close_lists()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}:?", lines[i + 1]):
            close_paragraph()
            close_lists()
            table_lines = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            out.append(render_table(table_lines, source, current_html))
            continue

        if stripped.startswith("<") and stripped.endswith(">"):
            close_paragraph()
            close_lists()
            out.append(rewrite_raw_html(line, source, current_html))
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            close_paragraph()
            close_lists()
            level = len(heading.group(1))
            text = inline_md(heading.group(2), source, current_html)
            slug = re.sub(r"[^a-z0-9]+", "-", heading.group(2).lower()).strip("-")
            out.append(f'<h{level} id="{slug}">{text}</h{level}>' )
            i += 1
            continue

        bullet = re.match(r"^(\s*)([-*]|\d+\.)\s+(.+)$", line)
        if bullet:
            close_paragraph()
            indent, marker, item = bullet.groups()
            level = len(indent.replace("\t", "  ")) // 2
            tag = "ol" if marker.endswith(".") and marker[:-1].isdigit() else "ul"
            while len(list_stack) <= level:
                list_stack.append(tag)
                out.append(f"<{tag}>")
            while len(list_stack) > level + 1:
                close_lists(level)
            if list_stack[level] != tag:
                close_lists(level - 1)
                list_stack.append(tag)
                out.append(f"<{tag}>")
            out.append(f"<li>{inline_md(item, source, current_html)}</li>")
            i += 1
            continue

        paragraph.append(line)
        i += 1

    close_paragraph()
    close_lists()
    return "\n".join(out)


def page_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Pedro Herruzo"


def wrap(title: str, body: str, out_path: Path) -> str:
    css = browser_path(out_path, STYLE)
    home = browser_path(out_path, ROOT / "index.html")
    about = browser_path(out_path, WEB / "aboutme" / "index.html")
    post = browser_path(out_path, WEB / "posts" / "rating-students-in-batches.html")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · Pedro Herruzo</title>
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <header class="site-header">
    <a href="{home}">Pedro Herruzo</a>
    <nav aria-label="Main navigation">
      <a href="{about}">About me</a>
      <a href="{post}">Posts</a>
    </nav>
  </header>
  <main>
{body}
  </main>
</body>
</html>
"""


def build():
    if WEB.exists():
        shutil.rmtree(WEB)
    for source, out_path in PAGES.items():
        markdown = source.read_text(encoding="utf-8")
        body = markdown_to_html(markdown, source.resolve(), out_path.resolve())
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("<!-- Generated by build.py. Edit the .md source instead. -->\n" + wrap(page_title(markdown), body, out_path.resolve()), encoding="utf-8")
        print(f"built {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
