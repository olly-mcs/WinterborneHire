// Quote builder price list, from the Winterborne "Styling Catalogue & Pricing Guide 2027/28".
// price: the catalogue price in pounds. For "From £X" items that's X; for "£8-£12" it's the midpoint.
// The estimate shows 20% below to 20% above the total of these prices (see QUOTE_RANGE in quote-builder.js).
// unit: how the price is counted, shown next to the price ("each", "per ladder", "set of 3"...).
// from: true when the catalogue says "from", so the item is shown as "from £X".
window.QUOTE_CATALOGUE = [
  {
    id: "statement",
    title: "The statement",
    intro: "One big floral feature: pillars, urns and archways, custom designed to your colour and theme.",
    items: [
      { id: "xl-pillars", name: "XL floral pillars", note: "H 2.1m", price: 545 },
      { id: "full-floral-arch", name: "Full floral arch", note: "Pillars H 2.1m and 1.8m", price: 595 },
      { id: "moongate", name: "Moongate", note: "H 2m", price: 495 },
      { id: "metal-moongate", name: "Metal moongate", note: "H 2m", price: 250, from: true },
      { id: "moongate-draping", name: "Draping for metal moongate", price: 20 },
      { id: "pagoda-garlands", name: "Pagoda garlands", price: 225, from: true },
      { id: "urns-plinths", name: "Large urns & plinths", price: 450 },
      { id: "churn-arrangements", name: "Churn arrangements", price: 400 },
      { id: "xl-foliage-arch", name: "XL foliage arch", note: "H 2.4m", price: 295 },
      { id: "aisle-meadows", name: "Aisle meadows", price: 50, unit: "each" },
    ],
  },
  {
    id: "installations",
    title: "Custom installations",
    intro: "Made-to-measure pieces, installation included.",
    items: [
      { id: "ladder-decor", name: "Ladder decor", note: "Foliage or custom, 3m / 4.5m", price: 150, unit: "per ladder", from: true },
      { id: "chandelier-decor", name: "Chandelier decor", note: "Foliage or custom, 3ft / 4ft", price: 360, from: true },
      { id: "arbor-design", name: "Custom arbor design", note: "Made to measure for any arbor", price: 495, from: true },
      { id: "mantle-installation", name: "Mantle installation", note: "Priced on size", price: 120, from: true },
    ],
  },
  {
    id: "reception",
    title: "The reception",
    intro: "Centrepieces and the top table.",
    items: [
      { id: "tall-podiums", name: "Tall podium arrangements", note: "Gold, black or clear stands, H 70cm", price: 145, unit: "each" },
      { id: "footed-bowl", name: "Footed bowl arrangements", note: "Gold or white bowls", price: 55, unit: "each" },
      { id: "large-bowl", name: "Large bowl arrangements", price: 65, unit: "each" },
      { id: "table-wreath", name: "Table wreaths", price: 45, unit: "each", from: true },
      { id: "budvases", name: "Budvases & stems", note: "Clear, pink, green, orange or teal vases (£8-£12)", price: 10, unit: "each" },
      { id: "top-table", name: "Top table centrepiece", price: 145, from: true },
      { id: "table-trees", name: "Luxury table trees", note: "H 80cm stand + arrangement", price: 135, unit: "each" },
    ],
  },
  {
    id: "personal",
    title: "Personal florals",
    intro: "For you and your wedding party.",
    items: [
      { id: "bridal-bouquet", name: "Bespoke bridal bouquet", price: 125, unit: "each", from: true },
      { id: "bridesmaid-bouquet", name: "Bespoke bridesmaid bouquets", price: 55, unit: "each", from: true },
      { id: "buttonholes", name: "Bespoke buttonholes", price: 10, unit: "each", from: true },
      { id: "single-stem", name: "Single stem bouquets", price: 30, unit: "each", from: true },
      { id: "fairy-wand", name: "Fairy wands", note: "To keep", price: 15, unit: "each" },
      { id: "cake-florals", name: "Cake florals", note: "To keep", price: 25, from: true },
      { id: "dog-collar", name: "Dog collar florals", note: "To keep", price: 25, unit: "each" },
      { id: "hair-combs", name: "Hair combs", note: "To keep", price: 25, unit: "each" },
    ],
  },
  {
    id: "signage",
    title: "Signage & stationery",
    intro: "Coordinated designs, custom made to your colours.",
    items: [
      { id: "mirror-tableplan", name: "Mirror table plan", note: "Includes wooden easel", price: 195, from: true },
      { id: "arched-mirror", name: "Small arched mirror", note: "Welcome or order of the day", price: 65, from: true },
      { id: "selfie-mirror", name: "Selfie mirror", note: "Free standing", price: 85, from: true },
      { id: "wooden-welcome", name: "Wooden welcome sign", note: "With wooden easel", price: 65, from: true },
      { id: "hanging-sign-large", name: "Hanging sign, large (A1)", note: "Welcome, table plan or order of events", price: 145, from: true },
      { id: "hanging-sign-small", name: "Hanging sign, small (A2)", note: "Welcome, order of events or menu", price: 85, from: true },
      { id: "banner-frame", name: "Banner + frame", note: "80cm x 250cm, black or gold frame", price: 165, from: true },
      { id: "menu-cards", name: "Menu cards", price: 2.25, unit: "each", from: true },
      { id: "place-cards", name: "Place cards", price: 1.45, unit: "each", from: true },
    ],
  },
  {
    id: "finishing",
    title: "The finishing touches",
    intro: "Table details and decor.",
    items: [
      { id: "candlesticks", name: "Candlesticks", price: 3, unit: "each" },
      { id: "cylinder-vases", name: "Cylinder vases", note: "Set of 3, LED pillar or floating candle", price: 10, unit: "set" },
      { id: "taper-hurricane", name: "Taper candle hurricanes", note: "Sleeve + candlestick", price: 5, unit: "each" },
      { id: "card-box", name: "Card box", note: "Gold or wicker", price: 10 },
      { id: "charger-plates", name: "Charger plates", note: "Gold beaded, gold or seagrass", price: 1.5, unit: "each", from: true },
      { id: "napkins", name: "Coloured napkins", note: "Sage, latte, pink, burnt orange, dark green or blue", price: 1.75, unit: "each" },
      { id: "cutlery", name: "Matte gold cutlery", note: "6-piece setting", price: 3.6, unit: "setting" },
      { id: "tealights", name: "Tealight holders", note: "Clear, reeded, coloured or twine", price: 1.5, unit: "each" },
      { id: "chair-drapes", name: "Chair drapes / runners", note: "Various colours", price: 3, unit: "each" },
    ],
  },
  {
    id: "services",
    title: "Styling services",
    intro: "Let us set everything up on the day.",
    items: [
      { id: "full-styling", name: "Full wedding styling & set-up", note: "Two-person team, ceremony & reception set-up, next-day pack-down", price: 695, from: true, max: 1 },
      { id: "outdoor-ceremony", name: "Outdoor ceremony set-up", note: "Two-person set-up of chairs, aisle and ceremony area", price: 195, from: true, max: 1 },
    ],
  },
];
