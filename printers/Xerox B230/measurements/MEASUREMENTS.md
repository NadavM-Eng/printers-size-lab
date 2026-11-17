# Xerox B230 (B230V_DNI in Israel/Europe, B230/DNI in the US): measurements

Mono laser printer, same chassis as the Lexmark B2236dw (identical 355 x 333 mm footprint, 6.8 kg, 2-line LCD,
port layout). All numbers in cm. Model frame: x = 0 centre of the width (+x = right seen from the front),
y = 0 centre of the depth (front face y = -16.65, back face y = +16.65), z = 0 under the feet.

## Official size and what it includes

| source | H x W x D (mm) | note |
|---|---|---|
| Xerox dimension graphic (product page, `xerox-B230-Dimensions_800x450.jpg`) | 216 x 356 x 333 | arrow drawn to the main top surface |
| Xerox datasheets B23BR-01E / -01U / -01W | 232 x 355 x 333 | 9.1 x 14.0 x 13.1 in |
| Lexmark B2236dw (same chassis), Adorama, ITPro | 215 x 355 x 333 | Lexmark's own top |

The 16 mm difference is the raised control-panel wedge: in the front catalog photo the top edge of the LCD
wedge stands about 26 px above the top surface at the wedge's depth (17.98 px/cm, camera about 11 deg above),
i.e. about 1.5 cm. So: main top surface 21.6 cm (216 mm), top of the LCD wedge 23.2 cm (232 mm). The model is
checked against 355 x 333 x 232 (datasheet), and the main top is kept at 21.6.
Depth 333 mm is the closed body with the 250-sheet tray set to Letter length and the paper stop folded. With
A4 paper the tray "pokes slightly out of its rear panel" behind a dust flap (ITPro review); from the paper
lengths (A4 297 mm vs Letter 279 mm) that is at most about 1-2 cm at the bottom centre of the back, less than
the power plug needs, so it does not change the cable space below. Not modelled.

## Photo index (`printers/Xerox B230/photos/`)

| file | view | what it shows | source |
|---|---|---|---|
| 00_dims_official.png | 3/4 front-right + dims | Xerox dimension graphic 216/356/333 mm, 6.8 kg | xerox.com product page (office.xerox.com asset) |
| 01_front.png | front, ~11 deg above | catalog photo B230_DNI_FRONT: logo plate, power button, manual-feed flap, cassette, paper gauge | xerox.com/catalog_photos |
| 03_back.png | back, ~8 deg above | rear door, finger notch, label area, duplex strip + black/blue handle, port column (Ethernet, slot, USB-B), power pocket | Best Buy gallery (Xerox render) |
| 05_34fl.png | 3/4 front-left | left side: full-length horizontal vent grille in the lower half, handhold notch | Best Buy gallery (Xerox render) |
| 06_34fr.png | 3/4 front-right | right side: vent grille high at the back, handhold step at the bottom | MediaMarkt NL (B230V_DNI) |
| 07_top_paper.png | top, ~58 deg above | output bin with a sheet, panel column (B230 plate, LCD, LEDs, D-pad, 2 buttons) | MediaMarkt NL (B230V_DNI) |
| 08_34fl_hi.png | 3/4 front-left | same as 05, sharper | MediaMarkt NL (B230V_DNI) |
| 09_top_real.png | top-front, real photo | real used unit: bin ribs, paper stop flap, panel, US power cord | eBay listing 407215997892 |
| 20_panel_detail.png | panel close-up | LCD wedge, "B230" print, 2 LEDs, D-pad, menu + cancel buttons, right-side vent | shop.xerox.com gallery |
| 21_front_door_open.png | 3/4 front-left, door open | front door hinged at the bottom, drops to about horizontal | shop.xerox.com gallery |
| 30_manual_rear_ports.png | rear 3/4 drawing | User Guide p.34: 1 Ethernet, 2 USB, 3 power cord socket, at the rear corner on the printer's left side | Xerox B230 User Guide (support.xerox.com) |
| 10_top_real.png | top-front, real photo | used unit: bin ribs, paper stop, panel column, B230 print | OLX.pl listing (used B230) |
| 11_back34_real.png | behind-left, real photo | rear door + label, port notch, power notch with C13 plug, tray-extension dust cover sticking out | OLX.pl listing (same unit) |
| 12_back_ports_real.png | port corner close-up | crop of 11: Ethernet, slot, USB-B, screw in the upper notch; C13 plug in the lower notch | OLX.pl listing (same unit) |
| 13_back_real.png | back, real photo | rear door, finger notch, rating label, duplex handle (no ports in frame) | Kleinanzeigen listing |

User Guide pages also looked at (not saved): p.21 configuration, p.36-37 tray (fixed-length tray, blue rear
length guide), p.180 jam areas, p.184 rear door (hinged at the bottom, opens down; fuser access door inside),
p.185 duplex unit (pulls out of the back at the bottom, below the rear door).

## Scales

- Front (01_front, 656 x 512 px): bottom front edge x 8..648 = 640 px = 35.6 cm -> 17.98 px/cm. Camera about
  11 deg above (top depth 33.3 cm seen as ~145 px), so heights are divided by cos 11 = 0.98.
- Back (03_back, 744 x 565 px): body x 8..735 = 727 px -> 20.4 px/cm; bottom edge y = 552.
- Top (07_top_paper, 410 x 407 px): x 8..402 = 394 px -> 11.07 px/cm across; depth foreshortened by 0.85.

## Body

- Plan: rounded rectangle 35.6 x 33.3, vertical corner radius about 1.0 (top cover corners about 1.2).
- Feet: 4 small rubber feet, 0.25 tall, at x = +-15.8, y = +-14.8. Body bottom z = 0.25.
- White shell: z 0.25 -> 19.8. Navy top cover: z 19.8 -> 21.6 (front lip 1.8: navy band bottom at y = 157 px in
  the front photo; white face 157 -> 497 px = 19.3 cm / 0.98), top edges rounded about 0.6.
- Cassette / front door seam: y = 364 px in the front photo -> 39 % of the white face from the bottom -> z 7.9.
- Front door (upper front, white): z 7.9 -> 19.8, full width; vertical seam on each side about 1 cm behind the
  front face (05_34fl). Opens down about 90 deg (21_front_door_open). Not a state on the site.

### Front face (01_front)
- Logo plate: x 273..380 px -> 6.0 wide, centred x = -0.1; z 14.5 -> 16.2. Dark (#333) rounded plate, white "xerox".
- Power button: centre x = +15.0, z = 17.85, ring diameter 1.45.
- Manual feed flap (outline groove on 3 sides, bottom edge on the seam): x -13.1 -> +13.1 (93..563 px), z 7.9 -> 12.4,
  top corners rounded about 0.8. Four tiny dots on its top centre.
- Cassette (z 0.25 -> 7.85, full width front cap): finger grip cut-out at the bottom centre x -7.55 -> +7.55,
  z up to 2.1 (188..460 px, top at 465 px), about 2 cm deep.
- Paper level gauge: slot x +10.3 -> +11.15, z 0.4 -> 4.7, dark with a blue indicator, icons to its right.

### Top (07_top_paper, 09_top_real)
- Output bin recess: x -11.0 -> +10.4 (83..322 px), back wall at y = +11.1 (5.5 behind... from the back edge),
  front lip at y = -4.7 (ribs end level with the D-pad centre in 09_top_real). Floor slopes from about z 17.2 at the
  back wall (exit slot with black rollers) up to z 21.0 at the front lip. 5 ribs along y, about 4.2 apart.
- Two small light-grey paper guides at the back corners of the bin (x about -8.5 and +8.0).
- Paper stop flap: x -4.4 -> +3.6 (8 wide, centred -0.4 like the bin), y -16.2 -> -8.85 (its back edge is level
  with the two buttons in 09_top_real), flush in the top. Hinge at the front (finger notch at its back end).
  Printing state: raised about 105 deg so it stands up at the front edge, leaning slightly forward.
- Control panel column on the right, centre x = +14.2 (362 px in 07):
  "B230" plate y +3.8 -> +5.9 (4 x 2.1); LCD wedge x 11.9 -> 16.5, y -1.2 -> +1.5, back top 1.6 above the top
  surface (23.2), front edge 0.3; LCD window 3.6 x 1.0 on its slanted face; LEDs at y -2.45 (x 13.3 and 14.9);
  D-pad centre y -5.65, radius 1.75, OK button radius 0.7; two buttons (menu, cancel with red X) at y -8.85,
  x 13.4 and 15.0, 1.45 x 0.75 each.

### Back (03_back, 30_manual_rear_ports). "xb" = cm from the left edge seen from behind; x = 17.8 - xb.
- Rear door: xb 3.1 -> 32.1 -> x +14.7 -> -14.3; z 7.0 -> 19.8. Finger notch at the top centre x -2.5 -> +3.0,
  z 17.8 -> 19.8. Label area x -6.1 -> +5.4, z 10.1 -> 14.9 (flat).
- Duplex unit strip: x -13.4 -> +13.8, z 4.4 -> 7.0; black handle x -3.8 -> +3.2, z 3.2 -> 5.4 with a blue tab.
  Flush with the back when closed (pulls out backward only to clear jams).
- Port column at the rear corner on the printer's LEFT side (seen from the front): recessed panel
  x -17.45 -> -14.6, z 9.8 -> 17.4. Ethernet (RJ45) centre x -16.7, z 16.1; a small slot at z 14.5;
  USB-B centre x -16.4, z 12.3 (order Ethernet, USB from the top, as in the User Guide's numbering).
- Power inlet (IEC C14, mounted vertically: the pocket is 2.1 wide x 3.5 tall) in its own dark pocket
  x -16.4 -> -14.3, z 2.1 -> 5.6, centre x -15.35, z 3.85.
- Recess depths, from the real photo 12_back_ports_real (camera about 58 deg off the back, 32 deg off the left side;
  vertical scale about 59 px/cm from the 7.8 cm notch height, so about 50 px/cm along y on the side-facing walls):
  port notch inner wall about 150 px -> **3.0 cm**; power notch about 190 px -> **3.6 cm**, and the C13 plug housing
  in it measures about 170 px = 3.4 cm, which is the real housing length, so the scale checks out. Both notches are
  open to the back AND to the left side (from that camera a closed side wall would hide the whole port plate, but
  the plate is fully visible). The earlier estimate (1.5 / 2.5 cm from the render's shading) was too shallow.

### Sides
- Left: horizontal vent slots over the lower half, y -15 -> +14, z 3.8 -> 9.0 (05_34fl, 08_34fl_hi).
- Right: horizontal vent slots high at the back, y +4.3 -> +13.6, z 11.9 -> 18.9 (06_34fr, 00, 20).
- Handholds: recesses at the bottom of both sides, y about +3 -> +13, z 0.25 -> 2.2, 1.3 deep.

## Cable space behind (the user's rule)

Both sockets are in notches about 3.0 cm (Ethernet/USB) and 3.6 cm (power) deep, so the plug bodies sit inside:
- Power: C13 housing 3.4 cm in a 3.6 cm notch -> housing ends 0.2 cm inside the back; the strain relief (about 2.4 cm)
  and the squashed bend stick out -> **3.3 cm** behind the back (3D model "cables reach 3.3 cm").
- Ethernet: RJ45 2.4 cm in a 3.0 cm notch -> plug ends 0.6 inside; boot 1.6 + bend -> 1.9 cm.
So this is close to the user's "recessed" case: only the cable (and the kettle plug's strain relief) needs room.
`cable_space.behind_body_cm` = 3.3 in specs.json. An angled C13 cord would bring it to about 1.5-2 cm.
Less than the HP OfficeJet J4580 on the shelf now (4.5 cm measured).

A4 paper: the tray extends out of the back at the bottom centre under a dust cover (ITPro; seen in 11_back34_real,
where the cover sticks out further, probably set to Legal). For A4 it is about 2 cm (A4 297 vs Letter 279 mm). It sits
beside the power notch, under the rear door, and is shorter than the power cable reach. Not modelled.

## Moving parts and states

- `cassette`: slides straight out of the front. refill: out 26 cm (paper is loaded with the tray removed;
  the tray is about 31 cm long).
- `flap` (paper stop on top, front centre): hinge on its front edge at y -16.2, z 21.6; printing: +105 deg about x.
- Front door, rear door, duplex unit and manual-feed flap: part of `body` (only opened for toner and jams).

## Colours (sRGB) and finish

- White body: #e6e7e8, satin (render reads #e5e5e5 lit).
- Navy top cover: #2f3d4c, fine matte texture (render reads #35424e in shade, #48555e lit).
- Logo plate, D-pad, buttons: #2b2d30 (plate #333 in the photo); logo text white.
- Exit slot, ports, handle, pockets: near black #101112.
- Blue accents (paper gauge, duplex tab): #3d7bd0.
- LCD: grey-blue #b8c4c8 with dark text; status LED blue.

## Model status (2026-11-17)

- Height settled: the Xerox dimension graphic's 216 mm arrow ends at the front-left top edge of the top cover, so
  216 mm = top cover and the datasheet's 232 mm = overall height with the raised LCD pod (16 mm above the cover).
  specs.json keeps 232 as the closed height (it is the true overall height); the model is 35.5 x 33.4 x 23.1 cm
  (official 35.5 x 33.3 x 23.2), top cover at 21.6.
- Photos added: 10_top_real, 11_back34_real, 12_back_ports_real, 13_back_real (real used units, from leads already
  downloaded in work/photo_candidates; no new web search was needed).
- Rounds: round1a/b (earlier helper), round2 (front, real back, real top, 3/4 front-left, real back-left), round3
  (port close-up, back-left, printing state) in work/compare/xerox-b230/. Change this time: the notches deepened to
  3.0 / 3.6 cm from the real port photo.
- States: printing = paper stop flap up (H 27.9 cm); refill = cassette out 26 cm (D 59.3 cm).
- Still differs: the blue duplex tab is brighter than on the real unit; the paper stop is navy, a bit lighter than
  the near-black one on real units; the slot and screw in the port notch are simplified; the A4 tray extension
  and its dust cover are not modelled.
- Without a photo (kept plain): the underside and the right side apart from the vents.

