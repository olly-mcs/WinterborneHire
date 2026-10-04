---
name: add-testimonial
description: Add a couple's testimonial to the Winterborne testimonials page (our-testimonials.html) in the house format - Google review as live text with stars, names, venue and month, a photo slider, and a brush-stroke floral palette. Use whenever someone wants to add, update or remove a testimonial.
---

# Add a testimonial

Every couple on `/our-testimonials` uses the same block. Follow these steps so they all match.
The first one, Laura & Alexandra, is the reference: copy its `<article class="tm">` in `our-testimonials.html`.

## 1. Collect

Ask for anything missing before building:

- **The Google review** (screenshot or text). Copy the wording **exactly**, keeping the reviewer's paragraph breaks,
  and read the star count from the screenshot. Don't correct spelling or grammar. Show only the reviewer's
  **first name**, the review text and the stars: no review date, "time ago", review count, profile photo,
  Local Guide badge or Google branding.
- **First names** of both partners, in the order the couple prefers (bride & bride, groom & groom, bride & groom).
- **Venue** and **month and year** of the wedding (no exact day unless asked).
- **The story**: how they found us, what they're like as a couple, their vision for the day and the florals we made.
  Write it as three paragraphs in glowing, warm terms (first one is the lead, shown larger). If the user only gives
  notes, draft it and show them before publishing.
- **Showroom visits** (how many) and **first visit to wedding** (the lead time, e.g. "14 months").
- **Photos.** For a big set, ask them to push a folder to `images/testimonials/incoming/` with GitHub Desktop.

## 2. Choose the photos

Pick **6-8** photos, varied, with the **florals as the priority**. Aim for a mix of:

1. the biggest floral installation (arch, columns, backdrop): this is slide 1;
2. a wide shot of the ceremony or reception styling;
3. a close-up of the bouquet (also the best source for the palette);
4. tables, aisle or other floral details;
5. one or two moments with energy (confetti, walking) where the flowers still show;
6. a portrait to finish.

Drop near-duplicates and photos with little or no floristry. Tell the user which you picked and why.

Save them as `images/testimonials/<first>-<first>/NN-short-description.jpg` (e.g. `01-floral-archway.jpg`),
in slider order. Keep files under about 300 KB each.

## 3. Build the palette

Find **5-7 colours** from the flowers and foliage only (not dresses, skin, stone or sky):

```bash
python3 -m http.server 8099 --directory . &   # from the repo root
node .claude/skills/add-testimonial/palette.js testimonials/<slug> 03-bridal-bouquet.jpg:0.18,0.66,0.76,0.86 01-floral-archway.jpg:0,0.25,0.3,0.95
```

Regions are fractions of the image covering only flowers. If skin, wood or floors creep in (common with very bright
florals), rerun with `MIN_SAT=0.45` in front of the command. Merge near-identical clusters, drop any that are skin or
background, and give each a short floral name (Burgundy, Blush, Lilac, Foliage...). Always include the main foliage green.
Round to clean hex values; small adjustments towards what the flowers actually look like are fine.

## 4. Write the block

Copy Laura & Alexandra's `<article class="tm">` and change:

- `id` and the `aria-labelledby` ids to the new slug;
- the story: three paragraphs in `.tm-story-text` (first keeps `class="tm-story-lead"`), and the `.tm-facts`
  values (showroom visits, first visit to wedding, venue, wedding month);
- names in `.tm-names` (keep the `<span class="tm-amp">&amp;</span>`), and `.tm-meta` (venue, month year);
- slides: one `<li class="tm-slide">` per photo with descriptive `alt` text (what the florals are, who is in shot).
  Landscape photos get `tm-slide tm-slide-wide` and `style="--tm-backdrop:url('...')"` on the `.tm-open` button.
  If most of a couple's photos are landscape, add `tm-gallery-landscape` to `.tm-gallery` for a 3:2 frame instead,
  and give the portrait photos `tm-slide tm-slide-fit` plus the same backdrop style;
- thumbnails (same order) and the total in `.tm-count`;
- stars: one `<svg>` per star and the `aria-label` ("Rated N out of 5");
- the review paragraphs in `.tm-quote`, and `.tm-cite` (the reviewer's first name only);
- swatches: `style="--swatch:..."`, the `fill` on the first `<path>`, the name and the hex. Cycle the three stroke
  shapes already used.

**Newest wedding goes first** in `.tm-list` (by wedding month, not by when it was added). Layout alternates sides automatically.


## 5. Check and publish

- Serve the site and check `/our-testimonials` at desktop (1440px) and phone (390px) widths: slider arrows, thumbnails,
  the full-screen viewer, and that nothing overflows.
- Commit to `main` with a message like "Add testimonial: <names>, <venue>" and push.
