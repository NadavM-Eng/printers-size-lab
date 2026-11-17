"""
Xerox B230 (B230V_DNI in Israel/Europe, B230/DNI in the US): mono laser printer, Wi-Fi, auto duplex.
Same chassis as the Lexmark B2236dw. Every number comes from
printers/Xerox B230/measurements/MEASUREMENTS.md (measured on the photos in printers/Xerox B230/photos/).

Frame (cm): x = 0 centre of the width (+x right seen from the front), y = 0 centre of the depth
(front face -16.65, back face +16.65), z = 0 under the feet. Z up, FRONT = -Y.

Official: 355 x 333 x 232 mm (W x D x H, Xerox datasheet). The 232 mm includes the raised LCD pod;
the top cover itself is at 216 mm (Xerox dimension graphic, whose arrow ends at the top cover).

Run:  .venv/Scripts/python.exe build/build_printer.py xerox-b230 --render front,34fl,back
"""
import math

import numpy as np

# The power inlet (IEC C14) is mounted vertically, so the C13 plug goes in turned 90 degrees.
PLUGS.setdefault("C13v", (1.6, 2.2, 3.4, 2.4, 0.75, 3.0))

# Comparison renders only: the kit's default lights clip this white body; Xerox's own renders read
# white #e5e5e5 and navy #4d5761, which a gain of about 0.45 reproduces. (Runtime setting, the kit file is untouched.)
try:
    import printer_kit as _K
    _K.LIGHT_GAIN = 0.45
    if not getattr(_K, "_xb230_world", False):   # dimmer world so the navy top is not washed out at grazing angles
        _orig_setup_render = _K.setup_render

        def _setup_render(size=900, samples=48, bg="#d9d9d6"):
            _orig_setup_render(size, samples, bg)
            _K.bpy.context.scene.world.node_tree.nodes.get("Background").inputs[1].default_value = 0.3

        _K.setup_render = _setup_render
        _K._xb230_world = True
except Exception:
    pass


def loft(name, mat, rings):
    """Closed solid through a stack of plan outlines. rings: [(z, Nx2 array)], bottom to top, same N."""
    n = len(rings[0][1])
    verts = []
    for z, P in rings:
        verts += [(float(u), float(v), float(z)) for u, v in P]
    m = len(rings)
    faces = [list(range(n))[::-1], [(m - 1) * n + i for i in range(n)]]
    for k in range(m - 1):
        for i in range(n):
            j = (i + 1) % n
            faces.append([k * n + i, k * n + j, (k + 1) * n + j, (k + 1) * n + i])
    return mesh_obj(name, verts, faces, mat)


class Builder(Printer):
    W, D = 35.5, 33.3
    H_TOP = 21.6        # top cover surface (216 mm)
    H_POD = 23.2        # top of the LCD pod (232 mm, the datasheet height)
    Z0 = 0.25           # underside of the body; rubber feet below
    Z_LIP = 20.25       # bottom edge of the navy top cover (front 20.2-20.4, back 20.2)
    Z_SEAM = 8.3        # cassette / front door seam
    R_FRONT, R_BACK = 1.4, 1.8   # vertical corner radii in plan
    R_TOP = 0.75        # rounding of the top cover's upper edge

    # output bin (recess in the top): opening, back wall, floor ramp
    BIN_X = (-12.0, 11.2)
    BIN_Y = (-7.5, 11.25)     # where the floor reaches the top surface, back wall
    BIN_Z_BACK = 17.9         # floor at the back wall

    # paper stop flap on top (front centre), hinge at its front edge
    FLAP_X = (-4.2, 3.4)
    FLAP_Y = (-15.5, -8.85)

    # rear connectors: two notches cut into the rounded rear corner on the printer's left side
    PORT_NOTCH = (-14.67, 9.8, 17.63)    # inner x, z0, z1
    PORT_RECESS = 3.0         # real photo 12_back_ports_real: inner wall ~150 px at ~50 px/cm
    ETH = (-16.56, 16.5)
    USB = (-16.33, 12.5)
    PWR_NOTCH = (-14.33, 1.79, 5.76)
    PWR_RECESS = 3.6          # the C13 housing (3.4) sits inside it, only the strain relief sticks out
    PWR = (-15.3, 4.35)
    LEDGE = 0.14              # tan(8 deg): the notch floors slope down toward the back

    def plan(self, inset=0.0, n=8):
        hw, hd = self.W / 2 - inset, self.D / 2 - inset
        rf, rb = max(self.R_FRONT - inset, 0.05), max(self.R_BACK - inset, 0.05)
        P = fillet([(-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd)], [rf, rf, rb, rb], n=n)
        out = []          # support points 0.05 cm beside every corner arc, so the flat walls shade flat
        m = n + 1
        for c in range(4):
            arc_pts = P[c * m:(c + 1) * m]
            prev_end, next_start = P[c * m - 1], P[((c + 1) * m) % len(P)]
            out.append(arc_pts[0] + nrm(prev_end - arc_pts[0]) * 0.05)
            out.extend(arc_pts)
            out.append(arc_pts[-1] + nrm(next_start - arc_pts[-1]) * 0.05)
        return np.array(out)

    def slab(self, name, mat, z0, z1, r_top=0.0, r_bot=0.0, seg=5):
        """The plan outline from z0 to z1 with rounded bottom and/or top edges."""
        rings = []
        if r_bot > 0:
            for k in range(seg):
                a = math.radians(90 - 90 * k / seg)
                rings.append((z0 + r_bot * (1 - math.sin(a)), self.plan(r_bot * (1 - math.cos(a)))))
        rings.append((z0 + r_bot, self.plan()))
        if r_bot > 0:
            rings.append((z0 + r_bot + 0.05, self.plan()))
        if r_top > 0:
            rings.append((z1 - r_top - 0.05, self.plan()))
        rings.append((z1 - r_top, self.plan()))
        if r_top > 0:
            for k in range(1, seg + 1):
                a = math.radians(90 * k / seg)
                rings.append((z1 - r_top + r_top * math.sin(a), self.plan(r_top * (1 - math.cos(a)))))
        return loft(name, mat, rings)

    def floor_z(self, y):
        y0, y1 = self.BIN_Y
        return self.H_TOP + (self.BIN_Z_BACK - self.H_TOP) * (y - y0) / (y1 - y0)

    # ------------------------------------------------------------------------------------------
    def build(self):
        W, D = self.W, self.D
        hw, hd = W / 2, D / 2
        Z0, ZL, ZS, HT = self.Z0, self.Z_LIP, self.Z_SEAM, self.H_TOP

        white = self.mat("white", "#e6e7e8", 0.42)
        navy = self.mat("navy", "#2d3a49", 0.7)
        navy2 = self.mat("navy_plate", "#3b4a5a", 0.5)
        dark = self.mat("dark", "#2b2d30", 0.45)
        okgrey = self.mat("okgrey", "#3c4045", 0.4)
        black = self.mat("black", "#101112", 0.6)
        rubber = self.mat("rubber", "#151515", 0.9)
        blue = self.mat("blue", "#3f6fbf", 0.35)
        grey = self.mat("grey", "#bfc2c5", 0.5)
        mgrey = self.mat("midgrey", "#8d9196", 0.5)
        vent = self.mat("vent", "#6f7377", 0.7)
        key = self.mat("key", "#131416", 0.6)
        lcdtxt = self.mat("lcdtext", "#2a3238", 0.5)
        trayc = self.mat("tray", "#cfd0d2", 0.5)
        paper = self.mat("paper", "#f5f5f2", 0.7)
        lcd = self.mat("lcd", "#8f9ba1", 0.35, emit="#9fb0b8", emit_strength=0.12)
        txt = self.mat("text", "#f4f4f4", 0.4)
        lgrey = self.mat("labelgrey", "#9aa4ad", 0.4)
        red = self.mat("red", "#d02a2a", 0.4)
        font = find_font("DejaVuSans-Bold")

        # ---------------------------------------------------------------- white shell
        shell = self.slab("shell", white, Z0, ZL + 0.03, r_bot=0.5)
        # front-bottom slab replaced by the cassette's front cap, and the tray cavity behind it
        cut(shell, box("cap_cut", None, -hw - 1, hw + 1, -hd - 1, -hd + 1.6, Z0 - 1, ZS + 0.06))
        cut(shell, box("tray_cut", None, -14.4, 14.4, -hd + 1.5, hd - 2.6, Z0 - 1, ZS - 0.3))
        # pocket under the output bin (filled by the navy tub so no white shows inside the bin)
        bx0, bx1 = self.BIN_X
        by0, by1 = self.BIN_Y
        cut(shell, box("tub_cut", None, bx0 - 0.56, bx1 + 0.56, by0 - 0.56, by1 + 0.56, 16.9, ZL + 1))
        # vents (horizontal slots): left side lower part along the whole depth, right side high at the back
        for i in range(12):
            z = 3.0 + i * 0.31
            cut(shell, box("vl%d" % i, None, -hw - 1, -hw + 0.15, -14.6, 14.6, z, z + 0.16))
            self.add("body", box("vlb", vent, -hw + 0.1, -hw + 0.15, -14.6, 14.6, z, z + 0.16))
        for i in range(20):
            z = 11.7 + i * 0.37
            cut(shell, box("vr%d" % i, None, hw - 0.15, hw + 1, 4.3, 13.9, z, z + 0.19))
            self.add("body", box("vrb", vent, hw - 0.15, hw - 0.1, 4.3, 13.9, z, z + 0.19))
        # handholds: the underside is raised in the middle of both sides, with a finger pocket
        for s in (-1, 1):
            x0, x1 = (-hw - 1, -hw + 1.5) if s < 0 else (hw - 1.5, hw + 1)
            cut(shell, box("hand%d" % s, None, x0, x1, -3.8, 8.0, Z0 - 1, 1.45))
            x0, x1 = (-hw - 1, -hw + 1.2) if s < 0 else (hw - 1.2, hw + 1)
            cut(shell, box("handp%d" % s, None, x0, x1, 1.5, 7.5, 1.0, 2.5))
        # front door: side seams just behind the rounded front corners
        for s in (-1, 1):
            x0, x1 = (-hw - 0.5, -hw + 0.1) if s < 0 else (hw - 0.1, hw + 0.5)
            cut(shell, box("dseam%d" % s, None, x0, x1, -hd + 1.52, -hd + 1.66, ZS, ZL))
        # manual-feed flap: groove on 3 sides (pocket), refilled by a flush panel below
        MX, MZ = 13.3, 13.2
        mf_out = fillet([(-MX, ZS - 0.5), (MX, ZS - 0.5), (MX, MZ), (-MX, MZ)], [0, 0, 0.62, 0.62])
        cut(shell, extrude("mf_cut", None, mf_out, axis="y", a0=-hd - 1, a1=-hd + 0.22))
        # back: rear door outline, duplex strip outline (grooves with a dark bottom)
        RD0, RD1, RDZ = -14.2, 14.7, 7.3          # rear door x range, bottom edge
        DU0, DU1, DUZ = -13.35, 13.85, 4.67       # duplex strip x range, bottom edge
        for (x0, x1, z0, z1) in [(RD0 - 0.07, RD0 + 0.07, RDZ, ZL), (RD1 - 0.07, RD1 + 0.07, RDZ, ZL),
                                 (RD0 - 0.07, RD1 + 0.07, RDZ - 0.07, RDZ + 0.07),
                                 (DU0, DU1, DUZ - 0.07, DUZ + 0.07),
                                 (DU0 - 0.07, DU0 + 0.07, DUZ, RDZ), (DU1 - 0.07, DU1 + 0.07, DUZ, RDZ)]:
            cut(shell, box("rseam", None, x0, x1, hd - 0.3, hd + 1, z0, z1))
            self.add("body", box("rseam_dark", black, x0, x1, hd - 0.3, hd - 0.24, z0, z1))
        # label outline (thin groove)
        for (x0, x1, z0, z1) in [(-6.13, 5.35, 15.3, 15.36), (-6.13, 5.35, 10.4, 10.46), (-6.13, -6.07, 10.4, 15.36),
                                 (5.29, 5.35, 10.4, 15.36)]:
            cut(shell, box("lseam", None, x0, x1, hd - 0.1, hd + 1, z0, z1))
        # finger scoop at the top of the rear door, pocket for the duplex handle
        notch = fillet([(-2.5, 18.3), (3.0, 18.3), (3.0, ZL + 1), (-2.5, ZL + 1)], [0.5, 0.5, 0, 0])
        cut(shell, extrude("notch_cut", None, notch, axis="y", a0=hd - 1.2, a1=hd + 1))
        cut(shell, box("handle_cut", None, -3.7, 3.15, hd - 0.45, hd + 1, 3.43, 5.76))
        # connectors: two notches in the rounded rear corner, open to the side, floors sloping to the back
        nx, nz0, nz1 = self.PORT_NOTCH
        d = self.PORT_RECESS
        prof = [(hd - d, nz0 + d * self.LEDGE), (hd + 1, nz0 - self.LEDGE), (hd + 1, nz1), (hd - d, nz1)]
        cut(shell, extrude("port_cut", None, prof, axis="x", a0=-hw - 1, a1=nx))
        qx, qz0, qz1 = self.PWR_NOTCH
        d = self.PWR_RECESS
        prof = [(hd - d, qz0 + d * self.LEDGE), (hd + 1, qz0 - self.LEDGE), (hd + 1, qz1), (hd - d, qz1)]
        cut(shell, extrude("pwr_cut", None, prof, axis="x", a0=-hw - 1, a1=qx))
        # power button ring groove
        PBX, PBZ = 15.1, 18.7
        cut(shell, cyl("pb_cut", None, (PBX, -hd, PBZ), "y", 0.8, 0.24, seg=32))
        self.add("body", shell)

        # flush manual-feed panel (inside the groove)
        mf_in = fillet([(-MX + 0.13, ZS + 0.1), (MX - 0.13, ZS + 0.1), (MX - 0.13, MZ - 0.13), (-MX + 0.13, MZ - 0.13)],
                       [0, 0, 0.5, 0.5])
        self.add("body", extrude("mf_panel", white, mf_in, axis="y", a0=-hd + 0.0, a1=-hd + 0.12))
        self.add("body", box("seam_dark", black, -hw + 1.5, hw - 1.5, -hd + 0.25, -hd + 1.45, ZS - 0.1, ZS + 0.1))
        mf_bg = fillet([(-MX + 0.02, ZS + 0.1), (MX - 0.02, ZS + 0.1), (MX - 0.02, MZ - 0.02), (-MX + 0.02, MZ - 0.02)],
                       [0, 0, 0.6, 0.6])
        self.add("body", extrude("mf_bg", mgrey, mf_bg, axis="y", a0=-hd + 0.15, a1=-hd + 0.22))
        for i in range(4):   # four pairs of small dots near the flap's top centre
            for z in (12.25, 11.8):
                self.add("body", cyl("mfdot", grey, (-1.45 + i * 0.95, -hd - 0.01, z), "y", 0.06, 0.04, seg=10))

        # ---------------------------------------------------------------- navy top cover
        top = self.slab("top", navy, ZL, HT, r_top=self.R_TOP)
        tub = box("tub", navy, bx0 - 0.55, bx1 + 0.55, by0 - 0.55, by1 + 0.55, 17.0, ZL - 0.01)
        bin_prof = fillet([(by0, HT + 1), (by0, HT), (by1, self.BIN_Z_BACK), (by1, HT + 1)], [0, 0, 0.6, 0])
        cut(top, extrude("bin_cut", None, bin_prof, axis="x", a0=bx0, a1=bx1))
        cut(tub, extrude("bin_cut2", None, bin_prof, axis="x", a0=bx0, a1=bx1))
        fx0, fx1 = self.FLAP_X
        fy0, fy1 = self.FLAP_Y
        cut(top, box("flap_pocket", None, fx0 - 0.07, fx1 + 0.07, fy0 - 0.07, fy1 + 0.07, HT - 0.3, HT + 1))
        self.add("body", top)
        self.add("body", tub)
        self.add("body", box("flap_floor", black, fx0 - 0.07, fx1 + 0.07, fy0 - 0.07, fy1 + 0.07, HT - 0.31, HT - 0.28))
        # bin details: exit slot with rollers in the back wall, ribs on the floor, two paper guides
        self.add("body", box("exit", black, bx0 + 3.6, bx1 - 3.4, by1 - 0.1, by1 + 0.04, 19.25, 20.75))
        for x in (-6.3, -4.4, -2.5, 1.7, 3.6, 5.5):
            self.add("body", cyl("roller", dark, (x, by1 - 0.22, 19.95), "x", 0.42, 1.1, seg=16))
        for x in (-7.8, -4.0, -0.4, 3.4, 7.1):
            ya, yb = by0 + 0.5, by1 - 0.5
            rib = [(ya, self.floor_z(ya) - 0.1), (yb, self.floor_z(yb) - 0.1),
                   (yb, self.floor_z(yb) + 0.22), (ya, self.floor_z(ya) + 0.03)]
            self.add("body", extrude("rib", navy, rib, axis="x", a0=x - 0.1, a1=x + 0.1))
        for (x0, x1) in ((bx0 + 0.1, -8.5), (7.6, bx1 - 0.1)):
            self.add("body", box("guide", navy2, x0, x1, by1 - 1.9, by1 + 0.1, 19.9, 20.95, bevel=0.1))

        # ---------------------------------------------------------------- control panel (right of the bin)
        self.add("body", box("b230_plate", navy2, 11.9, 16.7, 3.2, 6.0, HT - 0.05, HT + 0.04, bevel=0.04))
        self.add("body", text3d("b230", lgrey, "B230", 0.75, (14.3, 4.6, HT + 0.05), "+z", depth_cm=0.02, font=font))
        # LCD pod: display face tilted toward the front, rounded top, steep back
        pod = fillet([(-1.05, HT - 0.45), (1.45, HT - 0.45), (1.45, HT + 1.25), (0.75, self.H_POD), (-1.05, HT + 0.1)],
                     [0, 0, 0.3, 0.3, 0.06])
        self.add("body", extrude("pod", navy, pod, axis="x", a0=11.4, a1=17.2, bevel=0.2))
        p0 = np.array([-1.05, HT + 0.1])
        t = np.array([0.75 + 1.05, self.H_POD - HT - 0.1])
        L = float(np.linalg.norm(t))
        t = t / L
        nn = np.array([-t[1], t[0]])
        s0, s1 = 0.16 * L, 0.8 * L
        win = [p0 + t * s0 - nn * 0.03, p0 + t * s1 - nn * 0.03, p0 + t * s1 + nn * 0.03, p0 + t * s0 + nn * 0.03]
        self.add("body", extrude("lcd", lcd, win, axis="x", a0=12.0, a1=16.6))
        for (frac, x0, x1) in ((0.6, 13.6, 15.2), (0.32, 12.2, 13.5)):      # "Status" / "Ready" as two text bars
            c = p0 + t * (frac * L)
            bar = [c - t * 0.13 + nn * 0.03, c + t * 0.13 + nn * 0.03, c + t * 0.13 + nn * 0.045, c - t * 0.13 + nn * 0.045]
            self.add("body", extrude("lcd_txt", lcdtxt, bar, axis="x", a0=x0, a1=x1))
        # two status lights (unlit in every photo), D-pad with OK, menu and cancel buttons
        for x in (12.8, 14.5):
            self.add("body", box("led", black, x - 0.18, x + 0.18, -2.5, -2.3, HT - 0.02, HT + 0.03))
        DPX, DPY = 14.3, -5.5
        self.add("body", cyl("dpad", key, (DPX, DPY, HT + 0.05), "z", 1.7, 0.14, seg=40, bevel=0.04))
        self.add("body", cyl("ok_ring", mgrey, (DPX, DPY, HT + 0.125), "z", 0.74, 0.02, seg=32))
        self.add("body", cyl("ok", key, (DPX, DPY, HT + 0.15), "z", 0.68, 0.12, seg=32, bevel=0.03))
        self.add("body", text3d("oktxt", txt, "OK", 0.36, (DPX, DPY, HT + 0.22), "+z", depth_cm=0.02, font=font))
        for (dx, dy, ch) in ((-1.2, 0, "◀"), (1.2, 0, "▶")):
            self.add("body", text3d("arrow", txt, ch, 0.3, (DPX + dx, DPY + dy, HT + 0.13), "+z", depth_cm=0.02, font=font))
        for (x0, x1) in ((12.85, 14.2), (14.5, 15.85)):
            self.add("body", box("btn", key, x0, x1, -9.2, -8.4, HT - 0.02, HT + 0.1, bevel=0.05))
        self.add("body", text3d("xmark", red, "X", 0.5, (15.18, -8.8, HT + 0.11), "+z", depth_cm=0.02, font=font))
        self.add("body", box("wrench", txt, 13.2, 13.85, -8.84, -8.76, HT + 0.1, HT + 0.115))

        # ---------------------------------------------------------------- front face details
        self.add("body", extrude("logo_plate", dark, rrect(6.0, 1.75, 0.4, cx=-0.1, cy=16.12), axis="y",
                                 a0=-hd - 0.08, a1=-hd + 0.05, bevel=0.03))
        self.add("body", text3d("logo", txt, "xerox", 1.85, (-0.1, -hd - 0.09, 16.15), "-y", depth_cm=0.03, font=font))
        self.add("body", cyl("pb_ring", self.mat("ringgrey", "#7d8287", 0.4), (PBX, -hd + 0.06, PBZ), "y", 0.8, 0.1, seg=32))
        self.add("body", cyl("pb", white, (PBX, -hd + 0.0, PBZ), "y", 0.66, 0.1, seg=32))
        self.add("body", cyl("pb_icon", dark, (PBX, -hd - 0.06, PBZ), "y", 0.33, 0.02, seg=24))
        self.add("body", cyl("pb_icon2", white, (PBX, -hd - 0.075, PBZ), "y", 0.25, 0.02, seg=24))
        self.add("body", box("pb_bar", dark, PBX - 0.05, PBX + 0.05, -hd - 0.1, -hd - 0.07, PBZ - 0.05, PBZ + 0.4))
        self.add("body", box("pb_gap", white, PBX - 0.14, PBX + 0.14, -hd - 0.09, -hd - 0.076, PBZ + 0.1, PBZ + 0.4))

        # ---------------------------------------------------------------- back details
        self.add("body", box("handle", black, -3.65, 3.1, hd - 0.45, hd - 0.2, 3.48, 5.71))
        self.add("body", box("dup_tab", blue, -1.63, 1.3, hd - 0.25, hd - 0.1, 3.6, 4.7))
        # port notch: Ethernet, small slot, USB-B on the recessed face; a raised bar on its inner side
        yf = hd - self.PORT_RECESS
        ex, ez = self.ETH
        self.add("body", box("rj45_rim", mgrey, ex - 0.62, ex + 0.62, yf - 0.05, yf + 0.03, ez - 0.68, ez + 0.68))
        self.add("body", box("rj45", grey, ex - 0.5, ex + 0.5, yf - 0.05, yf + 0.045, ez - 0.56, ez + 0.56))
        self.add("body", box("slot_rim", mgrey, -17.2, -15.85, yf - 0.05, yf + 0.03, 14.6, 15.25))
        self.add("body", box("slot", grey, -17.1, -15.95, yf - 0.05, yf + 0.045, 14.7, 15.15))
        ux, uz = self.USB
        self.add("body", box("usb", black, ux - 0.5, ux + 0.5, yf - 0.08, yf + 0.05, uz - 0.5, uz + 0.5))
        self.add("body", box("port_bar", white, nx - 0.85, nx, yf - 0.1, yf + 0.5, 13.15, nz1, bevel=0.08))
        # power notch: the C14 inlet, mounted vertically, flush with the notch floor
        qy = hd - self.PWR_RECESS
        px, pz = self.PWR
        self.add("body", box("inlet", black, px - 0.88, px + 0.88, qy - 0.3, qy + 0.05, pz - 1.37, pz + 1.36))
        for (dx, dz) in ((0.0, 0.7), (0.0, -0.7), (-0.35, 0.0)):
            self.add("body", box("pin", mgrey, px + dx - 0.07, px + dx + 0.07, qy + 0.0, qy + 0.09, pz + dz - 0.25, pz + dz + 0.25))

        # ---------------------------------------------------------------- feet
        for sx in (-1, 1):
            for sy in (-1, 1):
                self.add("body", cyl("foot", rubber, (sx * 15.2, sy * 14.2, Z0 / 2 + 0.03), "z", 0.55, Z0 + 0.06, seg=16))

        # ---------------------------------------------------------------- cassette (moving)
        cap = self.slab("cap", white, Z0, ZS - 0.06, r_bot=0.5)
        cut(cap, box("cap_keep", None, -hw - 1, hw + 1, -hd - 1, -hd + 1.6, Z0 - 1, ZS + 1), op="INTERSECT")
        tray = box("tray", trayc, -14.2, 14.2, -hd + 1.5, hd - 2.8, Z0 + 0.35, ZS - 0.5)
        cut(tray, box("tray_in", None, -13.9, 13.9, -hd + 1.9, hd - 3.1, Z0 + 0.7, ZS))
        gprof = fillet([(-8.0, Z0 - 1), (7.6, Z0 - 1), (7.6, 2.7), (-8.0, 2.7)], [0, 0, 0.5, 0.5])
        cut(cap, extrude("grip_cut", None, gprof, axis="y", a0=-hd - 1, a1=-hd + 2.3))
        cut(tray, extrude("grip_cut2", None, gprof, axis="y", a0=-hd - 1, a1=-hd + 2.3))
        GX0, GX1, GZ0, GZ1 = 10.8, 11.45, 1.1, 5.25
        cut(cap, box("gauge_cut", None, GX0, GX1, -hd - 1, -hd + 0.12, GZ0, GZ1))
        self.add("cassette", cap, kind="moving", pivot=(0, -hd, Z0))
        self.add("cassette", tray)
        self.add("cassette", box("gauge_bg", black, GX0, GX1, -hd + 0.08, -hd + 0.14, GZ0, GZ1))
        self.add("cassette", box("gauge_ind", blue, GX0 + 0.1, GX1 - 0.1, -hd + 0.05, -hd + 0.09, 4.15, 4.65))
        self.add("cassette", box("gauge_low", txt, GX0 + 0.15, GX1 - 0.15, -hd + 0.05, -hd + 0.09, 1.5, 1.95))
        for z in (1.45, 4.95):
            self.add("cassette", box("gauge_icon", grey, 11.75, 12.3, -hd - 0.02, -hd + 0.01, z - 0.28, z + 0.28))
        self.add("cassette", box("paper", paper, -10.5, 10.5, -hd + 2.5, hd - 3.3, Z0 + 0.72, Z0 + 3.2))

        # ---------------------------------------------------------------- paper stop flap (moving)
        flap = box("flap", navy, fx0, fx1, fy0, fy1, HT - 0.24, HT - 0.02, bevel=0.06)
        self.add("flap", flap, kind="moving", pivot=((fx0 + fx1) / 2, fy0 + 0.12, HT - 0.13))

        # ---------------------------------------------------------------- cables (power + Ethernet)
        self.plug_cable("cable_power", "C13v", x=px, z=pz, back_y=hd, recess=self.PWR_RECESS)
        self.plug_cable("cable_eth", "RJ45", x=ex, z=ez, back_y=hd, recess=self.PORT_RECESS)
        self.notes.append("Height 23.2 cm includes the raised LCD pod; the top cover itself is 21.6 cm (216 mm).")
        self.notes.append("Power inlet and data ports sit in two notches cut into the rounded rear corner on the left side "
                          "(seen from the front), open to the back and the side, about 3.6 cm (power) and 3.0 cm "
                          "(Ethernet/USB) deep (real photo 12_back_ports_real). The C13 plug body fits inside; only its "
                          "strain relief and the bent cable stick out behind the printer.")
        self.notes.append("With A4 (or Legal) paper the tray extends out of the back at the bottom centre under a dust "
                          "cover (ITPro; real photo 11_back34_real). About 2 cm for A4, more for Legal; not modelled.")

    def states(self):
        return {
            "printing": [("rot", "flap", "x", 100)],
            "refill": [("move", "cassette", (0, -26, 0))],
        }
