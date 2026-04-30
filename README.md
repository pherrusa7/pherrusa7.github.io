# Pedro Herruzo Website

This repo keeps the website content in Markdown and compiles it to plain static HTML.

The idea is to stay focused while writing: edit pure Markdown, avoid website machinery, then run one build command when ready. If something breaks or feels awkward, an LLM can help adjust the compiler or the generated site quickly.

Start reading/editing here: [content/index.md](content/index.md).

To rebuild the website after editing Markdown:

```bash
python3 build.py
```

Open `index.html` locally, or push the generated HTML to GitHub Pages.
