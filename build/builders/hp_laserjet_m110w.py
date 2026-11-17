"""
HP LaserJet M110w (7MD66F; M110we is the same body): very small mono laser, USB + Wi-Fi, no Ethernet.

Every number traces back to printers/HP LaserJet M110w/measurements/MEASUREMENTS.md
(official 346 x 189 x 159 mm; back photo 03 at 32.7 px/cm, front 24 at 21.3 px/cm, top 05 at 15.3 px/cm,
real side photos 10 / 11, real open-tray photos 15 / 21).

Frame: cm, Z up, FRONT = -Y, BACK = +Y, x = 0 centre of the width, y = 0 centre of the depth
(front -9.45, back +9.45), z = 0 under the feet.

Parts
- body:        base (drafted side walls), top cover with the rear hood and the grey output bin, feet, ports.
- input_tray:  the front door. It IS the paper tray: hinge along its bottom edge, folds 90 deg forward.
- tray_ext:    the pull-out plate in the door (same hinge as the door, then slides 2.85 cm further out).
- support:     the grey two-stage output extension; its end tab is the grey tab at the bin's front lip.
- paper:       an A4 stack on the open tray (hidden when closed).
The top cover (toner door, hinged at the back) is not a moving part: it is opened only to change toner.
"""
import math
import os
import sys

import numpy as np

# The C14 inlet is turned 90 degrees (photo 03 / 08): the plug face is 1.6 wide x 2.2 tall.
PLUGS["C13v"] = (1.6, 2.2, 3.4, 2.4, 0.75, 3.0)

# A white printer clips under the default render lights (comparison renders only, not the GLB).
if "printer_kit" in sys.modules:
    sys.modules["printer_kit"].LIGHT_GAIN = 0.24

W, D, H = 34.6, 18.9, 15.9
HW, HD = W / 2, D / 2
BH = 9.37            # half depth of the base: the top cover overhangs it by 0.08 front and back
Z0 = 0.3             # underside of the base (feet below)
HOOD_Y = 1.45        # front edge of the rear hood (8.0 cm from the back)
STEP = 0.2           # the shoulders start this much lower than the hood
R_TOP = 30.0         # radius of the curved front part of the top
Z_SH = H - STEP      # shoulder height right in front of the hood
LIP_Y = -8.7         # front lip of the output bin
FLOOR_Z_HOOD = 13.1  # bin floor under the hood's front edge (the exit opening is 2.4 cm tall)
DOOR_HW = 13.93
DOOR_Z0, DOOR_Z1 = 0.45, 12.63
DOOR_Y0, DOOR_Y1 = -BH, -BH + 0.9
HINGE = (0.0, -BH + 0.45, 0.9)
EXT_OUT = 2.85       # tray extension travel: door 11.2 cm + 2.85 = 14.05 cm in front (HP: 32.96 cm deep open)
SUP_OUT = 9.9        # output extension travel
# rear connectors (model x; both are at the printer's left rear corner = right side seen from behind)
POCKET_X = -14.15    # inner wall of the USB corner pocket (open to the back and to the left side)
POCKET_Z = (8.2, 12.5)
POCKET_DEPTH = 2.5
USB = (-14.65, 10.2)
PWR = (-13.94, 2.99)


def z_top(y):
    """Top surface at the shoulders (left and right of the bin); the hood is flat at 15.9."""
    if y >= HOOD_Y:
        return H
    return Z_SH - (R_TOP - math.sqrt(R_TOP ** 2 - (HOOD_Y - y) ** 2))


def top_normal(y):
    s = (HOOD_Y - y) / math.sqrt(R_TOP ** 2 - (HOOD_Y - y) ** 2) if y < HOOD_Y else 0.0
    return tuple(float(c) for c in nrm((0.0, -s, 1.0)))


def z_seam(y):
    """Seam between the base and the top cover: 0.4 under the hood top, 12.75 at the front face."""
    if y >= HOOD_Y:
        return 15.5 - 0.05 * (HD - y) / (HD - HOOD_Y)
    return 15.45 - 0.0227 * (HOOD_Y - y) ** 2


FLOOR_SLOPE = (z_top(LIP_Y) - 0.05 - FLOOR_Z_HOOD) / (HOOD_Y - LIP_Y)   # the floor rises toward the front


def z_floor(y):
    return FLOOR_Z_HOOD + FLOOR_SLOPE * (HOOD_Y - y)


def hw_bin(y):
    """Half width of the output bin: 22.4 cm at the hood, 22.9 at the front lip."""
    return 11.2 + 0.25 * (HOOD_Y - y) / (HOOD_Y - LIP_Y)


def hw_base(z):
    """Half width of the base: 32.84 cm wide at the bottom, 34.36 under the cover (draft, photo 03)."""
    return 16.42 + 0.76 * (z - Z0) / (H - Z0)


def _plan(hw, hd, rf, rb, z, n=8):
    p = fillet([(-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd)], [rf, rf, rb, rb], n)
    return np.c_[p, np.full(len(p), z)]


def _loft(name, mat, rings):
    n = len(rings[0])
    V = [tuple(p) for r in rings for p in r]
    F = [list(range(n))[::-1]]
    for k in range(len(rings) - 1):
        a, b = k * n, (k + 1) * n
        F += [[a + i, a + (i + 1) % n, b + (i + 1) % n, b + i] for i in range(n)]
    F.append([(len(rings) - 1) * n + i for i in range(n)])
    return mesh_obj(name, V, F, mat)


def _wedge(name, mat, prof, hwf, inset=0.0):
    """Like extrude(axis='x') of a (y, z) profile, but the half width follows hwf(y) (linear in y)."""
    n = len(prof)
    V = [(-(hwf(y) - inset), y, z) for y, z in prof] + [(hwf(y) - inset, y, z) for y, z in prof]
    F = [list(range(n))[::-1], list(range(n, 2 * n))] + [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    return mesh_obj(name, V, F, mat)


def _strip(f, y0, y1, lo, hi, n=14):
    """Closed (y, z) profile of a thin skin lying on the curve z = f(y) between y0 and y1."""
    ys = np.linspace(y0, y1, n + 1)
    return [(y, f(y) + hi) for y in ys] + [(y, f(y) + lo) for y in ys[::-1]]


def _weighted_normals(ob):
    """Face-area weighted normals: big flat faces stay flat next to rounded corners."""
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


def _shear_x(ob, k, z_ref):
    """Italic: shift x by k * (z - z_ref)."""
    me = ob.data
    for v in me.vertices:
        v.co.x += k * (v.co.z - z_ref * CM)
    me.update()
    return ob


class Builder(Printer):

    def build(self):
        white = self.mat("white", "#e6e6e2", 0.5)
        white2 = self.mat("white_inner", "#dcdcd8", 0.55)
        emboss = self.mat("emboss", "#d2d2ce", 0.5)
        grey = self.mat("bin_grey", "#7e8084", 0.6)
        black = self.mat("black", "#151618", 0.6)
        frame = self.mat("inlet", "#1c1c1c", 0.5)
        metal = self.mat("metal", "#a0a0a0", 0.35, metal=0.8)
        plate = self.mat("panel", "#cfd0ca", 0.4)
        rim = self.mat("panel_rim", "#a9aaa6", 0.5)
        btn = self.mat("button", "#e9e9e6", 0.4)
        tabgrey = self.mat("lift_tab", "#c4c5c4", 0.5)
        silver = self.mat("logo", "#b4b5b8", 0.32, metal=0.7)
        logo_w = self.mat("logo_white", "#f4f4f2", 0.4)
        ink = self.mat("ink", "#8a8c8e", 0.5)
        iconc = self.mat("icon", "#8d9296", 0.5)
        rubber = self.mat("rubber", "#cfcfcb", 0.8)
        paper = self.mat("paper", "#f7f7f4", 0.75)
        led_g = self.mat("led_green", "#35c46a", 0.3, emit="#35c46a", emit_strength=2.5)
        led_b = self.mat("led_blue", "#58b6e8", 0.3, emit="#58b6e8", emit_strength=1.5)
        led_a = self.mat("led_amber", "#c9a45a", 0.4)
        font = find_font("DejaVuSans-Bold")

        # ------------------------------------------------------------------ base (below the seam)
        base = _loft("base", white, [
            _plan(hw_base(Z0) - 0.4, BH - 0.4, 1.9, 0.6, Z0),
            _plan(hw_base(0.75), BH, 2.3, 0.9, 0.75),
            _plan(hw_base(16.3), BH, 2.3, 0.9, 16.3)])
        ys = np.linspace(-HD - 1, HD + 1, 40)
        above = [(y, z_seam(y)) for y in ys] + [(HD + 1, 20), (-HD - 1, 20)]
        cut(base, extrude("seam_cut", None, above, axis="x", a0=-20, a1=20))
        # room behind the door (the door is 0.9 thick; the fixed inner panel sits 1.1 behind the front)
        cut(base, box("door_cut", None, -DOOR_HW - 0.12, DOOR_HW + 0.12, -BH - 1, -BH + 1.12, 0.38, DOOR_Z1 + 0.08))
        for s in (-1, 1):   # slots beside the inner panel for the tray's side rails
            cut(base, box("rail_cut", None, min(s * 12.9, s * 14.05), max(s * 12.9, s * 14.05),
                          -BH + 1.0, -BH + 1.85, 0.38, DOOR_Z1 + 0.08))
        # USB corner pocket: open to the back and to the left side (photos 03, 10, 17)
        pz0, pz1 = POCKET_Z
        pocket = box("pocket_cut", None, -HW - 1, POCKET_X, BH - POCKET_DEPTH, BH + 1, pz0, pz1, bevel=0.3, seg=3)
        bake(pocket)
        cut(base, pocket)
        cut(base, box("pocket_rim", None, -16.6, POCKET_X + 0.3, BH - 0.05, BH + 1, pz0 - 0.4, pz1 + 0.35))
        # power inlet opening (the black frame fills it)
        px, pz = PWR
        cut(base, box("inlet_cut", None, px - 1.2, px + 1.2, BH - 1.9, BH + 1, pz - 1.58, pz + 1.58))
        # output bin and the exit under the hood (cut from the base and the top cover)
        bin_prof = [(LIP_Y, z_floor(LIP_Y)), (3.6, z_floor(3.6)), (3.6, 15.5), (HOOD_Y, 15.5),
                    (HOOD_Y, 17.5), (LIP_Y, 17.5)]
        bin_cut = _wedge("bin_cut", None, bin_prof, hw_bin)
        bin_cut["cutter"] = True
        cut(base, bin_cut)
        base["bevel"] = [0.07, 2, 30.0]
        self.add("body", base)

        # ------------------------------------------------------------------ top cover
        lid = _loft("lid", white, [_plan(HW - 0.22, HD + 0.004, 2.6, 1.0, 11.5),
                                   _plan(HW, HD + 0.004, 2.6, 1.0, H),
                                   _plan(HW, HD + 0.004, 2.6, 1.0, 16.5)])
        arc_pts = [(y, z_top(y)) for y in np.linspace(-HD + 1.2, HOOD_Y, 16)]
        seam_pts = [(y, z_seam(y) + 0.045) for y in np.linspace(HD, -HD, 30)]
        prof = [(-HD, z_top(-HD))] + arc_pts + [(HOOD_Y, H), (HD, H)] + seam_pts
        rad = [0.7] + [0.0] * len(arc_pts) + [0.0, 0.3] + [0.0] * len(seam_pts)
        cut(lid, extrude("lid_prof", None, fillet(prof, rad, n=6), axis="x", a0=-20, a1=20), op="INTERSECT")
        cut(lid, bin_cut)
        # split line between the hood and the shoulders
        cut(lid, box("split", None, -20, 20, HOOD_Y - 0.07, HOOD_Y - 0.01, Z_SH - 0.25, 17))
        for s in (-1, 1):
            cut(lid, box("split_side", None, min(s * 17.2, s * 18), max(s * 17.2, s * 18),
                         HOOD_Y - 0.07, HOOD_Y - 0.01, 14.0, 17))
        lid["bevel"] = [0.16, 3, 30.0]
        self.add("body", lid)

        # grey bin floor, black exit under the hood, rollers, end guides
        floor = _strip(z_floor, LIP_Y + 0.02, 2.0, -0.08, 0.025, n=2)
        self.add("body", _wedge("bin_floor", grey, floor, hw_bin, inset=0.01))
        self.add("body", box("exit", black, -11.14, 11.14, HOOD_Y + 0.3, 3.58, z_floor(3.6) - 0.02, 15.48))
        for xc in (-6.5, -3.1, 3.1, 6.5):
            for k in range(4):
                self.add("body", cyl("roller", white, (xc - 0.6 + k * 0.4, HOOD_Y + 0.32, 14.45), "x", 0.3, 0.22, seg=14))
        for s in (-1, 1):
            x0, x1 = sorted((s * 9.7, s * 11.12))
            self.add("body", box("guide", black, x0, x1, HOOD_Y + 0.02, HOOD_Y + 0.5, z_floor(HOOD_Y), 14.9, bevel=0.06))

        # ------------------------------------------------------------------ control panel (left shoulder)
        def panel(name, mat, w, h, lo, hi):
            ob = extrude(name, mat, _strip(z_top, -6.9, -1.5, lo, hi, n=10), axis="x", a0=-16.2, a1=-13.1)
            cut(ob, extrude(name + "_round", None, rrect(w, h, 0.4, cx=-14.65, cy=-4.19), axis="z", a0=10, a1=17),
                op="INTERSECT")
            return ob

        self.add("body", panel("panel_rim", rim, 2.82, 5.3, -0.05, 0.018))
        self.add("body", panel("panel", plate, 2.7, 5.18, -0.05, 0.035))

        def on_top(x, y, lift=0.0):
            return (x, y, z_top(y) + lift)

        for y, col in ((-3.04, led_b), (-4.32, iconc)):          # Wireless, Cancel
            n = top_normal(y)
            self.add("body", cyl("btn_ring", rim, on_top(-15.03, y, 0.035), n, 0.5, 0.03, seg=28))
            self.add("body", cyl("btn", btn, on_top(-15.03, y, 0.045), n, 0.44, 0.03, seg=28))
            self.add("body", cyl("btn_icon", col, on_top(-15.03, y, 0.058), n, 0.2, 0.02, seg=20))
        self.add("body", cyl("led_attn", led_a, on_top(-14.25, -4.32, 0.04), top_normal(-4.32), 0.07, 0.03, seg=10))
        yp = -5.52                                               # Power: a pill with the green icon at its right end
        self.add("body", extrude("pill_ring", rim, rrect(1.84, 0.92, 0.45, cx=-14.39, cy=yp), axis="z",
                                 a0=z_top(yp) - 0.06, a1=z_top(yp) + 0.065))
        self.add("body", extrude("pill", btn, rrect(1.72, 0.8, 0.39, cx=-14.39, cy=yp), axis="z",
                                 a0=z_top(yp) - 0.06, a1=z_top(yp) + 0.08))
        self.add("body", cyl("pwr_icon", led_g, on_top(-13.95, yp, 0.09), top_normal(yp), 0.24, 0.02, seg=20))

        # ------------------------------------------------------------------ behind the door (fixed)
        yi = -BH + 1.12                                          # inner panel face
        self.add("body", box("paper_slot", black, -10.8, 10.8, yi - 0.03, yi + 0.05, 0.75, 1.95))
        self.add("body", cyl("inner_logo", emboss, (0, yi, 7.3), "y", 1.75, 0.06, seg=40))
        # lift tab of the top cover, seen through the finger notch of the door
        self.add("body", box("lift_tab", tabgrey, -4.55, 4.55, -BH + 0.3, -BH + 0.72, 11.8, 12.77, bevel=0.05))

        # ------------------------------------------------------------------ back: USB port and power inlet
        yw = BH - POCKET_DEPTH
        ux, uz = USB
        self.add("body", box("usb_shell", metal, ux - 0.6, ux + 0.6, yw - 0.2, yw + 0.06, uz - 0.55, uz + 0.55))
        self.add("body", box("usb_hole", black, ux - 0.45, ux + 0.45, yw, yw + 0.075, uz - 0.4, uz + 0.4))
        self.add("body", box("usb_tongue", self.mat("usb_tongue", "#8c8c8c", 0.5), ux - 0.28, ux + 0.28,
                             yw, yw + 0.085, uz - 0.18, uz + 0.14))
        fr = box("inlet_frame", frame, px - 1.22, px + 1.22, BH - 1.85, BH + 0.02, pz - 1.6, pz + 1.6, bevel=0.06)
        cav = [(px + 0.82, pz - 1.2), (px - 0.42, pz - 1.2), (px - 0.82, pz - 0.8), (px - 0.82, pz + 0.8),
               (px - 0.42, pz + 1.2), (px + 0.82, pz + 1.2)]          # earth side = model -x
        cut(fr, extrude("inlet_cav", None, cav, axis="y", a0=BH - 1.6, a1=BH + 1))
        self.add("body", fr)
        for dx, dz in ((0.22, 0.7), (-0.2, 0.0), (0.22, -0.7)):
            self.add("body", box("pin", metal, px + dx - 0.2, px + dx + 0.2, BH - 1.6, BH - 0.45, pz + dz - 0.05, pz + dz + 0.05))

        # ------------------------------------------------------------------ feet (photo 13: small pads)
        for sx in (-1, 1):
            for y in (-6.5, 7.0):
                self.add("body", cyl("foot", rubber, (sx * 13.0, y, Z0 / 2 + 0.02), "z", 0.75, Z0 + 0.04, seg=18))

        # ------------------------------------------------------------------ front door = paper tray (moving)
        door = box("door", white, -DOOR_HW, DOOR_HW, DOOR_Y0, DOOR_Y1, DOOR_Z0, DOOR_Z1, bevel=0.1)
        notch = fillet([(-4.65, 11.87), (4.65, 11.87), (4.65, 13.5), (-4.65, 13.5)], [0.35, 0.35, 0, 0])
        cut(door, extrude("notch_cut", None, notch, axis="y", a0=DOOR_Y0 - 1, a1=DOOR_Y1 + 1))
        dparts = [door]
        dparts.append(cyl("logo_disc", silver, (0, DOOR_Y0 - 0.005, 6.1), "y", 2.05, 0.05, seg=56))
        hp = text3d("logo_hp", logo_w, "hp", 2.5, (0.0, DOOR_Y0 - 0.035, 6.2), "-y", depth_cm=0.02, font=font)
        dparts.append(_shear_x(hp, 0.22, 6.1))
        dparts.append(text3d("model_txt", ink, "HP LaserJet M110w", 0.46, (9.6, DOOR_Y0 - 0.01, 1.8), "-y",
                             depth_cm=0.015, font=find_font("DejaVuSans.ttf") or font))
        for s in (-1, 1):   # side rails of the tray (they stand up when the door lies open)
            x0, x1 = sorted((s * 13.05, s * 13.3))
            dparts.append(box("rail", white, x0, x1, DOOR_Y1 - 0.02, DOOR_Y1 + 0.6, 1.7, 12.2, bevel=0.05))
        self.add("input_tray", join(dparts, "input_tray"), kind="moving", pivot=HINGE)

        # pull-out tray extension: a plate set into the door's inner face, with a low stop at its tip
        ext = [box("ext", white2, -5.75, 5.75, DOOR_Y1 - 0.1, DOOR_Y1 + 0.03, 5.6, DOOR_Z1, bevel=0.03),
               box("ext_stop", white2, -5.75, 5.75, DOOR_Y1, DOOR_Y1 + 0.2, DOOR_Z1 - 0.3, DOOR_Z1, bevel=0.05)]
        self.add("tray_ext", join(ext, "tray_ext"), kind="moving", pivot=HINGE)

        # A4 stack on the open tray (built in the open position, hidden when closed). Letter paper ends
        # at the door's edge (photo 01), so the sheet goes 16.7 cm in and A4 ends 13.0 cm in front.
        z_tray = HINGE[2] + (DOOR_Y1 - HINGE[1]) + 0.04
        self.add("paper", box("paper", paper, -10.5, 10.5, -HD - 13.0, -BH + 1.3, z_tray, z_tray + 0.4),
                 kind="moving", hidden=True)

        # ------------------------------------------------------------------ output extension (moving)
        # Closed: the grey tab at the lip; the two stages lie flush in the bin floor behind it.
        sup = [extrude("sup_tab", grey, _strip(z_floor, LIP_Y + 0.02, -6.4, -0.05, 0.17, n=1), axis="x",
                       a0=-4.6, a1=4.6, bevel=0.05)]
        sup.append(extrude("sup_stage2", grey, _strip(z_floor, -6.45, -3.2, -0.1, 0.04, n=1), axis="x", a0=-2.45, a1=2.45))
        sup.append(extrude("sup_stage1", grey, _strip(z_floor, -3.2, 3.5, -0.1, 0.04, n=1), axis="x", a0=-4.65, a1=4.65))
        self.add("support", join(sup, "support"), kind="moving", pivot=(0, LIP_Y, z_floor(LIP_Y)))

        # ------------------------------------------------------------------ cables (power + USB; no Ethernet)
        # power: C14 inlet flush on the flat back -> the plug and its strain relief stick straight out.
        # USB-B: on the back wall of the 2.5 cm deep corner pocket -> the 3 cm plug is nearly inside it.
        self.plug_cable("cable_power", "C13v", x=px, z=pz, back_y=HD, recess=HD - BH)
        self.plug_cable("cable_usb", "USB-B", x=ux, z=uz, back_y=HD, recess=HD - BH + POCKET_DEPTH)
        self.notes.append("Power inlet (C14, turned 90 deg) is flush on the flat back: the C13 plug and its strain "
                          "relief stick straight out. USB-B sits in a 2.5 cm deep corner pocket; no Ethernet.")
        self.notes.append("It cannot print closed: the front door folds down into the paper tray (11.2 cm in front), "
                          "the tray extension adds 2.85 cm (33.0 cm deep in total, HP user guide: 32.96 cm) and the "
                          "grey output extension slides out about 10 cm over it. HP's datasheet maximum is 36.0 cm.")
        self.notes.append("The top cover (toner door) lifts to 28 cm for toner changes only; not modelled as a state.")

    def finish(self):
        super().finish()
        for part, ob in self.parts.items():
            if self.meta[part]["kind"] != "cable":
                _weighted_normals(ob)

    def states(self):
        a = math.atan(FLOOR_SLOPE)
        slide = (0.0, -SUP_OUT * math.cos(a), SUP_OUT * math.sin(a))
        door = [("rot", "input_tray", "x", 90), ("rot", "tray_ext", "x", 90)]
        tray = door + [("move", "tray_ext", (0, -EXT_OUT, 0)), ("show", "paper")]
        st = {
            "printing": tray + [("move", "support", slide)],
            "refill": tray,
        }
        if os.environ.get("M110_CMP"):   # comparison renders only: photo 21 = door down, tray extension in
            st["cmp21"] = door + [("move", "support", slide)]
        return st
