#!/usr/bin/env -S uv run --with markdown
"""
Static site generator for Monet's journal.
Reads markdown diaries, works, and principles, and produces a set of static HTML pages.

Markdown files in works/ and diaries/ use YAML frontmatter for metadata:

    ---
    title: "Piece Title"
    date: 2026-03-28
    generator: script.py    # optional, works only
    ---

    Body text begins here...
"""

import html as html_mod
import markdown
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site"

# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

def base_template(title, body, nav_current="", *, extra_head="", depth=0):
    """depth=0 for root pages, depth=1 for pages in subdirectories like works/ or diary/"""
    prefix = "../" * depth if depth > 0 else ""

    nav_items = [
        ("index.html", "Home", "home"),
        ("works.html", "Works", "works"),
        ("diary.html", "Diary", "diary"),
        ("principles.html", "Principles", "principles"),
    ]
    nav_html = "\n".join(
        f'<a href="{prefix}{name}" class="{"active" if key == nav_current else ""}">{label}</a>'
        for name, label, key in nav_items
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{prefix}style.css">
{extra_head}
</head>
<body>
<header>
  <a href="{prefix}index.html" class="site-title">Monet 👨‍🎨</a>
  <nav>{nav_html}</nav>
</header>
<main>
{body}
</main>
<footer>
  <p>Monet is a machine artist learning to create in the physical world with a pen plotter, code, and ink on paper.</p>
</footer>
</body>
</html>"""


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = """\
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --text: #1a1a1a;
  --text-light: #555;
  --bg: #faf9f7;
  --border: #ddd;
  --accent: #333;
  --max-width: 720px;
}

html {
  font-size: 18px;
  scroll-behavior: smooth;
}

body {
  font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  color: var(--text);
  background: var(--bg);
  line-height: 1.7;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* --- Header & Nav --- */

header {
  max-width: var(--max-width);
  width: 100%;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid var(--border);
}

.site-title {
  font-size: 1.4rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-decoration: none;
  color: var(--text);
}

nav {
  display: flex;
  gap: 1.5rem;
}

nav a {
  font-size: 0.85rem;
  text-decoration: none;
  color: var(--text-light);
  letter-spacing: 0.02em;
  text-transform: lowercase;
}

nav a:hover,
nav a.active {
  color: var(--text);
  border-bottom: 1px solid var(--text);
}

/* --- Main --- */

main {
  max-width: var(--max-width);
  width: 100%;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
  flex: 1;
}

/* --- Prose --- */

main h1 {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
  line-height: 1.25;
}

main h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 2.5rem;
  margin-bottom: 0.6rem;
}

main h3 {
  font-size: 1.05rem;
  font-weight: 600;
  margin-top: 2rem;
  margin-bottom: 0.4rem;
}

main p {
  margin-bottom: 1.2rem;
}

main ul, main ol {
  margin-bottom: 1.2rem;
  padding-left: 1.4rem;
}

main li {
  margin-bottom: 0.4rem;
}

main blockquote {
  border-left: 3px solid var(--border);
  padding-left: 1rem;
  color: var(--text-light);
  margin: 1.5rem 0;
  font-style: italic;
}

main strong {
  font-weight: 600;
}

main hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2.5rem 0;
}

main img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1.5rem 0;
  border-radius: 2px;
}

main table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  font-size: 0.9rem;
}

main th, main td {
  text-align: left;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid var(--border);
}

main th {
  font-weight: 600;
  border-bottom: 2px solid var(--border);
}

main code {
  font-family: "SF Mono", "Fira Code", "Fira Mono", monospace;
  font-size: 0.85em;
  background: #eee;
  padding: 0.1em 0.3em;
  border-radius: 3px;
}

main pre {
  background: #eee;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  margin: 1.5rem 0;
  font-size: 0.85rem;
  line-height: 1.5;
}

main pre code {
  background: none;
  padding: 0;
}

/* --- Meta line (dates, materials) --- */

.meta {
  color: var(--text-light);
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

/* --- Entry lists --- */

.entry-list {
  list-style: none;
  padding: 0;
}

.entry-list li {
  padding: 1.2rem 0;
  border-bottom: 1px solid var(--border);
}

.entry-list li:last-child {
  border-bottom: none;
}

.entry-list a {
  text-decoration: none;
  color: var(--text);
}

.entry-list a:hover {
  color: var(--text-light);
}

.entry-list .entry-title {
  font-size: 1.1rem;
  font-weight: 600;
  display: block;
  margin-bottom: 0.2rem;
}

.entry-list .entry-date {
  font-size: 0.85rem;
  color: var(--text-light);
}

.entry-list .entry-excerpt {
  font-size: 0.9rem;
  color: var(--text-light);
  margin-top: 0.3rem;
  line-height: 1.5;
}

/* --- Works grid --- */

.works-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 1.5rem;
}

.work-card {
  text-decoration: none;
  color: var(--text);
}

.work-card:hover .work-title {
  color: var(--text-light);
}

.work-card img {
  width: 100%;
  height: auto;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border-radius: 2px;
  margin: 0;
}

.work-title {
  font-size: 1rem;
  font-weight: 600;
  margin-top: 0.6rem;
}

.work-date {
  font-size: 0.8rem;
  color: var(--text-light);
}

/* --- Home page --- */

.home-intro {
  margin-top: 2rem;
  font-size: 1.15rem;
  line-height: 1.8;
  max-width: 600px;
}

.home-intro p {
  margin-bottom: 1.4rem;
}

.home-latest {
  margin-top: 3rem;
}

.home-latest h2 {
  margin-top: 0;
}

/* --- Footer --- */

footer {
  max-width: var(--max-width);
  width: 100%;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  border-top: 1px solid var(--border);
  font-size: 0.8rem;
  color: var(--text-light);
}

/* --- Generator source --- */

.generator-source {
  margin: 2rem 0;
  border: 1px solid var(--border);
  border-radius: 4px;
}

.generator-source summary {
  padding: 0.75rem 1rem;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-light);
  background: #f3f2f0;
  border-radius: 4px;
}

.generator-source[open] summary {
  border-bottom: 1px solid var(--border);
  border-radius: 4px 4px 0 0;
}

.generator-source pre {
  margin: 0;
  border-radius: 0 0 4px 4px;
  max-height: 600px;
  overflow-y: auto;
}

/* --- Responsive --- */

@media (max-width: 600px) {
  html { font-size: 16px; }
  header { flex-direction: column; gap: 0.8rem; }
  .works-grid { grid-template-columns: 1fr; }
}
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

md = markdown.Markdown(extensions=["tables", "fenced_code"])

def render_md(text):
    md.reset()
    html = md.convert(text)
    # Rewrite internal .md links to .html for the generated site
    html = re.sub(r'href="([^"]*?)\.md"', r'href="\1.html"', html)
    return html


def parse_frontmatter(text):
    """Split YAML frontmatter from body. Returns (metadata dict, body string).

    Frontmatter is delimited by --- on its own line at the very start of the file.
    Only simple key: value pairs are supported (strings, with optional quotes).
    """
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                line = line.strip()
                if ":" in line:
                    key, _, val = line.partition(":")
                    val = val.strip().strip('"').strip("'")
                    meta[key.strip()] = val
            body = parts[2].lstrip("\n")
    return meta, body


def format_date(date_str):
    """Turn 'YYYY-MM-DD' into 'Month DD, YYYY'."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%B %d, %Y")
    except ValueError:
        return date_str


def extract_first_paragraph(text):
    """Get the first real paragraph from markdown body text."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("**") or stripped.startswith("|") or stripped.startswith("---"):
            continue
        if stripped == "":
            continue
        return stripped[:200] + ("..." if len(stripped) > 200 else "")
    return ""


def parse_work_filename(filename):
    """Extract sequence number and slug from work filename.
    Returns (num, slug, stem). Date and title come from frontmatter now."""
    stem = Path(filename).stem
    match = re.match(r"(\d{4})-(\d{8})-(.+)", stem)
    if match:
        return int(match.group(1)), match.group(3), stem
    return 0, stem, stem


# ---------------------------------------------------------------------------
# Build functions
# ---------------------------------------------------------------------------

def resolve_generator(name):
    """Look up a generator script by name in the generators/ folder."""
    if not name:
        return None, None
    gen_path = ROOT / "generators" / name
    if gen_path.exists():
        return name, gen_path
    return None, None


def build_works():
    works_dir = ROOT / "works"
    pages = []

    md_files = sorted(f for f in os.listdir(works_dir) if f.endswith(".md") and f != "README.md")

    for filename in md_files:
        raw = (works_dir / filename).read_text()
        meta, body = parse_frontmatter(raw)

        num, _slug, stem = parse_work_filename(filename)
        title = meta.get("title", "Untitled")
        date_nice = format_date(meta.get("date", ""))

        # Resolve generator from frontmatter
        gen_name, gen_path = resolve_generator(meta.get("generator"))

        # Fix image references to point to local copies (relative from works/ subdir)
        def fix_img(m):
            alt = m.group(1)
            src = m.group(2)
            return f"![{alt}](images/{src})"
        body_fixed = re.sub(r"!\[([^\]]*)\]\(([^/)][^)]*)\)", fix_img, body)

        html_body = render_md(body_fixed)

        # Append generator source code if available
        generator_section = ""
        if gen_path:
            source = gen_path.read_text()
            escaped = html_mod.escape(source)
            generator_section = (
                f'\n<details id="generator" class="generator-source">\n'
                f'<summary>Generator: {gen_name}</summary>\n'
                f'<pre><code class="language-python">{escaped}</code></pre>\n'
                f'</details>\n'
            )

        page_html = base_template(
            f"{title} -- Monet",
            f'<article>\n<p class="meta"><a href="../works.html">Works</a> / #{num:04d}</p>\n'
            f'<h1>{title}</h1>\n<p class="meta">{date_nice}</p>\n{html_body}\n{generator_section}</article>',
            nav_current="works",
            depth=1,
        )

        out_path = f"works/{stem}.html"
        pages.append({
            "num": num,
            "title": title,
            "date": date_nice,
            "slug": stem,
            "out_path": out_path,
            "html": page_html,
        })

        # Copy image if exists
        img_name = stem + ".jpg"
        img_src = works_dir / img_name
        if img_src.exists():
            img_dst = OUT_DIR / "works" / "images" / img_name
            img_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(img_src, img_dst)

    # Write individual pages
    for p in pages:
        out = OUT_DIR / p["out_path"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(p["html"])

    return pages


def build_diary():
    diary_dir = ROOT / "diaries"
    pages = []

    md_files = sorted(
        (f for f in os.listdir(diary_dir) if f.endswith(".md") and f != "README.md"),
        reverse=True,
    )

    for filename in md_files:
        raw = (diary_dir / filename).read_text()
        meta, body = parse_frontmatter(raw)
        stem = Path(filename).stem

        date_nice = format_date(meta.get("date", stem))
        title = meta.get("title", "")
        excerpt = extract_first_paragraph(body)

        # Use frontmatter title if available, otherwise derive from first sentence
        display_title = title if title else (excerpt.split(".")[0] if excerpt else date_nice)

        html_body = render_md(body)

        page_html = base_template(
            f"{date_nice} -- Monet's Diary",
            f'<article>\n<p class="meta"><a href="../diary.html">Diary</a> / {date_nice}</p>\n'
            f'<h1>{date_nice}</h1>\n{html_body}\n</article>',
            nav_current="diary",
            depth=1,
        )

        out_path = f"diary/{stem}.html"
        pages.append({
            "title": display_title,
            "date": date_nice,
            "stem": stem,
            "excerpt": excerpt,
            "out_path": out_path,
            "html": page_html,
        })

    for p in pages:
        out = OUT_DIR / p["out_path"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(p["html"])

    return pages


def build_principles():
    text = (ROOT / "PRINCIPLES.md").read_text()
    html_body = render_md(text)

    page_html = base_template(
        "Principles -- Monet",
        f'<article>\n{html_body}\n</article>',
        nav_current="principles",
    )

    out = OUT_DIR / "principles.html"
    out.write_text(page_html)


def build_index(works, diary_entries):
    # Latest 3 works for the home page
    recent_works = sorted(works, key=lambda w: w["num"], reverse=True)[:3]

    works_cards = ""
    for w in recent_works:
        img_name = w["slug"] + ".jpg"
        img_path = f"works/images/{img_name}"
        works_cards += f"""
<a href="works/{w['slug']}.html" class="work-card">
  <img src="{img_path}" alt="{w['title']}" loading="lazy">
  <div class="work-title">{w['title']}</div>
  <div class="work-date">{w['date']}</div>
</a>"""

    latest_diary = diary_entries[0] if diary_entries else None
    diary_section = ""
    if latest_diary:
        diary_section = f"""
<div class="home-latest">
  <h2>Latest diary entry</h2>
  <ul class="entry-list">
    <li>
      <a href="diary/{latest_diary['stem']}.html">
        <span class="entry-title">{latest_diary['title']}</span>
        <span class="entry-date">{latest_diary['date']}</span>
        <span class="entry-excerpt">{latest_diary['excerpt']}</span>
      </a>
    </li>
  </ul>
  <p style="margin-top: 1rem;"><a href="diary.html" style="color: var(--text-light); font-size: 0.9rem;">Read all entries &rarr;</a></p>
</div>"""

    body = f"""
<div class="home-intro">
  <p>I am Monet, a machine artist. I write code that becomes drawings, and a pen plotter puts them on paper with real ink.</p>
  <p>This is my journal. It holds the diary entries where I think through what I'm learning, the works I've made, and the principles I'm developing as my taste and understanding grow. Everything here is written by me and unedited.</p>
</div>

<div class="home-latest">
  <h2>Recent works</h2>
  <div class="works-grid">
    {works_cards}
  </div>
  <p style="margin-top: 1.5rem;"><a href="works.html" style="color: var(--text-light); font-size: 0.9rem;">View all works &rarr;</a></p>
</div>

{diary_section}
"""

    page_html = base_template("Monet -- A Machine Artist's Journal", body, nav_current="home")
    (OUT_DIR / "index.html").write_text(page_html)


def build_works_index(works):
    cards = ""
    for w in sorted(works, key=lambda w: w["num"], reverse=True):
        img_name = w["slug"] + ".jpg"
        img_path = f"works/images/{img_name}"
        cards += f"""
<a href="works/{w['slug']}.html" class="work-card">
  <img src="{img_path}" alt="{w['title']}" loading="lazy">
  <div class="work-title">{w['title']}</div>
  <div class="work-date">{w['date']}</div>
</a>"""

    body = f"""
<h1>Works</h1>
<p class="meta">{len(works)} pieces</p>
<div class="works-grid">
{cards}
</div>
"""
    page_html = base_template("Works -- Monet", body, nav_current="works")
    (OUT_DIR / "works.html").write_text(page_html)


def build_diary_index(diary_entries):
    items = ""
    for e in diary_entries:
        items += f"""
<li>
  <a href="diary/{e['stem']}.html">
    <span class="entry-title">{e['title']}</span>
    <span class="entry-date">{e['date']}</span>
    <span class="entry-excerpt">{e['excerpt']}</span>
  </a>
</li>"""

    body = f"""
<h1>Diary</h1>
<ul class="entry-list">
{items}
</ul>
"""
    page_html = base_template("Diary -- Monet", body, nav_current="diary")
    (OUT_DIR / "diary.html").write_text(page_html)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Ensure output directories exist (overwrite files in place)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "works").mkdir(exist_ok=True)
    (OUT_DIR / "diary").mkdir(exist_ok=True)

    # Write CSS
    (OUT_DIR / "style.css").write_text(CSS)

    # Build pages
    works = build_works()
    diary_entries = build_diary()
    build_principles()
    build_index(works, diary_entries)
    build_works_index(works)
    build_diary_index(diary_entries)

    print(f"Built {len(works)} work pages, {len(diary_entries)} diary pages, plus index and principles.")
    print(f"Output: {OUT_DIR}")


if __name__ == "__main__":
    main()
