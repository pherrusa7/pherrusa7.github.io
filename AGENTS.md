# Agent Notes

This is a markdown-first personal website. The source of truth is Markdown; generated HTML is committed so the site can be opened locally by double-clicking `index.html` and served directly by GitHub Pages.

## Structure

- `content/index.md` is the homepage source.
- `content/aboutme/*.md` contains About Me pages.
- `content/posts/*.md` contains posts.
- `assets/css/style.css` contains the visual theme.
- `assets/js/fun.js` contains the optional Fun text interaction.
- `build.py` compiles Markdown into static HTML.
- `index.html` and `web/**/*.html` are generated output.

## Build Rule

After editing any Markdown, CSS, JavaScript, or `build.py`, run:

```bash
python3 build.py
```

Commit both source changes and generated HTML changes. Do not edit generated HTML directly except for emergency debugging; fix the source or compiler instead.

Do not add Jekyll, Ruby, npm, bundlers, or a local-server requirement for normal development. The intended loop is plain Markdown plus `python3 build.py`.

If `assets/js/fun.js` changes, also run:

```bash
node --check assets/js/fun.js
```

## Local Preview

Open `index.html` in a browser. No server, Jekyll, Ruby, npm, or dependencies are required. Ignore or delete `_site/` and `.jekyll-cache/` if they ever appear locally.

## Content Style

- Keep content concrete, dense, and specific.
- Avoid generic resume language.
- Homepage should stay light: only `About me` and Posts.
- About Me owns the Career and Research tree.
- Keep links in Markdown source Cursor-friendly when possible.

## Visual Style

- Minimal dark blue Bear-inspired theme.
- No cards, no heavy layout, no decoration beyond the home mark and optional Fun mode.
- Header is a fixed top band with a minimal universe home logo.
- Regular reading text is intentionally light/thin by default.

## Fun Mode

Fun mode is optional and off by default for new visitors. It can be toggled with the button or `f`.

Controls:

- `q` force
- `w` radius
- `e` motion
- `r` return
- `t` settle
- `y` regular text weight/ink
- `a` decrease selected control
- `s` increase selected control

The `y` control should affect regular reading text only: paragraphs, list items, and table text. It should not affect headings, header/logo, or UI controls.

The effect should remain playful but not get in the way of reading. Respect `prefers-reduced-motion`.
