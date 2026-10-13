"""Product page content for each Bespoke Florals type, keyed by the type's slug (see SECTIONS in
build-bespoke-florals.py, which sets the name, section and short text).

- gallery: the slider photos, first one first. "wf:<collection>/<file>" means a Webflow product photo, served from the
  600px and 1200px copies in images/webflow-sized/. A path without an extension (e.g. P + "minterne-house") means a
  photo saved in images/bespoke-florals/<type>/originals/, served from the copies scripts/resize-bespoke-images.mjs
  makes beside it. Anything else is a normal image path.
- about: the paragraphs beside the slider (four).
- details: "Good to know" rows as (label, value). Rows can be left out; the section only shows when there are any.
- faq: extra questions for this type, shown before the questions every page shares (FAQ in the build script).
"""

T = "/images/testimonials/"
P = "/images/bespoke-florals/pillars/"
B = "/images/bespoke-florals/"

PRODUCTS = {
    # ---------- The Ceremony ----------
    "aisle-meadows": dict(
        gallery=[
            (B + "aisle-meadows/lulworth-castle", "Couple walking back down an aisle at Lulworth Castle lined on both sides with white meadow arrangements"),
            (B + "aisle-meadows/kingston-maurward-detail", "Close up of pale blue, peach and white meadow arrangements along an aisle at Kingston Maurward"),
            (B + "aisle-meadows/alysha-and-chris", "Bride walking down an aisle lined with pale blue and white meadow florals"),
            (B + "aisle-meadows/aisle-detail", "White and green meadow arrangement at the end of a row of chairs"),
            (B + "aisle-meadows/minterne-house", "Couple kissing at Minterne House, the aisle lined with white meadow florals"),
            (B + "aisle-meadows/gorwell", "Outdoor ceremony with colourful meadow florals leading to a gazebo"),
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
            (B + "moongates/grand-hall-aisle", "Aisle in a grand hall lined with colourful meadow florals, leading to a floral moongate"),
            (B + "moongates/vows-black-and-white", "Couple holding hands for their vows in front of a floral moongate, in black and white"),
            (B + "moongates/bridesmaids-at-the-moongate", "Bridesmaids in blush dresses holding bouquets in front of a floral moongate"),
            (B + "moongates/indoor-ceremony", "Couple exchanging vows beneath a floral moongate at an indoor ceremony"),
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
            (P + "church-wedding", "Couple outside a church doorway framed by tall pillars of peach, pink and white blooms"),
            (P + "minterne-house", "Couple at Minterne House between pillars of deep red, burgundy and pink florals"),
            (P + "italian-villa", "Couple on stone steps between lush white floral pillars"),
            (P + "gazebo-couple", "Couple beneath a wrought iron gazebo framed by peach and white floral pillars"),
            (P + "upwey-wishing-well", "Couple and flower girl walking out between pastel floral pillars at Upwey Wishing Well"),
            (P + "subtropical-gardens", "Couple beneath a wooden gazebo at Abbotsbury Subtropical Gardens, framed by peach and white floral pillars"),
            (P + "church-doorway-kiss", "Couple kissing in a church doorway between pillars of pink and red blooms"),
            (P + "rudge-farm", "Couple at Rudge Farm in front of a wall of bright, colourful florals"),
            (P + "kingston-maurward", "Pastel blue and peach floral pillars framing a tall window at Kingston Maurward"),
            (P + "indoor-ceremony-arch", "Pink, peach and white floral pillars framing a doorway in a grand hall"),
            (P + "gazebo-ceremony-walk", "Grooms walking back down the aisle from a gazebo framed by floral pillars"),
            (P + "gazebo-kiss", "Couple kissing beneath a gazebo between white and blue floral pillars"),
            (P + "kingston-courtyard-aisle", "Outdoor courtyard ceremony with soft blue and white florals"),
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
            (B + "urns-and-plinths/minterne-house", "Couple kissing at Minterne House between white floral urns on plinths, beneath a crystal chandelier"),
            (B + "urns-and-plinths/lulworth-castle-aisle", "Aisle at Lulworth Castle lined with white floral urns, leading to a grand chandelier"),
            (B + "urns-and-plinths/lulworth-castle-exit", "Couple walking back down the aisle at Lulworth Castle between white floral urns"),
            (B + "urns-and-plinths/pennsylvania-castle", "Couple kissing between pastel floral urns on plinths in a bright white ceremony room"),
            (B + "urns-and-plinths/wedding-fair", "White floral urns on plinths framing tall glass doors"),
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
            (B + "footed-bowls/ruby-and-henry", "Round table with a pink, red and white footed bowl arrangement and taper candles, floral pillars behind"),
            (B + "footed-bowls/alysha-and-chris-table", "Footed bowl of pale blue, yellow and white blooms on a round table"),
            (B + "footed-bowls/alysha-and-chris-gin-menu", "Yellow and white footed bowl arrangement with candles beside a table menu"),
            (B + "footed-bowls/candlelit-table", "Candlelit round table with a white footed bowl arrangement in a stone and brick hall"),
            (B + "footed-bowls/violet-rose-table", "White and green footed bowl arrangement on a table draped with ivory fabric"),
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
            (B + "podiums/ruby-and-henry", "Tall podium arrangement of red, pink and white blooms above a round table"),
            (B + "podiums/sage-reception", "Reception room with tall white and green podium arrangements above round tables and sage chair sashes"),
            (B + "podiums/marquee-podium", "Tall podium arrangement of white and blush blooms on a round table in a marquee"),
            (B + "podiums/marquee-tables", "Marquee reception with tall podium arrangements and hanging greenery above round tables"),
            (B + "podiums/ruby-and-henry-room", "Reception room with tall red and white podium arrangements on every table"),
            (B + "podiums/pennsylvania-castle", "Round table set beneath a tall pastel podium arrangement in a bright white room"),
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
            (B + "top-table/ruby-and-henry", "Top table with a pink and red floral arrangement, framed by floral pillars in front of a round window"),
            (B + "top-table/garland-speeches", "Couple at a top table dressed with a long garland of white blooms and greenery"),
            (B + "top-table/garland-laughter", "Bride laughing at a top table dressed with white florals and greenery"),
            (B + "top-table/sophie-and-ben", "Sophie and Ben at their top table behind white and blush florals"),
            (B + "top-table/long-top-table", "Long top table dressed with a full garland of white and green florals"),
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
            (B + "bridal-bouquets/autumn-bouquet", "Bride holding a loose bouquet of burnt orange, peach and white blooms with dried grasses"),
            (B + "bridal-bouquets/sophie-and-ben-portrait", "Bride by a tall window holding a soft pastel bouquet of pink, blue and white"),
            (B + "bridal-bouquets/moody-portrait", "Bride in a lace dress holding an autumnal bouquet with pampas, in moody light"),
            (B + "bridal-bouquets/laura-and-alexandra-portrait", "Bride seated in a grand room holding a bouquet of deep red and burgundy blooms"),
            (B + "bridal-bouquets/bright-meadow-bouquet", "Bride with a bright meadow bouquet in front of colourful floral pillars"),
            (B + "bridal-bouquets/alysha-and-chris", "Bride in a long veil holding a white, yellow and pale blue bouquet"),
            (B + "bridal-bouquets/hollie-and-tom", "Couple smiling in a garden, the bride holding a blush and white bouquet"),
            (B + "bridal-bouquets/gazebo-garden", "Couple walking from a gazebo, the bride holding a blush bouquet"),
            (B + "bridal-bouquets/pink-peony-bouquet", "Bride holding a bouquet of hot pink and white peonies beside her groom in military dress"),
            (B + "bridal-bouquets/sophie-and-ben-garden", "Couple walking across a lawn, the bride holding a pastel bouquet"),
            (B + "bridal-bouquets/laura-and-alexandra-lawn", "Couple walking across a lawn, the bride holding a deep red bouquet"),
            (B + "bridal-bouquets/pink-dress-bouquet", "Bride in a bright pink dress with a colourful bouquet, beneath a garden arch"),
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
            (B + "bridesmaids-bouquets/bridesmaids-in-orange", "Two bridesmaids in burnt orange dresses holding bright, colourful bouquets"),
            (B + "bridesmaids-bouquets/alysha-and-chris-bridal-party", "Bride with four bridesmaids in pale blue, all holding white, yellow and blue bouquets"),
            (B + "bridesmaids-bouquets/alysha-and-chris-aisle", "Bridesmaid in pale blue walking down an aisle lined with meadow florals, holding a white and yellow bouquet"),
            (B + "bridesmaids-bouquets/lavender-path", "Two bridesmaids in black holding white bouquets on a path lined with lavender"),
            (B + "bridesmaids-bouquets/alysha-and-chris-ceremony", "Bridesmaids in pale blue holding bouquets at an outdoor ceremony"),
            (B + "bridesmaids-bouquets/colourful-bridal-party", "Bride in bright pink with her bridesmaids in blue, all holding colourful bouquets"),
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
            (B + "buttonholes/buttonhole-close-up", "Close up of a bright buttonhole of pink, orange and yellow blooms on a navy suit lapel"),
            (B + "buttonholes/pinning-the-buttonhole", "Hands pinning a deep red and white buttonhole onto a tweed jacket"),
            (B + "buttonholes/laura-and-alexandra", "Couple at a wrought iron gate, one wearing a deep red buttonhole to match the bouquet"),
            (B + "buttonholes/couple-portrait", "Groom in a grey suit with a blush buttonhole, embracing the bride"),
            (B + "buttonholes/groom-with-dog", "Groom in a pink suit with a bright buttonhole, crouching beside a fluffy dog"),
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
            (B + "installations/autumn-arbor", "Outdoor ceremony with an oak arbor dressed in rust, burgundy and white florals, the aisle lined with meadow arrangements"),
            (B + "installations/autumn-arbor-kiss", "Couple kissing beneath an oak arbor dressed with autumnal florals"),
            (B + "installations/gazebo-garland", "Couple kissing beneath a gazebo dressed with a garland of bright, colourful florals"),
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
            (B + "installations/gazebo-garland", "Couple kissing beneath a gazebo dressed with a garland of bright, colourful florals"),
            (B + "installations/autumn-arbor", "Outdoor ceremony with an oak arbor dressed in rust, burgundy and white florals, the aisle lined with meadow arrangements"),
            (B + "installations/autumn-arbor-kiss", "Couple kissing beneath an oak arbor dressed with autumnal florals"),
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
            (B + "installations/autumn-arbor-kiss", "Couple kissing beneath an oak arbor dressed with autumnal florals"),
            (B + "installations/autumn-arbor", "Outdoor ceremony with an oak arbor dressed in rust, burgundy and white florals, the aisle lined with meadow arrangements"),
            (B + "installations/gazebo-garland", "Couple kissing beneath a gazebo dressed with a garland of bright, colourful florals"),
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
