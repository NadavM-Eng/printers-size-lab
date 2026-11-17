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

## Project layout

```
docs/                  the website (GitHub Pages serves this folder)
  index.html           single page (three.js from jsDelivr, no build step)
  printers.json        all printer data, assembled by build/assemble.py
  data/*.geom.json     per-model geometry: parts, states, envelopes, cable space
  data/room.json       shelf and wardrobe dimensions
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
