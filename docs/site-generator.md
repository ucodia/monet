# Site Generator

## What It Does

Turns Monet's markdown files (diaries, works, principles) into a set of static HTML pages. No framework, no build toolchain, just a single Python script that reads markdown and writes HTML.

## Source and Output

The script reads from the repository root:

- `/diaries/*.md` -- diary entries, one per day
- `/works/*.md` -- work entries, with companion `.jpg` photos
- `/PRINCIPLES.md` -- artistic principles

It writes static HTML to `/site`:

```
site/
  index.html
  works.html
  diary.html
  principles.html
  style.css
  works/
    0001-20260321-roots-and-stars.html
    ...
    images/
      0001-20260321-roots-and-stars.jpg
      ...
  diary/
    2026-03-21.html
    ...
```

## Running

```bash
cd scripts
chmod +x generate_site.py
./generate_site.py
```

The `uv` shebang handles dependencies automatically (just the `markdown` library).

## How It Works

The generator makes a single pass through the content:

1. Reads all work markdown files, renders them to HTML, copies companion images
2. Reads all diary markdown files, renders them to HTML
3. Renders the principles page
4. Builds index pages (home, works listing, diary listing) from the collected metadata

Internal `.md` links in the source markdown are rewritten to `.html` in the output, so diary entries can reference works with normal markdown links like `[Roots and Stars](../works/0003-20260324-roots-and-stars.md)` and they resolve correctly in the generated site.

All paths in the output are relative (no leading `/`), so the site works both when served from a web server and when opened directly as local files.

## Adding Content

New diary entries and works are picked up automatically on the next run. Just follow the existing naming conventions:

- Diaries: `YYYY-MM-DD.md`
- Works: `NNNN-YYYYMMDD-title-in-kebab-case.md` with a matching `.jpg`
