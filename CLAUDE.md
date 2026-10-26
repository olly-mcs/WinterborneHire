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

## Hire collection (menu and structure)

The hire collection mirrors Bespoke Florals: an overview, four sections and a page per product. Everything is in
`scripts/hire_products.py` (sections, products, their colours or styles, copy, and which old Webflow products each one
replaces); `scripts/build-bespoke-florals.py` builds the pages, the **Hire Collection** menu (two columns, like Bespoke
Florals) and the footer's Hire Collection list. Styles: `css/hire-collection.css` on top of the Bespoke Florals ones.

- `/wedding-prop-hire-collection`: the overview (hero, section strip, a block per section with its products)
- `/table-decor`, `/signage`, `/small-props`, `/seating-areas`: a section each (Seating Areas is chairs, tables, rugs
  and runners; it replaced Furniture & Rugs)
- `/<section>/<product>`: product pages. Each merges several old products. Their options ("variants") show as colour
  swatches (`options="swatches"`, e.g. Coloured Napkins) or a row of style names; choosing one moves the slider to its
  photos and sets what "Add to your wish list" adds (`js/hire-options.js`). A product or option with no photos yet
  shows "Photos coming soon".
- **Old URLs:** every old product page redirects (301) to the product it was merged into, or to its section if it's no
  longer hired. The build writes these into `netlify.toml` between `# hire-redirects:start` / `end`; don't edit them by
  hand. Old product pages are deleted by the build.
- **Large Props** is hidden from the menu; its page and products are still live (built by `build-webflow-content.py`).
- **Florals & Foliage** is gone (Bespoke Florals covers it). Each old product redirects to its closest Bespoke
  Florals product, or `/bespoke-florals` where there's no match (`netlify.toml`).
- `js/hire-items.js` (written by the build) names the hire products and options for the wish list; no stock count or
  price is shown.
- Copy still to come: the Table Decor, Small Props and Seating Areas section text (lorem ipsum for now).

## Products and older testimonials (from the Webflow CMS)

The Webflow CMS exports (CSV) were converted to `data/webflow-content.json`: Florals & Foliage, Signage, Rugs & Runners,
Large Props, Small Props, Table Decor, Furniture, the Faux Florals gallery and the older testimonials. `scripts/build-webflow-content.py` builds from it:

- the Large Props product grid and its product pages (`/large-prop-collection/<slug>`), between
  `<!-- products:start -->` / `<!-- products:end -->` markers (the rest of the hire collection is built from
  `scripts/hire_products.py`, above; the photos still come from `images/webflow-sized/`);
- the "More kind words" section on `our-testimonials.html` (between `kind-words` markers).

Images: `scripts/fetch-webflow-images.mjs` saves them from Webflow's CDN into `images/webflow/`; the build uses a saved
copy when it exists, otherwise Webflow's URL. `scripts/resize-webflow-images.mjs` (needs `npm install --no-save sharp`)
makes WebP copies at 600px and 1200px wide in `images/webflow-sized/`; pages use those with `srcset` and never load the
originals, which are kept as the archive. The GitHub Action `.github/workflows/save-webflow-images.yml` runs both
(it can be started by hand from the Actions tab). To change a product, edit the JSON and run the build script.
`netlify.toml` rewrites `/signage` and `/florals-foliage` to their `.html` pages because a folder of
product pages shares each name. Styles: `css/products.css`.

## Old Webflow URLs

`data/webflow-sitemap.xml` is the old Webflow site's sitemap (saved by `.github/workflows/fetch-webflow-sitemap.yml`).
`python3 scripts/check-sitemap.py` lists every old URL that has no page or redirect yet. Keep new pages at the old
addresses where they exist, so launch needs as few redirects as possible.

## Bespoke Florals

A top-level menu item, right of Collection, on every page. It has four sections, each with its types:

- **The Ceremony**: Aisle Meadows, Moongates, Pillars, Urns & Plinths
- **The Reception**: Bud Vases, Footed Bowls, Podiums, Top Table
- **Your Florals**: Bridal Bouquets, Bridesmaids' Bouquets, Buttonholes
- **Installations**: Arbors, Chandeliers, Ladders

Everything is generated by `scripts/build-bespoke-florals.py` from its `SECTIONS` list (names and short text) and
`scripts/bespoke_products.py` (each type's slider photos, four paragraphs, "Good to know" details and extra questions),
so edit those and run `python3 scripts/build-bespoke-florals.py`. Types are always sorted alphabetically. It writes:

- `bespoke-florals/index.html`: the overview. Under the hero, a strip of the four sections, then a numbered block per
  section with its types as a row of cards.
- `bespoke-florals/<section>.html` (`the-ceremony`, `the-reception`, `your-florals`, `installations`): a numbered block
  per type, each with an anchor, e.g. `/bespoke-florals/the-ceremony#pillars`. Built in the old Faux Florals style
  (its `ff-` classes in `site.css`) plus `css/bespoke-florals.css`. `netlify.toml` rewrites each section's URL to its
  `.html` page because a folder of product pages shares its name.
- `bespoke-florals/<section>/<type>.html`, e.g. `/bespoke-florals/the-ceremony/aisle-meadows`: a product page per
  type. A photo slider on the left (`js/bespoke-gallery.js`; arrows, thumbnails and the counter only show with more
  than one photo), the name, price and four paragraphs on the right, then "Good to know" and questions, the section's
  other types and tiles for the other three sections. Styles: `css/bespoke-product.css`. Prices come from the
  price guide (the same figures as `js/quote-data.js`).
- **Adding product photos**: put the originals in `images/bespoke-florals/<type>/originals/` with short names
  (e.g. `minterne-house.jpg`), run `node scripts/resize-bespoke-images.mjs` (needs `npm install --no-save sharp`) to
  make the 600px and 1200px WebP copies beside them, then list them in the type's `gallery` in
  `scripts/bespoke_products.py` without the extension (e.g. `P + "minterne-house"`) and run the build. The first photo
  is also the type's photo on the overview and section pages. With more than five photos the thumbnail row scrolls.
- **Sliding between sections**: the overview and the four section pages load `css/bespoke-slide.css` and
  `js/bespoke-slide.js` (in `<head>`), so moving between them slides sideways (forward to the right along the strip,
  back to the left) with the header and section strip held still. It uses the browser's cross-page View Transitions:
  Chrome, Edge and Safari 18.2+; other browsers load the page normally. Product pages don't slide.
- **the menu on every page**: a two-column dropdown. Sections on the left; hovering one shows its types on the right
  (The Ceremony's show by default). Clicking "Bespoke Florals" on desktop opens `/bespoke-florals` (`js/nav.js`).
  On phones the dropdown lists everything, types indented under their section, after an "All bespoke florals" link.

Photos are the old Webflow product photos plus site and testimonial photos for now (a wireframe).

## Floral wish list

The wish list tab (bottom right) is on every page (`ensure_wishlist` in `scripts/build-bespoke-florals.py`). Under the
list, "Add more florals" lists the Bespoke Florals sections and "Add hire collection items" lists Table Decor, Signage,
Small Props and Seating Areas; a hire product with colours or styles opens a nested list of its options
(`window.HIRE_SECTIONS` in `js/hire-items.js`, written by the build).

Every Bespoke Florals page loads `js/wishlist.js` and `css/wishlist.css` (added by the build script). Product pages
have an "Add to your wish list" button; a panel slides out from the right where couples change quantities and send
the list with their name, email, phone, wedding date, venue, how they heard about us and (optional, in "Why not book a
showroom appointment?") a day and time to visit. No prices or estimates are shown to them; the email includes a guide
total from the price list for Winterborne only. It posts to the Netlify form `quote` (subject "Floral wish list from <name>"); the
extra fields are declared as hidden inputs in that form in `quote-builder.html`, so Netlify keeps them. It's emailed to winterbornevintage@gmail.com like the quote builder. Under the list, "Add more florals" shows the four sections collapsed, each listing its products not yet in the list
with "+ Add" buttons, so the whole range can be added from the panel; the sections and page names come from `js/bespoke-sections.js`, which
the build script writes. A "Your wish list" tab stays bottom-right on every
Bespoke Florals page. The list is kept in the browser and shared with `/quote-builder`. Each product's `quote` in
`scripts/bespoke_products.py` is its id in `js/quote-data.js`, whose guide prices feed the estimate.

## Bridal bouquet shop (mock-up)

A design prototype for selling bouquets with UK delivery. `/bridal-bouquets-delivery` (`bridal-bouquets-delivery.html`,
built by `scripts/build-shop.py` from its `PRODUCTS` list: 6 bridal bouquets and 2 buttonholes, placeholder names,
copy and prices). "Add to basket" opens a basket panel (`js/shop.js`, `css/shop.css`), kept in the visitor's browser;
checkout isn't built. Every page has a "UK-wide delivery / Bouquets & buttonholes" pull tab hanging under the menu, added by
`scripts/build-bespoke-florals.py` (set `SHOP_TAB = False` there to remove it everywhere).

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

- Removed later: the Faux Florals page (now redirects to `/bespoke-florals`) and the Commercial page (redirects to
  the homepage). Both redirects are in `netlify.toml`.
- Removed: the test pages, `small-props-old`, the search page, the password page and the empty `detail_*` CMS templates.
  Old URLs for the removed pages redirect in `netlify.toml`.
- **The Webflow export does not include CMS content.** The product collections and testimonials have been rebuilt from
  the CSV exports (see above). The blog and wedding packages haven't been yet.
- The hero video, jQuery and share images are hosted with the site. Fonts, jQuery UI, Masonry, Elfsight and
  still load from their own CDNs.

## Staging (not indexed)

While the Webflow site is still live, this copy is hidden from search engines so Google doesn't see duplicate pages:

- every page has `<meta name="robots" content="noindex, nofollow">`
- `netlify.toml` sends an `X-Robots-Tag: noindex, nofollow` header for every file (images and video too)

Don't block the site in `robots.txt`: crawlers would then never see the noindex. **At launch**, remove the meta tag
from every page and the `X-Robots-Tag` block from `netlify.toml`.

## SEO

**Page titles and meta descriptions** are signed off in `data/page-meta.json` (one entry per page, keyed by its path
without `.html`). `scripts/apply-page-meta.py` writes them into each page's `<title>`, meta description and the
og:/twitter: tags, and every build script runs it last, so it wins over anything a build script sets. Change a title
or description there, not in the build scripts. Keep titles to about 60 characters and descriptions to about 155.

- **Business details for Google** (the `LocalBusiness` structured data, with `knowsAbout`/`makesOffer` listing the services, in every page's `<head>`): Steven's
  Farm, Dorchester DT2 9JR, 01305 889656, visits by appointment (no opening hours listed), 5.0 from 101 Google reviews.
  Keep these identical to the Google Business Profile (primary category: Wedding service); update the rating and count as they change.
- **Homepage** is six sections: hero, Bespoke Florals (the four sections), why couples choose Winterborne (facts),
  how it works, styling & hire, reviews and questions (with `FAQPage` structured data), then the showroom call to
  action. Its questions and answers are in `index.html` (both the visible text and the structured data).

- One `<h1>` per page. Headings retagged from the Webflow export carry `was-h1` / `was-h2` so they keep their old
  spacing (rules at the end of `css/bespoke-florals.css`).
- Titles about 60 characters and meta descriptions 70-160. Product pages get them from `seo_title` / `seo_description`
  in `scripts/build-webflow-content.py`; Bespoke Florals pages from `page()` / `meta_description` in its build script.
- `scripts/seo-images.py` sets each page's sharing image (`og:image`, `twitter:image`) to its main photo; both build
  scripts run it at the end. The homepage keeps its hand-picked image.
- Pages load only Cinzel and Raleway from Google Fonts (a plain stylesheet link). jQuery UI loads only on the showroom
  page, for its date picker. Don't add Masonry, reCAPTCHA or the WebFont loader back.
- At launch: remove the noindex (see "Staging"), add `sitemap.xml` and `robots.txt`, add GA4 (the old `UA-` tag is dead),
  and redirect or rebuild the 7 blog posts and 7 wedding packages that `scripts/check-sitemap.py` lists.

## "Captured at a real Winterborne wedding"

A small white caption (`.real-caption`, bottom right) on photos from real weddings, across the site: Bespoke Florals
(`REAL_CAPTION_PAGES`), the Our Services photos and the hire overview's real-wedding photos (`REAL_WEDDING_PHOTOS`).
Never on the testimonials page, product photos (hire and shop), photos with an overlay or hover effect (heroes,
homepage cards and panels), or wedding fair photos.

## Menu

The main menu is Bespoke Florals, Hire Collection, Our Services, Showroom, Testimonials, Contact. The About us dropdown
(Who we are, The Wedding Blog, Testimonials) is hidden for now and replaced by a plain Testimonials link; both pages are
still live and in the footer. To bring it back, swap the Testimonials link in every page's menu (marked with an
"About us dropdown ... hidden for now" comment) for the dropdown markup from git history.

## Reviews block

"Kind words from our couples" (homepage, Who we are and every Bespoke Florals product page) is built by
`scripts/reviews_block.py` from the four featured couples' reviews on `our-testimonials.html`. Each block holds all
four; `js/reviews.js` shows a random one per visit. To change a quote, edit the review on the testimonials page and
rebuild (`python3 scripts/build-bespoke-florals.py`). The old per-product `testimonial` entries in
`scripts/bespoke_products.py` are no longer shown.

## Rules for changes

- **Fonts: only these three, ever.** Don't bring in fonts from mockups or designs; translate them to these:
  - **Cinzel** for headlines, buttons and navigation (not for sentences or paragraphs; it's hard to read at length);
  - **Raleway** for all body copy, including lead paragraphs, quotes, labels and captions;
  - **Fake serif** (`"Fake serif", serif`, self-hosted in `fonts/`) for stylised, handwritten-looking headings
    such as "& styling".

- Keep the Webflow class names and `data-w-id` / `data-wf-page` attributes. `js/webflow.js` uses them.
- Link pages as `/page-name` and assets as `/images/...` (root-relative), so the 404 page works at any URL.
- Commit to `main` with a clear message. Netlify deploys it within about a minute.
