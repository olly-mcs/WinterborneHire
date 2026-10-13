"""Product page content for each Bespoke Florals type, keyed by the type's slug (see SECTIONS in
build-bespoke-florals.py, which sets the name, section and short text).

- gallery: the slider photos, first one first. "wf:<collection>/<file>" means a Webflow product photo, served from the
  600px and 1200px copies in images/webflow-sized/; anything else is a normal image path.
- about: the paragraphs beside the slider (four).
- details: "Good to know" rows as (label, value). Rows can be left out; the section only shows when there are any.
- faq: extra questions for this type, shown before the questions every page shares (FAQ in the build script).
"""

T = "/images/testimonials/"

PRODUCTS = {
    # ---------- The Ceremony ----------
    "aisle-meadows": dict(
        gallery=[
            ("wf:florals-foliage/english-garden-meadow-aisle-arrangements-hover", "Aisle lined on both sides with white and green meadow arrangements"),
            ("wf:florals-foliage/english-garden-meadow-aisle-arrangements", "Meadow arrangement of pale blue, peach and white blooms at the end of a row of chairs"),
            (T + "laura-alexandra/02-ceremony-aisle.jpg", "Outdoor ceremony aisle with guests either side"),
            (T + "sophie-ben/03-ceremony-aisle.jpg", "Ceremony aisle lined with pastel floral pedestals"),
        ],
        about=[
            "Create a breathtaking aisle with our meadow arrangements: low, loose clusters of blooms and foliage that line the way to your ceremony, so the walk to your partner feels like a stroll through a garden.",
            "Each arrangement is custom made to match your colour palette and style, from soft whites and greens to bright, joyful wildflower mixes. They sit at the ends of your rows, and look just as good in a grand hall as on a lawn.",
            "They're one of our most versatile pieces. Once the ceremony is over they can be moved to the edges of the dance floor, along the front of the top table, around the bar or beside your cake.",
            "Like all our bespoke florals, they're made with high-quality silk and real-touch blooms, so they stay fresh all day, whatever the weather, and look perfect in every photo.",
        ],
        details=[("Price", "£50 each"), ("Colours", "Designed in your colour palette"),
                 ("Indoors or out", "Both, from great halls to garden lawns"), ("After the ceremony", "Easy to move to the top table, bar or dance floor")],
    ),
    "moongates": dict(
        gallery=[
            ("wf:large-props/foliage-circular-arch", "Couple embracing in front of a full circle moongate of white florals and foliage"),
            ("wf:large-props/foliage-circular-arch-hover", "Full circle floral moongate at a ceremony"),
            ("/images/173MelDave-1-1.jpg", "Bride beneath a moongate of rich jewel-toned blooms"),
            ("wf:large-props/gold-metal-moongate-hover", "Gold metal moongate behind a top table, dressed with florals and terracotta draping"),
            ("wf:large-props/crescent-moon-floral-backdrop", "Crescent moon backdrop of green foliage and white blooms"),
        ],
        about=[
            "Our moongates provide the perfect framework for a stunning floral backdrop. Their circular shape frames the two of you beautifully, and gives every guest a clear view of the moment you say I do.",
            "Keep the florals concentrated for a modern look, create an abundant crescent sweeping around the circle, or go for a totally foliage-led design. Every moongate is custom designed to your colour palette and floral style.",
            "Choose our full floral moongate, or our gold metal moongate dressed with a bespoke floral arrangement and fabric draping in your colours.",
            "Freestanding and fully movable, a moongate can frame your ceremony and then move behind your top table, giving you a picture-perfect backdrop for the speeches too.",
        ],
        details=[("Moongate", "£495, 2m high"), ("Metal moongate", "From £250, 2m high"), ("Draping", "£20 for the metal moongate"),
                 ("Colours", "Designed in your colour palette"), ("After the ceremony", "Moves behind your top table")],
    ),
    "pillars": dict(
        gallery=[
            ("wf:large-props/xl-straight-pillars", "Couple standing between two tall floral pillars of peach, white and green in front of a gazebo"),
            ("wf:large-props/xl-straight-pillars-hover", "Couple kissing between white floral pillars beneath a wrought iron gazebo"),
            (T + "laura-alexandra/01-floral-archway.jpg", "Floral pillars of burgundy, crimson and dusty pink framing a stone archway"),
            (T + "laura-alexandra/04-doorway-arch.jpg", "Greenery and red rose pillars framing an open doorway"),
            (T + "hannah-dave/04-reaching-up-to-the-arch.jpg", "Bride reaching up to a colourful floral arch made from two pillars"),
        ],
        about=[
            "Our floral pillars are one of our most versatile pieces, creating a statement backdrop for your ceremony without needing a traditional arch.",
            "Each pair is custom designed for your wedding, matched to your colour palette and floral style. Keep them soft and romantic, fill them with colour, or style them with dramatic blooms for a contemporary look.",
            "Freestanding and fully movable, they can frame your ceremony and then be repositioned behind your top table or at the entrance, so they work hard all day. Two pillars of different heights can also be joined into a full floral arch.",
            "Made with high-quality silk blooms, they give you the luxury and beauty of fresh flowers without the high cost, and create picture-perfect moments wherever they stand.",
        ],
        details=[("XL floral pillars", "£545, 2.1m high"), ("As a full arch", "£595, pillars of 2.1m and 1.8m"),
                 ("Colours", "Designed in your colour palette"), ("After the ceremony", "Move behind the top table or to the entrance")],
    ),
    "urns-and-plinths": dict(
        gallery=[
            ("wf:large-props/english-garden-floral-urns-plinths", "Couple kissing between two large white floral urns on plinths"),
            ("wf:large-props/english-garden-floral-urns-plinths-hover", "White floral urns on plinths either side of a staircase"),
            (T + "sophie-ben/04-ceremony-kiss.jpg", "Couple kissing at the ceremony between tall pastel floral arrangements"),
            (T + "sophie-ben/03-ceremony-aisle.jpg", "Ceremony aisle lined with pastel floral pedestals"),
        ],
        about=[
            "Our large urns on plinths are perfect for couples who want to make an impact. Filled with abundant florals and foliage, they bring a sense of grandeur to your ceremony.",
            "They work beautifully in grand country houses, historic venues and formal ceremony spaces, but can also be styled with softer, looser blooms for a more relaxed look.",
            "Placed in pairs to frame your ceremony, they move easily to the reception afterwards to dress the top table, the entrance or the foot of a staircase.",
            "Each arrangement is crafted in our floral design studio using the highest quality silk flowers and foliage stems, giving you the luxury look of fresh florals without the high price tag.",
        ],
        details=[("Price", "£450"), ("Colours", "Designed in your colour palette"),
                 ("Best for", "Grand, historic and formal venues"), ("After the ceremony", "Move to the top table or entrance")],
    ),
    # ---------- The Reception ----------
    "bud-vases": dict(
        gallery=[
            ("/images/Table-Decor.webp", "Bud vases with bright stems along a wooden table"),
            ("wf:table-decor/pink-bud-vases", "Soft pink glass bud vases"),
            ("wf:table-decor/vinatge-cut-glass-bud-vases", "Vintage cut glass bud vases"),
            ("wf:table-decor/turquoise-bud-vases", "Turquoise glass bud vases"),
            ("wf:table-decor/orange-bud-vases", "Orange glass bud vases"),
        ],
        about=[
            "Little pops of colour, all along the table. Our bud vases hold single stems and small sprigs, and look beautiful clustered down long tables or grouped around a larger centrepiece.",
            "Choose clear, pink, green, orange or teal glass, or mix them together, then we'll fill them with stems in your colours.",
            "They're perfect for relaxed, colourful weddings, and pair beautifully with candles, tealights and taper candlesticks for a soft glow as the evening draws in.",
            "Because they're small, they're also an easy way to carry your florals onto the welcome table, the bar, the cake table and the signing table.",
        ],
        details=[("Price", "£8 to £12 each, with stems"), ("Glass", "Clear, pink, green, orange or teal"),
                 ("Colours", "Stems in your colour palette"), ("Pairs with", "Candles, tealights and taper candlesticks")],
    ),
    "footed-bowls": dict(
        gallery=[
            ("wf:florals-foliage/english-garden-low-centrepiece-arrangement", "Footed bowl arrangement of pink, peach and red blooms with taper candles"),
            ("wf:florals-foliage/english-garden-low-centrepiece-arrangement-hover", "White footed bowl arrangement on a long wooden table"),
            ("/images/Winterborne-Hire-Styling-Table-Decor-Closeup.jpg", "Table setting with candles and soft florals"),
        ],
        about=[
            "Elevate your table décor with our footed bowl arrangements: low, generous centrepieces custom made to match your style, design or colour theme.",
            "They sit below eye level, so your guests can see and chat to each other across the table, and the florals still feel abundant.",
            "Perfect for both round and straight tables, they add a touch of timeless elegance. Choose gold or white bowls, and style them with candles, taper candlesticks and bud vases.",
            "For a fuller look we also make larger bowl arrangements, which work well at the centre of long tables or on the top table.",
        ],
        details=[("Price", "£55 each"), ("Large bowls", "£65 each"), ("Bowls", "Gold or white"),
                 ("Tables", "Round and long tables"), ("Colours", "Designed in your colour palette")],
    ),
    "podiums": dict(
        gallery=[
            ("wf:florals-foliage/tall-podium-centrepiece", "Tall podium centrepiece of white blooms and greenery on a gold stand"),
            ("wf:florals-foliage/tall-podium-centrepiece-hover", "Tall peach and white podium arrangements above round tables in a marquee"),
            (T + "sophie-ben/01-reception-floral-centrepieces.jpg", "Tall pastel floral arrangements above reception tables"),
        ],
        about=[
            "Make a bold statement with our tall floral podium centrepieces, custom designed to match your style, colour palette or theme.",
            "Lifted on 70cm stands, the florals sit above your guests' heads, so they fill the room without blocking anyone's view across the table.",
            "Perfect for round or straight tables, they're the ultimate in table décor and really come into their own in marquees, barns and rooms with high ceilings.",
            "Choose from our range of stands in gold, black or clear, and finish the table with candles and smaller arrangements underneath.",
        ],
        details=[("Price", "£145 each"), ("Stands", "Gold, black or clear, 70cm high"),
                 ("Tables", "Round and long tables"), ("Best for", "Marquees, barns and high ceilings")],
    ),
    "top-table": dict(
        gallery=[
            ("wf:florals-foliage/english-garden-top-table-centrepiece", "Top table dressed with a long white and green floral arrangement in front of a fireplace"),
            ("wf:florals-foliage/english-garden-top-table-centrepiece-hover", "Couple raising a toast behind a top table of white florals"),
            (T + "hannah-dave/02-reception-arch-and-tables.jpg", "Long reception tables with a floral arch at the top table"),
            ("wf:large-props/gold-metal-moongate-hover", "Gold moongate with florals behind a top table"),
        ],
        about=[
            "All eyes are on the two of you at the top table, so make it unforgettable with a stunning floral centrepiece designed just for it.",
            "Custom designed to suit your style, it can be a long, low garland of blooms running the length of the table, or a fuller arrangement with height at the centre.",
            "It can be tailored to any colour palette or theme, and is a lovely way to carry the florals from your ceremony through to the reception, especially with pillars, a moongate or urns moved in behind.",
            "Designed to look as good in the speeches photos as it does in the room, it's the finishing touch your reception deserves.",
        ],
        details=[("Price", "From £145"), ("Colours", "Designed in your colour palette"),
                 ("Pairs with", "Pillars, moongates or urns moved from the ceremony")],
    ),
    # ---------- Your Florals ----------
    "bridal-bouquets": dict(
        gallery=[
            ("wf:florals-foliage/custom-made-bridal-bouquets", "Bride holding a white and green bridal bouquet"),
            ("wf:florals-foliage/custom-made-bridal-bouquets-hover", "Couple embracing, the bride holding a white bouquet"),
            (T + "hannah-dave/03-bridal-bouquet.jpg", "Bride holding a bright meadow bouquet"),
            (T + "sophie-ben/02-bouquet-close-up.jpg", "Close up of a pastel bridal bouquet"),
            (T + "laura-alexandra/03-bridal-bouquet.jpg", "Bridal bouquet of deep reds and dusty pinks"),
        ],
        about=[
            "Complete your wedding look with a custom-made bridal bouquet, designed around you: your dress, your colours and your style.",
            "From loose and wild meadow bouquets to neat, classic posies, every one is made in our Dorset studio with high-quality faux florals that match the rest of your wedding.",
            "Faux bouquets don't wilt, so yours will look as fresh in the last photo of the night as it did walking down the aisle, whatever the weather.",
            "Pair it with matching bridesmaids' bouquets and buttonholes so every detail ties together into one cohesive look.",
        ],
        details=[("Price", "From £125"), ("Colours", "Designed around your dress and colour palette"),
                 ("Pairs with", "Bridesmaids' bouquets and buttonholes")],
    ),
    "bridesmaids-bouquets": dict(
        gallery=[
            (T + "hannah-dave/06-bridesmaids-bouquets.jpg", "Bridesmaids holding colourful bouquets"),
            (T + "hannah-dave/07-bouquet-flat-lay.jpg", "Flat lay of a bridal bouquet, bridesmaids' bouquets and buttonholes"),
            (T + "steph-karl/03-bouquet-in-the-marquee.jpg", "Bride holding a bright bouquet in a colourful marquee"),
        ],
        about=[
            "Your wedding party, all in bloom. Our bridesmaids' bouquets are smaller arrangements designed to complement yours and tie the whole party together.",
            "Choose matching designs for a classic look, or give each bridesmaid her own colour from your palette for something more playful.",
            "Like your bridal bouquet, they're made with high-quality faux florals, so they stay perfect from the first photos to the last dance.",
            "For younger members of the wedding party, we also make single stem bouquets and fairy wands.",
        ],
        details=[("Price", "From £55 each"), ("Colours", "Matched to your bouquet and palette"),
                 ("Also available", "Single stem bouquets and fairy wands")],
    ),
    "buttonholes": dict(
        gallery=[
            (T + "hannah-dave/05-buttonhole.jpg", "Floral buttonhole on a suit lapel"),
            (T + "hannah-dave/07-bouquet-flat-lay.jpg", "Flat lay of bouquets and buttonholes"),
        ],
        about=[
            "The finishing touch. Our bespoke buttonholes are made with the same blooms as your bouquet, so the whole wedding party matches.",
            "They're for the groom and groomsmen, the fathers of the couple, and anyone else you'd like to include on the day.",
            "Choose a single bloom with a sprig of foliage for a classic look, or something a little wilder to match a meadow bouquet.",
            "Made with high-quality faux florals, they won't wilt or bruise, so they look just as good in the evening photos.",
        ],
        details=[("Price", "From £10 each"), ("Colours", "Matched to your bouquet"),
                 ("For", "Grooms, groomsmen, parents and family")],
    ),
    # ---------- Installations ----------
    "arbors": dict(
        gallery=[
            ("/images/Abbotsbury-Subtropical-Gardens.webp", "Couple at a gazebo dressed with white florals"),
            ("/images/backdrops-arches.webp", "Couple beneath a white rose and greenery arch"),
            (T + "hannah-dave/01-kiss-under-floral-arch.jpg", "Couple kissing beneath a rainbow floral arch"),
        ],
        about=[
            "Many venues have their own arbor, pergola or gazebo, and with the right florals it becomes the most beautiful spot in the place.",
            "We design florals made to measure for your venue's structure, so the design fits it exactly: a cascade across the top, blooms climbing the sides, or a full floral frame.",
            "Every design is created in your colours and floral style, to tie in with the rest of your ceremony and reception florals.",
            "Start with photos of your venue's arbor at your showroom consultation, and we'll design the florals around it.",
        ],
        details=[("Price", "From £495"), ("Made to measure", "For any arbor, pergola or gazebo"),
                 ("Colours", "Designed in your colour palette")],
    ),
    "chandeliers": dict(
        gallery=[
            ("wf:florals-foliage/faux-floral-chandelier-decor", "Floral chandelier of autumnal blooms and foliage hanging in a stone barn"),
            ("/images/Styling.webp", "Hanging floral chandeliers above round tables in a marquee"),
        ],
        about=[
            "A beautiful installation designed to create the wow factor. We decorate your venue's chandelier light fittings with gorgeous florals and foliage.",
            "Hanging florals draw the eye up and fill tall spaces, without taking up any room on your tables.",
            "Available for 3ft and 4ft chandeliers, in foliage alone or with custom florals in your colour scheme, from autumnal seasonal blooms to soft whites and greens.",
            "We install them for you. Please note the decor is for your light fitting, which isn't included.",
        ],
        details=[("Price", "From £360"), ("Sizes", "For 3ft and 4ft chandeliers"), ("Styles", "Foliage, or custom florals in your colours"),
                 ("Installation", "Installed for you"), ("Light fitting", "Not included, decor only")],
    ),
    "ladders": dict(
        gallery=[
            ("wf:florals-foliage/wisteria-foliage-suspended-ladder-decor", "Suspended ladders dressed with wisteria and foliage above long tables in a barn"),
            ("wf:florals-foliage/faux-foliage-garland-decor-for-suspended-ladders", "Suspended ladders with foliage garlands above long tables"),
            ("wf:florals-foliage/faux-foliage-garland-decor-for-suspended-ladders-hover", "Foliage-dressed ladders above tables in a rustic barn"),
        ],
        about=[
            "Create an amazing rustic statement with suspended ladders dressed in lush foliage, wisteria or custom florals, hung above your long tables.",
            "They form a canopy of greenery over your guests, and make a beautiful backdrop for the speeches and first dance photos.",
            "Available for both 3m and 4.5m ladders, in foliage alone or with florals in your colours. They're a real showstopper in barns and marquees.",
            "We install them for you. Please note the decor is for your venue's ladder light fitting, which isn't included.",
        ],
        details=[("Price", "From £150 per ladder"), ("Sizes", "For 3m and 4.5m ladders"), ("Styles", "Foliage, wisteria or custom florals"),
                 ("Installation", "Installed for you"), ("Ladder", "Not included, decor only")],
    ),
}
