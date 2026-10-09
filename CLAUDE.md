# Winterborne Hire & Styling website: notes for Claude

The Winterborne Hire & Styling site (wedding styling and prop hire, Dorset), moved from Webflow to Netlify.
It is the plain Webflow export: static HTML, no build step. Every push to `main` deploys automatically.

## Working on it

There is nothing to install or build. To preview locally, serve the repo root, for example:

```bash
npx serve .      # http://localhost:3000
```

## Where things live

| What | File |
| --- | --- |
| Pages | `*.html` in the repo root (served without `.html`, e.g. `/contact-us`), plus `bespoke-florals/` |
| Styles | `css/winterborne-vintage.webflow.css` (the Webflow export), `css/site.css` (our additions, loaded after it), `css/webflow.css`, `css/normalize.css` |
| Scripts | `js/webflow.js` (animations, menu, tabs), `js/jquery-3.5.1.min.js`, `js/contact-form.js` |
| Images, video, fonts | `images/`, `videos/`, `fonts/` |
| Netlify settings (redirects, headers) | `netlify.toml` |

The navigation and footer are repeated in every page, so a change there must be made in each `.html` file.

## Forms

The forms use **Netlify Forms**. Submissions appear in the Netlify dashboard under *Forms*:

- `contact` on `contact-us.html`
- `showroom` on `showroom.html`
- `commercial` on `commercial-installations.html`
- `quote` on `quote-builder.html` (sent by `js/quote-builder.js`, see below)

`js/contact-form.js` sends the form and shows the Webflow thank-you or error message. The wrapper div has the class
`netlify-form` instead of Webflow's `w-form`, so `webflow.js` doesn't take over the submit. Spam is filtered with a honeypot field.

## Instagram feed

Pages with the "Instagram" section show a grid of the latest posts, straight from Instagram's API (no LightWidget):

- `netlify/functions/instagram.mjs` serves `/api/instagram`: the latest 12 posts as JSON, cached by Netlify for an hour.
- `netlify/functions/instagram-refresh.mjs` runs weekly and renews the access token (they expire after 60 days).
  The renewed token is kept in Netlify Blobs; `netlify/lib/instagram-token.mjs` reads and saves it.
- `js/instagram-feed.js` and `css/instagram-feed.css` draw the grid. If the feed can't load, only the
  "Follow @winterbornehireandstyling" button shows.
- The token lives in the Netlify environment variable `INSTAGRAM_ACCESS_TOKEN`, never in the code. Pasting a new token
  there (then redeploying) always takes over from the renewed one.

## Bespoke Florals

A top-level menu item, right of Collection, on every page. Hovering shows a dropdown of the five subcategories
(alphabetical); clicking "Bespoke Florals" on desktop opens `/bespoke-florals` (`js/nav.js`). On phones the dropdown
starts with an "All bespoke florals" link instead.

- `bespoke-florals/index.html`: overview with a numbered section per subcategory.
- `bespoke-florals/<slug>.html`: archways, custom-installations, floral-pillars, moongates, urns-and-plinths.
  Built in the Faux Florals style (reusing its `ff-` classes) plus `css/bespoke-florals.css`.
- Every page has the subcategory strip (`.bf-subnav`); the current one has `is-current` (dark olive highlight).
- Photos are existing site and testimonial photos for now.

## Quote builder (prototype)

`/quote-builder` lets couples add florals, hire pieces and services, see an estimated range, then save it.

- **Prices** are in `js/quote-data.js`, taken from the "Styling Catalogue & Pricing Guide 2027/28". "From £X" uses X;
  "£8-£12" uses the midpoint. Update this file when the price list changes.
- **The range** is 20% below to 20% above the total, rounded to £5 (`QUOTE_RANGE` in `js/quote-builder.js`).
- **Saving** posts the quote to the Netlify form `quote` (name, email, venue, date, estimate and the full item list as
  text; the hidden `subject` field sets the notification email's subject). Netlify emails it to
  winterbornevintage@gmail.com via a form notification set up in the Netlify dashboard, and downloads a PDF made in the browser with jsPDF (`js/vendor/jspdf.umd.min.js`, v2.5.2, hosted with the site).
- The half-built quote is remembered in the visitor's browser (localStorage) until they clear it.
- The page isn't linked from the navigation yet.

## Testimonials

`/our-testimonials` is plain HTML (no CMS): one `<article class="tm">` per couple in `our-testimonials.html`, newest
first, with styles in `css/testimonials.css` and the slider/full-screen viewer in `js/testimonials.js`. Photos live in
`images/testimonials/<names>/`. To add a couple, follow `.claude/skills/add-testimonial/SKILL.md` so every block matches.

## Notes from the Webflow move

- Removed: the test pages, `small-props-old`, the search page, the password page and the empty `detail_*` CMS templates.
  Old URLs for the removed pages redirect in `netlify.toml`.
- **The Webflow export does not include CMS content.** Lists built from Webflow collections (the prop grids on
  Large Props, Small Props, Table Decor, Florals and so on, plus testimonials, gallery and blog lists) show
  "No items found" until that content is rebuilt from the collections' CSV exports.
- The hero video, jQuery and share images are hosted with the site. Fonts, jQuery UI, Masonry, Elfsight and
  still load from their own CDNs.

## Staging (not indexed)

While the Webflow site is still live, this copy is hidden from search engines so Google doesn't see duplicate pages:

- every page has `<meta name="robots" content="noindex, nofollow">`
- `netlify.toml` sends an `X-Robots-Tag: noindex, nofollow` header for every file (images and video too)

Don't block the site in `robots.txt`: crawlers would then never see the noindex. **At launch**, remove the meta tag
from every page and the `X-Robots-Tag` block from `netlify.toml`.

## Rules for changes

- Keep the Webflow class names and `data-w-id` / `data-wf-page` attributes. `js/webflow.js` uses them.
- Link pages as `/page-name` and assets as `/images/...` (root-relative), so the 404 page works at any URL.
- Commit to `main` with a clear message. Netlify deploys it within about a minute.
