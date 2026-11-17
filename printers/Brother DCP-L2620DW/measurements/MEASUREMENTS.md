# Brother DCP-L2620DW: measurements

Mono laser all-in-one with a flatbed scanner (no document feeder). Official closed size
**410 W x 399 D x 272 H mm**, 10.1 kg (Brother online user guide, Specifications:
https://support.brother.com/g/s/id/htmldoc/mfc/cv_dcpl2508dw/uke/html/GUID-7A38839F-5CD3-4CAD-A170-5EA17E89A64E_1.html).
The same guide's "typical outline view" (photo 91) is an orthographic front + side drawing of this
exact body (the flatbed DCP-L2600D/L2620DW row of the size table), so it is the main source for the
side profile. Photos are scaled to the official size; studio shots are perspective, so proportions
come from them and absolute sizes from the official numbers.

Frame used below (same as the builder): cm, X across (+X = printer's right seen from the front),
Y front to back (front = -Y), Z up, z = 0 under the feet. Depth is also given as "from the front"
(0 = the paper-tray/front-cover face, 39.9 = rear-most point). y = depth - 19.95.

## Photo index

Files in `photos/` (not in the repo). All exact-model
unless marked SIBLING (same chassis, used only where noted).

| file | view | shows | source |
|---|---|---|---|
| 01_mfr_34_front_right | 3/4 front-RIGHT, ~22 deg up | panel, output, right side with vent and grip slot, rear overhang step | Brother UK store, alt DCPL2620DW_left.png (Brother's name says "left" but the camera is on the printer's right; the earlier agent's label was wrong and its low-res copy moved to `_rejected/`) https://store.brother.co.uk/devices/laser/dcp/dcpl2620dw |
| 02_mfr_front | front, ~18 deg up | front faces, panel, output with paper, logo, slot, tray grip | Brother UK store, DCPL2620DW_main.png |
| 03_mfr_back | back, straight, about lid height | power inlet, USB, LAN blank, back cover, hinges, overhang | Brother UK store, DCPL2620DW_1.png (captured enlarged) |
| 04_mfr_front_lifestyle | front at lid height, long lens | best straight front: widths of lid vs lower body | Brother UK store, DCPL2620DW_2.png |
| 05_mfr_top_lifestyle | high from front-left, person for scale | lid top, panel | Brother UK store, DCPL2620DW_3.png |
| 10_used_front_top | front ~45 deg up, real | whole control panel layout readable, DCP logo on lid | OLX.pl listing https://www.olx.pl/d/oferta/brother-dcp-l2620dw-drukarka-wielofunkcyjna-mono-laserowa-3w1-wifi-CID99-ID19cm7N.html |
| 11_used_34_front_left_close | close 3/4 front-left, real | panel section (top face + front band + light lower band), left grip slot, left vent | same OLX listing ("DCP-L2620DW" printed above the LCD) |
| 12_used_34_front_right_close | close 3/4 front-right, real | output floor colour/texture, right vent, rear overhang step | same OLX listing |
| 13_used_lid_open | lid raised, from front-high, real | lid angle (~80 deg), two hinges at the back, glass | same OLX listing |
| 20_used_panel_closeup | panel close-up (rotated) | LCD with "DCP-L2620DW", Menu/Clear/OK keys | Kleinanzeigen https://www.kleinanzeigen.de/s-anzeige/brother-dcp-l2620dw-multifunktions-laserdrucker-wie-neu-/3568689446-225-1262 |
| 90_diag_ports_back | manual drawing | port locations: LAN (network models only) and USB in a vertical channel at the right end of the back seen from behind | user guide "Input/Output Port Locations" (drawing shows the ADF sibling body) |
| 91_diag_outline_dims | manual drawing, orthographic | front and right-side outline with the 410/272/399 arrows | user guide Specifications |
| 92_diag_tray_out | manual drawing | paper tray pulled fully out | user guide "Load Paper in the Paper Tray" (ADF sibling body) |
| 93_diag_support_flap | manual drawing | support flap flips up at the front of the output tray | same page, step 7 (ADF sibling body) |
| 94_diag_qsg_power_back | SIBLING manual drawing | power cord plugged in straight back, under the rear overhang | Quick Setup Guide CHN-ENG (DCP-L2508DW/L2628DW family) https://download.brother.com/welcome/doc101432/cv_dcpl2508dw_chne_qsg.pdf |
| 95_diag_back_cover_open | manual drawing | back cover hinged at its bottom, opens down | user guide "Paper is Jammed in the Back" (ADF sibling body) |

No straight side, bottom or back-3/4 photo of the exact model was reachable (Amazon blocks agents,
Galaxus/Scan/x-kom show bot checks); the side profile comes from the orthographic outline drawing,
checked against the 3/4 photos.

## Scales

* Outline drawing 91 (trimmed capture, 2.2x of a 292x116 GIF): side view depth 399 mm = x 442.5 to
  735.5 px -> 1.362 mm/px; height 272 mm = y 7 to 200 px -> 1.409 mm/px. Lines are 2-3 px thick, so
  about +-3 mm.
* Front lifestyle 04: lid 63..512 px = 41.0 cm -> 10.95 px/cm (camera at lid height, long lens).
* Studio front 02: lid front edge 8..581 px = 41.0 cm -> 14.0 px/cm at the scanner plane.
* Back 03: scanner/lid 8..770 px = 41.0 cm -> 18.6 px/cm at the rear plane; the lower back is
  4.4 cm further away: lower-body widths (38.1 cm at z 14, 36.3 cm at z 1) give 17.8 px/cm there
  (camera ~1 m away). Body bottom at y 566 px.
* Panel close-up 10: panel 28..545 px = 27.6 cm -> 18.7 px/cm along the panel.

## Overall body (from the side outline, cross-checked with photos)

| part | depth from front (cm) | z (cm) | width (cm) |
|---|---|---|---|
| lower body (cassette + front cover + engine) | 0 -> 35.3 | 0 -> 20.7 (front top edge 18.8) | 36.2 at the feet -> 38.8 at z 18.8 (sides lean in toward the bottom; 04: 397/423 px vs lid 449 px; 02 agrees) |
| upper rear block (overhang) | 25 -> 39.9 | 14.2 -> 20.7 | ~40.0 (back photo 734-750 px) |
| scanner unit | 6.0 -> 39.9 | 20.7 -> 25.5 | 41.0 |
| lid (document cover) | 6.0 -> 39.5 | 25.5 -> 27.2 (lid 1.7 thick) | 41.0 |
| control panel | 0.9 -> 6.0 (sticks out in front of the scanner) | 21.8 -> 25.3 | from the left side to 27.6 cm (X -20.5 -> +7.1) |

* Rear overhang: the outline shows the lower back as a vertical line at x 700-703 px (35.3 cm) from
  z 0 to 14.2 cm, and the block above it reaching 39.7-39.9 cm with a rounded lower-rear corner
  (r ~1 cm). Photos 01 and 12 show the same step on the right side behind the vent.
* Side seams: tray/cover side seam 2.4 cm from the front (z 0 -> 14.2), stepping back to 5.7-7.0 cm
  from z 14.2 to 18.8. Tray/front-cover seam at z 9.2 (outline 8.8, photo 04 9.5).
* Top front: lid front edge and scanner front flush at 6.0 cm; front-top lid corner r ~0.5.
* Lid front notch (finger grip): 9.8 cm wide, centred, upper 1 cm of the lid front (outline x 109-177 px;
  photo 02 dark slot 135 px = 9.7 cm).
* Grip slots on both sides near the top: from 17.1 to 26.4 cm from the front, z 16.6 -> 19.4 (deep
  slot), with a vent grille below it on the right side (z 9 -> 16, irregular 6x7 square holes).
  Left side: grip slot at the same place, vent grille low at the front (photo 11).

## Front

* Front cover face z 9.2 -> 18.8; recessed name plate X +-15.2 (30.4 wide; photo 02: 418/529 px of a
  38.8 cm face = 30.7), z 10.6 -> 15.7, recessed ~0.15.
* "brother" logo centred at z 13.7, 5.1 cm wide, silver.
* Manual feed slot: X +-5.3, z 15.2 -> 16.6 (outline x 106-180 px), a bevelled recess with a dark slit.
* Cassette front z 0.3 -> 9.2, full lower-body width; grip notch at the bottom centre 10 cm wide, 3 cm
  tall (outline 106-180 px = 10.6; photo 02 9.6).
* Output floor: z 18.8, light-grey textured (photo 12), from X -18 to +15.5, running back under the
  scanner to the exit slot; side walls rise to z 20.7 outside that.
* Support flap: 9.8 x 4.5 cm plate centred in the output floor just behind the front edge, with two
  small angled guide ribs at X +-7.3 (outline rows 69-85; photos 01, 02).

## Control panel (photos 01, 10, 11, 20)

Section: an inclined top face (falls ~12 deg toward the front) carrying the LCD and keys, a
rounded front edge (r ~1), a dark front band down to z ~22.8, and a lighter-grey lower band
set back ~0.3 down to z 21.8. Right end rounded in plan (r ~2.5). Along the panel (from its left
end, photo 10 scale): LCD bezel 2.0 -> 9.5 (screen 3.0 -> 8.7, 1.9 tall), Clear/Menu keys at 11.1,
up/OK/down pad at 13.9, Scan / 2-in-1 ID Copy at 16.8, Copy/Scan Options / Wi-Fi at 19.2,
Stop/Exit (red bar) and Start (green bar) at 21.9, power key at 24.7.

## Back (photo 03, lower-back scale 17.8 px/cm, centre x 389 px, bottom y 566 px)

Seen from behind, "left" is the printer's right side (+X).

| item | photo px (x, y) | X (cm) | z (cm) | from left seen from behind (cm, of 41) | recess |
|---|---|---|---|---|---|
| power inlet (C14, turned 90 deg: pins in a vertical line) | 68-122, 330-398; centre 95, 364 | +16.5 | 11.3 (9.4 -> 13.3 pocket) | 4.0 | pocket ~3.0 x 3.8, ~1 cm deep, on the lower back face |
| USB-B | 672-696, 429-452; centre 684, 440 | -16.6 | 7.1 | 37.1 | ~0.6, at the bottom of a vertical channel |
| LAN blank plate (no Ethernet) | 668-708, 341-430 | -16.6 | 7.7 -> 12.6 | - | light grey plate in the same channel |
| rear overhang underside | y ~313-320 | - | 14.2 | - | the block above it reaches 4.5 cm further back |
| back cover (opens down) | 130-655, 280-470 | -14.9..+14.6 | 5.4 -> 14.2 | - | flat |
| duplex/fuser lever, green | 380-420, 505-535 | 0 | 1.7 -> 3.4 | - | in a dark recess |
| lid hinges | 70-110 and 540-580, y 100-130 | +15.0 / -9.3 | 25-27 | - | proud of the lid back ~0.4 |
| dark cavity in the upper back | 175-495, 195-250 | +11.5..-5.7 | 17.5 -> 20.5 | - | ~2 cm deep |
| corner vents | 75-140, 490-560 | +17.6..+14 | 0.4 -> 4.3 | - | slots |

Both sockets are on the lower back face (35.3 cm from the front), below the overhang (rear line at
39.9). A C13 plug with strain relief is ~5.8 cm long; from a socket face 1 cm inside the pocket it ends
~0.2 cm past the rear line before the cord bends down. USB-B plug + relief ~4.5 cm: ends inside the
outline. So the printer can stand with the scanner overhang ~1-2 cm from the wall (the squashed
cords), the user's "concave" case.

## Moving parts

* Cassette: pulled straight out to the front (manual: "Pull the paper tray completely out"). Modelled
  34.5 cm long; refill state slides it 30 cm forward.
* Support flap: hinged at its front edge (z 18.8, 1.4 cm behind the front face); printing state flips it
  up and forward 125 deg (manual step 7, drawing 93).
* Scanner lid: hinges at the back, pivot ~1 cm in from the rear at z 25.9; opens ~80 deg (photo 13).
* Back cover (static here): hinged at its bottom edge, opens down for jams and the face-up exit.

## Colours (sRGB, matte unless noted)

| part | hex | note |
|---|---|---|
| lower body, cassette, front cover | #4c4e51 | dark grey, fine texture |
| output floor | #5a5d60 | lighter textured grey (photo 12) |
| scanner unit band, panel front band | #1e1f21 | near black |
| lid top | #26272a | charcoal, slight sheen (rough 0.42) |
| panel top face | #2f3236 | blue-grey textured |
| panel lower band, upper side band | #6b6e72 | lighter grey trim (photos 01, 11) |
| logo | #b8babc | silver |
| LCD | #9cc1d6 | backlit pale blue |
| Start / Stop bars | #2fbf4f / #d23a3a | |
| USB/LAN plate | #a9acb2 | light grey |
| rear lever | #3cbf4c | green |
| feet | #111111 | rubber |

## Model status

* Round 1 (17 Nov 2026, sheets `work/compare/brother-dcp-l2620dw/round1.png`, `round1b.png`): the first draft
  compared with photos 01, 02, 03, 04, 11, 12 and the side outline 91. Differences found: body colour too light;
  front cover top was a sharp box (photos: big rounded front-top edge and rounded top corners); the paper exit was a
  shallow flat light-grey floor (photos: a dark well, 29.7 cm wide, X -16.5..+13.2); the scanner unit was all black
  (photos and outline: black frame only above z 23.4, a body-grey base below it down to z 20.5); the rear had no
  "ears" and the upper rear block was a plain box; the side walls did not flare under the scanner; socket positions
  and the camera distance of the back photo were off (see the corrected Back section). Builder rewritten.
* Rounds 2-3 (17 Nov 2026, earlier helpers): sheets `round2*.png`, `round3*.png`; builder brought to the
  current shape (rounded front cover, dark exit well, grey scanner base under a black frame, rear ears,
  side grips and vents, panel with keys).
* Round 4 (17 Nov 2026, sheets `round4.png` for back / 3/4 right / front-high and `round4_states.png` for
  printing, refill, lid open and cables): no big differences left in silhouette, panel, seams or port
  positions. No new photos added: back, front and top were already covered; the unsorted candidates in
  `work/photo_candidates/brother-dcp-l2620dw/` add no new view (no straight side, bottom or top exists
  online, per `work/photos_wanted.md`).
* Cables checked again: side outline 91 puts the lower back at 35.5 cm from the front and the overhang
  block at 39.9 cm (4.4 cm overhang, its underside at z 14.0); both sockets are below it. Back photo 03:
  the C14 inlet sits in a pocket (shadow on its side, ~1 cm), the USB-B at the bottom of a shallow channel
  (~0.6 cm). Plug recesses set to 1.0 / 0.6 cm; the power plug's bent cord reaches 1.4 cm past the rear
  line, the USB cord stays inside it. specs.json `behind_body_cm` = 1.4.
* Final build: closed 41.0 x 39.9 x 27.2 cm (exact); printing D 42.4 (support flap flipped out); refill
  D 69.9 (cassette 30 cm out); lid_open H 58.7 (lid raised 80 deg about its rear hinge, as photo 13
  suggests; Brother publishes no lid-open height). 13.2k triangles, 0.59 MB.
* Still differs / modelled without a photo: left and right sides from the 3/4 photos and the outline only
  (no straight side photo); bottom plain; lid-open angle estimated; lid and frame read slightly lighter
  than the glossy black in the studio photos.
