# Printers Size Lab

See how different printers would sit on a shelf or cabinet, shown in 3D. You can resize the shelf,
raise or lower it, or turn it into a cabinet. For each printer the page shows how far it sticks out
past the front edge, how much space its plugged-in cables need behind it, where its top sits compared with your eye level, and its full
specs, box contents and prices.

**Live site:** https://nadavm-eng.github.io/printers-size-lab/

## Features

- **Eight printers:** the current HP OfficeJet J4580 plus seven candidates (Brother DCP-L2620DW,
  HL-L2445DW, HL-L2400DW, Pantum BP2300NW, HP LaserJet M110w, Xerox B230, Xerox B110).
- **On the shelf:** the printer stands on a shelf against a plain wall, as close to the wall as its power
  and data plugs allow.
- **States:** closed, printing (trays and paper stops out), adding paper, and lid open for the
  printers with a scanner.
- **Measurements:** overhang past the shelf edge, cable space behind, width, depth, height, height of
  the top above the floor, whether the printer's middle still sits on the shelf, and whether the
  wardrobe door clears it.
- **Adjustable shelf or cabinet:** drag it in the 3D view, or use the sliders under it. Drag the shelf up
  or down for its height (10 to 200 cm), its front-edge handle for its depth (15 to 80 cm) and its left-end
  handle for its length (30 to 150 cm). Shelf mode is a board on wall brackets; Cabinet mode is a cabinet
  standing on the floor. Values snap to whole centimetres and click onto the defaults (a 129 cm high,
  24.5 cm deep, 68.5 cm long shelf); Reset goes back to them.
- **A person** (height slider) standing beside the shelf, with an eye-level line, and a **wardrobe**
  beside it whose door swing is checked against the printer; both can be hidden.
- The printer's position on the shelf (left, centre, right).
- **Compare two printers on the shelf:** A on the shelf, B as an outline in the same spot.
- **Camera presets:** front, side, top, 3/4 and far (keys 1 to 5).
- **Side by side view:** the two printers alone, next to each other, each with its sizes. **Ghost** puts
  one inside the other and makes one of them see-through.

## Project layout

```
docs/                  the website (GitHub Pages serves this folder)
  index.html           single page (three.js from jsDelivr, no build step)
  printers.json        all printer data, assembled by build/assemble.py
  data/*.geom.json     per-model geometry: parts, states, envelopes, cable space
  data/scene.json      default shelf size and the wardrobe beside it (the scene itself is made in index.html)
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
