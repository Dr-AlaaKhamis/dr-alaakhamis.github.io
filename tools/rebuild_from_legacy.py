"""Rebuild alaakhamis.org as a modern two-theme static site.

Reads the legacy pages, extracts their editorial content, cleans it up and
re-emits it inside a new shell (assets/css/style.css + assets/js/main.js).
"""

import os
import re
import shutil
import html as htmllib

SRC = r"C:\Users\alaa.rashwan\Documents\1-Teaching\MyWebsite\alaakhamis.github.io"
OUT = r"C:\Users\alaa.rashwan\Documents\1-Teaching\MyWebsite\alaakhamis-modern"

# --------------------------------------------------------------------------
# Shell
# --------------------------------------------------------------------------

NAV = [
    ("index.html", "Home"),
    ("shortbio.html", "About"),
    ("research.html", "Research"),
    ("publications.html", "Publications"),
    ("books.html", "Books"),
    ("teaching.html", "Teaching"),
    ("services.html", "Service"),
    ("awards.html", "Awards"),
    ("events.html", "News"),
]

SOCIAL = [
    ("https://scholar.google.ca/citations?user=btM72xsAAAAJ&hl=en", "Google Scholar",
     '<path d="M12 2 1 8.5 12 15l9-5.32V16h2V8.5L12 2Z"/><path d="M5.5 12.1v3.6c0 2.2 2.9 4 6.5 4s6.5-1.8 6.5-4v-3.6L12 16.2l-6.5-4.1Z"/>'),
    ("https://www.linkedin.com/in/alaakhamis/", "LinkedIn",
     '<path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3zM10 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.6 4.78 6V21h-4v-5.3c0-1.27-.02-2.9-1.8-2.9-1.8 0-2.08 1.38-2.08 2.8V21h-4z"/>'),
    ("https://www.researchgate.net/profile/Alaa-Khamis", "ResearchGate",
     '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2Zm-1.1 5.6h2.5c1.9 0 3 .95 3 2.55 0 1.2-.66 2.05-1.7 2.4l2.2 3.85h-1.9l-2-3.6h-1.2v3.6H10.9V7.6Zm1.9 1.35v2.55h.85c.95 0 1.45-.45 1.45-1.3 0-.83-.5-1.25-1.45-1.25h-.85Z"/>'),
    ("https://amazon.com/author/alaakhamis", "Amazon Author page",
     '<path d="M2.6 16.2c3.2 2.3 7.2 3.5 11 3.5 2.6 0 5.4-.55 8.1-1.7.4-.17.74.27.35.57-2.4 1.8-5.9 2.75-8.9 2.75-4.2 0-8-1.55-10.9-4.15-.23-.2-.03-.5.35-.97Zm19.2.9c-.3-.4-2-.2-2.8-.1-.24.03-.28-.18-.06-.34 1.36-.95 3.58-.68 3.84-.36.26.33-.07 2.56-1.34 3.63-.2.16-.38.07-.3-.14.28-.7.9-2.28.66-2.69ZM13.4 10.5c0 1.1.03 2-.53 2.97-.45.78-1.16 1.26-1.96 1.26-1.08 0-1.72-.83-1.72-2.06 0-2.42 2.17-2.86 4.21-2.86v.69Zm2.83 6.85a.58.58 0 0 1-.66.07c-.93-.77-1.1-1.13-1.6-1.86-1.54 1.57-2.63 2.04-4.62 2.04-2.36 0-4.2-1.46-4.2-4.37 0-2.28 1.24-3.83 3-4.59 1.53-.67 3.67-.79 5.3-.97v-.36c0-.67.05-1.46-.34-2.03-.34-.52-1-.73-1.57-.73-1.07 0-2.02.55-2.25 1.68-.05.25-.23.5-.48.51l-2.7-.29c-.23-.05-.48-.23-.41-.58C6.32 2.68 8.94 1.8 11.3 1.8c1.2 0 2.78.32 3.73 1.23 1.2 1.13 1.09 2.63 1.09 4.27v3.86c0 1.16.48 1.67.93 2.3.16.22.2.49-.01.65-.5.42-1.4 1.2-1.9 1.64l-.01-.01Z"/>'),
    ("https://medium.com/@alaakhamis", "Medium",
     '<path d="M13.54 12a6.8 6.8 0 0 1-6.77 6.82A6.8 6.8 0 0 1 0 12a6.8 6.8 0 0 1 6.77-6.82A6.8 6.8 0 0 1 13.54 12ZM20.96 12c0 3.54-1.51 6.42-3.38 6.42S14.2 15.54 14.2 12s1.51-6.42 3.38-6.42S20.96 8.46 20.96 12ZM24 12c0 3.17-.53 5.75-1.19 5.75-.66 0-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75C23.47 6.25 24 8.83 24 12Z"/>'),
    ("https://github.com/Dr-AlaaKhamis", "GitHub",
     '<path d="M12 .5a12 12 0 0 0-3.79 23.4c.6.11.82-.26.82-.58v-2.2c-3.34.72-4.04-1.42-4.04-1.42-.55-1.4-1.34-1.77-1.34-1.77-1.09-.75.08-.73.08-.73 1.2.08 1.84 1.24 1.84 1.24 1.07 1.84 2.81 1.31 3.5 1 .1-.78.42-1.31.76-1.61-2.67-.3-5.47-1.34-5.47-5.96 0-1.32.47-2.39 1.24-3.23-.12-.3-.54-1.53.12-3.18 0 0 1.01-.32 3.3 1.23a11.4 11.4 0 0 1 6.01 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.23 0 4.63-2.81 5.65-5.49 5.95.43.37.82 1.1.82 2.22v3.29c0 .32.21.7.83.58A12 12 0 0 0 12 .5Z"/>'),
    ("mailto:alaakhamis@gmail.com", "Email",
     '<path d="M2 5.5A2.5 2.5 0 0 1 4.5 3h15A2.5 2.5 0 0 1 22 5.5v13a2.5 2.5 0 0 1-2.5 2.5h-15A2.5 2.5 0 0 1 2 18.5v-13Zm2.3-.5 7.7 5.9L19.7 5H4.3ZM20 7.3l-7.4 5.66a1 1 0 0 1-1.2 0L4 7.3V18.5c0 .28.22.5.5.5h15a.5.5 0 0 0 .5-.5V7.3Z"/>'),
]

ICON_SUN = ('<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            'stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/>'
            '<path d="M12 2v2.4M12 19.6V22M2 12h2.4M19.6 12H22M4.9 4.9l1.7 1.7M17.4 17.4l1.7 1.7'
            'M19.1 4.9l-1.7 1.7M6.6 17.4l-1.7 1.7"/></svg>')
ICON_MOON = ('<svg class="moon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
             '<path d="M21 13.2A8.6 8.6 0 0 1 10.8 3 8.6 8.6 0 1 0 21 13.2Z"/></svg>')


def social_html(cls="social"):
    out = ['<div class="%s">' % cls]
    for url, label, path in SOCIAL:
        ext = '' if url.startswith("mailto:") else ' target="_blank" rel="noopener noreferrer"'
        out.append(
            '<a href="%s"%s aria-label="%s" title="%s">'
            '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">%s</svg></a>'
            % (url, ext, label, label, path)
        )
    out.append("</div>")
    return "\n".join(out)


def nav_html(active):
    out = ['<nav class="nav" id="primary-nav" aria-label="Primary">']
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        out.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    out.append("</nav>")
    return "\n".join(out)


FOOTER_COLS = [
    ("Explore", [("shortbio.html", "About"), ("research.html", "Research"),
                 ("publications.html", "Publications"), ("books.html", "Books")]),
    ("More", [("teaching.html", "Teaching"), ("services.html", "Service"),
              ("awards.html", "Awards & Honors"), ("events.html", "News & Events")]),
]


def shell(active, title, description, body, head_extra="", body_class=""):
    year = 2026
    cols = []
    for heading, links in FOOTER_COLS:
        items = "\n".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l in links)
        cols.append('<div><h4>%s</h4><ul class="footer-links">%s</ul></div>' % (heading, items))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="Alaa Khamis">
<meta name="keywords" content="Alaa Khamis, smart mobility, artificial intelligence, agentic AI, optimization algorithms, KFUPM, intelligent transportation systems, robotics">
<meta name="google-site-verification" content="OY0mTH-DtTA1DKj1HWdV9a2cHhToE-Za0cQ2WLQuLcg">
<link rel="canonical" href="https://alaakhamis.org/{active}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://alaakhamis.org/{active}">
<meta property="og:image" content="https://alaakhamis.org/images/AlaaKhamis.png">
<meta name="twitter:card" content="summary">
<link rel="icon" href="images/AlaaKhamis.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
<script>
  // Set the theme before first paint so there is no flash of the wrong colors.
  (function () {{
    try {{
      var t = localStorage.getItem("theme");
      if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
    }} catch (e) {{}}
  }})();
</script>
{head_extra}<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-SEV4N949B2"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-SEV4N949B2');
</script>
</head>
<body{(' class="%s"' % body_class) if body_class else ''}>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="brand__mark" aria-hidden="true">AK</span>
      <span class="brand__name">Alaa Khamis<span>, PhD</span></span>
    </a>
    {nav_html(active)}
    <button class="icon-btn theme-toggle" type="button" aria-label="Switch theme" aria-pressed="false">{ICON_SUN}{ICON_MOON}</button>
    <button class="icon-btn nav-toggle" type="button" aria-label="Toggle navigation" aria-expanded="false" aria-controls="primary-nav">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <h4>Alaa Khamis, PhD, SMIEEE</h4>
        <p>Associate Professor and Director of the AI for Smart Mobility Lab, King Fahd University of Petroleum and Minerals.</p>
        {social_html()}
      </div>
      {cols[0]}
      {cols[1]}
    </div>
    <div class="site-footer__bottom">
      <span>&copy; {year} Alaa Khamis. All rights reserved.</span>
      <span><a href="https://ai4sm.org/" target="_blank" rel="noopener noreferrer">AI for Smart Mobility Lab</a> &middot; Dhahran, Saudi Arabia</span>
    </div>
  </div>
</footer>

<button class="to-top" type="button" aria-label="Back to top">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
</button>

<script src="assets/js/main.js"></script>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Content extraction / cleaning
# --------------------------------------------------------------------------

TYPOS = [
    ("Rersearch", "Research"),
    ("Undergardaute", "Undergraduate"),
    ("Networkin ", "Networking "),
    ("Networkin)", "Networking)"),
    ("Sepetmber", "September"),
    ("apponinted", "appointed"),
    ("Founder nad program chair", "Founder and program chair"),
    ("Exceution", "Execution"),
    ("Pricinple Investigator", "Principal Investigator"),
    ("Principle Investigator", "Principal Investigator"),
    ("Hperloop", "Hyperloop"),
    ("THe International Conference", "The International Conference"),
    ("intenational", "international"),
    ("Fredricton", "Fredericton"),
    ("Universite de Sherbrooke", "Universit&eacute; de Sherbrooke"),
    ("taregt=", "target="),
    ("Moracco", "Morocco"),
    ("Onatrio", "Ontario"),
    ("gallary", "gallery"),
    ("AI & Smart Technical Leader", "AI &amp; Smart Mobility Technical Leader"),
    ("is is a Medium publication", "is a Medium publication"),
    ("Machine Learning Engineer at Brightskies", "Machine Learning Engineer at Brightskies"),
    ("He co-invented and filed 72 patents", "I co-invented and filed 72 patents"),
    ("earning recognition as &ldquo;Inventor of the Month&rdquo; multiple times",
     "earning recognition as &ldquo;Inventor of the Month&rdquo; multiple times"),
    ("https://alaakhamis.org/AI4SM/index.html", "https://ai4sm.org/"),
    ("http://alaakhamis.org/RAS/", "RAS/index.html"),
    ("http://alaakhamis.org/MineProbe/", "MineProbe/index.html"),
    ("Supervised 9 ZC students toward participation in SpacX",
     "Supervised 9 Zewail City students toward participation in SpaceX"),
    # house style: American English, no em dashes
    ("smart mobility triad — technology, governance, and city planning — work together",
     "smart mobility triad (technology, governance, and city planning) work together"),
]

# Words to keep as-is even though they look British: they are proper nouns
# (organisation names, journal titles, official programme names).
SPELLING_EXCEPTIONS = [
    "Minesweepers: Towards", "Engine: Towards", "Intelligent Defence Support Systems",
    "Defence R&D Canada", "Journal of Modelling", "Centre for Pattern Analysis",
    "International Centre for Humanitarian Demining", "centre-pattern-analysis",
    "Innovation Programme", "Executive Programme", "DAAD", "Programme\n", "Programme\"",
]


def read(name):
    with open(os.path.join(SRC, name), "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def extract_body(raw):
    """Return everything between the first body-copy block and the footer."""
    start = raw.find('class="body-copy w-richtext">')
    if start == -1:
        raise ValueError("no body-copy block")
    start = raw.index(">", start) + 1
    end = raw.find("<footer", start)
    chunk = raw[start:end]
    # drop the trailing wrapper divs the old template left open
    chunk = re.sub(r"(?:\s*</div>)+\s*$", "", chunk)
    return chunk


DIV_RE = re.compile(r"<div[^>]*>|</div>|</li>", re.I)


def rewrite_divs(s):
    """Unwrap `div.content`, turn `div[align=center]` into <figure>, drop the rest."""
    out = []
    pos = 0
    stack = []
    for m in DIV_RE.finditer(s):
        out.append(s[pos:m.start()])
        pos = m.end()
        tag = m.group(0)
        low = tag.lower()
        if low.startswith("<div"):
            if 'class="content"' in low:
                stack.append("content")
            elif "align=" in low and "center" in low:
                stack.append("figure")
                out.append("<figure>")
            else:
                stack.append("drop")
        elif low == "</div>":
            kind = stack.pop() if stack else "drop"
            if kind == "figure":
                out.append("</figure>")
        else:  # </li> closes any still-open content div
            while stack and stack[-1] == "content":
                stack.pop()
            out.append(tag)
    out.append(s[pos:])
    return "".join(out)


BQ_RE = re.compile(r"<blockquote>(.*?)</blockquote>", re.S | re.I)


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = htmllib.unescape(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


def promote_headings(s):
    """The legacy pages used <blockquote> both for pull quotes and for section
    titles. Short ones become real headings; long ones stay as quotes."""

    def repl(m):
        inner = m.group(1).strip()
        plain = re.sub(r"<[^>]+>", "", inner).strip()
        if len(plain) <= 60 and not plain.endswith("."):
            return '<h2 id="%s">%s</h2>' % (slugify(plain), htmllib.escape(plain, quote=False))
        return "<blockquote>%s</blockquote>" % inner

    return BQ_RE.sub(repl, s)


# Targets that were already missing from the legacy repository. The link text is
# kept, the dead href is dropped.
DEAD_LINKS = [
    "images/award.jpg",
    "images/Scholars.jpg",
    "images/TechnSummit.jpg",
    "news/media.pdf",
    "Course%20Schedule.pdf",
    "teaching/MobileRobotics/MobileRobotics.pdf",
    "teaching/Robotics/Robotics.pdf",
]


ALT_TEXT = {
    "OptimizationAlgorithms.jpeg": "Cover of Optimization Algorithms (Manning, 2024)",
    "Cover.jpg": "Cover of Smart Mobility: Exploring Foundational Technologies and Wider Impacts",
    "sm.png": "Screenshot of the AI Search Algorithms for Smart Mobility Jupyter book",
    "AI4SM.png": "Banner of the AI for Smart Mobility publication on Medium",
    "FutureMobility.png": "Diagram: future mobility is people-centric, software defined, connected and electric",
    "SMT.png": "Diagram of the smart mobility triad: technology, governance and city planning",
    "AlaaKhamis.png": "Portrait of Alaa Khamis",
}


def add_alt_text(s):
    def repl(m):
        tag = m.group(0)
        if re.search(r'\balt="', tag):
            return tag
        src = re.search(r'src="([^"]+)"', tag)
        name = os.path.basename(src.group(1)) if src else ""
        alt = ALT_TEXT.get(name, "")
        return tag[:-1].rstrip() + ' alt="%s">' % alt

    return re.sub(r"<img\b[^>]*>", repl, s, flags=re.I)


def unwrap_dead_links(s):
    for href in DEAD_LINKS:
        pattern = re.compile(r'<a\s+href="%s"[^>]*>(.*?)</a>' % re.escape(href), re.S | re.I)
        s = pattern.sub(lambda m: m.group(1), s)
    return s


def clean(s):
    # the legacy pages carry large commented-out drafts; drop them
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)

    for bad, good in TYPOS:
        s = s.replace(bad, good)

    # malformed attributes in the legacy markup
    s = s.replace('href=https://www.manning.com', 'href="https://www.manning.com')
    s = re.sub(r'"\s*,\s*target=', '" target=', s)

    # blockquotes wrapped in paragraphs
    s = re.sub(r"<p>\s*<blockquote>", "<blockquote>", s, flags=re.I)
    s = re.sub(r"</blockquote>\s*</p>", "</blockquote>", s, flags=re.I)

    s = promote_headings(s)
    s = rewrite_divs(s)          # needs align="center" intact -> run before stripping it
    s = re.sub(r'\s+align="(?:justify|center|left)"', "", s)

    # <p><strong>Heading</strong> -> real heading
    s = re.sub(r"<p>\s*<strong>(.*?)</strong>\s*",
               lambda m: '<h2 id="%s">%s</h2>\n' % (slugify(m.group(1)), m.group(1)),
               s, flags=re.S | re.I)

    # course accordions
    s = s.replace("&#11166;", "").replace("&#150;", "&ndash;")
    s = re.sub(r'<p style="[^"]*">', '<p class="details-body">', s)

    # media
    s = re.sub(r"<figure>\s*(<iframe[^>]*youtube[^>]*>\s*</iframe>)\s*</figure>",
               r'<div class="video">\1</div>', s, flags=re.I)
    s = re.sub(r"(?<!\">)(<iframe[^>]*youtube[^>]*>\s*</iframe>)",
               r'<div class="video">\1</div>', s, flags=re.I)
    s = add_alt_text(s)
    s = re.sub(r"<figure>(.*?)</figure>",
               lambda m: "<figure>%s</figure>" % re.sub(r"<br\s*/?>", "", m.group(1), flags=re.I),
               s, flags=re.S | re.I)
    s = re.sub(r'\s(?:width|height|border|cellpadding|cellspacing)="\d+"', "", s)

    # link hygiene
    s = re.sub(r'target="_blank"(?![^<>]*rel=)', 'target="_blank" rel="noopener noreferrer"', s)
    s = unwrap_dead_links(s)

    # tidy whitespace / empty paragraphs
    s = re.sub(r"<p>\s*(?:<br\s*/?>\s*)*</p>", "", s, flags=re.I)
    s = re.sub(r"<p>\s*$", "", s)
    s = re.sub(r"(?:<br\s*/?>\s*){2,}", "", s, flags=re.I)
    s = "\n".join(re.sub(r"[ \t]+", " ", line).rstrip() for line in s.split("\n"))
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def page_header(title, subtitle="", meta=""):
    sub = '<p class="page-header__sub">%s</p>' % subtitle if subtitle else ""
    met = '<div class="page-meta">%s</div>' % meta if meta else ""
    return """<section class="page-header">
  <div class="wrap">
    <div class="eyebrow">Alaa Khamis</div>
    <h1>%s</h1>
    %s
    %s
  </div>
</section>
""" % (title, sub, met)


def prose(content, narrow=True):
    cls = "wrap wrap--narrow" if narrow else "wrap"
    return '<div class="prose">\n  <div class="%s">\n%s\n  </div>\n</div>\n' % (cls, content)


# --------------------------------------------------------------------------
# Page builders
# --------------------------------------------------------------------------

def build_simple(src_name, out_name, title, subtitle, page_title, description,
                 narrow=True, updated=""):
    body = clean(extract_body(read(src_name)))
    meta = "<span>Updated %s</span>" % updated if updated else ""
    html = page_header(title, subtitle, meta) + prose(body, narrow)
    write(out_name, shell(out_name, page_title, description, html))
    return body


BRITISH_RE = re.compile(
    r"\b\w*(?:ise[sdr]?|ising|isation[s]?|our[s]?|ogue|isence)\b|"
    r"\bprogramme[s]?\b|\bcentre[s]?\b|\bdefence\b|\bmodelling\b|\btowards\b|"
    r"\bwhilst\b|\bamongst\b|\bhonours?\b|\bcolours?\b",
    re.I)

# Ordinary English words that the crude pattern above would flag by accident.
BRITISH_FALSE_POSITIVES = {
    "our", "your", "yours", "four", "hour", "hours", "tour", "tours", "pour",
    "labour-", "wise", "rise", "rises", "raise", "raises", "praise", "noise",
    "precise", "concise", "expertise", "revise", "revised", "franchise",
    "promise", "promises", "premise", "premises", "advertise", "surprise",
    "supervise", "supervised", "supervisor", "comprise", "comprises", "rising",
    "arising", "raising", "cruising", "advising", "revising", "devise", "devices",
    "labour",
}


def style_check(name, text):
    """Fail loudly on em dashes; report British spellings outside proper nouns."""
    problems = []
    if "—" in text or "&mdash;" in text:
        for m in re.finditer(r"—|&mdash;", text):
            problems.append("em dash: ..." + text[max(0, m.start() - 45):m.end() + 40].replace("\n", " "))

    for m in BRITISH_RE.finditer(text):
        word = m.group(0)
        if word.lower() in BRITISH_FALSE_POSITIVES:
            continue
        window = text[max(0, m.start() - 45):m.end() + 25]
        if any(x in window for x in SPELLING_EXCEPTIONS):
            continue
        problems.append("spelling: %r in ...%s" % (word, window.replace("\n", " ")))

    for p in problems:
        print("  ! %s: %s" % (name, p))
    return problems


def write(name, text):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    flagged = style_check(name, text) if name.endswith(".html") else []
    print("wrote", name, "%.1f KB%s" % (len(text) / 1024.0,
                                        "  [%d style flags]" % len(flagged) if flagged else ""))


# ---- publications --------------------------------------------------------

def build_publications():
    body = clean(extract_body(read("publications.html")))

    # split on the generated <h2 id="..."> headings
    parts = re.split(r'(<h2 id="[^"]+">.*?</h2>)', body, flags=re.S)
    intro = parts[0].strip()

    sections = []
    for i in range(1, len(parts), 2):
        head = parts[i]
        content = parts[i + 1] if i + 1 < len(parts) else ""
        m = re.search(r'id="([^"]+)">(.*?)</h2>', head, re.S)
        slug, label = m.group(1), m.group(2)
        content = re.sub(r"<li>", '<li data-item>', content)
        sections.append((slug, label, head, content.strip()))

    chips = ['<button class="chip is-active" type="button" data-group="all" aria-pressed="true">All</button>']
    for slug, label, _, _ in sections:
        short = label.split("[")[0].strip()
        chips.append('<button class="chip" type="button" data-group="%s" aria-pressed="false">%s</button>'
                     % (slug, short))

    blocks = []
    for slug, label, head, content in sections:
        blocks.append('<section data-group="%s">\n%s\n%s\n</section>' % (slug, head, content))
    blocks.append('<p class="empty-state is-hidden">No publications match that search.</p>')

    toolbar = """<div class="toolbar" data-filter-root="#pub-list">
  <div class="wrap">
    <div class="toolbar__inner">
      <div class="search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <label class="sr-only" for="pub-search" hidden>Search publications</label>
        <input id="pub-search" type="search" placeholder="Search title, co-author, venue&hellip;" autocomplete="off">
      </div>
      <div class="chips">%s</div>
      <span class="filter-status" role="status"></span>
    </div>
  </div>
</div>
""" % ("\n        ".join(chips))

    html = (page_header(
        "Publications",
        "Six books, seven book chapters, more than 200 peer-reviewed papers and 72 filed US patents, "
        "trade secrets and defensive publications.",
        "<span>Updated June 2026</span>")
        + toolbar
        + '<div class="prose">\n  <div class="wrap wrap--narrow">\n'
        + intro + '\n<div id="pub-list">\n' + "\n\n".join(blocks) + "\n</div>\n  </div>\n</div>\n")

    write("publications.html", shell(
        "publications.html", "Publications | Alaa Khamis",
        "Books, book chapters, journal and conference papers, standards and patents by Alaa Khamis.",
        html))


# ---- news / events -------------------------------------------------------

def build_events():
    body = clean(extract_body(read("events.html")))
    body = re.sub(r"<li>", "<li data-item>", body)
    body = '<div id="news-list">%s\n<p class="empty-state is-hidden">No items match that search.</p></div>' % body

    toolbar = """<div class="toolbar" data-filter-root="#news-list">
  <div class="wrap">
    <div class="toolbar__inner">
      <div class="search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <input id="news-search" type="search" placeholder="Search news and events&hellip;" aria-label="Search news and events" autocomplete="off">
      </div>
      <span class="filter-status" role="status"></span>
    </div>
  </div>
</div>
"""
    html = (page_header("News &amp; Events",
                        "Talks, appointments, papers, awards and lab announcements, most recent first.",
                        "<span>Updated August 2026</span>")
            + toolbar + prose(body))
    write("events.html", shell("events.html", "News &amp; Events | Alaa Khamis",
                               "Recent news, keynotes, appointments and announcements from Alaa Khamis.", html))


# ---- teaching ------------------------------------------------------------

def build_teaching():
    raw = read("teaching.html")
    # a stray "Seminars" label sat loose inside the keynote list
    raw = raw.replace("</li>\nSeminars\n<li>",
                      '</li>\n</ol>\n<p><strong>Seminars and Invited Talks</strong>\n<ol>\n<li>')
    body = clean(extract_body_from_string(raw))
    html = (page_header("Teaching",
                        "Forty-four undergraduate and graduate courses taught in Canada, Saudi Arabia, "
                        "Spain and Egypt, with class sizes from 8 to 600 students.",
                        "<span>Updated 2025&ndash;2026</span>")
            + prose(body))
    write("teaching.html", shell("teaching.html", "Teaching | Alaa Khamis",
                                 "Courses, keynote speeches, tutorials and seminars by Alaa Khamis.", html))


def extract_body_from_string(raw):
    start = raw.find('class="body-copy w-richtext">')
    start = raw.index(">", start) + 1
    end = raw.find("<footer", start)
    chunk = raw[start:end]
    return re.sub(r"(?:\s*</div>)+\s*$", "", chunk)


# ---- books ---------------------------------------------------------------

def build_books():
    raw = read("books.html")
    start = raw.find('<div class="post-title-section">')
    end = raw.find("<footer", start)
    chunk = raw[start:end]

    # each work is introduced by an <h1> inside a post-title-section
    chunk = re.sub(r'<div class="post-title-section">\s*</div>', "", chunk)
    chunk = re.sub(r'<div class="post-title-section">\s*<h1>(.*?)</h1>\s*'
                   r'<div class="post-info-wrapper"><div class="post-info">(.*?)</div></div></div>',
                   lambda m: '<h2 id="%s">%s</h2>\n<p class="pub-date"><em>%s</em></p>'
                             % (slugify(m.group(1)), m.group(1), m.group(2)),
                   chunk, flags=re.S)
    # one entry lost its wrapper in the legacy file
    chunk = re.sub(r'<h1>(.*?)</h1>\s*<div class="post-info-wrapper"><div class="post-info">(.*?)</div></div>',
                   lambda m: '<h2 id="%s">%s</h2>\n<p class="pub-date"><em>%s</em></p>'
                             % (slugify(m.group(1)), m.group(1), m.group(2)),
                   chunk, flags=re.S)
    chunk = re.sub(r'<div class="body-copy w-richtext">', "", chunk)
    chunk = re.sub(r"(?:\s*</div>)+\s*$", "", chunk)
    body = clean(chunk)
    body = body.replace("<p>By the end of the book you should understand:<p>",
                        "<p>By the end of the book you should understand:</p>")

    html = (page_header("Books &amp; Publications Hubs",
                        "Two published books, an open-source Jupyter book and a Medium publication on "
                        "AI for smart mobility.")
            + prose(body))
    write("books.html", shell("books.html", "Books | Alaa Khamis",
                              "Optimization Algorithms, Smart Mobility, AI Search Algorithms for Smart "
                              "Mobility and the AI4SM Medium publication.", html))


# ---- home ----------------------------------------------------------------

STATS = [
    ("6", "Books authored"),
    ("200+", "Peer-reviewed papers"),
    ("72", "US patents filed"),
    ("44", "Courses taught"),
    ("Top 2%", "Most-cited scientists"),
]

CARD_ICONS = {
    "research": '<path d="M9 3v6.5L3.8 18A2 2 0 0 0 5.5 21h13a2 2 0 0 0 1.7-3L15 9.5V3M8 3h8M8.5 14h7"/>',
    "publications": '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v15H6.5A2.5 2.5 0 0 0 4 19.5zM4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/>',
    "teaching": '<path d="M12 3 2 8l10 5 10-5-10-5Z"/><path d="M6 10.5V16c0 1.7 2.7 3 6 3s6-1.3 6-3v-5.5M21 9v6"/>',
    "service": '<path d="M12 21s-7.5-4.6-7.5-10A4.5 4.5 0 0 1 12 7.6 4.5 4.5 0 0 1 19.5 11c0 5.4-7.5 10-7.5 10Z"/>',
}

HOME_CARDS = [
    ("research", "Research", "research.html",
     "AI at the intersection of mobility systems, services, and business models: seamless "
     "integrated mobility, software-defined vehicle observability, contextual causal "
     "inference, and design, planning, and control problems.",
     "Explore research"),
    ("publications", "Publications", "publications.html",
     "Six books, seven book chapters, more than 200 refereed papers and 72 filed US patents, "
     "trade secrets and defensive publications.",
     "Browse publications"),
    ("teaching", "Teaching", "teaching.html",
     "Forty-four undergraduate and graduate courses across Canada, Saudi Arabia, Spain and Egypt, "
     "with class sizes from 8 to 600 students.",
     "See courses"),
    ("service", "Service &amp; Honors", "services.html",
     "Founding chair of the IEEE ITSS Saudi Arabia Chapter and of IEEE SM; editor, reviewer, and "
     "recipient of the 2018 IEEE MGA Achievement Award.",
     "View service record"),
]

HOME_NEWS = [
    'As part of KFUPM&rsquo;s Ibn Battuta Global Scholarship Program, I spent June and July 2026 as a '
    'Visiting Professor at the <a href="https://uttri.utoronto.ca/" target="_blank" rel="noopener noreferrer">'
    'University of Toronto Transportation Research Institute (UTTRI)</a>, working on adaptive traffic signal control.',

    'I have been appointed Founding Chair of the <a href="https://ieee-itss.org/chapters-committees/saudi-chapter/" '
    'target="_blank" rel="noopener noreferrer">IEEE Intelligent Transportation Systems Society (ITSS) Saudi Arabia '
    'Chapter</a>, leading the establishment of the Society&rsquo;s activities in the Kingdom.',

    'My paper &ldquo;<a href="https://doi.org/10.1016/j.array.2026.100932" target="_blank" rel="noopener noreferrer">'
    'Agentic Ontology-guided Image Generation and Evaluation for Rare-Event Data Augmentation in Safety-Critical '
    'Perception</a>&rdquo; has been accepted for publication in <em>Array</em>, 2026.',

    'Two post-doctoral fellow positions are open in the AI for Smart Mobility Lab at KFUPM, on agentic AI for '
    'seamless integrated mobility and contextual observability of software-defined vehicles. '
    '<a href="https://ai4sm.org/join.html" target="_blank" rel="noopener noreferrer">Details here</a>.',

    'My papers &ldquo;<a href="https://ieeexplore.ieee.org/abstract/document/11083588" target="_blank" '
    'rel="noopener noreferrer">Agentic AI Systems: Architecture and Evaluation using a Frictionless Parking '
    'Scenario</a>&rdquo; and &ldquo;Rethinking Vehicle Architecture Through Softwarization and Servitization&rdquo; '
    'were accepted by <em>IEEE Access</em>, 2025.',

    'I won first place in the <a href="https://umrah.sspchallenge.com/en/" target="_blank" rel="noopener noreferrer">'
    'Sustainable Solutions for Pilgrims Challenge (Umrah Challenge)</a>, part of the Umrah and Ziyarah Forum '
    'organized by the Ministry of Hajj and Umrah in Al-Madinah, April 2025.',
]


def build_home():
    stats = "\n".join(
        '<div class="stat"><div class="stat__num">%s</div><div class="stat__label">%s</div></div>' % (n, l)
        for n, l in STATS)

    cards = "\n".join("""<article class="card">
  <div class="card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg></div>
  <h3>%s</h3>
  <p>%s</p>
  <a class="link-more" href="%s">%s</a>
</article>""" % (CARD_ICONS[key], title, blurb, href, cta)
        for key, title, href, blurb, cta in HOME_CARDS)

    news = "\n".join("<li>%s</li>" % n for n in HOME_NEWS)

    body = """<section class="hero">
  <div class="wrap">
    <div class="hero__grid">
      <div>
        <div class="eyebrow">AI for Smart Mobility</div>
        <h1>Alaa Khamis</h1>
        <p class="hero__credentials">PhD, SMIEEE &middot; Associate Professor, KFUPM</p>
        <p class="hero__lead">
          My research sits at the intersection of artificial intelligence and mobility systems, services and
          business models: from seamless integrated mobility and software-defined vehicle observability
          to the design, planning, and control problems behind people mobility, logistics, and
          transportation infrastructure.
        </p>
        <ul class="affiliations">
          <li><strong>Director</strong>, <a href="https://ai4sm.org/" target="_blank" rel="noopener noreferrer">AI for Smart Mobility Lab</a>, KFUPM</li>
          <li><strong>Chair</strong>, <a href="https://ieee-itss.org/chapters-committees/saudi-chapter/" target="_blank" rel="noopener noreferrer">IEEE Intelligent Transportation Systems Society, Saudi Chapter</a></li>
          <li>Department of Industrial and Systems Engineering &amp; IRC for Smart Mobility and Logistics, College of Computing and Mathematics, King Fahd University of Petroleum and Minerals</li>
          <li>Adjunct Faculty, University of Toronto and Ontario Tech University</li>
          <li>Formerly AI &amp; Smart Mobility Technical Leader, General Motors</li>
        </ul>
        <div class="actions">
          <a class="btn btn--primary" href="shortbio.html">Read the full bio
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </a>
          <a class="btn btn--ghost" href="publications.html">Publications</a>
        </div>
      </div>
      <div class="hero__portrait">
        <img src="images/AlaaKhamis.png" alt="Portrait of Alaa Khamis" width="260" height="318">
      </div>
    </div>
    <div style="margin-top:36px">%s</div>
  </div>
</section>

<section class="stats">
  <div class="wrap">
    <div class="stats__grid">
%s
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <div>
        <h2>What I work on</h2>
        <p>Research, writing and teaching around artificial intelligence for smart, sustainable and inclusive mobility.</p>
      </div>
    </div>
    <div class="cards">
%s
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section__head">
      <div>
        <h2>Books</h2>
        <p>Written for practitioners who need to put search, optimization, and mobility technology to work.</p>
      </div>
      <a class="link-more" href="books.html">All books and publication hubs</a>
    </div>
    <div class="books-grid">
      <article class="book">
        <a href="https://www.manning.com/books/optimization-algorithms" target="_blank" rel="noopener noreferrer">
          <img src="images/OptimizationAlgorithms.jpeg" alt="Cover of Optimization Algorithms">
        </a>
        <div>
          <h3>Optimization Algorithms: AI techniques for design, planning, and control problems</h3>
          <p>Manning Publications, 2024. Deterministic and stochastic derivative-free optimization, nature-inspired
             search and machine-learning methods, with Python case studies throughout.</p>
          <a class="link-more" href="books.html#optimization-algorithms-ai-techniques-for-design-planning-and-control-problems">About this book</a>
        </div>
      </article>
      <article class="book">
        <a href="https://link.springer.com/book/10.1007/978-1-4842-7101-8" target="_blank" rel="noopener noreferrer">
          <img src="images/Cover.jpg" alt="Cover of Smart Mobility">
        </a>
        <div>
          <h3>Smart Mobility: Exploring Foundational Technologies and Wider Impacts</h3>
          <p>Apress (Springer Nature), 2021. A holistic view of how the smart mobility triad (technology,
             governance, and city planning) combines to create sustainable mobility.</p>
          <a class="link-more" href="books.html#smart-mobility-exploring-foundational-technologies-and-wider-impacts">About this book</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <div>
        <h2>Latest news</h2>
        <p>Appointments, papers, keynotes and lab announcements.</p>
      </div>
      <a class="link-more" href="events.html">All news and events</a>
    </div>
    <ul class="news-list">
%s
    </ul>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section__head"><div><h2>Get in touch</h2></div></div>
    <div class="contact">
      <div class="contact__item">
        <h3>Office</h3>
        <p>Department of Industrial and Systems Engineering, King Fahd University of Petroleum and Minerals,
           Dhahran 31261, Saudi Arabia</p>
      </div>
      <div class="contact__item">
        <h3>Email</h3>
        <p><a href="mailto:alaakhamis@gmail.com">alaakhamis@gmail.com</a></p>
      </div>
      <div class="contact__item">
        <h3>Lab</h3>
        <p><a href="https://ai4sm.org/" target="_blank" rel="noopener noreferrer">AI for Smart Mobility Lab</a>.
           Open postdoctoral positions.</p>
      </div>
    </div>
  </div>
</section>
""" % (social_html(), stats, cards, news)

    write("index.html", shell(
        "index.html", "Alaa Khamis | AI for Smart Mobility",
        "Alaa Khamis, PhD, SMIEEE. Associate Professor and Director of the AI for Smart Mobility Lab at KFUPM; "
        "author of Optimization Algorithms and Smart Mobility.",
        body))


# --------------------------------------------------------------------------
# Run
# --------------------------------------------------------------------------

if __name__ == "__main__":
    # bring the images across so the new site is self-contained
    src_img = os.path.join(SRC, "images")
    dst_img = os.path.join(OUT, "images")
    if not os.path.isdir(dst_img):
        shutil.copytree(src_img, dst_img)

    build_home()

    build_simple("shortbio.html", "shortbio.html", "About",
                 "Associate Professor and Director of the AI for Smart Mobility Lab at KFUPM.",
                 "About | Alaa Khamis",
                 "Biography of Alaa Khamis: Associate Professor at KFUPM, former AI &amp; Smart Mobility "
                 "Technical Leader at General Motors.",
                 updated="November 2024")

    build_simple("research.html", "research.html", "Research",
                 "AI at the intersection of mobility systems, services, and business models: "
                 "projects, grants, and graduate supervision.",
                 "Research | Alaa Khamis",
                 "Research program, funded projects and thesis supervision of Alaa Khamis.",
                 updated="November 2024")

    build_simple("services.html", "services.html", "Service",
                 "Community and university service, editorial boards and reviewing.",
                 "Service | Alaa Khamis",
                 "Professional and community service, editorial boards and reviewing activity.",
                 updated="July 2025")

    build_simple("awards.html", "awards.html", "Awards &amp; Honors",
                 "Recognition from IEEE, General Motors, Stanford/Elsevier and others.",
                 "Awards &amp; Honors | Alaa Khamis",
                 "Awards, honours, fellowships and appointments received by Alaa Khamis.",
                 updated="May 2025")

    build_publications()
    build_events()
    build_teaching()
    build_books()

    # 404
    not_found = """<section class="page-header">
  <div class="wrap">
    <div class="eyebrow">Error 404</div>
    <h1>This page doesn&rsquo;t exist</h1>
    <p class="page-header__sub">The link may be out of date, or the page may have moved when the site was rebuilt.</p>
  </div>
</section>
<div class="prose">
  <div class="wrap wrap--narrow">
    <p>Try one of these instead:</p>
    <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="shortbio.html">About</a> &middot; <a href="research.html">Research</a> &middot; <a href="publications.html">Publications</a></li>
      <li><a href="books.html">Books</a> &middot; <a href="teaching.html">Teaching</a> &middot; <a href="services.html">Service</a></li>
      <li><a href="awards.html">Awards &amp; Honors</a> &middot; <a href="events.html">News &amp; Events</a></li>
    </ul>
  </div>
</div>
"""
    write("404.html", shell("404.html", "Page not found | Alaa Khamis",
                            "The page you were looking for could not be found.", not_found))

    # sitemap + robots
    urls = "\n".join(
        "  <url><loc>https://alaakhamis.org/%s</loc></url>" % ("" if h == "index.html" else h)
        for h, _ in NAV)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % urls)
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: https://alaakhamis.org/sitemap.xml\n")

    print("done")
