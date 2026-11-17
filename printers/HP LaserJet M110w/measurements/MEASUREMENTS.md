# HP LaserJet M110w (7MD66F): measurements for the 3D model

Model frame used below and in `build/builders/hp_laserjet_m110w.py`: cm, x to the right seen from the
front, y towards the back, z up; x = 0 at the centre of the width, y = 0 at the centre of the depth
(front face y = -9.45, back face y = +9.45), z = 0 under the feet.

## Official size

| | W | D | H | source |
|---|---|---|---|---|
| closed ("minimum") | 34.6 | 18.9 | 15.9 | HP datasheet 7MD66F (gb-en Oct 2024), user guide table A-1, HP "Built to Fit" image (photo 28) |
| HP "maximum" | 34.6 | 36.0 | 28.0 | HP datasheet; height = top cover (toner door) raised |
| user guide "printer fully open" | 34.6 | 32.96 | 28.01 | user guide table A-1 |

The 18.9 cm depth is the whole body from the flat back to the closed front door. Nothing on the back
sticks out except the plugs. Some HP sheets give the height as 158 mm; the model uses 159 mm.

The M110we (7MD66E, HP+) has the same body; several photos below are of an M110we and are used for
shape only.

## Photo index

All files are in `printers/HP LaserJet M110w/photos/` (they belong to their
owners). "HP" = HP product images, "eBay" = marketplace listing photos of real units.

| file | view | what it shows | source |
|---|---|---|---|
| 01_front_tray_open | front | straight front (slightly above), front door folded down into the input tray with paper | HP US store, M110w (7MD66F), image 1 |
| 02_detail_output_panel | detail | top close-up: control panel, exit slot under the hood, sheet in the bin | HP US store, M110w, image 2 |
| 03_back | back | straight back, nearly level, 2x2 stitched hi-res: flat back, USB-B in the rear-left corner pocket, C14 inlet flush lower left (both on the right when seen from behind) | HP US store, M110w, image 3 |
| 04_34fl_tray_open | 3/4 front-left | door open with paper; inner front panel with embossed logo; lift tab under the top cover | HP US store, M110w, image 4 |
| 05_top | top | straight top (front at the bottom): hood, grey bin, control panel at the front-left, extension tab | HP US store, M110w, image 5 |
| 06_lifestyle_34fl_closed | 3/4 front-left | on a desk, closed, sheet on the output | HP US store, M110w, image 7 |
| 07_detail_usb_pocket | detail back | crop of 03: the USB pocket, port near the pocket's inner wall | HP (crop of image 3) |
| 08_detail_power_inlet | detail back | crop of 03: C14 inlet in a black frame, flush with the back, turned 90 deg | HP (crop of image 3) |
| 09_back_real | back (from above) | real unit: flat back, pocket, inlet | eBay 257394048636 (M110we) |
| 10_left_real | left (from above) | real unit left side: corner notch at the rear, seam line, curved front-top | eBay 257394048636 |
| 11_right_real | right (from above) | real unit right side, seam line | eBay 257394048636 |
| 12_front_closed_real | front | real unit closed, stickers | eBay 257394048636 |
| 13_bottom_real | bottom | underside (front at the top of the image) | eBay 257394048636 |
| 14_top_front_real | top from front | real unit: control panel, bin, extension tab, exit slot with rollers | eBay 257394048636 |
| 15_front_tray_open_real | front | real unit, door folded down (empty tray), inner front panel, paper slot | eBay 257394048636 |
| 16_34bl | 3/4 rear-left | back and left side: pocket wraps the corner, inlet flush | HP US store, M110we, image 4 |
| 17_detail_back_corner | detail 3/4 rear-left | crop of 16: pocket depth visible on its side wall | HP (crop) |
| 18_34fl_door_opening | low 3/4 front-left | front door half open on its bottom hinge | HP US store, M110we, image 7 |
| 19_34fl_closed | 3/4 front-left | closed, from above | HP US store, M110we, image 3 |
| 20_top_cover_open_real | front | top cover (toner door) raised + door down | eBay 800880230631 (M110w) |
| 21_printing_extension_real | front from above | door down AND output extension pulled out (printing) | eBay 137897880920 (M110w, label 7MD66F) |
| 22_back_above_real | back from above | real unit back, pocket, inlet | eBay 137897880920 |
| 23_top_cover_open_real | front from above | top cover raised, 142A cartridge | eBay 137897880920 |
| 24_front_closed | front | straight front closed (camera ~18 deg above): best front reference | Coolblue M110w page (HP image) |
| 25_34fr_low_closed | low 3/4 front-right | right side and the stepped top | Coolblue (HP image) |
| 26_34bl_low | low 3/4 rear-left | pocket and inlet close | Coolblue (HP image) |
| 27_ports_callout | detail back | HP "Ports" callout | Currys UK (HP image) |
| 28_dims_marketing | 3/4 | HP "Built to Fit": 346 x 189 x 159 mm, 3.8 kg | Currys UK (HP image) |

Photo count by view: front 5 (01, 12, 15, 24 + 06 lifestyle), back 4 (03, 09, 22, 27), 3/4 rear 3 (16, 17, 26),
left 1 (10), right 1 (11), 3/4 front 5 (04, 18, 19, 25, 28), top 3 (05, 14, 21), bottom 1 (13),
details 3 (02, 07, 08), top cover open 2 (20, 23).

## Scales

- 03_back (1146 x 542): back face 1131 px wide at the top = 34.6 cm -> 32.69 px/cm; height 515 px
  (y 20 -> 535) = 15.9 cm -> 32.4 px/cm. Camera almost level (top surface shows as a 15 px band).
- 24_front_closed (737 x 369): 736 px = 34.6 cm at the top cover (21.27 px/cm); camera about 18 deg
  above with noticeable keystone (scale shrinks 0.0287 % per px going down, from the door edges, which
  are vertical in reality).
- 05_top (542 x 297): 529 px = 34.6 cm (15.29 px/cm across), 284 px = 18.9 cm deep (15.03 px/cm).
- 10_left_real: 18.9 cm = 504 px at the near side (26.7 px/cm); camera about 20 deg above.

## Body shape

**Side walls have a draft.** In the near-orthographic back view the outline is a straight line from
x 7 -> 35 px (left) and 1138 -> 1110 px (right) between the top and the bottom: 1131 px -> 1075 px, i.e.
34.6 -> 32.9 cm. The front view agrees once its keystone is removed (outline leans twice as much as the
door edges). Model: half-width 17.3 at z >= 15.5, falling linearly to 16.5 at z = 0.3 (0.8 cm per side).
The front and back faces are vertical (side photos: front and back edges lean symmetrically = keystone).

**Side profile** (at the side areas, from 10/11 and 05):
- back face vertical, top-back edge radius about 1.0;
- rear hood: flat top at z = 15.9 from the back to 8.0 cm from the back (y = +1.45; dark seam line in
  05 at 120 px from the back edge = 8.0 cm);
- front section (left area with the control panel, the bin, the right area): starts about 0.45 cm
  lower than the hood (z 15.45) and curves down to the front edge: z 13.6 at the front face (front /
  back height ratio of the side face 0.85-0.87 in photos 10 and 11), convex arc of radius about 32 cm
  (z = 15.45 - (32.17 - sqrt(32.17^2 - (1.3 - y)^2))); front-top edge radius about 1.0;
- front face of the top cover (band) from z 12.15 to 13.6; seam to the door/columns at z 12.15
  (24: dark line at y 101-104 px across the full width).

| y (cm) | +9.45 | +5 | +1.45 | 0 | -2 | -4 | -6 | -8 | -9.45 |
|---|---|---|---|---|---|---|---|---|---|
| top z (side areas) | 15.9 (R1) | 15.9 | 15.9 / 15.45 step | 15.42 | 15.28 | 15.0 | 14.6 | 14.1 | 13.6 (R1) |

**Plan**: rectangle 34.6 x 18.9; back corners radius about 1.0 (05: inset 14 px at the back edge);
front corners radius about 2.5 at the top (05: inset 3.5 cm at 0.27 cm from the front, 1.3 cm at 1.3 cm);
the front columns wrap about 2 cm round the corner (vertical line on the side photos).

**Output bin** (05, 14): centred, 22.5 cm wide at the hood (x 99..443 px) narrowing to 21.7 cm at the
front, from the hood face (8.0 cm from the back) to the front lip. Floor z 13.1 at the front rising to
13.7 at the hood face; grey #7E8084. Exit slot under the hood front: x +-10.9, z 13.75-14.95, black,
with white roller wheels. Hood front face above the slot white.

**Control panel** (05 crop): light-grey rounded plate on the sloping front-left area, x -16.0..-13.1
(1.3-4.2 cm from the left edge), y -6.75..-1.55 (11.0-16.2 cm from the back); buttons from the back:
Wireless (blue icon) at y -3.05, Cancel (x) at y -4.35 with the amber "!" LED to its right, Power (pill
with green icon) at y -5.65.

**Front** (24, 12, 15):
- front door = input tray: 28.0 cm wide (x +-14.0, keystone-corrected 591 px at 21.12 px/cm), from
  z 0.45 to 12.05, about 1.0 thick, flush with the columns, 0.12 gaps; hinged at its bottom.
- finger notch at the top centre of the door: x +-4.85 (200 px = 9.7 cm), 0.8 tall; behind it the lift
  tab of the top cover (grey in 24, #C0C0C0 shadow).
- columns: the rest of the front, 3.1 cm wide at the top, 2.5 at the bottom (draft).
- HP logo: silver disc 4.1 cm, centre x 0, z 6.0 (24: centre y 237 px, 89 px tall).
- "HP LaserJet M110w(e)" small grey text at x +9.6, z 1.8, about 0.45 tall.
- behind the door (15, 04): fixed inner panel set back 1.1 cm, embossed white logo, paper slot at the
  bottom (x +-11, z 0.9-1.9, dark).

**Back** (03, 07, 08, 16, 17, 26, 27), x in the model frame (the ports are at the printer's LEFT rear
corner, i.e. on the right when seen from behind):

| item | x (model) | from left edge seen from behind | z | size | recess |
|---|---|---|---|---|---|
| USB corner pocket | -17.3 .. -14.0 | 31.3 .. 34.6 | 8.4 .. 12.4 | 3.3 w x 4.0 h, open to back and left side | 2.5 deep (side photo 10: 65 px / 26.7; 3/4 view 17: 2.7) |
| USB-B port (on the pocket's back wall) | -15.0 | 32.3 | 10.4 | 1.2 x 1.1 | socket face 2.5 inside the outline |
| power inlet IEC C14 (black frame) | -13.95 | 31.25 | 3.0 | frame 2.5 w x 3.2 h, turned 90 deg (pins horizontal, earth to the right seen from behind) | 0: flush on the flat back |

So: the power plug (C13, about 3.4 cm + 2.4 cm strain relief) sticks straight out of a flat back; the
USB-B plug sits half inside its pocket (about 3 cm plug in a 2.5 cm deep pocket). Nothing else on the
back sticks out; there is no rear tray or bulge. No Ethernet port.

**Bottom** (13): flat base with small round pads; model 4 feet 1.5 cm diameter, 0.3 tall at x +-13,
y -6.5 / +7.0; bottom edge chamfer about 0.5.

## Moving parts

| part | how | numbers |
|---|---|---|
| input_tray (front door) | rotates forward about a hinge at its bottom, y -8.95, z 1.1 | 90 deg: lies flat 0.6 cm above the shelf, reaching y -19.9 |
| tray_ext | slides out of the open door | 3.5 cm more, so the printing depth = 9.45 + 23.5 = 33.0 cm (user guide fully open 32.96) |
| support (output extension, grey) | slides forward out of the bin front | 10.5 cm (photo 21: two stages + wider end tab, tip about 10 cm in front of the face, over the tray) |
| top cover (toner door, hinged at the back) | not modelled as moving | HP max height 28.0 with it raised |

States: printing = door open + tray extension + paper + output extension out; refill = door open + tray
extension + paper (paper is loaded only in this front tray). No scanner, so no lid_open.

## Colours (sRGB) and finish

| part | colour | finish |
|---|---|---|
| body, door, columns, hood | #E6E6E2 | matte to satin plastic |
| bin floor, output extension | #7E8084 | matte grey plastic |
| exit slot | #151618 | black |
| control panel plate | #D3D4CE | satin light grey |
| HP logo disc | #BDBEC0 | metallic silver (printed/embossed grey on real units, #B7B8B2) |
| power inlet frame | #1C1C1C | black |
| USB port | #2A2A2A with metal shell #A0A0A0 | |

## Model status (2026-11-17)

- Builder: `build/builders/hp_laserjet_m110w.py`. First GLB and geom.json exported (`docs/models/hp-laserjet-m110w.glb`,
  0.57 MB, 18.3k triangles).
- Size: closed 34.6 x 18.9 x 15.9 (official 346 x 189 x 159 mm, diff 0). `printing` and `refill`: 34.6 x 32.9 x 15.9
  (door folded down 11.2 cm + tray extension 2.85 cm in front; HP user guide "fully open" 32.96 cm). HP's datasheet
  "maximum" 36.0 x 28.0 is with the toner door raised, which is not a state here.
- Cables: power (C14 inlet flush on the flat back) sticks out; USB-B sits 2.5 cm deep in the corner pocket (recessed).
  Build: cables reach 6.8 cm behind the back; specs.json `cable_space.behind_body_cm` = 6.8 to match.
- Photos: none added; the set (28 photos) already covers back, front, top, sides and bottom, so no web search.
- Rounds: 1-2 by the earlier helper, round 3 here (`work/compare/hp-laserjet-m110w/round3a.png` front/back/top,
  `round3b.png` 3/4 front, 3/4 rear, printing, `round3c.png` printing vs photo 21). No big differences left.
- Still differs: HP logo is a flat disc with "hp" text, not the real italic emblem; the exit slot is plain black with
  simple roller blocks; the output extension is three flat grey plates; the inner front panel's embossed logo is a
  plain disc. Paper on the open tray is a plain A4 block. The toner door is not a moving part.
