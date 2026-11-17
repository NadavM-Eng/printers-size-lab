# How a printer model is made here

This is the brief the builders of this project's printer models follow: from reference photos to a
finished, photo-checked 3D model. Anyone, person or AI assistant, can follow it to add a printer.

The site puts each printer on a shelf in 3D and shows how far it sticks out, how much space its cables
need behind it, and its states (printing, adding paper, lid open). So the model has to be right where
that matters.

**What matters most, in order:** the BACK (power inlet, ports, anything that sticks out), the FRONT, the
TOP. The left and right sides and the bottom usually have nothing special: use a photo if one exists,
otherwise keep them plain.

**Good and done beats perfect**, but "done" means checked against photos, not against a description.

## Where things are

Run every command from the repository root, with a Python environment that has Blender's `bpy` module
(`python -m pip install bpy numpy pillow`; there is no Blender program to open).

| What | Path |
|---|---|
| Research (sizes, box, prices, cable space) | `printers/<printer>/specs.json` |
| Reference photos (never committed) | `printers/<printer>/photos/<name>.png` + `index.json` |
| New downloads, before they are sorted | `printers/<printer>/photos/_incoming/` |
| Measurements and model status | `printers/<printer>/measurements/MEASUREMENTS.md` |
| The builder | `build/builders/<id_with_underscores>.py` |
| Build output | `docs/models/<id>.glb`, `docs/data/<id>.geom.json` |
| Renders / comparison sheets | `work/renders/<id>/`, `work/compare/<id>/` |

`<printer>` is the printer's folder name: the names of the built-in printers are listed in
`build/paths.py`; a new printer uses its id.

## Step 1. Photos

1. Run `python build/photos.py contact <id>` and open `photos/_contact.png`. Read `photos/index.json`
   for what each photo shows and which model it is.
2. Decide what is missing: a sharp, real photo of the exact model for the **back**, the **front** and the
   **top**. Side and bottom are optional. Photos of each open state help a lot.
3. Look for what is missing: the maker's product and support pages, the user manual's dimension and parts
   drawings, shop galleries, reviews, and used-unit listings (these often show the back and the bottom).
   Search only for the printer's model names. Save candidates into `photos/_incoming/`.
   - Images only; never download or run programs, archives or scripts.
   - If a site refuses automated access, shows a robot check, or needs a login, leave it and use
     another source. Don't work around it.
   - Reference photos belong to their owners. They are used only to measure and compare, and they stay
     out of the repository (`printers/*/photos/` is git-ignored).
4. LOOK at every candidate. Keep one only if it shows the exact model (a readable model name, or a page
   about that exact model) and is sharp enough to measure. File each keeper with its source:
   `python build/photos.py add <id> <file> --name NN_<view> --view <view> --url <image url> --page <page url> --source <kind> --evidence "<why this is the exact model>" --no-trim`
   Then delete `_incoming/`.

## Step 2. Measure, then model

**Measure before modelling**, in `MEASUREMENTS.md`:

- A photo index: file, view, what it shows, source. Double-check it against the photos.
- Scale each straight view from an official dimension (pixels per cm). Studio photos often look 10-15 %
  deeper than the official size: take proportions from the photo and scale them to the official size.
- Side profile: the top surface's height every ~2 cm of depth, slopes and curves. Front: widths at
  several heights, cassette, seams, control panel, display, buttons, logo. Back: the exact position of
  the power inlet and every port (cm from the left edge seen from behind, cm above the bottom) and how
  deep each is recessed (0 = flat back). Bottom: feet.
- Moving parts: hinge positions, opening angles, travel, extended sizes.
- Colours as sRGB hex per part, and finish.

**Build** `build/builders/<id_with_underscores>.py`: `class Builder(Printer)` with `build()` and
`states()`. See the docstrings in `build/printer_kit.py`, `build/builders/example.py`, and a finished
builder such as `build/builders/hp_laserjet_m110w.py`.

    python build/build_printer.py <id> --render front,back,top,34fl
    python build/build_printer.py <id> --render 34fl --state printing
    python build/build_printer.py <id> --render back --cables
    python build/build_printer.py <id> --view p07:-35:18:60     # name:azimuth:elevation:lens
    (add --no-export for renders only; a render takes a few seconds)

**Compare.** Put each photo next to a render from the same angle:

    python -c "import sys; sys.path.insert(0,'build'); import printer_kit as K; K.compare_sheet([(photo, render, label), ...], 'work/compare/<id>/roundN.png')"

Look at the sheet, list the differences, fix the biggest first (silhouette, top slope, panel, seams,
port positions, colour), and repeat. Three to five rounds. Stop when nothing big is wrong.

**Two checks a render can't do for you.**

- *Same-plane overlaps.* Two surfaces of different materials lying in the same plane flicker on the site
  when the camera turns, and a still render looks fine. Every build lists them ("same-plane overlaps");
  `python build/check_model.py docs/models/<id>.glb` does the same for a finished file. For each one
  that can be seen from outside, move one surface 0.05 cm in or out, or cut the surface under it.
- *Colours.* Take each part's colour from the maker's studio photos, not by eye:
  `python build/check_model.py --colour <photo> x0,y0,x1,y1` prints the median colour of that region
  (fractions of the image, top left first), and `photo_color(path, box)` does it inside a builder. Run
  it on the same spot of your render and bring the two close.

Rules the site depends on:

- Frame: cm, Z up, FRONT is -Y, BACK is +Y, x = 0 at the centre of the width, y = 0 at the centre of the
  closed body's depth, z = 0 under the feet. Azimuth 0 = front, -90 = left, +90 = right, 180 = back.
- The closed body matches the official W x D x H in `specs.json` within 0.5 cm.
- Part names: `body` for everything static; each moving part separately with its pivot at the hinge:
  `cassette`, `flap` or `support`, `lid`, `adf_tray`, `input_tray`, `front_cover`, `rear_cover`.
- States, only those that apply: `printing` (whatever must be open or extended to print), `refill`
  (loading paper), `lid_open` (scanner lid, printers with a scanner only).
- Cables: `self.plug_cable(part, kind, x, z, back_y, recess=...)`. Always `cable_power`, plus `cable_eth`
  if the printer has Ethernet, otherwise `cable_usb`, at the socket positions seen in the back photo.
  The rule of thumb for the space behind: a socket recessed inside the body needs only 1-2 cm for the
  squashed cable; a plug on a flat back adds its own length, 5-8 cm. Check the build's "cables reach"
  line against it and set `cable_space.behind_body_cm` in `specs.json` to the same number.
- Limits: 150k triangles and 6 MB per GLB. Logos: `text3d(...)` with `find_font("DejaVuSans-Bold")`.
- Model only what the photos show. Where there is no photo, keep the surface plain and say so.

Finish with one build **without** `--no-export`, so the GLB and geom.json match the builder.

## Step 3. Close out

- Add or update a "Model status" section at the end of `MEASUREMENTS.md`: photos used, rounds done,
  what still differs from the photos, and what was modelled without a photo.
- To hand the printer to someone else as one file, pack it:
  `python build/export_printer_file.py <id>` writes `<id>.printer.json`, which can be dropped onto the
  site (see `docs/ai-instructions.md`).
