# Printers Size Lab

See how different printers would sit on one real shelf, shown in 3D. For each
printer the page shows how far it sticks out past the shelf's front edge, how much space its
plugged-in cables need behind it, where its top sits compared with your eye level, and its full
specs, box contents and prices.

**Live site:** https://nadavm-eng.github.io/printers-size-lab/

## Features

- **Eight printers:** the current HP OfficeJet J4580 plus seven candidates (Brother DCP-L2620DW,
  HL-L2445DW, HL-L2400DW, Pantum BP2300NW, HP LaserJet M110w, Xerox B230, Xerox B110).
- **On the shelf** (129 cm high), standing as close to the wall as its power and data plugs allow.
- **States:** closed, printing (trays and paper stops out), adding paper, and lid open for the
  printers with a scanner.
- **Measurements:** overhang past the shelf edge, cable space behind, width, depth, height, height of
  the top above the floor, whether the printer's middle still sits on the shelf, and whether the
  wardrobe door clears it.
- **A person** (height slider) standing beside the shelf, with an eye-level line.
- **What-if shelf height** slider, and the printer's position on the shelf (left, centre, right).
- **Compare two printers in the room:** A on the shelf, B as an outline in the same spot.
- **Side by side view:** the two printers alone, next to each other, each with its sizes. **Ghost** puts
  one inside the other and makes one of them see-through.

- **Add your own printer:** "Add your printer" (top right) gives instructions to paste into any AI
  assistant with web search; it writes one `<id>.printer.json` file that you drop on the page. See below.

## Project layout

```
docs/                  the website (GitHub Pages serves this folder)
  index.html           single page (three.js from jsDelivr, no build step)
  printers.json        all printer data, assembled by build/assemble.py
  data/*.geom.json     per-model geometry: parts, states, envelopes, cable space
  data/room.json       shelf and wardrobe dimensions
  ai-instructions.md   the instructions a visitor gives their AI to write a printer file
  examples/            hand-written printer files (minimal, full, and the one in the instructions)
  models/*.glb         3D models of the printers
build/
  printer_kit.py       Blender (bpy) toolkit shared by all printer builders
  build_printer.py     builds one printer: GLB + geometry JSON, optional photo-matched renders
  builders/<id>.py     one builder per printer
  assemble.py          merges research and geometry into docs/printers.json
  photos.py            reference-photo index used while modelling
  paths.py             where each printer's research folder is
  fonts/               DejaVu fonts used for the logos on the models
printers/<name>/       per printer: specs.json (research), SOURCES.md (photo sources),
                       measurements/MEASUREMENTS.md (measured from the photos, and the model's status)
```

## Add your own printer (printer files)

Visitors can put any printer on the shelf. The panel behind **Add your printer** has the text of
[`docs/ai-instructions.md`](docs/ai-instructions.md) (Copy / Download). The visitor pastes it into
ChatGPT, Gemini, Claude or similar, names the printer and their country, and gets back one JSON file,
`<id>.printer.json`, which they drop anywhere on the page (or pick, or paste). Nothing is uploaded: the
file is kept in that browser's `localStorage` (key `psl-mine-v1`) and listed under "Your printers"
in both pickers, each with Remove.

The file (`"format": "printers-size-lab/printer@1"`) holds:

- specs: `name`, `brand`, `type`, `functions`, `dims_mm.closed` (official size in mm, required),
  `dims_mm.max`, `weight_kg`, `specs` (rows with the same labels as the built-in printers), one `price`
  in any ISO currency, `running_cost.cartridges` (cost per page is worked out from them),
  `software`, `notes`, and a source URL for every number;
- `cable_space.sockets`: kind (C13, C7, C5, DC, USB-B, RJ45, RJ11), position and recess of each plug
  on the back; the page draws the plugs and bent cables and measures the space they need;
- `model`: a recipe in centimetres, in the same frame as the GLBs (x across with +x to the right
  seen from the front, y up from the shelf, +z toward the front, origin at the bottom centre): parts
  (`body` plus moving parts with a `pivot`), each made of `box` (x/y/z from–to ranges, optional
  rounded edges), `profile` (a side outline of [z, y] points pushed across a width), `cylinder` and
  `inset` (a flat dark rectangle on a face), with colour, roughness and glow; and `states`
  (`printing`, `refill`, `lid_open`) as lists of `rotate` / `move` / `show` / `hide`.

The page checks the file (format, required fields, number ranges, at most 400 shapes and 500 KB,
only http(s) links, text shown as text), builds the three.js model and a geom object like
`docs/data/*.geom.json` (state envelopes, cable space, body size), and warns when the closed shape
differs from the official size by more than 0.5 cm. A file without `model` shows a plain box at the
official size. Errors are listed in words the visitor can paste back to their AI.

## Run the site locally

```bash
cd docs
python3 -m http.server 8000
# open http://localhost:8000
```

## Rebuild

```bash
pip install bpy==5.2.3 pillow numpy       # Blender as a Python module (needs Python 3.13)
python3 build/build_printer.py <id> --render front,34fl
python3 build/assemble.py
```

Model conventions: glTF Y-up in metres, origin at the bottom centre of the closed body, front +Z,
width along X. Nodes are named `<id>_<part>`; moving parts (paper cassette, paper stops, scanner lid)
have their pivot at the hinge, and `docs/data/<id>.geom.json` lists the poses for each state.

## How the models are made

Each printer is modelled from real photos of that exact model (manufacturer images, reviews and
marketplace listings), measured first and written to `printers/<name>/measurements/MEASUREMENTS.md`, then compared
with the photos side by side over several rounds. The photos themselves are not included because
they belong to their owners; each printer's `SOURCES.md` links to them.

## Notes

Brand names and logos belong to their owners and appear only to identify the products. This project
is not affiliated with any manufacturer or shop. Specs, box contents and prices come from the linked
pages and may have changed.

## License

Code: [MIT](LICENSE).
