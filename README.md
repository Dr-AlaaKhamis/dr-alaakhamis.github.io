# alaakhamis.org — rebuilt

A modern, responsive, two-theme (light/dark) rebuild of the personal site, generated from the
content of the previous `alaakhamis.github.io` site. Plain static HTML/CSS/JS — no build step,
no framework, no dependencies to install.

## Structure

```
index.html          Home — hero, key figures, section cards, books, latest news, contact
shortbio.html       About
research.html       Research programme, funded projects, thesis supervision
publications.html   Publications (searchable + filterable by category)
books.html          Books and publication hubs
teaching.html       Courses, keynotes, tutorials, seminars
services.html       Community and university service, editorial boards, reviewing
awards.html         Awards and honours
events.html         News and events (searchable)
404.html            Not-found page
sitemap.xml         Sitemap
robots.txt          Crawler policy
assets/css/style.css  Design system + all components
assets/js/main.js     Theme toggle, mobile nav, back-to-top, list filtering
images/             Portrait, book covers, diagrams
teaching/ PDF/ projects/ RAS/ MineProbe/   Course archives carried over unchanged
```

Page filenames are unchanged from the old site, so existing inbound links and bookmarks keep working.

## Themes

The accent is IEEE blue — `#00629b` in light, lifted to `#6db3ea` in dark so it stays legible on the
dark navy ground. Light is the default. Dark applies automatically when the visitor's OS prefers it, and the
sun/moon button in the header overrides that; the choice is stored in `localStorage`. The theme is
applied by an inline script in `<head>` before first paint, so there is no flash of the wrong colours.

All colours live as custom properties at the top of `assets/css/style.css` — in `:root` (light),
`:root[data-theme="dark"]`, and a `prefers-color-scheme: dark` block. Change the palette there
and both themes follow.

## Deploying

Copy the contents of this folder over the root of the `alaakhamis.github.io` repository, commit
and push. Google Analytics (`G-SEV4N949B2`) and the Google site-verification tag are carried over.

## Editing

### Adding a news item
Add an `<li>` at the top of the list in `events.html`, and (optionally) a matching `<li>` in the
`news-list` on `index.html`.

### Adding a publication
Add an `<li data-item>` inside the right `<section data-group="…">` in `publications.html`. The
`data-item` attribute is what makes the entry searchable and filterable.

### Adding a course
Copy an existing `<li><details><summary>…</summary><p class="details-body">…</p></details></li>`
block in `teaching.html`.

### Updating the key figures on the home page
Edit the `.stats__grid` block near the top of `index.html`.
