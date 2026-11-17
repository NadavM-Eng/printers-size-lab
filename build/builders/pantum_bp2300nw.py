"""
Pantum BP2300NW (mono laser, print only, USB + Ethernet + Wi-Fi).

Every number traces back to printers/Pantum BP2300NW/measurements/MEASUREMENTS.md:
official 337 x 220 x 179 mm; front photo 02 scaled at 15.3 px/cm, side photo 19 (sister BP2300) at
31.5 px/cm, top photo 05 at 15.6 px/cm; back layout from the official BP2300 Series User Guide
rear-view drawing (14) and the sister BP2300W port close-up (12).

Frame: cm, Z up, FRONT = -Y, BACK = +Y, x = 0 centre of the width, y = 0 centre of the depth,
z = 0 under the feet.

Moving parts
- input_tray:  the whole front door is the feeder tray; hinge along its bottom edge, folds 90 deg forward
               and lies on the shelf (reaches 15 cm in front of the body).
- paper_stop:  light-blue paper stop at the outer end of the open tray (hidden while the door is closed).
- paper:       A4 stack on the open tray (hidden; shown in the printing state, as in photos 07-09).
- output_tray: flap that covers the output bin in the top; hinge along its front edge, flips 163 deg
               forward and rests on the front edge of the top (reaches 12 cm in front, 22 cm high).
- output_stop: small stopper at the far end of the flap, raised when printing.
"""
import math
import sys

import numpy as np
from mathutils import Matrix, Vector

# the C14 inlet sits vertically (official rear drawing): plug face 1.6 wide x 2.2 tall
PLUGS["C13v"] = (1.6, 2.2, 3.4, 2.4, 0.75, 3.0)

# a white printer clips under the default render lights; the kit documents LIGHT_GAIN for this
# (affects only this process's comparison renders, not the GLB)
if "printer_kit" in sys.modules:
    sys.modules["printer_kit"].LIGHT_GAIN = 0.2

FLAP_DEG = 163.0          # output flap: closed (lying back) -> open (pointing forward, 17 deg above level)
STOP_DEG = 90.0           # stopper raised square to the flap


def _weighted_normals(ob):
    """Face-area weighted custom normals: big flat faces stay flat next to rounded corners
    (plain smooth shading bleeds the corner normals across the whole side panel)."""
    m = ob.modifiers.new("wn", "WEIGHTED_NORMAL")
    m.mode = "FACE_AREA"
    m.weight = 100
    m.keep_sharp = True
    deps = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(deps), preserve_all_data_layers=True, depsgraph=deps)
    old = ob.data
    ob.modifiers.clear()
    ob.data = me
    if old.users == 0:
        bpy.data.meshes.remove(old)


def _fit_text(ob, width, height, center, plan=False):
    """Scale a text3d object to width x height (cm) and move its centre to `center`.
    plan=False: text facing -y (size in x, z); plan=True: text lying flat facing +z (size in x, y)."""
    me = ob.data
    V = np.array([v.co for v in me.vertices], float) / 0.01
    lo, hi = V.min(0), V.max(0)
    c = (lo + hi) / 2
    k = 1 if plan else 2
    s = [1.0, 1.0, 1.0, 1.0]
    s[0] = width / max(hi[0] - lo[0], 1e-6)
    s[k] = height / max(hi[k] - lo[k], 1e-6)
    me.transform(Matrix.Translation(Vector(-c * 0.01)))
    me.transform(Matrix.Diagonal(s))
    me.transform(Matrix.Translation(Vector(np.asarray(center, float) * 0.01)))
    me.update()
    return ob


def _stroke_poly(pts, hw):
    """Outline polygon of a polyline drawn with a flat pen of half-width hw (mitred joints, butt ends)."""
    P = [np.asarray(p, float) for p in pts]
    left, right = [], []
    for i, p in enumerate(P):
        d0 = nrm(P[i] - P[i - 1]) if i > 0 else None
        d1 = nrm(P[i + 1] - P[i]) if i < len(P) - 1 else None
        if d0 is None or d1 is None:
            d = d1 if d0 is None else d0
            n = np.array([-d[1], d[0]])
            left.append(p + n * hw)
            right.append(p - n * hw)
            continue
        n0, n1 = np.array([-d0[1], d0[0]]), np.array([-d1[1], d1[0]])
        m = nrm(n0 + n1)
        k = 1.0 / max(float(np.dot(m, n0)), 0.2)
        turn = d0[0] * d1[1] - d0[1] * d1[0]          # > 0: the path turns left, so the outer side is the right
        if k > 1.5:                                   # sharp corner: flatten the outer side
            if turn > 0:
                left.append(p + m * hw * k)
                right.extend([p - n0 * hw, p - n1 * hw])
            else:
                left.extend([p + n0 * hw, p + n1 * hw])
                right.append(p - m * hw * k)
        else:
            left.append(p + m * hw * k)
            right.append(p - m * hw * k)
    return np.array(left + right[::-1])


# PANTUM logotype as pen strokes (wide geometric capitals, the A has no crossbar: photos 02 and 10).
# Each letter: (width, [polylines]) with x in 0..width and z in 0..1.
_LOGO = [
    (1.25, [[(0, 1), (0.95, 1), (1.25, 0.82), (1.25, 0.62), (0.95, 0.44), (0.3, 0.44)], [(0.1, 0.62), (0.1, 0)]]),   # P (open stem)
    (1.30, [[(0, 0), (0.65, 1), (1.3, 0)]]),                                                            # A
    (1.25, [[(0, 0), (0, 1), (1.25, 0), (1.25, 1)]]),                                                   # N
    (1.25, [[(0, 1), (1.25, 1)], [(0.625, 1), (0.625, 0)]]),                                            # T
    (1.25, [[(0, 1), (0, 0.26), (0.22, 0), (1.03, 0), (1.25, 0.26), (1.25, 1)]]),                       # U
    (1.30, [[(0, 0), (0, 1), (0.65, 0.05), (1.3, 1), (1.3, 0)]]),                                       # M
]


def _logo(name, mat, width, height, center, y_front, depth=0.03, pen=0.2, gap=0.14):
    """PANTUM logo facing -y: overall width x height (cm) centred at (x, z) = center."""
    total = sum(w for w, _ in _LOGO) + gap * (len(_LOGO) - 1)
    hw = pen * height / 2
    sx, sz = (width - 2 * hw) / total, height - 2 * hw
    x0, z0 = center[0] - width / 2 + hw, center[1] - height / 2 + hw
    objs = []
    cx = 0.0
    for w, lines in _LOGO:
        for line in lines:
            pts = [(x0 + (cx + u) * sx, z0 + v * sz) for u, v in line]
            objs.append(extrude(name, mat, _stroke_poly(pts, hw), "y", y_front, y_front + depth))
        cx += w + gap
    return join(objs, name)


def _band(cx, cy, r0, r1, a0, a1, n=14):
    """Closed polygon of a ring segment (for icon arcs)."""
    return np.concatenate([arc(cx, cy, r1, a0, a1, n), arc(cx, cy, r0, a1, a0, n)])


class Builder(Printer):
    W, D, H = 33.7, 22.0, 17.9

    # hinge of the output flap and of its stopper (closed positions), used by build() and states()
    FLAP_PIVOT = (0.0, -9.5, 17.7)
    STOP_PIVOT = (-0.8, 4.1, 17.33)
    DOOR_PIVOT = (0.0, -10.65, 0.4)

    def build(self):
        W, D, H = self.W, self.D, self.H
        hx, hy = W / 2, D / 2                      # 16.85, 11.0
        zb = 0.22                                  # underside of the body (feet below)
        z_band0, z_band1 = 15.75, 16.7             # black trim band
        z_lid0, z_lid1 = 16.7, H                   # lid (upper cover)
        y_rear = 10.68                             # rear panel between the corner pillars
        x_sl, x_sr = -13.3, 12.6                   # seams of the rear panel (pillars outside them)

        white = self.mat("body", "#eeeeec", 0.5)
        lidm = self.mat("lid", "#f1f1ef", 0.36)
        black = self.mat("band", "#1c1c1e", 0.22)
        notch = self.mat("notch", "#3a3a3d", 0.4)
        slot = self.mat("slot", "#161616", 0.7)
        roller = self.mat("roller", "#343436", 0.6)
        inner = self.mat("inner", "#e6e6e3", 0.55)
        blue = self.mat("blue", "#8fb0dc", 0.45)
        blue2 = self.mat("blue2", "#a9c4e8", 0.45)
        rubber = self.mat("rubber", "#2a2a2a", 0.9)
        logo = self.mat("logo", "#303032", 0.35)
        ring = self.mat("ring", "#9c9c9c", 0.4)
        plate = self.mat("plate", "#dededb", 0.45)
        sticker = self.mat("sticker", "#fbfbfb", 0.4)
        ink = self.mat("ink", "#111111", 0.5)
        metal = self.mat("metal", "#8d8d8d", 0.35, metal=0.8)
        paperm = self.mat("paper", "#f8f8f6", 0.6)
        led = self.mat("led", "#3ccf6a", 0.3, emit="#3ccf6a", emit_strength=3.0)
        font = find_font("DejaVuSans-Bold")

        def plan(x0, x1, y0, y1, rf, rb, n=8):
            # rounded plan rectangle: front corners (y0) radius rf, back corners (y1) radius rb
            return fillet([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], [rf, rf, rb, rb], n=n)

        # ---------------------------------------------------------------- body shell
        body = extrude("shell", white, plan(-hx, hx, -hy, hy, 2.0, 0.3, n=10), "z", zb, z_band0 + 0.03, bevel=0.22)
        # door pocket: the whole front panel between the pillars is the feeder door (inner wall at y = -9.6)
        cut(body, box("door_pocket", None, -14.15, 14.15, -hy - 1, -9.6, zb + 0.03, z_band0 + 0.5))
        # paper entry behind the door (the automatic feeder slot)
        cut(body, box("entry", None, -11.9, 11.9, -9.7, -6.5, 0.6, 3.9))
        # rear panel set 0.3 cm in between the two corner pillars (side photo 19: back at +10.68 above the pillars)
        cut(body, box("rear_recess", None, x_sl, x_sr, y_rear, hy + 1, zb - 1, z_band0 + 1))
        # pillars end at z 15.0 with a chamfer; above them the back is at the rear-panel plane
        cut(body, extrude("pillar_top", None, [(y_rear, 15.32), (hy + 0.02, 14.98), (hy + 1, 14.98),
                                               (hy + 1, 17.0), (y_rear, 17.0)], "x", -hx - 1, hx + 1))
        # scooped notch under each pillar (side photo 19, bottom back corner)
        scoop = fillet([(10.45, -1.0), (hy + 1, -1.0), (hy + 1, 1.75), (10.95, 1.75), (10.45, 1.15)],
                       [0, 0, 0, 0.3, 0.3], n=4)
        cut(body, extrude("scoop_r", None, scoop, "x", x_sr, hx + 1))
        cut(body, extrude("scoop_l", None, scoop, "x", -hx - 1, x_sl))
        # seam where the corner pillars meet the side panels (0.8 cm from the back, photos 04/21)
        for sx in (-1, 1):
            cut(body, box("side_seam", None, sx * hx - 0.05 - (1 if sx < 0 else 0), sx * hx + 0.05 + (1 if sx > 0 else 0),
                          10.14, 10.21, 1.9, 14.8))
        # vent grilles on the rear panel (two, upper half; official rear drawing)
        # each grille: 3 columns of 12 slots between the RJ45 and USB heights (real BP2300W back, photo 22)
        for xa, xb in ((1.1, 9.7), (-10.55, -1.95)):
            cw = (xb - xa - 0.6) / 3
            for c in range(3):
                x0 = xa + c * (cw + 0.3)
                for k in range(12):
                    z0 = 9.65 + k * 0.3
                    cut(body, box("vent", None, x0, x0 + cw, y_rear - 0.3, hy, z0, z0 + 0.15))
        # network + USB pocket in the corner pillar on the printer's right, 0.8 cm deep (photo 12)
        cut(body, extrude("port_pocket", None, rrect(2.0, 5.4, 0.35, cx=15.5, cy=11.2), "y", hy - 0.8, hy + 1))
        # power inlet frame, 0.5 cm deep, lower in the same pillar
        cut(body, extrude("pwr_pocket", None, rrect(2.0, 2.8, 0.25, cx=14.74, cy=3.1), "y", hy - 0.5, hy + 1))
        self.add("body", body)

        # inside of the door pocket: inner front panel with its own logo, dark back of the paper entry
        self.add("body", box("inner_panel", white, -12.9, 12.9, -9.8, -9.55, 4.3, 14.9, bevel=0.1))
        self.add("body", _logo("logo_in", logo, 5.8, 0.72, (0, 10.5), -9.83))
        self.add("body", box("entry_back", slot, -11.9, 11.9, -6.62, -6.5, 0.6, 3.9))
        self.add("body", box("entry_roof", slot, -11.9, 11.9, -9.55, -6.5, 3.84, 3.9))
        # light-blue feed (width) guides at both ends of the entry (photos 08/09)
        for sx in (-1, 1):
            self.add("body", box("guide", blue, sx * 10.75 - 0.2, sx * 10.75 + 0.2, -9.9, -8.0, 0.6, 3.0, bevel=0.05))

        # back details: label plate, RJ45 + USB sockets, C14 inlet
        self.add("body", box("rear_plate", plate, -6.1, 5.5, y_rear - 0.02, y_rear + 0.04, 1.2, 6.5, bevel=0.03))
        yp = hy - 0.8
        self.add("body", box("rj45_shell", metal, 14.7, 16.3, yp - 0.05, yp + 0.03, 12.2, 13.6))
        self.add("body", box("rj45_hole", slot, 14.85, 16.15, yp - 0.05, yp + 0.05, 12.35, 13.45))
        self.add("body", box("usb_shell", metal, 14.9, 16.1, yp - 0.05, yp + 0.03, 9.15, 10.25))
        self.add("body", box("usb_hole", slot, 15.0, 16.0, yp - 0.05, yp + 0.05, 9.25, 10.15))
        self.add("body", box("usb_tongue", inner, 15.2, 15.8, yp - 0.05, yp + 0.07, 9.5, 9.85))
        yq = hy - 0.5
        self.add("body", box("c14_inlet", slot, 13.94, 15.54, yq - 0.05, yq + 0.04, 1.95, 4.25, bevel=0.06))
        for dz in (-0.55, 0.0, 0.55):                                 # the three pins
            self.add("body", box("c14_pin", metal, 14.64, 14.84, yq - 0.05, yq + 0.07, 3.1 + dz - 0.2, 3.1 + dz + 0.2))
        # lid hinge tabs on the back, under the lid (rear drawing; black in the real BP2300W photo 22)
        for xc in (-11.9, 11.9):
            self.add("body", box("hinge", black, xc - 1.0, xc + 1.0, 10.3, 10.75, 15.6, z_lid0 + 0.1, bevel=0.08))

        # feet (front pair shows as small dark blocks under the pillars in photo 02)
        for sx in (-1, 1):
            for y0, y1 in ((-10.3, -8.8), (8.6, 10.1)):
                self.add("body", box("foot", rubber, sx * 14.72 - 0.62, sx * 14.72 + 0.62, y0, y1, 0.0, zb + 0.02))

        # ---------------------------------------------------------------- output bin under the flap
        # wedge: 0.45 deep at the front, 1.8 deep at the back where the paper comes out under the fixed strip
        bx0, bx1 = -11.6, 11.05

        def bin_cutter():
            return extrude("bin_cut", None, [(-9.6, H + 1), (-9.6, 17.2), (4.5, 15.85), (6.7, 15.85), (6.7, H + 1)],
                           "x", bx0, bx1)

        # ---------------------------------------------------------------- black trim band + grip
        band = extrude("band", black, plan(-hx + 0.25, hx - 0.25, -hy + 0.2, 10.4, 1.8, 0.3), "z",
                       z_band0 - 0.05, z_band1 + 0.02, bevel=0.05)
        cut(band, box("grip_cut", None, -2.8, 2.8, -hy - 1, -10.15, z_band0 - 0.1, z_band1 + 0.1))
        cut(band, bin_cutter())
        self.add("body", band)
        self.add("body", box("grip_back", notch, -2.8, 2.8, -10.2, -10.1, z_band0, z_band1))

        # ---------------------------------------------------------------- lid (upper cover)
        lid = extrude("lid", lidm, plan(-hx, hx, -hy + 0.1, hy - 0.25, 2.0, 2.0, n=10), "z",
                      z_lid0, z_lid1, bevel=0.25)
        cut(lid, bin_cutter())
        self.add("body", lid)
        # bin liner (floor + side walls), dark paper exit with rollers at the back, fixed strip over the exit
        self.add("body", extrude("bin_floor", lidm, [(-9.6, 17.2), (4.5, 15.85), (6.7, 15.85), (6.7, 15.9),
                                                     (4.5, 15.9), (-9.6, 17.25)], "x", bx0, bx1))
        for xa, xb in ((bx0, bx0 + 0.05), (bx1 - 0.05, bx1)):
            self.add("body", extrude("bin_wall", lidm, [(-9.6, 17.2), (4.5, 15.85), (6.7, 15.85), (6.7, 16.75),
                                                        (-9.6, 17.25)], "x", xa, xb))
        self.add("body", box("exit_back", slot, bx0, bx1, 5.9, 6.0, 15.9, 17.32))
        for xc in (-7.6, -2.6, 2.4, 7.2):
            self.add("body", cyl("exit_roller", roller, (xc, 5.5, 16.45), "x", 0.45, 2.2, seg=14))
        self.add("body", extrude("exit_strip", lidm, [(4.5, 17.32), (4.5, 17.5), (5.1, 17.7), (6.7, 17.7), (6.7, 17.32)],
                                 "x", bx0, bx1, bevel=0.05))

        # control panel: outlined strip with three buttons (Wi-Fi at the back, cancel, power at the front)
        zt = H
        self.add("body", extrude("panel_line", ring, rrect(2.58, 9.97, 0.4, cx=13.94, cy=-4.42), "z", zt - 0.02, zt + 0.004))
        self.add("body", extrude("panel", sticker, rrect(2.5, 9.89, 0.36, cx=13.94, cy=-4.42), "z", zt - 0.02, zt + 0.008))
        bx = 13.96
        for yc in (-3.2, -5.63, -8.05):
            for r, m, dz in ((0.74, ring, 0.012), (0.69, sticker, 0.016), (0.56, ring, 0.020), (0.52, sticker, 0.024)):
                self.add("body", cyl("btn", m, (bx, yc, zt + dz - 0.004), "z", r, 0.008, seg=40))
        zi0, zi1 = zt + 0.022, zt + 0.03
        # Wi-Fi icon: three arcs opening to the back + dot
        for r0, r1 in ((0.12, 0.19), (0.25, 0.32), (0.38, 0.45)):
            self.add("body", extrude("ic_wifi", ring, _band(bx, -3.42, r0, r1, 50, 130, n=8), "z", zi0, zi1))
        self.add("body", cyl("ic_wifi_dot", ring, (bx, -3.4, (zi0 + zi1) / 2), "z", 0.06, zi1 - zi0, seg=10))
        # cancel icon: X
        for a in (45, -45):
            c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
            L, h = 0.3, 0.035
            pts = [(bx + c * L - s * h, -5.63 + s * L + c * h), (bx - c * L - s * h, -5.63 - s * L + c * h),
                   (bx - c * L + s * h, -5.63 - s * L - c * h), (bx + c * L + s * h, -5.63 + s * L - c * h)]
            self.add("body", extrude("ic_x", ring, pts, "z", zi0, zi1))
        # power icon: open ring + bar
        self.add("body", extrude("ic_pwr", ring, _band(bx, -8.05, 0.24, 0.31, 120, 420, n=20), "z", zi0, zi1))
        self.add("body", box("ic_pwr_bar", ring, bx - 0.035, bx + 0.035, -8.02, -7.7, zi0, zi1))
        # status LEDs behind the buttons (2 x 2 dots in the manual drawings; one lit)
        for i, (dx, dy) in enumerate(((-0.3, 0), (0.3, 0), (-0.3, 0.6), (0.3, 0.6))):
            self.add("body", cyl("led", led if i == 0 else ring, (bx + dx, -1.55 + dy, zt + 0.012), "z", 0.07, 0.012, seg=10))
        # black model label at the back right of the lid (photos 09 and 13)
        self.add("body", extrude("model_label", ink, rrect(3.0, 0.8, 0.12, cx=14.1, cy=6.35), "z", zt - 0.01, zt + 0.012))
        lbl = text3d("model_txt", sticker, "BP2300NW", 0.5, (0, 0, 0), "+z", depth_cm=0.01, font=font)
        self.add("body", _fit_text(lbl, 2.4, 0.42, (14.1, 6.35, zt + 0.018), plan=True))

        # ---------------------------------------------------------------- output flap (moving)
        fp = self.FLAP_PIVOT
        flap = box("flap", lidm, -11.5, 10.95, fp[1], 4.4, 17.35, fp[2], bevel=0.08)
        cut(flap, box("flap_notch", None, -1.2, 1.2, 3.95, 4.6, 17.5, 17.8))
        self.add("output_tray", flap, kind="moving", pivot=fp)

        # stopper folded under the far end of the flap; raised square to the flap when printing (photos 09, 11)
        sp = self.STOP_PIVOT
        st = [box("stop_bar", lidm, sp[0] - 4.5, sp[0] + 4.5, sp[1] - 0.3, sp[1], sp[2] - 0.16, sp[2], bevel=0.04)]
        for k in range(4):
            x0 = sp[0] - 4.5 + k * 2.3
            st.append(box("stop_finger", lidm, x0, x0 + 2.1, sp[1] - 1.8, sp[1] - 0.2, sp[2] - 0.16, sp[2], bevel=0.06))
        self.add("output_stop", join(st, "output_stop"), kind="moving", pivot=sp)

        # ---------------------------------------------------------------- front door = feeder tray (moving)
        dz0, dz1 = 0.3, z_band0 - 0.07
        yi = -10.3                                  # inner face of the door
        door = box("door", white, -14.1, 14.1, -hy, yi, dz0, dz1, bevel=0.1)
        dparts = [door, _logo("logo", logo, 8.08, 0.98, (0.07, 11.9), -hy - 0.025)]
        # Wi-Fi Certified logo + setup logo, printed on the door (photo 10): 3.8 - 7.1 cm from the left edge
        yf = -hy
        dparts.append(extrude("st_line", ink, rrect(2.07, 0.95, 0.42, cx=-11.97, cy=14.47), "y", yf - 0.012, yf + 0.01))
        dparts.append(extrude("st_fi", sticker, rrect(1.97, 0.85, 0.37, cx=-11.97, cy=14.47), "y", yf - 0.016, yf + 0.01))
        dparts.append(extrude("st_wi", ink, fillet([(-13.0, 14.0), (-11.9, 14.0), (-11.7, 14.95), (-13.0, 14.95)],
                                                   [0.42, 0.0, 0.0, 0.42], n=6), "y", yf - 0.02, yf))
        t = text3d("st_wi_txt", sticker, "Wi", 0.5, (0, 0, 0), "-y", depth_cm=0.01, font=font)
        dparts.append(_fit_text(t, 0.8, 0.56, (-12.42, yf - 0.024, 14.47)))
        t = text3d("st_fi_txt", ink, "Fi", 0.5, (0, 0, 0), "-y", depth_cm=0.01, font=font)
        dparts.append(_fit_text(t, 0.52, 0.56, (-11.37, yf - 0.02, 14.47)))
        t = text3d("st_cert", ink, "CERTIFIED", 0.3, (0, 0, 0), "-y", depth_cm=0.01, font=font)
        dparts.append(_fit_text(t, 1.74, 0.2, (-11.97, yf - 0.016, 13.72)))
        dparts.append(extrude("st_setup", ink, rrect(0.69, 1.25, 0.15, cx=-10.15, cy=14.25), "y", yf - 0.02, yf))
        dparts.append(extrude("st_setup_c", sticker, _band(-10.15, 14.5, 0.14, 0.22, 40, 320, n=10), "y", yf - 0.026, yf))
        # inner side (faces up when the door lies open): ribs along the feed direction and the stop's rail
        for xc in (-12.6, -10.4, -8.2, -6.0, -3.8, 3.8, 6.0, 8.2, 10.4, 12.6):
            dparts.append(box("rib", inner, xc - 0.14, xc + 0.14, yi, yi + 0.3, 3.2, dz1 - 0.5, bevel=0.04))
        dparts.append(box("rail", inner, -1.4, 1.4, yi, yi + 0.3, 3.2, dz1 - 0.5, bevel=0.04))
        dparts.append(box("rail_slot", plate, -0.5, 0.5, yi + 0.28, yi + 0.31, 3.6, dz1 - 0.9))
        self.add("input_tray", join(dparts, "input_tray"), kind="moving", pivot=self.DOOR_PIVOT)

        # ---------------------------------------------------------------- open-tray extras (hidden when closed)
        # built in the open position: the door lies from y -10.55 to -25.93, inner face up at z 0.75, ribs to 1.05
        y_end = self.DOOR_PIVOT[1] - (dz1 - self.DOOR_PIVOT[2])       # outer end of the open door (-25.93)
        z_in = self.DOOR_PIVOT[2] + (yi - self.DOOR_PIVOT[1])         # inner face of the open door (0.75)
        ys = y_end + 0.45                                             # front of the paper stop
        stop = [box("ps_plate", blue, -3.0, 3.0, ys, ys + 0.3, z_in + 0.3, z_in + 2.0, bevel=0.08),
                box("ps_cap", blue, -3.0, 3.0, ys, ys + 2.1, z_in + 1.45, z_in + 2.0, bevel=0.1),
                box("ps_grip", blue2, -1.5, 1.5, ys + 0.35, ys + 1.75, z_in + 1.98, z_in + 2.05, bevel=0.02)]
        self.add("paper_stop", join(stop, "paper_stop"), kind="moving", hidden=True)
        # A4 stack (21 cm wide) from the stop into the entry; only the part outside the body is modelled
        self.add("paper", box("paper", paperm, -10.5, 10.5, ys + 0.3, -7.2, z_in + 0.32, z_in + 0.75),
                 kind="detail", hidden=True)

        # ---------------------------------------------------------------- cables
        # power: vertical C14 inlet in a 0.5 cm frame; network: RJ45 in the 0.8 cm pocket. Both plugs stick out.
        self.plug_cable("cable_power", "C13v", x=14.74, z=3.1, back_y=hy, recess=0.5)
        self.plug_cable("cable_eth", "RJ45", x=15.5, z=12.9, back_y=hy, recess=0.8)
        self.notes.append("Ports and mains inlet on the back, at the printer's right end (left seen from behind); "
                          "shallow pockets only (0.8 and 0.5 cm), so the C13 mains plug sticks out ~5 cm before "
                          "the cable bends: about 6.4 cm between the back and the wall.")
        self.notes.append("To print, the whole front door folds down as the paper tray (15 cm in front, at shelf level; "
                          "it must stay open while paper is loaded) and the output flap flips forward out of the top "
                          "(12 cm in front, 22-24 cm high).")

    def finish(self):
        super().finish()
        for part, ob in self.parts.items():
            if self.meta[part]["kind"] != "cable":
                _weighted_normals(ob)

    def states(self):
        # the stopper rides on the flap: rotate it with the flap about the flap's hinge, then raise it
        a = math.radians(FLAP_DEG)
        fp, sp = np.array(self.FLAP_PIVOT), np.array(self.STOP_PIVOT)
        d = sp - fp
        moved = fp + np.array([d[0], d[1] * math.cos(a) - d[2] * math.sin(a), d[1] * math.sin(a) + d[2] * math.cos(a)])
        tray = [("rot", "input_tray", "x", 90), ("show", "paper_stop")]
        return {
            "printing": tray + [("show", "paper"),
                                ("rot", "output_tray", "x", FLAP_DEG),
                                ("rot", "output_stop", "x", FLAP_DEG + STOP_DEG),
                                ("move", "output_stop", tuple(float(c) for c in (moved - sp)))],
            "refill": tray,
        }
