# Design language: the "Size Lab" look

This describes the visual and interaction design of Printers Size Lab
(https://nadavm-eng.github.io/printers-size-lab/) so another app can be built to match it. It is written
to be handed to an AI assistant or a developer as is. The reference implementation is one file,
`docs/index.html`.

## The idea in one paragraph

A calm measuring instrument, not a shop. Warm off-white paper in light mode and warm charcoal in dark
mode; one typeface; hairline borders instead of shadows; everything interactive is a pill; cards have one
radius. Colour is reserved for meaning: orange-red is always thing A, blue is always thing B, green is
the single accent for "on" and for the primary action. Numbers are the heroes: large, tabular, with a
small muted unit. Text is short, plain and honest.

## Tokens

Define these as CSS custom properties on `:root`. Support light, dark (via
`prefers-color-scheme`), and a manual override with `data-theme="light|dark"` on `<html>`.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--page` | `#e8e6e1` | `#1b1b1a` | page background |
| `--surface` | `#f4f3ef` | `#262624` | cards, bars, pills, menus |
| `--well` | `#dedcd6` | `#1f1f1e` | recessed areas: segmented-control track, hover rows, bar tracks |
| `--line` | `#d3d1ca` | `#3a3936` | 1px borders and dividers |
| `--line-strong` | `#bebcb4` | `#4a4945` | hover borders, dashed drop zones |
| `--ink` | `#1d1d1b` | `#ecebe6` | primary text |
| `--ink-2` | `#3d3c38` | `#cfcdc6` | secondary text, long-form text |
| `--muted` | `#66655f` | `#a6a49c` | labels, units, captions |
| `--on-ink` | `#f4f3ef` | `#1b1b1a` | text on an ink-filled control |
| `--viewer` | `#f4f3ef` | `#2c2c2a` | background of the 3D or main canvas panel |
| `--accent` | `#3f8f4f` | `#5fae6e` | focus ring, "on" indicator, links to act on |
| `--accent-fill` | `#367d45` | `#5fae6e` | filled primary button, selected preset |
| `--on-accent` | `#ffffff` | `#1b1b1a` | text on accent fill |
| `--sig-a` | `#d4542b` | `#e8714a` | item A, and warnings |
| `--sig-b` | `#2f6f9f` | `#5b9bd0` | item B |

Shadow: almost none. One soft bar shadow, `0 1px 2px rgba(40,38,30,.05), 0 6px 18px rgba(40,38,30,.05)`
in light and `0 1px 2px rgba(0,0,0,.25)` in dark, used only on the floating control bar and menus.
Everything else is separated by a 1px `--line` border.

## Typography

- One family: **Archivo** (Google Fonts, weights 400, 500, 700), falling back to
  `system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.
- `font-variant-numeric: tabular-nums` on the whole page, so numbers line up.
- Weight 500 is the "bold" of this design. 700 is used only inside a sentence to name a winner, and in
  the tiny A / B badges.
- Sizes:

| Role | Size / line | Weight | Notes |
|---|---|---|---|
| App title | 22 / 1.2 | 500 | letter-spacing −0.01em |
| Section heading | 20 / 1.2 | 500 | letter-spacing −0.01em |
| Selected item name | 22 / 1.25 | 500 | ellipsis on overflow |
| Hero number | 30 / 1.1 | 500 | letter-spacing −0.02em; unit follows at 15, weight 400, `--muted` |
| Body | 15 / 1.5 | 400 | |
| Control label | 14 | 500 | |
| Meta, captions | 13 | 400 | `--muted` |
| Fine print, notes | 12.5 | 400 | `--muted` |

- Sentence case everywhere. No all-caps, no letter-spaced labels.

## Shape and spacing

- Page: content column max 1232px, centred, 16px side gutters (respect safe-area insets), 64px bottom.
- Radii: **14px** for cards and panels (12px under 640px wide); **999px** (full pill) for every button,
  toggle, chip, select and segmented control; 10–12px for small message boxes and list rows.
- Spacing steps: 4, 6, 8, 12, 16, 20, 24, then 40 and 56 between major sections.
- Control heights: 40px pills and icon buttons, 34px buttons inside a segmented control, 44px for the
  large "show all" disclosure.
- Borders are 1px `--line`; a border darkens to `--line-strong` on hover (150ms).

## Components

- **Item picker card.** A surface card with a 36px round badge filled with the item's signal colour and
  a white letter, the item name (22/500), one meta line (13, muted), and a small chevron at the right.
  Open state: the border takes the item's colour. The menu is a surface panel, radius 14, 6px padding,
  rows with 10px radius that fill with `--well` on hover, group captions at 12px muted, a green check on
  the selected row. An "empty" badge is an outline ring instead of a fill.
- **Segmented control.** A pill track filled with `--well`, 3px padding; buttons are text only,
  14/500 `--muted`; the pressed one is a `--surface` pill with a hairline ring and `--ink` text. The
  one top-level mode switch uses the stronger variant: surface track with a hairline, pressed button
  filled with `--ink` and `--on-ink` text.
- **Toggle pill.** Outline pill with an 8px dot before the label: dot is `--line-strong` when off and
  `--accent` when on. The pill itself does not fill.
- **Choice pill** (one of several, such as camera presets). Outline pill; the chosen one fills with
  `--accent-fill` and `--on-accent` text.
- **Primary action.** A pill filled with `--accent-fill`, optional 16px line icon. One per screen.
- **Icon button.** 40px circle, surface fill, hairline border.
- **Destructive affordance.** A small red × in `--sig-a` at the right end of a row, with an
  "Undo" message for a few seconds instead of a confirmation dialog.
- **Control bar.** Groups of the controls above inside one surface bar with a hairline border, 10px
  padding and the bar shadow; fully rounded when it fits on one line, 16–20px radius when it wraps.
- **Main panel (viewer).** Fills the column, about 74vh tall (min 380px), radius 14, `--viewer`
  background, an inset hairline instead of a border. Overlays sit in its corners: legend chips top
  left, view name top right, a quiet hint bottom right, status messages bottom left.
- **Label chip** (floating value on the canvas). A small pill, 12.5/500, surface-coloured fill and a
  1.5px border in the colour of the thing it measures; the tag letter before the value is muted. The
  one headline value is the "strong" variant: filled with the signal colour, white text.
- **Status message.** Surface box, radius 10, 13px text, hairline ring. Warning variant: a 1.5px
  `--sig-a` ring and a 16px round `--sig-a` badge with "!". Loading variant: a 3px progress bar inside.
- **Comparison tile.** Surface card, radius 14, 22–24px padding. A muted 14/500 label, then one block
  per item: a 10px colour dot, the hero number with its unit, the item name in 13 muted, and a 6px
  rounded track in `--well` with a bar in the item's colour. A hairline divider, then one plain
  sentence stating the difference with the winner's name in bold ("**X** costs ₪50 more."), or a muted
  "About the same". Three columns, two under 980px, one under 640px.
- **Spec table.** Inside a surface card: a label column (200px, 14 muted) and one column per item;
  rows divided by hairlines, 14px vertical padding. A value may carry a 12.5 muted note beneath it.
  Long detail goes in a **"More" disclosure**: a small muted summary with a chevron that opens
  justified 13px paragraphs, with 500-weight inline labels and bullet lists.
- **Slider.** 4px track, filled with `--accent-fill` up to the thumb; 20px round thumb in `--surface`
  with a 1.5px `--ink-2` border and a soft shadow. Label left in muted 14/500, value right in 500 with
  a small muted hint after it.
- **Side sheet.** Slides in from the right for secondary tasks, numbered steps inside, closes with
  Escape and returns focus to its opener.
- **Drop zone.** 1.5px dashed `--line-strong`, radius 14, centred 14px text; on drag-over the border
  turns `--accent` and the fill becomes a 10% accent tint.
- **Drag handle on the canvas.** A small round surface chip with an accent ring and a direction arrow;
  it grows on hover, fills with `--accent-fill` while dragging and shows the live value beside it.
- **Links.** Inherit the text colour, 1px underline in `--line-strong`, 3px offset; the underline takes
  the text colour on hover. Never blue.
- **Focus.** `outline: 2px solid var(--accent); outline-offset: 2px` on everything focusable.

## Colour rules

- A and B keep their colours everywhere: badge, legend chip, outline box, label chips, dots, bars.
- The second item, when shown inside or over the first, is a "ghost": its signal colour at about 11–20%
  opacity, with no depth writing.
- Green means "on" or "do this". Orange-red also flags a problem, so a warning value is written in
  `--sig-a` at weight 500.
- Never rely on colour alone: pair it with a letter (A, B), a label, or an icon.

## The 3D canvas (if the app has one)

- three.js, `NeutralToneMapping`, exposure about 0.95, a soft room environment at low intensity, one
  hemisphere light and one key directional light with soft shadows.
- Scenery is quiet and generic: matte, low-saturation, warm greys and wood, so the subject stands out.
- Measurements are drawn like a technical drawing: thin dimension lines with extension lines and 45°
  ticks, dashed bounding boxes in the item's colour, values in label chips.
- Camera moves are eased over about 750ms; parts animate over about 520ms; both stop instantly under
  `prefers-reduced-motion`.

## Motion

- 150ms for hover and border changes, 200ms for chevrons, 400ms for bar widths.
- Ease-in-out cubic for anything that travels. No bounces, no parallax, no decorative animation.
- `@media (prefers-reduced-motion: reduce)` turns all transitions and animations off.

## Writing

- Sentence case. Short labels of one to three words: "Sizes", "Cables", "Adding paper".
- State facts with a number and a unit: "Sticks out 7.0 cm", "148 cm from the floor, 11 cm below your
  eyes". Say "About the same" when a difference is too small to matter.
- Be honest about uncertainty, in plain words: "Not enough evidence", "estimated", "you measured about
  3.5 cm".
- No exclamation marks, no marketing words, no emoji.
- Errors say what is wrong and what to do: "Part 'lid' has no pivot."

## Responsive

- Under 980px: tiles go to two columns; the control bar wraps and takes a 20px radius.
- Under 640px: one column; pickers stack; cards take a 12px radius; segmented controls and toggle
  groups stretch to full width; secondary corner text on the canvas is hidden; the table's label
  becomes a full-width line above its values. No horizontal scrolling at 375px.

## Starter CSS

```css
:root{
  --page:#e8e6e1;--surface:#f4f3ef;--well:#dedcd6;--line:#d3d1ca;--line-strong:#bebcb4;
  --ink:#1d1d1b;--ink-2:#3d3c38;--muted:#66655f;--viewer:#f4f3ef;--on-ink:#f4f3ef;
  --accent:#3f8f4f;--accent-fill:#367d45;--on-accent:#fff;--sig-a:#d4542b;--sig-b:#2f6f9f;
  --bar-shadow:0 1px 2px rgba(40,38,30,.05),0 6px 18px rgba(40,38,30,.05);
  --font:"Archivo",system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  color-scheme:light;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --page:#1b1b1a;--surface:#262624;--well:#1f1f1e;--line:#3a3936;--line-strong:#4a4945;
    --ink:#ecebe6;--ink-2:#cfcdc6;--muted:#a6a49c;--viewer:#2c2c2a;--on-ink:#1b1b1a;
    --accent:#5fae6e;--accent-fill:#5fae6e;--on-accent:#1b1b1a;--sig-a:#e8714a;--sig-b:#5b9bd0;
    --bar-shadow:0 1px 2px rgba(0,0,0,.25);color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --page:#1b1b1a;--surface:#262624;--well:#1f1f1e;--line:#3a3936;--line-strong:#4a4945;
  --ink:#ecebe6;--ink-2:#cfcdc6;--muted:#a6a49c;--viewer:#2c2c2a;--on-ink:#1b1b1a;
  --accent:#5fae6e;--accent-fill:#5fae6e;--on-accent:#1b1b1a;--sig-a:#e8714a;--sig-b:#5b9bd0;
  --bar-shadow:0 1px 2px rgba(0,0,0,.25);color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);font:400 15px/1.5 var(--font);font-variant-numeric:tabular-nums}
button,select{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:3px;text-decoration-color:var(--line-strong)}
.app{max-width:1232px;margin:0 auto;padding:0 16px 64px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px}
.pill{height:40px;padding:0 14px;border:1px solid var(--line);border-radius:999px;background:transparent;
  font-size:14px;font-weight:500;display:inline-flex;align-items:center;gap:8px;cursor:pointer;transition:border-color .15s}
.pill:hover{border-color:var(--line-strong)}
.pill.primary{background:var(--accent-fill);border-color:var(--accent-fill);color:var(--on-accent)}
.seg{display:flex;padding:3px;border-radius:999px;background:var(--well)}
.seg button{border:0;background:transparent;border-radius:999px;height:34px;padding:0 14px;font-size:14px;font-weight:500;color:var(--muted);cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--surface);color:var(--ink);box-shadow:0 0 0 1px var(--line),0 1px 2px rgba(0,0,0,.06)}
.big{font:500 30px/1.1 var(--font);letter-spacing:-.02em}
.big small{font-size:15px;font-weight:400;color:var(--muted);margin-left:4px;letter-spacing:0}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}
```
