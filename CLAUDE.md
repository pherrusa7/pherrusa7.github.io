# Claude Project Notes

This repo is a small static personal website. Work in Markdown first, then run the Python build.

## Workflow

1. Edit source files under `content/`, or edit `assets/css/style.css`, `assets/js/fun.js`, or `build.py`.
2. Run:

```bash
python3 build.py
```

3. If `assets/js/fun.js` changed, run `node --check assets/js/fun.js`.
4. Review `index.html` locally.
5. Commit source and generated HTML together.

Generated files are:

- `index.html`
- `web/**/*.html`

Do not hand-edit generated HTML as the primary fix. Do not add Jekyll, Ruby, npm, bundlers, or a server requirement for normal development.

## Mental Model

The project exists so Pedro can write without website machinery: pure Markdown source, one build command, plain static HTML output.

## Design Direction

Minimal, dark blue, quiet, readable. The site should feel deliberate and light. Avoid adding frameworks or dependencies unless Pedro explicitly asks.

## Important Details

- `content/index.md` is the source homepage.
- About Me pages live in `content/aboutme/`.
- Posts live in `content/posts/`.
- The root homepage should not repeat all About Me subnavigation.
- The fixed header uses a tiny universe-like SVG as the home button.
- Fun mode lives in `assets/js/fun.js` and should remain optional, discoverable, and non-invasive.
- If `_site/` or `.jekyll-cache/` appear, they are local leftovers and should not be committed.
