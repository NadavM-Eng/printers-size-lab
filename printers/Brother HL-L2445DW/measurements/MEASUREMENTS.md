# Brother HL-L2445DW: measurements

Official closed size 356 W x 360 D x 183 H mm (Brother UK store, Brother AU product page and brochure).
Builder: `build/builders/brother_hl_l2445dw.py`, a thin subclass of `brother_hl_l2400dw.py` (the shared body).

**This model's back:** RJ45 (Ethernet) jack in the upper half of the port pocket and the USB-B port below it
(photo 07). Cables modelled: `cable_power` + `cable_eth` (the user's set-up for this model is Ethernet).
Everything else (body, front, top, panel, moving parts, colours) is the same body as the HL-L2400DW.


## Photo index

Photos live in `photos/` (not in the repo). Both ids hold the same set; each row says which model the photo actually shows. Rows marked *diagram* are Brother's own user-guide drawings (one guide covers HL-L2400DW, HL-L2400DWE, HL-L2402D, HL-L2442DW, HL-L2445DW, HL-L2447DW, HL-L2460DN, HL-L2865DW).

| file | view | what it shows / which model | source |
|---|---|---|---|
| 01_diagram_back34.png | back34_diagram | Brother Online User Guide 'Front View and Back View' for HL-L2400DW/HL-L2445DW series (same page covers both); drawing shows the Ethernet (8, wired models only) + USB (9) column, AC inlet (10), back cover (11) | [manufacturer_manual](https://support.brother.com/g/s/id/htmldoc/printer/cv_hll2460dw/uke/html/GUID-C9CDC847-CC46-48D1-8435-8634BBE2194A_1.html) |
| 02_diagram_front34.png | front34_diagram | Brother Online User Guide 'Front View and Back View' (HL-L2400DW/HL-L2445DW series): 1 control panel, 2 output support flap, 3 face-down output tray, 4 paper tray, 5 manual feed slot cover | [manufacturer_manual](https://support.brother.com/g/s/id/htmldoc/printer/cv_hll2460dw/uke/html/GUID-C9CDC847-CC46-48D1-8435-8634BBE2194A_1.html) |
| 03_diagram_front34_slot_open.png | front34_diagram_open | same guide page: 6 front cover, 7 manual feed slot (manual feed cover folded down) | [manufacturer_manual](https://support.brother.com/g/s/id/htmldoc/printer/cv_hll2460dw/uke/html/GUID-C9CDC847-CC46-48D1-8435-8634BBE2194A_1.html) |
| 04_front_hi.png | front_high | front, camera slightly above (~10 deg); paper in output tray; reflection below; Brother UK store page for HL-L2445DW, image file HLL2445DW_main.png; shows HL-L2445DW (body shared with HL-L2400DW) | [manufacturer](https://store.brother.co.uk/catalogs/brotheruk/devices/laser/hl/hll2445dw) |
| 05_34fl.png | 34fl | front-left 3/4 from above; left side vent grille near front; Brother UK store page for HL-L2445DW, image HLL2445DW_left.png; shows HL-L2445DW (shared body with HL-L2400DW) | [manufacturer](https://store.brother.co.uk/catalogs/brotheruk/devices/laser/hl/hll2445dw) |
| 06_34fr.png | 34fr | front-right 3/4 from above; right side vent grille near back; Brother UK store page for HL-L2445DW, image HLL2445DW_right.png; shows HL-L2445DW (shared body with HL-L2400DW) | [manufacturer](https://store.brother.co.uk/catalogs/brotheruk/devices/laser/hl/hll2445dw) |
| 07_back.png | back | straight back view: C14 inlet left (seen from behind), RJ45 over USB-B in a pocket right, back cover centre, rear tray panel with green tab; Brother UK store page for HL-L2445DW, image HLL2445DW_1.png; RJ45 + USB-B column visible = HL-L2445DW (wired model); HL-L2400DW has the same body without the RJ45 | [manufacturer](https://store.brother.co.uk/catalogs/brotheruk/devices/laser/hl/hll2445dw) |
| 08_front_shelf.png | front_lifestyle | real photo on a shelf, colour reference; Brother UK store page for HL-L2445DW, image HLL2445DW_2.png (lifestyle, on a shelf) | [manufacturer](https://store.brother.co.uk/catalogs/brotheruk/devices/laser/hl/hll2445dw) |
| 09_back_l2400dw.png | back | straight back view of HL-L2400DW: same C14 inlet, same pocket with a blank plate where the 2445DW has RJ45; Brother UK store page for HL-L2400DW, image HLL2400DW_01.png; port pocket holds only USB-B, RJ45 opening covered by a blank = HL-L2400DW | [manufacturer](https://store.brother.co.uk/catalogs/brotheruk/devices/laser/hl/hll2400dw) |
| 10_detail_panel.png | detail_panel | control panel close-up: LCD, power, Wi-Fi LED button, Back/OK, -/+, long Go button with green light; Coolblue product page for Brother HL-L2445DW (gallery image 5, official Brother render); same panel on HL-L2400DW (both 1-line LCD + Wi-Fi) | [retailer_official_image](https://www.coolblue.de/produkt/943025/brother-hl-l2445dw.html) |
| 11_diagram_support_flap.png | front34_diagram_flap | printing state: support flap at the front edge of the top output tray flips up/forward; Brother Online User Guide 'Load Paper in the Paper Tray' for HL-L2400DW/HL-L2445DW series: raise the output support flap | [manufacturer_manual](https://support.brother.com/g/s/id/htmldoc/printer/cv_hll2460dw/uke/html/GUID-D1474D8C-EF46-46AB-A8FF-010936F85B0F_1.html) |
| 12_diagram_back34_duplex_tray.png | back34_diagram | 2-sided tray occupies the bottom of the back; AC inlet at the far corner; Brother Online User Guide 'Paper is Jammed in the 2-sided Tray' (HL-L2400DW/HL-L2445DW series): back with the 2-sided tray outline; port column drawn as a recessed vertical pocket | [manufacturer_manual](https://support.brother.com/g/s/id/htmldoc/printer/cv_hll2460dw/uke/html/GUID-B1BDD306-D4CC-4ECE-92A0-10016B97CCB4_1.html) |
| 13_diagram_back_cover_open.png | back34_diagram_open | back cover = face-up output tray; Brother Online User Guide (HL-L2400DW/HL-L2445DW series): open the back cover (hinged at the bottom, folds down) | [manufacturer_manual](https://support.brother.com/g/s/id/htmldoc/printer/cv_hll2460dw/uke/html/GUID-B1BDD306-D4CC-4ECE-92A0-10016B97CCB4_1.html) |
| 14_diagram_tray_out.png | front34_diagram_tray | refill state: cassette slides out of the front; Brother Online User Guide 'Load Paper in the Paper Tray' (HL-L2400DW/HL-L2445DW series): pull the paper tray completely out | [manufacturer_manual](https://support.brother.com/g/s/id/htmldoc/printer/cv_hll2460dw/uke/html/GUID-D1474D8C-EF46-46AB-A8FF-010936F85B0F_1.html) |
| 15_top.png | top | real photo from above (front at the bottom): panel left, output slot centre-back, back-cover tab at the rear edge; paper being taken from the output tray; Brother Australia HL-L2445DW product page gallery; model label 'HL-L2445DW' visible on the top | [manufacturer](https://www.brother.com.au/en/printers/all-printers/hl-l2445dw) |
| 16_detail_panel_photo.png | detail_panel | control panel close-up, top-left corner, front cover seam; Brother Australia HL-L2445DW product page gallery (real photo) | [manufacturer](https://www.brother.com.au/en/printers/all-printers/hl-l2445dw) |
| 17_front_cover_open.png | front34_open | front cover hinged at the bottom, folded down; toner+drum unit inserted; Brother Australia HL-L2445DW product page gallery (real photo); model label on top | [manufacturer](https://www.brother.com.au/en/printers/all-printers/hl-l2445dw) |

## How the numbers were taken

Model frame (cm): x = 0 at the centre of the width (+x = the printer's right seen from the front), y = 0 at the
centre of the official depth (front = -y, back = +y), z = 0 under the feet. "Seen from behind, from the left" means
the printer's right side (+x): **x_model = 17.8 - (cm from the left edge seen from behind)**.

| photo | scale | how |
|---|---|---|
| 07_back / 09_back_l2400dw (768 px) | 17.7 px/cm across, 17.5 px/cm up | body 70..700 px = 35.6 cm; back face 103..423 px = 18.3 cm (camera about 9 deg above, ~2.9 m away) |
| 04_front_hi (688 px) | 18.65 px/cm across, ~17.7 px/cm up | body 12..676 px = 35.6 cm; camera about 18 deg above |
| 15_top (541 px) | 9.69 px/cm | top 58..403 px = 35.6 cm wide; it is also 345 px deep, so the lid alone is ~35.6 cm deep |
| 05_34fl / 06_34fr | shape only | renders, used for silhouettes, seams, vents |

The renders and studio photos agree with the official size within ~2 %, so the proportions were taken from the
photos and scaled to 356 x 360 x 183 mm.

## Overall shape (side profile)

- Feet: 4 rubber pads, 0.3 cm (assumed; no bottom photo yet). Body from z = 0.3.
- Sides are flat and vertical; vertical corner radius ~0.8 cm; plan corners of the lid ~1.0 cm (top view).
- Front face: one plane at y = -18.0 from z = 0.3 up to ~16.7, then a ~1.6 cm radius into the flat top.
- Top: flat at z = 18.3 from the front rounding back to the lid's rear edge at y = +17.4 (top view: lid ~35.6 cm deep).
- Back, from the top down (34fl silhouette: lid overhangs the upper back by ~0.45 cm, lower block sticks out ~0.3 cm):
  - lid rear lip z 17.0..18.3 at y = +17.4;
  - back panel (back cover + side strips) z 6.0..17.0 at y = +17.1;
  - lower back (2-sided tray, corner blocks) z 0.3..6.0 at y = +17.35;
  - back-cover handle tab x -2.1..+2.1, z 14.0..15.4, sticks out to y = +18.0. **The official 360 mm depth is
    measured to this tab** (top view: tab 0.7 cm behind the lid edge, 3.9 cm wide, centred).

## Back (photos 07, 09; diagrams 01, 12, 13)

Positions are centres; "from left" = cm from the left edge seen from behind.

| feature | from left (behind) | x_model | z (cm up) | size W x H | depth / notes |
|---|---|---|---|---|---|
| AC inlet (IEC C14, mounted upright) | 1.4 | +16.4 | 10.9 | black face 1.7 x 2.8 inside a 2.0 x 3.0 frame | **flat**: frame on the back strip, no pocket. Plug C13 stands out fully |
| dark slot right of the inlet | 2.9 | +14.9 | 10.9 | 0.8 x 2.2 | gap between the strip and the back cover |
| port pocket (rounded slot) | 33.95 | -16.25 | 8.0..14.9 | 2.6 x 6.9 | **recessed ~1.5 cm** (diagrams 12/13 draw a channel with side walls ~0.55 x its width) |
| RJ45 (HL-L2445DW only) | 33.95 | -16.15 | 12.6 | jack 1.3 x 1.2 | on the pocket floor, 1.5 cm in |
| blank plate (HL-L2400DW only) | 33.95 | -16.15 | 12.3 | 1.9 x 2.8 | lighter grey, same place as the RJ45 |
| USB-B | 33.95 | -16.15 | 10.6 | 1.1 x 1.0 | on the pocket floor, 1.5 cm in |
| back cover (face-up tray door) | 3.3..32.2 | +14.5..-14.4 | 6.0..17.0 | 28.9 x 11.0 | hinged at the bottom, folds down |
| back cover handle tab | 15.8..20.3 | +2.1..-2.1 | 14.0..15.4 | 4.2 x 1.4 | sticks out 0.9 cm |
| 2-sided tray, upper flange | 4.2..30.8 | +13.6..-13.0 | 4.2..6.0 | | sticks out ~0.1 cm |
| 2-sided tray, green lever | 15.0..19.8 | +2.8..-2.0 | 2.1..4.0 | 4.8 x 1.9 | in a dark recess |
| lower corner block (behind right) | 28.8..35.6 | -11.0..-17.8 | 0.3..8.2 | | seam around it |
| vents (behind left, bottom) | 0.2..4.6 | +17.6..+13.2 | 0.5..5.0 | L-shaped slots | |

Recess evidence and caveat: the straight back photo cannot show depth (the camera was ~2.9 m away, so side walls
of shallow pockets are invisible). The port pocket is drawn as a channel in Brother's diagrams; the power inlet is
drawn on the flat strip and the 34fr silhouette shows a small bump at the back-right corner around inlet height,
so the inlet frame sits on (or slightly proud of) the back surface. Rear 3/4 or side photos would settle both.

## Front (photo 04, diagrams 02/03)

| feature | x | z | notes |
|---|---|---|---|
| paper tray front | -17.5..+17.5 | 0.35..9.25 | seam to the front cover at z 9.25..9.4 |
| tray handle notch | -4.65..+4.65 | 0.35..2.4 | open at the bottom, ~2 cm deep |
| front cover (toner door) | full width | 9.4..top | hinged at the bottom; its top part forms the front 7.7 cm of the lid (seam at y = -10.3) |
| manual-feed cover panel | -14.8..+14.8 | 10.1..15.2 | thin groove around it |
| grip slot above it | -5.15..+5.15 | 15.25..15.85 | dark, ~0.8 cm deep |
| "brother" logo | centred | 12.5 | ~4.9 cm wide, ~1.1 cm tall (x-height), light grey |

## Top (photo 15, panel close-ups 10/16, renders 05/06)

| feature | x | y | notes |
|---|---|---|---|
| front-cover seam | full width | -10.3 | groove |
| output support flap (in the front strip) | -5.0..+5.0 | -16.6..-13.6 | 0.25 thick, hinge at its FRONT edge |
| output tray recess | -10.9..+12.5 | -1.3..+11.5 | floor slopes from 2.3 cm deep at the exit to ~0.6 cm at the front |
| paper exit slot (under the rear lid) | -10.4..+12.0 | +11.5..+13.0 | z 16.0..17.3, black rollers |
| model label plate | -0.6..+2.5 | +12.8..+13.9 | dark plate, small white model name |
| LCD window | -17.0..-11.4 | -2.95..-2.2 | grey-green |
| power button (round, 1.0) | -16.25 | -5.1 | |
| Wi-Fi button (round, 1.0, green LED) | -16.35 | -6.8 | |
| Back / OK (1.4 x 0.75) | -14.2 / -12.65 | -5.1 | |
| down / up (1.4 x 0.75) | -14.2 / -12.65 | -6.65 | |
| Go (3.0 x 0.8, green light bar) | -13.6 | -8.3 | |

## Sides (renders 05/06, photo 17)

- Left side (-x): square-hole vent grille near the front, y -16.5..-7.5, z 4.0..15.5.
- Right side (+x): louvred vent near the back, y 0..+9, z 8.5..16.0. The top photo shows a dark strip just outside
  the right side at the same depth (~0.6 cm); the back photo shows no bump there, so it was not modelled as width.

## Moving parts

| part | pivot / travel | state |
|---|---|---|
| `cassette` (paper tray) | slides along -y | `refill`: pulled out 27 cm (diagram 14 shows it pulled fully out) |
| `flap` (output support flap) | hinge at its front edge (y -16.6, z 18.2), rotates +95 deg about x | `printing`: stands up ~3 cm above the lid |
| back cover, front cover, manual-feed cover | modelled as part of the body | not used by any state |

## Colours (sRGB) and finish

| part | hex | finish |
|---|---|---|
| body, lid, tray, covers ("dark grey") | #4b4c50 | matte, fine texture (roughness 0.6) |
| openings, exit slot, pockets | #1b1c1d | |
| port pocket floor | #36373a | |
| back cover tab, tray lever recess | #2e2f31 | |
| 2-sided tray lever | #4cc24a | green plastic |
| LCD (off) | #8f9a94 | glossy |
| Wi-Fi LED, Go light | #3fd46a | emissive |
| logo | #cfd0d2 | |
| power inlet, plugs, cables | #141414 | |

## Model status (2026-11-17)

- Builder: `build/builders/brother_hl_l2445dw.py`, a subclass of the HL-L2400DW builder
  (`Base = load_builder("brother-hl-l2400dw")`) that sets MODEL = "HL-L2445DW" and ETHERNET = True.
- Same body checked: both specs.json give 356 x 360 x 183 mm and 7.1 kg; the photo sets are pixel-identical except
  04_front (each store page's own front shot, same body). The only visible difference is the RJ45 jack above the
  USB-B in the port niche (photo 07_back, Brother UK HLL2445DW_1.png; photo 09 shows the 2400DW's blank plate there),
  plus the model name on the lid label.
- Cables: `cable_power` + `cable_eth`. Power plug on the flat back reaches 6.5 cm behind the body; the RJ45 sits in
  the 1.1 cm deep niche and reaches about 2.9 cm. `cable_space.behind_body_cm` = 6.5.
- Built size 35.6 x 36.05 x 18.3 cm; printing 20.8 cm high; refill 63.0 cm deep (same as the 2400DW).
- Comparison sheets: `work/compare/brother-hl-l2445dw/round1_ports.png` (port niche close-up for both models),
  `round2_final.png` (back with cables). Front, top and sides: see the HL-L2400DW's sheets (same body).
