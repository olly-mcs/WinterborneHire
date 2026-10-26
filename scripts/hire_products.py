"""The Hire Collection: its sections, the products in each, and where the old Webflow product pages now go.
Used by scripts/build-bespoke-florals.py, which builds the pages (see CLAUDE.md, "Hire collection").

Each product merges what used to be several Webflow products into one page, with its options listed as "variants".
A variant's photos come from the old products ("wf:<collection>/<slug>" is a photo in images/webflow-sized/; the
builder adds that product's second "-hover" photo when there is one). Clicking a variant moves the slider to its photos.

- options="swatches": colour circles (give each variant a swatch colour), for example the napkins
- options="styles" (the default): a row of names
- a variant with no photos is still listed and can be added to the wish list; a product with no photos at all shows a
  "Photos coming soon" panel
- meta: a section's meta description for search results (under about 155 characters)
- old: the old product page slugs (in their old Webflow folder) that now redirect here
"""

LOREM = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore "
         "magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.",
         "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
         "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."]


def V(name, *photos, swatch=None):
    return dict(name=name, photos=list(photos), swatch=swatch)


OVERVIEW = dict(
    title="Hire Collection",
    meta="Wedding prop hire in Dorset: table decor, signage, small props, chairs, rugs and more to complete your venue. See it all at our showroom near Dorchester.",
    tag="All the finishing touches for your wedding day.",
    body=["From statement backdrops and aisle decor to table styling, candles and signage, our hirable collection has "
          "everything you need to bring your vision to life. Carefully chosen pieces to complement your florals and "
          "complete your venue, so every detail feels considered and beautifully cohesive."],
    img=("/images/hire-collection/minterne-reception", "Reception at Minterne House from above: round tables with gold "
         "chairs, white florals along the top table and a floral mantelpiece", "50% 45%"),
)

SECTIONS = [
    dict(slug="table-decor", meta="Wedding table decor hire in Dorset: coloured napkins, charger plates, gold cutlery, candlesticks, bud vases and tea light holders to finish every table.",
         name="Table Decor", tag="Lorem ipsum dolor sit amet.", body=LOREM,
         img=("/images/testimonials/hannah-dave/02-reception-arch-and-tables.jpg",
              "Long reception tables with orange napkins and bright florals beneath a floral arch", "50% 50%"),
         products=[
             dict(slug="coloured-napkins", name="Coloured Napkins", options="swatches", options_title="Available colours",
                  tag="A simple detail that makes a big difference.",
                  about=["Coloured napkins are a beautiful way to add colour, texture and personality to your table "
                         "styling. Perfect for tying in with your wedding palette, they bring a considered, sophisticated "
                         "look and help to finish each place setting.",
                         "Our linen-look napkins are available to hire in a range of colours, from soft neutrals to earthy "
                         "tones and dusty pastels, so you can find the perfect shade to complement your florals, tableware "
                         "and overall style.",
                         "Whether you choose a relaxed knot, an elegant fold or styled with a napkin ring, they’re a simple "
                         "yet effective finishing touch that elevates your table decor and brings everything together."],
                  variants=[V("Sage", "wf:table-decor/sage-napkins", swatch="#8f9a72"),
                            V("Terracotta", "wf:table-decor/terracotta-napkin", swatch="#b4633f"),
                            V("Soft Blue", "wf:table-decor/soft-dusty-blue-napkin", swatch="#9aaabb"),
                            V("Soft Pink", "wf:table-decor/soft-pink-napkin", swatch="#e6bdb6")],
                  old=["sage-napkins", "terracotta-napkin", "soft-dusty-blue-napkin", "soft-pink-napkin"]),
             dict(slug="charger-plates", name="Charger Plates", options="swatches", options_title="Available finishes",
                  tag="The perfect base for every place setting.",
                  about=["Charger plates frame each place setting and pull your table styling together, adding colour, "
                         "texture and a little luxury before the first course arrives.",
                         "Choose from classic gold, a gold beaded rim, warm copper or natural seagrass, to suit anything "
                         "from formal and elegant to relaxed and boho.",
                         "Pair them with our coloured napkins and gold cutlery for a beautifully finished table."],
                  variants=[V("Gold", "wf:table-decor/gold-charger-plates", swatch="#c8a14b"),
                            V("Gold Beaded Rim", "wf:table-decor/gold-beaded-rim-perspex-charger-plate", swatch="#e4d3a8"),
                            V("Copper", "wf:table-decor/copper-charger-plates", swatch="#b06a3f"),
                            V("Seagrass", "wf:table-decor/seagrass-charger-plates", swatch="#b49a6c")],
                  old=["gold-charger-plates", "gold-beaded-rim-perspex-charger-plate", "copper-charger-plates",
                       "seagrass-charger-plates"]),
             dict(slug="gold-cutlery", name="Gold Cutlery", tag="A touch of gold at every place.",
                  about=["Our matte gold cutlery adds a soft, elegant shine to every place setting.",
                         "It works beautifully with our charger plates and coloured napkins, from classic and formal "
                         "tables to relaxed and romantic ones."],
                  variants=[V("Matte Gold", "wf:table-decor/matt-gold-cutlery")],
                  old=["matt-gold-cutlery"]),
             dict(slug="candlesticks", name="Candlesticks", tag="Warm candlelight for every table.",
                  about=["Candlesticks bring height, warmth and that soft candlelit glow to your reception tables.",
                         "Choose from vintage brass, cut glass, gold, silver, black or white, in classic or chunky styles, "
                         "or make a statement with our acrylic candelabra.",
                         "Mix heights and finishes along long tables, or group them around your florals for a romantic, "
                         "evening-ready look."],
                  variants=[V("Vintage Brass", "wf:table-decor/assorted-vintage-brass-candlesticks"),
                            V("Vintage Cut Glass", "wf:table-decor/assorted-vintage-glass-candlesticks"),
                            V("Gold", "wf:table-decor/trio-of-gold-candlesticks"),
                            V("Silver", "wf:table-decor/trio-of-silver-candlestick-holders"),
                            V("Black", "wf:table-decor/black-candlesticks"),
                            V("Black Chunky", "wf:table-decor/black-chunky-candlesticks"),
                            V("White Chunky", "wf:table-decor/white-chunky-candlesticks"),
                            V("Acrylic Candelabra", "wf:table-decor/8-arm-acrylic-candlestick-candelabra-centrepiece")],
                  old=["assorted-vintage-brass-candlesticks", "assorted-vintage-glass-candlesticks",
                       "trio-of-gold-candlesticks", "trio-of-silver-candlestick-holders", "black-candlesticks",
                       "black-chunky-candlesticks", "white-chunky-candlesticks",
                       "8-arm-acrylic-candlestick-candelabra-centrepiece"]),
             dict(slug="bud-vases", name="Bud Vases", tag="Little pops of colour along your tables.",
                  about=["Bud vases are an easy way to add colour and character to your tables, with a single stem or a "
                         "few small blooms in each.",
                         "Choose from coloured glass in pink, orange, turquoise and dark green, vintage cut glass or "
                         "stoneware, or our assorted glass and stone bottles for a relaxed, collected look.",
                         "Scatter them along long tables, cluster them around candles, or use them on your gift, card and "
                         "signing tables."],
                  variants=[V("Pink", "wf:table-decor/pink-bud-vases"),
                            V("Orange", "wf:table-decor/orange-bud-vases"),
                            V("Turquoise", "wf:table-decor/turquoise-bud-vases"),
                            V("Dark Green", "wf:table-decor/dark-green-glass-bud-vases-votives"),
                            V("Vintage Cut Glass", "wf:table-decor/vinatge-cut-glass-bud-vases"),
                            V("Stoneware", "wf:table-decor/eartenware-bud-vases"),
                            V("Glass Bottles", "wf:table-decor/assorted-vintage-glass-bottles"),
                            V("Stone Bottles", "wf:table-decor/assorted-small-earthenware-bottles")],
                  old=["pink-bud-vases", "orange-bud-vases", "turquoise-bud-vases", "dark-green-glass-bud-vases-votives",
                       "vinatge-cut-glass-bud-vases", "eartenware-bud-vases", "assorted-vintage-glass-bottles",
                       "assorted-small-earthenware-bottles"]),
             dict(slug="tea-light-holders", name="Tea Light Holders", tag="A soft glow, table to table.",
                  about=["Tea light holders add a gentle, flickering glow to your tables as the evening draws in.",
                         "Choose from clear glass, gold rimmed, speckled, twine-wrapped or stemmed holders and glass "
                         "cylinders, or hanging glass baubles to suspend above the table.",
                         "Use them on their own, or mix them with candlesticks and bud vases for layered, candlelit tables."],
                  variants=[V("Clear Glass", "wf:table-decor/clear-glass-table-tealight-holders"),
                            V("Gold Rimmed", "wf:table-decor/gold-rimmed-tealight-holders"),
                            V("Speckled", "wf:table-decor/speckled-tea-light-holders"),
                            V("With Twine", "wf:table-decor/small-glass-candle-holders-with-twine"),
                            V("Stemmed", "wf:table-decor/trio-of-tall-glass-tealight-holders"),
                            V("Glass Cylinders", "wf:table-decor/trio-of-glass-table-cylinders"),
                            V("Hanging Baubles", "wf:table-decor/glass-hanging-baubles")],
                  old=["clear-glass-table-tealight-holders", "gold-rimmed-tealight-holders", "speckled-tea-light-holders",
                       "small-glass-candle-holders-with-twine", "trio-of-tall-glass-tealight-holders",
                       "trio-of-glass-table-cylinders", "glass-hanging-baubles"]),
             dict(slug="chair-drapes", name="Chair Drapes", options="swatches", options_title="Available colours",
                  tag="Soft colour for every chair.",
                  about=["Our crinkle chair drapes add a soft, romantic finish to your chairs, tied simply at the back for "
                         "a relaxed, flowing look.",
                         "Choose from five colours to tie in with your napkins, florals and overall palette."],
                  variants=[V("Cream", "wf:table-decor/cream-crinkle-chair-drapes", swatch="#eee5d3"),
                            V("Light Beige", "wf:table-decor/light-beige-crinkle-chair-drapes", swatch="#d6c4a6"),
                            V("Sage Green", "wf:table-decor/sage-green-crinkle-chair-drapes", swatch="#9aa583"),
                            V("Forest Green", "wf:table-decor/forest-green-crinkle-chair-drape", swatch="#3f5440"),
                            V("Soft Pink", "wf:table-decor/soft-pink-crinkle-chair-drapes", swatch="#e6bdb6")],
                  old=["cream-crinkle-chair-drapes", "light-beige-crinkle-chair-drapes", "sage-green-crinkle-chair-drapes",
                       "forest-green-crinkle-chair-drape", "soft-pink-crinkle-chair-drapes"]),
         ],
         # no longer hired: these old pages go to the Table Decor page
         removed=["blackboard-table-numbers", "chalkboard-table-number", "gold-frame-table-numbers-with-dried-fern",
                  "mini-table-easels"]),

    dict(slug="signage", meta="Wedding signage hire in Dorset: table plans, welcome signs, order of the day, menus, name cards and neon signs, designed in your colours and fonts.",
         name="Signage", tag="Beautiful details to guide your day.",
         body=["From welcome signs and seating plans to table numbers and personalised details, our hirable signage "
               "collection adds the perfect finishing touch to your wedding.",
               "We have a range of frames, stands and styles to suit every setting, whether you’re looking for something "
               "modern and minimal or bold and colourful. Pair with our faux florals, ribbons and props to create a "
               "cohesive look that ties everything together."],
         # stand-in until the signage photo is uploaded
         img=("wf:signage/metal-frames-with-custom-signage-designs",
              "A printed table plan in a black metal frame, with a smaller sign and blue and white florals", "50% 40%"),
         products=[
             dict(slug="table-plans", name="Table Plans", tag="Help every guest find their seat.",
                  about=["Your table plan is one of the first things guests look for, so it should look as good as it works.",
                         "Choose a statement mirror with your plan designed onto the glass, a fabric banner hung from our "
                         "large frame, or a printed design in a black or gold metal frame.",
                         "Every design is made in our studio in your colours and fonts, and can be finished with a small faux "
                         "floral arrangement to match your wedding florals."],
                  variants=[V("Mirror", "wf:signage/large-gilt-frame-mirror"),
                            V("Banner", "wf:signage/fabric-banner-wedding-sign"),
                            V("Printed", "wf:signage/metal-frames-with-custom-signage-designs")],
                  old=["large-gilt-frame-mirror", "fabric-banner-wedding-sign", "metal-frames-with-custom-signage-designs"]),
             dict(slug="welcome-signs", name="Welcome Signs", tag="Set the tone from the moment guests arrive.",
                  about=["A beautiful welcome sign greets your guests and sets the scene for the day ahead.",
                         "Choose an ornate mirror, a printed sign in a metal frame, or our gold arched full-length mirror, "
                         "which doubles as a selfie mirror your guests will love.",
                         "Each sign is designed in our studio with your names, date and message."],
                  variants=[V("Mirror", "wf:signage/decorative-arched-mirror-sign-hover"),
                            V("Printed", "wf:signage/metal-frames-with-custom-signage-designs-hover"),
                            V("Selfie Mirror", "wf:signage/gold-arched-full-length-mirror")],
                  old=["decorative-arched-mirror-sign", "gold-arched-full-length-mirror"]),
             dict(slug="order-of-the-day", name="Order of the Day", tag="Let your guests know what’s coming next.",
                  about=["An order of the day keeps everyone in the loop, from the ceremony and drinks to the speeches and "
                         "first dance.",
                         "Choose a mirror with your timeline designed onto the glass, or a printed sign in a metal frame, "
                         "styled in your colours."],
                  variants=[V("Mirror Timeline", "wf:signage/decorative-arched-mirror-sign"),
                            V("Printed")],
                  old=[]),
             dict(slug="menus", name="Menus", tag="A beautiful finishing touch for every place setting.",
                  about=["Printed menus let your guests know what’s on the table, and add a lovely finishing touch to each "
                         "place setting.",
                         "Choose a gold clip or a bow detail, designed in your colours and fonts to match the rest of your "
                         "stationery and signage."],
                  variants=[V("Gold Clip"), V("Bow Detail")], old=[]),
             dict(slug="name-cards", name="Name Cards", tag="Every guest, in their place.",
                  about=["Folded name cards show each guest where to sit, and finish your place settings beautifully.",
                         "They’re designed in our studio to match your table plan, menus and the rest of your signage."],
                  variants=[V("Folded")], old=[]),
             dict(slug="neon-signs", name="Neon Signs", tag="A fun, glowing statement for your backdrop.",
                  about=["A neon sign instantly brings a little fun and glow to your wedding.",
                         "Hang one in our moongates or archways, on a foliage wall, or add it to your own backdrop or venue "
                         "decor for a statement photo spot."],
                  variants=[V("Mr & Mrs", "wf:signage/mr-mrs-neon-sign"),
                            V("Crazy in Love", "wf:signage/crazy-in-love-neon-sign-in-pink")],
                  old=["mr-mrs-neon-sign", "crazy-in-love-neon-sign-in-pink"]),
         ],
         removed=["chalk-a-board", "antique-gold-metal-decorative-easel", "white-metal-decorative-easel",
                  "handmade-wooden-signs", "wooden-circular-welcome-sign", "rustic-wood-rectangular-welcome-sign",
                  "order-of-the-day-pallet-sign", "no-seating-plan-pallet-sign"]),

    dict(slug="small-props", meta="Wedding prop hire in Dorset: cake stands, card boxes, lanterns, disco balls and finishing touches to style your venue, from welcome table to dance floor.",
         name="Small Props", tag="Lorem ipsum dolor sit amet.", body=LOREM,
         # stand-in until the small props photo is uploaded
         img=("wf:small-props/gold-glass-card-box-hover", "Gold-framed glass card box on a white table", "50% 50%"),
         products=[
             dict(slug="cake-stands", name="Cake Stands", tag="Give your cake the stage it deserves.",
                  about=["Show off your wedding cake with one of our cake stands, chosen to suit your cake and your style.",
                         "Choose from a large gold cake hoop, a marble top stand, cut glass stands or a rustic three-tier "
                         "log slice stand."],
                  variants=[V("Gold Cake Hoop", "wf:small-props/large-gold-cake-hoop"),
                            V("Marble Top", "wf:small-props/marble-top-cake-stand"),
                            V("Cut Glass", "wf:small-props/assorted-cut-glass-cake-stands"),
                            V("Log Slice", "wf:small-props/3-tier-log-slice-cake-stand")],
                  old=["large-gold-cake-hoop", "marble-top-cake-stand", "assorted-cut-glass-cake-stands",
                       "3-tier-log-slice-cake-stand"]),
             dict(slug="card-boxes", name="Card Boxes", tag="Somewhere special for your cards.",
                  about=["Keep your cards and gifts safe and beautifully displayed with one of our card boxes.",
                         "Choose from clear or gold-framed glass card boxes, or a wicker card basket, with or without a "
                         "hessian lining."],
                  variants=[V("Gold Glass", "wf:small-props/gold-glass-card-box"),
                            V("Glass", "wf:small-props/glass-card-box"),
                            V("Wicker Basket", "wf:small-props/wicker-card-basket"),
                            V("Hessian Lined Basket", "wf:small-props/hessian-lined-wicker-card-basket")],
                  old=["gold-glass-card-box", "glass-card-box", "wicker-card-basket", "hessian-lined-wicker-card-basket"]),
             dict(slug="lanterns", name="Lanterns", tag="Candlelight for every corner.",
                  about=["Lanterns bring a warm glow to your aisle, entrance, tables and dance floor.",
                         "Choose from gold geometric, star, Moroccan, white and gold, rattan and handmade wooden lanterns, "
                         "or tall glass cylinders for floor-standing candlelight."],
                  variants=[V("Gold Geometric", "wf:small-props/gold-geometric-lanterns"),
                            V("Gold", "wf:small-props/gold-lantern"),
                            V("Star", "wf:small-props/star-lanterns"),
                            V("Moroccan", "wf:small-props/new-moroccan-lantern"),
                            V("White & Gold", "wf:small-props/white-gold-lanterns"),
                            V("Square Rattan", "wf:small-props/rattan-lanterns-2"),
                            V("Handmade Wooden", "wf:small-props/handmade-wooden-lanterns"),
                            V("Black Square Cylinders", "wf:small-props/black-square-cylinder-vases"),
                            V("Floor-Standing Glass", "wf:small-props/floor-standing-glass-cylinder-vases")],
                  old=["gold-geometric-lanterns", "gold-lantern", "star-lanterns", "new-moroccan-lantern",
                       "white-gold-lanterns", "rattan-lanterns-2", "handmade-wooden-lanterns", "black-square-cylinder-vases",
                       "floor-standing-glass-cylinder-vases"]),
             dict(slug="other-props", name="Other Props", tag="The little extras that finish the look.",
                  about=["Lots of little extras to style your venue, from the welcome table to the dance floor.",
                         "Choose from log slices, handmade wooden crates, a vintage galvanised tub, glass demijohns and "
                         "vintage flagons, vintage wooden shelving, gold and silver disco balls and a mirrored gold trolley."],
                  variants=[V("Log Slices", "wf:small-props/log-slices"),
                            V("Wooden Crates", "wf:small-props/handmade-wooden-crates"),
                            V("Galvanised Tub", "wf:small-props/vintage-galvanished-tub"),
                            V("Demijohns", "wf:small-props/glass-demijohns", "wf:small-props/vintage-flagons-demijons"),
                            V("Wooden Shelving", "wf:small-props/vintage-wooden-shelving"),
                            V("Disco Balls", "wf:small-props/disco-balls", "wf:small-props/gold-disco-balls"),
                            V("Mirrored Gold Trolley", "wf:small-props/mirrored-gold-metal-trolly")],
                  old=["log-slices", "handmade-wooden-crates", "vintage-galvanished-tub", "glass-demijohns",
                       "vintage-flagons-demijons", "vintage-wooden-shelving", "disco-balls", "gold-disco-balls",
                       "mirrored-gold-metal-trolly"]),
         ],
         removed=["boho-printed-square-cushions", "extra-large-dreamcatcher", "large-bottle-with-seagrass-twine"]),

    dict(slug="seating-areas", meta="Wedding furniture hire in Dorset: peacock chairs, cane armchairs, boho side tables, and vintage rugs and runners for lounge areas, top tables and aisles.",
         name="Seating Areas", tag="Lorem ipsum dolor sit amet.", body=LOREM,
         img=("/images/testimonials/steph-karl/02-peacock-chairs-and-florals.jpg",
              "Couple on peacock chairs on a round jute rug, with disco balls and a bright meadow arrangement", "50% 62%"),
         products=[
             dict(slug="chairs", name="Chairs", tag="A statement seat for the two of you, and your guests.",
                  about=["From our peacock chairs to cane armchairs, egg chairs and sofas, our seating creates relaxed, "
                         "stylish spaces for you and your guests.",
                         "Use them for a statement top table, a cosy lounge area or a photo spot, and add footstools and "
                         "pouffes to finish the look."],
                  variants=[V("Peacock Chairs", "wf:furniture/a-pair-of-peacock-chairs", "wf:furniture/cane-peacock-chair"),
                            V("Cane Armchair", "wf:furniture/cane-armchair"),
                            V("Egg Chair", "wf:furniture/small-cane-egg-chair"),
                            V("Vintage Wicker Chair", "wf:furniture/vintage-wicker-chair"),
                            V("Jay Sofa Set", "wf:furniture/jay-sofa-set"),
                            V("Footstools & Pouffes", "wf:furniture/wicker-and-cane-footstool",
                              "wf:furniture/vintage-boho-footstool", "wf:furniture/wicker-pouffe")],
                  old=["a-pair-of-peacock-chairs", "cane-peacock-chair", "cane-armchair", "small-cane-egg-chair",
                       "vintage-wicker-chair", "jay-sofa-set", "wicker-and-cane-footstool", "vintage-boho-footstool",
                       "wicker-pouffe"]),
             dict(slug="tables", name="Tables", tag="The finishing piece for your lounge areas.",
                  about=["Side and coffee tables pull a seating area together, with space for drinks, candles and florals.",
                         "Choose from cane, carved wood and brass-topped boho tables, and our vintage wicker peacock side "
                         "table."],
                  variants=[V("Cane Side Table", "wf:furniture/cane-side-table"),
                            V("Carved Brass Top", "wf:furniture/carved-brass-top-boho-table"),
                            V("Carved Wood Coffee Table", "wf:furniture/carved-wood-boho-coffee-table"),
                            V("Carved Wood Side Tables", "wf:furniture/pair-of-boho-carved-wood-side-tables"),
                            V("Wicker Peacock Side Table", "wf:furniture/vintage-wicker-peacock-side-table")],
                  old=["cane-side-table", "carved-brass-top-boho-table", "carved-wood-boho-coffee-table",
                       "pair-of-boho-carved-wood-side-tables", "vintage-wicker-peacock-side-table"]),
             dict(slug="rugs-and-runners", name="Rugs & Runners", tag="Layer up colour, pattern and comfort.",
                  about=["Rugs and runners make any space feel warm and welcoming, from an outdoor aisle to a cosy lounge "
                         "area.",
                         "Choose from vintage and Persian-style rugs in reds, creams, pinks, sage and orange, a round rattan "
                         "rug, and long runners for aisles and walkways."],
                  variants=[V("Charity Vintage", "wf:rugs-runners/charity-vintage-rug"),
                            V("Cornhill Vintage", "wf:rugs-runners/cornhill-vintage-rug"),
                            V("Judith", "wf:rugs-runners/large-brown-persian-rug"),
                            V("Large Vintage Red", "wf:rugs-runners/large-vintage-red-rug"),
                            V("Large Red Azerbaijan", "wf:rugs-runners/large-red-azerbaijan-rug"),
                            V("Pretty Cream Floral", "wf:rugs-runners/pretty-cream-floral-rug"),
                            V("Pretty Sage Vintage", "wf:rugs-runners/pretty-sage-vintage-rug"),
                            V("Red Aztec", "wf:rugs-runners/red-aztec-rug"),
                            V("Round Rattan", "wf:rugs-runners/round-rattan-rug"),
                            V("Vintage Cream & Pink", "wf:rugs-runners/vintage-cream-and-pink-rug"),
                            V("Vintage Orange", "wf:rugs-runners/vintage-orange-rug"),
                            V("Ethnic Runner", "wf:rugs-runners/ethnic-runner"),
                            V("Ivan Runner", "wf:rugs-runners/extra-long-persian-runner")],
                  old=["charity-vintage-rug", "cornhill-vintage-rug", "large-brown-persian-rug", "large-vintage-red-rug",
                       "large-red-azerbaijan-rug", "pretty-cream-floral-rug", "pretty-sage-vintage-rug", "red-aztec-rug",
                       "round-rattan-rug", "vintage-cream-and-pink-rug", "vintage-orange-rug", "ethnic-runner",
                       "extra-long-persian-runner"]),
         ],
         removed=[]),
]

# The old Webflow folders each section's old product pages lived in (all of them redirect, see netlify.toml)
OLD_FOLDERS = {
    "table-decor": ["/table-decor-collection"],
    "signage": ["/signage"],
    "small-props": ["/small-props-collection"],
    "seating-areas": ["/furniture-rugs", "/furniture-collection", "/rugs-runners-collection"],
}
# Old list pages that now redirect to a section
OLD_LIST_PAGES = {"/furniture-rugs": "/seating-areas", "/furniture": "/seating-areas", "/rugs-runners": "/seating-areas",
                  "/furniture-collection": "/seating-areas", "/rugs-runners-collection": "/seating-areas",
                  "/table-decor-collection": "/table-decor", "/small-props-collection": "/small-props"}


# The most of each product that can be added to the wish list (each colour or style counts separately). Keys are
# "section/product"; anything not listed can go up to 99.
MAX_QTY = {
    "table-decor/coloured-napkins": 200, "table-decor/charger-plates": 200, "table-decor/gold-cutlery": 200,
    "table-decor/candlesticks": 200, "table-decor/bud-vases": 200, "table-decor/tea-light-holders": 200,
    "table-decor/chair-drapes": 200,
    "signage/table-plans": 10, "signage/welcome-signs": 10, "signage/order-of-the-day": 10, "signage/menus": 200,
    "signage/name-cards": 200, "signage/neon-signs": 5,
    "small-props/cake-stands": 10, "small-props/card-boxes": 5, "small-props/lanterns": 20, "small-props/other-props": 10,
    "seating-areas/chairs": 3, "seating-areas/tables": 1, "seating-areas/rugs-and-runners": 1,
}
