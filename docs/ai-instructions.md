# Instructions for your AI: make a printer file for Printers Size Lab

You are helping someone add a printer to **Printers Size Lab** (https://nadavm-eng.github.io/printers-size-lab/),
a web page that shows printers as 3D models on a shelf and compares their size, how far they stick out,
the cable space they need behind them, prices and running costs. The page builds the 3D model itself
from a simple recipe of boxes and shapes that you write.

**Your output is exactly one JSON file**, named `<id>.printer.json`. If you can create files, create it
and give it to the user. If you can't, output the JSON in one code block and nothing else inside it, and
tell the user to save it as `<id>.printer.json`. The user then drops the file onto the page. Everything
below tells you what to research and how to write the file.

## 0. Before you start

You need two things from the user: **the exact printer model** and **the country where they would buy
it**. If either is missing, ask for it first and wait for the answer. Use the buyer's country for the
price, the currency and the cartridge prices.

## 1. Research (use web search; open the pages)

Find, for the exact model and its regional variant (for example "i-SENSYS" in Europe vs "imageCLASS" in
the US, a "w" or "dw" suffix):

1. **Official closed dimensions** (width × depth × height, in mm) from the manufacturer's spec sheet or
   manual, and **what the depth includes** (paper tray lip, rear bump, panel). Closed means every tray
   and cover shut, as it stands when not in use.
2. **Maximum dimensions in use** (trays open, paper stops out, lid up), if published.
3. **Weight** in kg (and whether it includes consumables).
4. Key specs: print speed, two-sided printing, connections, paper input and output capacity, manual
   feed, scanner, display, cartridges or toner (codes and page yields), drum, **what is in the box**.
5. **One current price in the buyer's country, in its currency**, with the shop name, a link and today's
   date. Prefer a big, reputable shop or a price-comparison site.
6. **Running cost:** for each cartridge (toner, ink, drum): code, page yield (ISO), and a price in the
   buyer's country with a link. Say whether it is original or compatible.
7. **The back panel:** where the power inlet and the data port (USB-B, Ethernet) are on the back
   (left or right, how high), the kind of plug, and whether each socket is **flat with the back** or
   **sunk into a recess** (and how deep). Look at photos of the back and at the manual's "parts" page.
8. **Photos from the front, the side and the back**, and of the printer with its trays open, so you can
   build its shape.
9. Optional: how well it works on Windows (drivers, software problems) and what owners say.

Good places: the manufacturer's spec page, its user manual or "getting started" PDF (drawings of the
parts, the back panel and how to load paper), big shops' photo galleries, and review sites with photos
of the back and of the trays open. If the exact variant has no listing in the buyer's country, you may
give the price of the closest sibling (same body, e.g. without Wi-Fi) and say so in `price.note`.

**Two kinds of numbers, two rules:**

- **Researched facts** (dimensions, weight, specs, prices, page yields): every one needs a source URL.
  **Never invent or guess them.** If you can't find one, leave the field out and say so in `notes`.
- **The shape** (profile, moving parts, pivots, socket positions): this is your **best estimate from
  photos and from how this kind of printer works**. Always build it, even when no photo shows every
  detail, and say in `notes` what is estimated. A plain box is not acceptable when photos exist. Every
  printer has at least a place where paper goes in (front tray, cassette, rear feeder) and where it
  comes out (output tray with a flap or paper stop): model both as moving parts. Give the power and
  data sockets from any photo of the back; leave `cable_space` out only if you found no picture of the
  back at all (the page then assumes 8 cm).
- **If you cannot see images**, read the manual's text instead: its "product parts" / "parts names"
  pages and its "loading paper" section say where each part is (for example "rear paper feed",
  "ink tanks on the right side", "output tray pulls out of the front", "USB port on the back, left").
  Don't guess a layout from other printers when the manual says otherwise.

## 2. The coordinate frame (read this carefully)

All model numbers are in **centimetres**. Stand in front of the printer, looking at its front panel:

- **x = across the width.** x = 0 is the middle of the width. **+x is to your right**, −x to your left.
  The printer spans x from −w/2 to +w/2.
- **y = height.** y = 0 is the shelf the printer stands on (the bottom of its feet). +y is up.
  The printer spans y from 0 to h.
- **z = depth.** z = 0 is the middle of the depth. **+z is the front (toward you)**, −z is the back
  (toward the wall). The printer spans z from −d/2 (back) to +d/2 (front).

Example: a printer 36 × 25 × 20 cm (w × d × h). Its body box spans x −18…18, y 0…20, z −12.5…12.5.
A control panel on the front top edge sits at z = +12.5 (the front face), y near 20. The power socket
on the back is at z = −12.5. A socket that you see on the **left** in a photo **of the back** is on the
printer's right, so it has **+x**.

## 3. The file, field by field

Fields marked *optional* may be left out. Text fields are plain text (no HTML, no Markdown).
Every `source` / `url` is a full `https://` link.

| Field | What to put |
|---|---|
| `format` | Always `"printers-size-lab/printer@1"`. |
| `id` | Lowercase letters, digits and dashes, e.g. `"canon-lbp6030w"`. The file name is `<id>.printer.json`. |
| `name`, `brand` | Full model name with the brand, as sold in the buyer's country (e.g. `"Canon i-SENSYS LBP6030w"`), and the brand. |
| `type` | Short, e.g. `"Mono laser printer"`, `"Colour inkjet all-in-one"`. |
| `functions` | *optional* List from `"print"`, `"scan"`, `"copy"`, `"fax"`. |
| `buyer_country` | The user's country, e.g. `"Israel"`. |
| `dims_mm.closed` | `{"w", "d", "h", "source", "includes"}`: official closed size in **mm**; `includes` = what the depth covers. Required. |
| `dims_mm.max` | *optional* `{"w", "d", "h", "what", "source"}`: largest size in use, mm; `what` says what is open. |
| `weight_kg` | *optional* `{"value", "what", "source"}`. |
| `specs` | *optional* List of `{"label", "value", "source", "note"}`. Use these labels where they fit: `Print speed`, `Two-sided printing`, `Connections`, `Paper in`, `Paper out`, `Manual feed`, `Scanner`, `Display`, `Toner`, `Ink`, `Drum`, `In the box`. `value` is text, or a list of texts for `In the box`. Other labels are allowed. |
| `price` | *optional* `{"value", "currency", "where", "url", "date", "note"}`: one price in the buyer's country. `currency` is the 3-letter ISO code (`"ILS"`, `"EUR"`, `"USD"`…), `date` is `YYYY-MM-DD`. |
| `running_cost.cartridges` | *optional* List of `{"code", "kind", "pages", "price", "currency", "original", "where", "url"}`. `kind` is `"toner"`, `"ink"` or `"drum"`; `pages` is the ISO yield; `original` is `true` for the brand's own cartridge. Leave out starter cartridges that come in the box. For colour inkjets list the black cartridge first. |
| `running_cost.compatible` | *optional* `{"allowed", "note", "source"}`: can third-party cartridges be used? `allowed` is `"yes"`, `"nags"`, `"blocked"` or `"unknown"`. |
| `software.windows`, `software.owners` | *optional* `{"rating", "why", "source"}`, `rating` is `"good"`, `"mixed"`, `"poor"` or `"unknown"`. |
| `cable_space.sockets` | *optional* List of the plugs on the back, see below. |
| `cable_space.why` | *optional* One or two sentences on what sets the space needed behind the printer. |
| `notes` | What a buyer should know about its size and shape, which parts of the shape are estimated, and **what you could not find**. At most 6 short sentences, impersonal (no "I"). |
| `model` | The 3D recipe, see section 4. |

**Sockets.** Each one is `{"kind", "x_cm", "height_cm", "recess_cm", "back_z_cm"}`:
`kind` is `"C13"` (kettle-style 3-pin power), `"C7"` (2-pin "figure 8"), `"C5"` (3-pin cloverleaf),
`"DC"` (round plug from an external power brick), `"USB-B"`, `"RJ45"` (Ethernet) or `"RJ11"` (phone);
`x_cm` is the socket's x (remember: left in a photo of the back = +x); `height_cm` its height above the
shelf; `recess_cm` how deep the socket sits inside the outline (0 = flat back; 2–4 for a socket in a
pocket); `back_z_cm` *optional*, the z of the back surface where the socket is, only when that part of
the back is in front of the rear-most point (for example a socket under a rear overhang). The page draws
the plugs and cables from these and works out the space behind; a plug on a flat back needs 5–8 cm, a
recessed one only 1–2 cm. Only list power and data sockets that are used (not a fax line nobody plugs in).

## 4. The 3D recipe (`model`)

```
"model": {
  "units": "cm",
  "parts": [ {"name": "body", "shapes": [ ... ]}, {"name": "lid", "pivot": {...}, "shapes": [ ... ]} ],
  "states": { "printing": [ ... ], "refill": [ ... ], "lid_open": [ ... ] }
}
```

**Parts.** The first part is `"body"`: everything that never moves. Every part that moves (paper tray,
cassette, output flap or paper stop, scanner lid, front door that opens to load paper) is its own part
with a `name` (lowercase, e.g. `"input_tray"`), a **`pivot`** `{"x", "y", "z"}` on its hinge line (for a
part that only slides, use any point on it, e.g. its front-bottom middle) and its shapes. Add
`"hidden": true` to a part that only appears in some states (a stack of paper in an open tray).
**Write every shape where it is when the printer is closed**, in the frame of section 2, never relative
to the pivot.

**Shapes.** Each shape gives a from–to range on axes. Common keys: `"color"` (`"#rrggbb"`), `"roughness"`
(0 shiny … 1 matte, default 0.55), `"glow"` (`"#rrggbb"`, only for a lit display or LED).

- **Box:** `{"type": "box", "x": [x1, x2], "y": [y1, y2], "z": [z1, z2], "radius": 0.8}`. `radius`
  *optional* rounds the edges (cm).
- **Profile** (side outline pushed across the width, for sloped tops, curved fronts, wedges):
  `{"type": "profile", "x": [x1, x2], "zy": [[z, y], [z, y], ...]}`. `zy` lists the corners of the side
  outline as **[z, y] pairs (depth first, then height)**, going around the outline once, as seen from
  the printer's right side. 3 to 64 points.
- **Cylinder:** `{"type": "cylinder", "axis": "x", "x": [x1, x2], "y": 3, "z": 10, "radius": 1}`. Along
  `axis` give a range; on the other two axes give the centre as a single number.
- **Inset** (a flat dark rectangle drawn on a surface: output slot, recess, display, button panel):
  `{"type": "inset", "face": "front", "x": [x1, x2], "y": [y1, y2], "z": 12.5, "color": "#111111"}`.
  `face` is `"front"`, `"back"`, `"top"`, `"left"` or `"right"`; the axis that faces that way gets a
  single number (the surface position) and the other two get ranges. Insets do not change the size.

**How to build it, in this order:**

1. Start from the official box: `x` −w/2…w/2, `y` 0…h, `z` −d/2…d/2 (w, d, h from `dims_mm.closed`
   in cm). Everything you add must stay inside this box when closed, unless the official depth leaves
   something out (then say so in `notes`).
2. Replace the box with the real side outline: look at a side photo and write a `profile` of the body
   (sloped top, stepped front, rear bump). Split it into a few boxes/profiles if the width changes.
3. Add what changes the silhouette or what a viewer recognises: the control panel, the output slot
   (inset), the paper tray front, the scanner lid on an all-in-one, feet, a display (inset with `glow`).
4. Make the moving parts separate parts with pivots, then define the states. If `dims_mm.max` is
   published, size the moving parts so the open states reach it (e.g. a published printing depth of
   57.8 cm on a 34.7 cm deep printer means trays stick out about 23 cm in total).
5. Colours: the real colours of the casing (most printers are off-white `#e8e8e6`, light grey or black
   `#202122`), darker for trays and slots.

Silhouette and depth matter most; small details don't. No logos, text or buttons smaller than 1 cm.
Use 10 to 80 shapes. Limits: 400 shapes, 24 parts, file under 500 KB.

**States** (lists of operations on parts; define only the states that apply, leave the others out):

- `"printing"`: what is out while printing: paper stops and output flaps flipped out, an input tray
  opened with paper in it.
- `"refill"`: loading paper: the cassette pulled out, or the input tray opened.
- `"lid_open"`: only for a scanner: the lid raised (about 70–80°).

Operations: `{"part": "lid", "rotate": {"axis": "x", "deg": -75}}` turns the part about its pivot;
`{"part": "cassette", "move": {"z": 25}}` slides it (cm); `{"part": "paper", "show": true}` /
`{"part": "paper", "hide": true}`.
Rotation directions about `x` (seen from the printer's right side):

| Motion | Rotation |
|---|---|
| Lid hinged at the back, lifting up | `"axis": "x", "deg": -75` |
| Front cover or tray hinged at its **bottom** edge, falling open toward you | `"axis": "x", "deg": 90` |
| Flap lying flat on top, hinged at its **front** edge, flipping up and over toward the front | `"axis": "x", "deg"` between 70 and 160 |
| Flap lying flat on top, hinged at its **back** edge, lifting up | `"axis": "x", "deg": -70` |
| Rear input tray standing up, hinged at its bottom, leaning back | `"axis": "x", "deg": -20` |

Positive degrees about x tip the part's top toward the front; negative tip it toward the back.

## 5. A complete example (a made-up printer)

```json
{
  "format": "printers-size-lab/printer@1",
  "id": "acme-inkbox-3100",
  "name": "Acme InkBox 3100",
  "brand": "Acme",
  "type": "Colour inkjet all-in-one",
  "functions": ["print", "scan", "copy"],
  "buyer_country": "Israel",
  "dims_mm": {
    "closed": {"w": 390, "d": 300, "h": 165, "includes": "paper cassette front; output tray pushed in", "source": "https://www.example.com/inkbox-3100/specs"},
    "max": {"w": 390, "d": 520, "h": 400, "what": "cassette pulled out; lid raised", "source": "https://www.example.com/inkbox-3100/manual"}
  },
  "weight_kg": {"value": 5.1, "what": "without ink", "source": "https://www.example.com/inkbox-3100/specs"},
  "specs": [
    {"label": "Print speed", "value": "10 pages/min black, 5 colour (ISO)", "source": "https://www.example.com/inkbox-3100/specs"},
    {"label": "Two-sided printing", "value": "Manual"},
    {"label": "Connections", "value": "USB, Wi-Fi", "source": "https://www.example.com/inkbox-3100/specs"},
    {"label": "Paper in", "value": "100 sheets, front cassette"},
    {"label": "In the box", "value": ["Printer", "Black and colour ink cartridges", "Power cord"], "source": "https://www.example.com/inkbox-3100/box"}
  ],
  "price": {"value": 449, "currency": "ILS", "where": "Example Shop", "url": "https://shop.example.co.il/inkbox-3100", "date": "2026-11-17"},
  "running_cost": {
    "cartridges": [
      {"code": "AC-31 black", "kind": "ink", "pages": 300, "price": 79, "currency": "ILS", "original": true, "where": "Example Shop", "url": "https://shop.example.co.il/ac31"},
      {"code": "AC-31 colour", "kind": "ink", "pages": 250, "price": 95, "currency": "ILS", "original": true, "where": "Example Shop", "url": "https://shop.example.co.il/ac31c"}
    ],
    "compatible": {"allowed": "unknown", "note": "No report found either way."}
  },
  "cable_space": {
    "sockets": [
      {"kind": "C7", "x_cm": 15, "height_cm": 4, "recess_cm": 0},
      {"kind": "USB-B", "x_cm": -13, "height_cm": 6, "recess_cm": 1.5}
    ],
    "why": "The power plug goes straight into the flat back; the USB socket is in a shallow pocket."
  },
  "notes": "The cassette slides 20 cm out of the front to load paper. The lid needs about 25 cm of free height. No Windows reviews were found.",
  "model": {
    "units": "cm",
    "parts": [
      {"name": "body", "shapes": [
        {"type": "box", "x": [-19.5, 19.5], "y": [0.5, 13], "z": [-15, 13.5], "radius": 1, "color": "#2a2b2d", "roughness": 0.6},
        {"type": "profile", "x": [-19.5, -6], "zy": [[13.5, 9], [15, 10.5], [15, 12.5], [13.5, 13]], "color": "#1c1c1e"},
        {"type": "inset", "face": "front", "x": [-17, -9], "y": [10.8, 12.2], "z": 15, "color": "#0e1a22", "glow": "#3d7fa8"},
        {"type": "inset", "face": "front", "x": [-14, 14], "y": [5.5, 7], "z": 13.5, "color": "#0b0b0c"},
        {"type": "box", "x": [-18, -15], "y": [0, 0.5], "z": [-13, -10], "color": "#111111"},
        {"type": "box", "x": [15, 18], "y": [0, 0.5], "z": [-13, -10], "color": "#111111"},
        {"type": "box", "x": [-18, -15], "y": [0, 0.5], "z": [9, 12], "color": "#111111"},
        {"type": "box", "x": [15, 18], "y": [0, 0.5], "z": [9, 12], "color": "#111111"}
      ]},
      {"name": "lid", "pivot": {"x": 0, "y": 13, "z": -15}, "shapes": [
        {"type": "box", "x": [-19.5, 19.5], "y": [13, 16.5], "z": [-15, 13.5], "radius": 0.8, "color": "#2f3032", "roughness": 0.5}
      ]},
      {"name": "cassette", "pivot": {"x": 0, "y": 0.5, "z": 15}, "shapes": [
        {"type": "box", "x": [-15, 15], "y": [0.5, 5], "z": [-11, 15], "radius": 0.4, "color": "#3a3b3e"}
      ]},
      {"name": "output_tray", "pivot": {"x": 0, "y": 5.2, "z": 13.5}, "shapes": [
        {"type": "box", "x": [-10, 10], "y": [5.2, 5.6], "z": [2, 13.4], "color": "#45464a"}
      ]}
    ],
    "states": {
      "printing": [{"part": "output_tray", "move": {"z": 14}}],
      "refill": [{"part": "cassette", "move": {"z": 20}}],
      "lid_open": [{"part": "lid", "rotate": {"axis": "x", "deg": -75}}]
    }
  }
}
```

The body box ends at z = 13.5, the cassette front at z = 15, so the closed depth is 15 − (−15) = 30 cm;
the lid top is at y = 16.5 = h. The power socket at `x_cm` 15 is on the right as you face the front.

## 6. Checklist before you answer

Go through every line; fix the file until all are true:

- [ ] The output is one valid JSON object (double quotes, no comments, no trailing commas, no `...`).
- [ ] `format` is `"printers-size-lab/printer@1"`, `id` matches the file name.
- [ ] `dims_mm.closed` has `w`, `d`, `h` in **mm** and a `source`.
- [ ] Closed, the model spans x −w/2…w/2, y 0…h and z −d/2…d/2 **within 0.5 cm** (w, d, h in cm).
      Compute the min and max of every shape's ranges (and profile points) to check.
- [ ] The front is +z: trays, panel and output slot have positive z; sockets are at the back (−z).
- [ ] The body follows the real side outline (a `profile` or several shapes), not just one box.
- [ ] There is a moving part for where paper goes in and one for where it comes out, and states
      `printing` and `refill` that move them (plus `lid_open` for a scanner).
- [ ] Every part has a `name`; every part except `body` has a `pivot` on its hinge or slide line.
- [ ] Every state only names parts that exist; a lid opens with a negative angle about x.
- [ ] Every number from research has a `source` or `url`; nothing is invented; gaps are in `notes`.
- [ ] Price and cartridge prices are in the buyer's country, with `currency` and `date`.
- [ ] Tell the user: save the file as `<id>.printer.json` and drop it onto the Printers Size Lab page.
