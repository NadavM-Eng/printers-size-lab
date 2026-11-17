# HP Officejet J4580 All-in-One (CB780A): measurements

The user's current printer. Every number in `build/builders/hp_officejet_j4580.py` comes from this file.
Frame used below: **u** = cm from the left edge seen from the FRONT (unless marked "from behind"),
**d** = cm from the back face toward the front, **z** = cm above the shelf (bottom of the feet).
In the builder: x = u - 21.675, y = 13.8 - d, z = z.

## Photo index

Photos live in `printers/HP OfficeJet J4580 (current printer)/photos/`. Checked one by one.

| File | View | What it shows | Source |
|---|---|---|---|
| 01_mfr_34fl_tray_out | 3/4 front-left | HP stock photo, main tray + extender out; panel reads "HP Officejet J4580 All-in-One" | eBay listing 403017501189 |
| 02_ne_front_closed | front | straight front, tray pushed in (closed) | Newegg N82E16828115212 (-22) |
| 03_ne_back | back | straight back: ports, label CB780A, rear notch | Newegg (-23) |
| 04_ne_right_tray_out | right | right side from above, tray + extender + stop out | Newegg (-13) |
| 05_ne_left_tray_out | left | left side, slightly from above, tray + extender + stop out | Newegg (-17) |
| 06_ne_34fl_tray_out | 3/4 front-left | tray out | Newegg (-12) |
| 07_ne_34br | 3/4 back-right | back, ports, rear notch, right side | Newegg (-14) |
| 08_ne_back_high | back | back from slightly above | Newegg (-15) |
| 09_ne_34bl | 3/4 back-left | ports near the left-rear corner, left side | Newegg (-16) |
| 10_ne_34fr_tray_out | 3/4 front-right | tray out | Newegg (-18) |
| 11_ne_front_tray_out | front (high) | tray + extender out | Newegg (-19) |
| 12_ne_lid_open | 3/4 front-left | scanner lid + ADF raised ~75-80 deg, glass | Newegg (-20) |
| 13_ne_top | top | from above, front at the bottom | Newegg (-21) |
| 14_ne_panel | detail | control panel, "HP Officejet J4580 All-in-One" | Newegg (-24) |
| 15_ne_front_door_open | front | front access door folded down, carriage | Newegg (-25) |
| 16_ne_in_box | detail | US box: power brick with purple DC plug, AC cord, phone cord + adapter, HP 901 cartridges | Newegg (-26) |
| 17_ne_ports_closeup | detail | crop of 03: USB-B, purple 3-pin DC socket "32V 600mA", RJ11 LINE/EXT | Newegg (-23) |
| 18_ne_ports_from_right | detail | crop of 07: port panel and the rear notch wall | Newegg (-14) |
| 19_ne_ports_from_left | detail | crop of 09: shallow framed port panel, rear-left corner | Newegg (-16) |
| 20_user_front_shelf | front | the user's unit on the shelf, near straight; A4 hangs over the shelf edge | user `ba8c6871` |
| 21_user_front_shelf_low | front | same, from lower left | user `a594e63f` |
| 22_user_34fl_shelf | 3/4 front-left | user's unit: left side, control panel overhang, tray pulled out a little | user `5ece6f62` |
| 23_user_overhang_ruler | detail | ruler from the shelf edge to the front-bottom corner of the base | user `347d274e` |
| 24_user_back_gap_ruler | detail | ruler from the wall to the back of the base; black DC plug and white USB cable | user `5bdec08b` |
| 25_user_from_below | detail | from below: underside of the base and of the pulled-out tray past the shelf edge | user `92364d39` |
| 26_user_niche, 27_user_niche_portrait | shelf_wide | wide shots of the shelf | user `b0e6bccc`, `6e932a0f` |
| 28_alo_front_tray_out | front (high) | a used J4580, tray out | alo.bg listing 10668101 |
| 29_alo_ports_closeup | detail | real unit's port panel (rotated): USB-B in a small raised collar, purple DC socket, RJ11 pair | alo.bg listing 10668101 |

Count by view: front 5, back 2, left 1, right 1, 3/4 front 4, 3/4 back 2, top 1, lid open 1, details
(panel, door, box, ports x5, rulers x2, below) 10, wide shots 2. 29 in total, 8 of them the user's own.

## What HP's size includes

HP (user guide p.156, RS datasheet, Officejet 4500 sheet which repeats it as "minimum dimensions"):
**433.5 x 401.5 x 216.7 mm**, 5.9 kg. HP does not say what the depth includes, and the closed printer is
much shallower:

- User, on the 24.5 cm shelf: the base sticks out ~3.5 cm past the shelf edge, the back is 4.5 cm from the wall
  (cables) -> **base 23.5 cm** (24.5 - 4.5 + 3.5). Reading the ruler photos again: the ruler's end, not its
  0 mark, touches the shelf edge in `347d274e` (0 mark is ~1.0 cm in), so the base could be up to ~24.5.
- Newegg left side (05), scaled by the scanner seam (12.8 cm, from the back view): base 24.3-24.7 cm.
- The flatbed glass (Letter/A4, 21.6 cm front-to-back plus frame) needs >= 24.5 cm for the scanner unit.

Used (2026-11-17, the user's shelf numbers outrank the photo scales): **base 23.5 cm** at shelf level, scanner
front 23.8, lid/feeder front 24.0-24.1, control panel front edge **27.0 cm**.

### Why 27.0 and not 27.6 (the closed depth)

Nothing else sticks out in front of the base when the tray is pushed in: the main tray lip is flush with the
base front, the feeder and lid are only 0.3-0.6 cm ahead of it, and the only real overhang is the control
panel wedge on the left half (u 0-22). Its front-most point is the cream lip under the dark keypad face,
d 27.0 at z 10.3-11.6 (about 10.5 cm above the shelf; the panel's underside is flat at z 10.3).

The panel's reach comes from the straight side photo 05 (702 x 348 px). Pixel rows of the silhouette:
back plane x = 7, base front x = 355 (vertical from the feet to the tray), panel tip x = 406-407,
lid front x = 363, feeder top front x = 364. Panel / base = 400 / 348 = **1.149**, lid 1.023, feeder 1.026.
Both points lie on the near (left) side plane, so the ratio is free of perspective.

- With the user's base of 23.5 cm: panel 27.0 cm, overhang of the panel past the base 3.5 cm.
- The old 27.6 cm came from the same ratio times an older base estimate of 24.0 cm (side photo scaled by the
  scanner seam). Getting 27.6 with a 23.5 cm base would need the panel 4.1 cm ahead of the base, 22 px more
  than photo 05 shows, so 27.6 is dropped. `specs.json` closed depth is now 270 mm.

On the shelf (24.5 cm deep, back 4.5 cm from the wall): base 3.5 cm past the edge at shelf level; the panel
7.0 cm past the edge, but 10.3 cm above the shelf.

Scale for the side photo 05: 348 px = 23.5 cm -> 14.8 px/cm.

With that scale (05, 04): main tray front lip at d = 35.8 (tray slides out 11.8 cm), tray extender end at
d = 43.2 (extender +7.4), raised paper stop tip at d = 47.7. HP's 40.15 cm lies between "tray out" and
"tray + extender fully out", so HP's depth is with the main tray pulled out (most likely with the extender
partly out). The closed state in the model is tray pushed in: **43.35 x 27.0 x 21.67** (tray distances above were scaled with the old 24.0 base; with 23.5 they are ~2% shorter, within the photo error).

## Front (02, straight, 15.85 px/cm from the width 688 px = 43.35 cm)

- Width 43.35 at the control panel / scanner level, 43.3 at the base (rounded vertical corners r ~1.5).
- Lower body cream. Dark front access door from u = 7.0 to 43.35, z = 4.3 to 15.3; its lower-left corner is
  rounded r ~2.5; on the right it wraps around the front-right corner onto the right side (d 21.6-24, z 4-13,
  from 04).
- Paper opening (output slot over the main tray): u 10.4-33.6, z 1.2-6.3, rollers at its top (z 5.0-6.3).
  Main tray front lip visible in it at z 1.2-2.6. Two small dark latch holes at u 9.4-10.2 and 33.8-34.6,
  z 1.5-2.6.
- Control panel: u 0-21.8 (right end rounded r ~2 in plan and front), dark glossy face z 11.8-15.0 above a cream
  lip z 10.5-11.8 that wraps around the right end. Power button (round, yellow ring) u 1.1 z 13.0; 3x4 keypad
  u 2.2-6.8 z 12.3-14.8; LCD u 7.8-14.2 z 13.6-14.6 (2 lines); function icons z 12.5-13.2 under it; arrows/OK
  u 15.8-19.0 z 14.3-14.9; back u 15.4 z 13.9; cancel (red X) u 15.9 z 13.1; Start (blue square) u 16.8-18.6
  z 12.9-13.9; setup (wrench) u 20.2 z 14.8. Label "HP Officejet J4580 All-in-One" above the LCD.
- Document feeder (dark) on the left of the top: u 0.6-17.5 at the top, 19.5 at its foot (sloped right side);
  front face z 15.4-21.2, top-left edge rounded r ~2. HP badge (silver, rounded) u 7.8-9.9, z 17.9-19.0.
- Feeder input tray (light grey, now cream) on the right of the top: u 16.5-37.5; front edge z ~18.3 for
  u 22-37.5, curving up into the feeder at u 16.5-22 (z up to ~21).
- Scanner lid (right part) front edge z 15.4-16.1, lighter grip strip u 36.5-43.3.
- Energy Star sticker on the base front u 1.6-3.4, z 1.8-3.7.

## Back (03, straight, 15.87 px/cm; positions from behind converted: u = 43.35 - u_behind)

- Feet (dark grey) u_behind 1.3-2.9 and 38.8-40.8, 0.4 tall.
- Seam between the cream base and the dark scanner: z 12.8 (side view 05 gives 12.5).
- Scanner back (dark) z 12.8-15.6; a recessed dark hinge bar u_behind 8.5-36.3 (u 7.1-34.9), z 13.6-14.8.
- Feeder body seen from behind on the right: u_behind 26.5-43.35, top z 21.3 sloping to 20.8.
- Feeder tray seen from behind: u_behind 5.3-28 (u 15.4-38.1), top z 17.6-18.3, ramping up to ~20.8 into the feeder.
- **Rear notch** (paper path, recessed, dark rollers inside): u_behind 5.2-33.0 (u 10.4-38.2), z 0.6-7.5,
  top corners rounded r ~1.5; about 3.5 cm deep (07, 09).
- Label "CB780A / Product of China" u_behind 18.6-25.3, z 8.5-10.4.
- **Port panel** (framed, ~0.3 cm deep): u_behind 29.5-40.8 (u 2.6-13.9), z 8.3-10.6.
  - USB-B: centre u_behind **31.3**, z **9.4** (u 12.05) - flush, in a small raised collar (29).
  - Power (HP purple 3-pin DC socket, "32V 600mA"): centre u_behind **33.9**, z **9.4** (u 9.45) - flush.
  - RJ11 1-LINE / 2-EXT: centre u_behind 38.6, z 9.5 (u 4.75), 3.2 x 1.3 cm.
- Rear-bottom edge rounded r ~2.5 (05); rear vertical corners r ~1.5 (09).

## Side profile (05 left, 04 right; d from the back)

| d | top of the dark scanner/feeder side | notes |
|---|---|---|
| 0 | 12.8 -> 18.8 (rounded rear-top r ~2.5) | back face |
| 2 | 21.0 | feeder top (left side) |
| 4-22 | 21.4-21.67 | feeder top, nearly flat; official max 21.67 |
| 24.0-24.1 | 21.0 -> 15.4 | lid / feeder front face, top-front edge r ~1.5 |
| 23.5-23.7 | 0.4 -> 12.8 | base front face (nearly vertical); scanner base 23.8 |
| 24.4-27.0 | 10.3 -> 15.25 | control panel wedge: face from (24.4, 15.25) to (26.9, 11.6), front edge 27.0 at z 10.7, flat underside at z 10.3 |

- Right part of the top: lid at z 16.1, feeder tray plate at z ~18.0 spanning d 2-23.8, with a dark window
  ~9 x 9 cm (u 24-33, d 7-16) and two white paper guides at d 4.5 and 21.5 (04, 13).
- Both sides have a shallow rectangular recessed panel (d 2-18.5, z 1-10, rounded corners) (05, 04, 5ece6f62).

## Moving parts

- **cassette** (main tray, slides straight out of the front): u 9.6-34.6 (24.4 wide... 25 with the walls),
  floor z ~1.2-1.8, low left wall (to z 3.3), taller right wall (to z 4.0), front lip z 1.2-3.0; 22 cm long.
  Closed: front flush with the base front (d 24.0). Out: +11.8 cm (lip at d 35.8).
- **extender** (slides out of the main tray): ~15 cm wide, thin plate with side rails; +7.4 cm beyond the tray
  (end at d 43.2).
- **flap** (paper stop, hinged at the extender's front end): 13 x 4.5 cm; folded flat back over the extender
  when closed, raised to point forward-up ~25 deg when printing (tip at d 47.7, from 05).
- **lid** (scanner lid with the whole document feeder and its tray), hinged at the back top of the scanner
  (d ~1.0, z ~15.6), opens ~75 deg (12).

States: printing = tray out + extender out + stop raised; refill = tray out (load paper); lid_open = lid up.

## Cables (user rule: recessed 1-2 cm, flat 5-8 cm)

Both used sockets are on the almost flat back (panel only ~0.3 cm deep), so the plugs stick out fully:
USB-B plug ~3.8 cm with strain relief, the HP DC plug ~3 cm. The user measured **4.5 cm** from the wall to the
back (24_user_back_gap_ruler: body edge at 3.3 on the scale + 1.2 cm from the ruler end to its 0 mark). The
builder uses a USB-B plug of 2.6 + 1.2 cm (compact moulded plug) so the squashed cable lands at ~4.5 cm.

## Colours (user's unit, white-balanced on the A4 paper in `ba8c6871` / `5ece6f62`)

| Part | sRGB | Finish |
|---|---|---|
| Base, lid edges, panel lip (aged light grey, now cream) | #dccfa6 | satin plastic, rough 0.55 |
| Main tray / extender (more yellowed) | #d9c39a | satin |
| Feeder tray | #d6c8a0 | satin |
| Scanner, feeder, front door (dark slate) | #2d3034 | satin, rough 0.45 |
| Control panel face | #1f2226 | gloss, rough 0.25 |
| LCD | #8f9a6e, lit | emit |
| Start button | #4b8fb5 | |
| Feet, rollers | #1a1a1a | |
| Purple DC socket | #8a3d8f | |
| HP badge | #c9cacc | metal |

(New units are light grey #e4e5e3; the user's has yellowed, so the model uses the yellowed colours.)

## Model status (2026-11-17)

- Size: 43.35 x 27.0 x 21.67 cm closed (= specs.json closed, HP's W and H). Base 23.5 cm deep at the shelf.
  Printing (tray + extender out, stop up) 47.5 cm deep; refill (tray out) 35.3; lid open 38.8 cm high, 32.8 deep.
- Cables: USB-B and the HP DC plug go into a flat back (0.3 cm panel): reach 4.5 cm behind the back plane,
  matching the user's measured wall gap; `cable_space.behind_body_cm` = 4.5.
- Photos: none added (back, front, top, sides and the user's ruler shots already covered). No web search.
- Rounds: 3 (`work/compare/hp-officejet-j4580/round1.png` all views, `round2.png` side + printing + back
  cables, `round3.png` side + 3/4 after the fixes). Fixed: base/lid/feeder/panel depths from photo 05;
  the panel's left end is dark above the cream lip.
- Still differs: the owner's unit is more yellowed than the model; the front-door wrap and the side
  recesses are approximate; the sticker on the scanner lid of the stock photos is left out.
- Modelled without a photo: the underside (plain, four feet; front feet from the user's photo from below)
  and the inside of the rear notch beyond what photos 07 and 09 show.
