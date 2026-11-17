"""
HP Officejet J4580 All-in-One (CB780A) - the user's current printer, the reference on the shelf.

Every number comes from printers/HP OfficeJet J4580 (current printer)/measurements/MEASUREMENTS.md.
Coordinates used below: u = cm from the left edge seen from the front, d = cm from the back plane toward
the front, z = cm above the shelf. Builder frame: x = u - W/2, y = YB - d (FRONT = -y, BACK = +y).

Depth, the important part (user's shelf measurements + side photos 05 / 04):
  d = 0      back plane (cream base and dark scanner are flush; the user's 4.5 cm wall gap is measured to it)
  d = 23.5   front face of the base where it meets the shelf (user: 24.5 - 4.5 + 3.5)
  d = 23.7   the same front face at the scanner seam (photo 05: the front wall is nearly vertical)
  d = 24.1   front of the document feeder at its top
  d = 27.0   front edge of the control panel, which hangs 3.5 cm in front of the base at z 10.3-15.3
             (photo 05: panel front / base front = 400 / 348 px = 1.149, times 23.5)
Closed (main tray pushed in) the printer is 43.35 x 27.0 x 21.67 cm. HP's listed depth (40.15 cm) is with
the main tray pulled out.
"""
import json
import math
import numpy as np

W = 43.35            # width (HP)
WC = W - 0.2         # the cream base is a hair narrower than the dark scanner unit above it
H = 21.67            # height to the top of the document feeder (HP)
D_PANEL = 27.0       # front edge of the control panel = front of the closed body (side photo 05: 1.149 x base)
YB = D_PANEL / 2     # back plane (y = 0 is the middle of the closed depth)
D_BASE0 = 23.5       # base front face at shelf level
D_BASE1 = 23.7       # base front face at the scanner seam (z 12.8); photo 05: nearly vertical
D_SCAN = 23.8        # scanner base front
D_LID = 24.0         # lid / feeder front at z 15.3
D_FEED_TOP = 24.1    # feeder front at its top
Z_FOOT = 0.4
Z_SEAM = 12.8        # cream base / dark scanner seam
Z_SCAN = 13.62       # top of the scanner base (glass level)
Z_LID0, Z_LID1 = 13.7, 16.1

# control panel wedge, side profile (d, z)
P_UNDER = 10.3
P_LIP = (26.9, 11.6)      # top of the cream lip = bottom of the dark face
P_TOP = (24.4, 15.25)     # top of the dark face
_t = np.array([-(P_TOP[0] - P_LIP[0]), P_TOP[1] - P_LIP[1]])      # (dy, dz) going up the face
_t = _t / np.linalg.norm(_t)
PN = np.array([0.0, -_t[1], _t[0]])     # outward normal (front-up)
PNT = tuple(float(c) for c in PN)

# moving parts
TRAY_OUT = 11.8      # main tray slides out (lip from d 23.5 to 35.3)
EXT_OUT = 19.6       # extender total travel (front end from d 23.3 to 42.9)
FLAP_UP = 155.0      # paper stop: folded back over the extender -> forward and 25 deg up
LID_DEG = -75.0      # scanner lid with the feeder, hinged at the back


def U(u):
    """cm from the left edge seen from the front -> x."""
    return u - W / 2


def D(d):
    """cm from the back plane -> y."""
    return YB - d


def base_front(z):
    """d of the base's front face at height z (leans forward going up, small radius at the bottom)."""
    d = D_BASE0 + (z - 0.9) * (D_BASE1 - D_BASE0) / (Z_SEAM - 0.9)
    if z < 0.8:
        d -= 0.4 - math.sqrt(max(0.0, 0.16 - (0.8 - z) ** 2))
    return d


def base_back(z):
    """d of the base's back face at height z: vertical, with a large radius (2.6) at the bottom."""
    if z >= 3.0:
        return 0.0
    return 2.6 - math.sqrt(max(0.0, 2.6 ** 2 - (3.0 - z) ** 2))


def loft(name, mat, sections):
    """Closed mesh through plan outlines: sections = [(z, [(x, y), ...]), ...], same point count each."""
    n = len(sections[0][1])
    verts, faces = [], []
    for z, pts in sections:
        assert len(pts) == n
        verts += [(float(x), float(y), float(z)) for x, y in pts]
    for k in range(len(sections) - 1):
        a, b = k * n, (k + 1) * n
        faces += [[a + i, a + (i + 1) % n, b + (i + 1) % n, b + i] for i in range(n)]
    faces.append(list(range(n))[::-1])
    faces.append([(len(sections) - 1) * n + i for i in range(n)])
    return mesh_obj(name, verts, faces, mat)


def inter(a, b):
    """a = a AND b, applied now."""
    cut(a, b, op="INTERSECT")
    bake(a)
    bpy.data.objects.remove(b)
    return a


class Builder(Printer):
    def build(self):
        cream = self.mat("cream", "#cdbf93", 0.6)
        tray_c = self.mat("tray", "#cbb98a", 0.6)
        feeder_c = self.mat("feeder_tray", "#cfc296", 0.55)
        dark = self.mat("dark", "#1e2226", 0.5)
        darker = self.mat("darker", "#121416", 0.6)
        gloss = self.mat("panel_face", "#0c0e10", 0.18)
        black = self.mat("black", "#0a0a0a", 0.7)
        rubber = self.mat("rubber", "#1a1a1a", 0.9)
        glass = self.mat("glass", "#10161c", 0.06)
        pad = self.mat("pad", "#ecebe6", 0.7)
        white = self.mat("label", "#e9e9e4", 0.45)
        keytext = self.mat("key_text", "#c9c9c4", 0.5)
        silver = self.mat("badge", "#c9cacc", 0.3, metal=0.8)
        blue = self.mat("start", "#3f86ad", 0.35)
        red = self.mat("cancel", "#8f2626", 0.4)
        lcd = self.mat("lcd", "#6f7a5a", 0.3, emit="#5d6644", emit_strength=0.3)
        led = self.mat("power_led", "#e8d23a", 0.3, emit="#f0dc40", emit_strength=2.0)
        icon = self.mat("icons", "#5aa6d8", 0.4, emit="#3f8fd0", emit_strength=0.6)
        purple = self.mat("dc_socket", "#8a3d8f", 0.4)
        estar = self.mat("energy_star", "#1f74b8", 0.4)
        roller = self.mat("roller", "#d8d8d2", 0.4)
        font = find_font("DejaVuSans-Bold")

        # ---------------------------------------------------------------- base (cream)
        def base_sections(x0, x1, proud=0.0, z0=Z_FOOT, z1=Z_SEAM, rf=(1.6, 2.0)):
            secs = []
            for z in [0.4, 0.44, 0.52, 0.64, 0.8, 1.1, 1.5, 2.0, 2.5, 3.0, Z_SEAM]:
                if z < z0 - 1e-6 or z > z1 + 1e-6:
                    continue
                ins = 0.0 if z >= 0.8 else 0.4 - math.sqrt(max(0.0, 0.16 - (0.8 - z) ** 2))
                yf, yb = D(base_front(z) + proud), D(base_back(z))
                secs.append((z, fillet([(x0 + ins, yf), (x1 - ins, yf), (x1 - ins, yb), (x0 + ins, yb)],
                                       [rf[0], rf[1], 1.5, 1.5], n=6)))
            return secs

        base = loft("base", cream, base_sections(-WC / 2, WC / 2))

        # paper opening over the main tray: u 10.6-33.8, z 1.35-6.4, plus the two small holes beside it
        def opening_cutter(name):
            prof = fillet([(U(10.6), 1.35), (U(33.8), 1.35), (U(33.8), 6.4), (U(10.6), 6.4)], [0.15, 0.15, 0.5, 0.5])
            return extrude(name, None, prof, axis="y", a0=D(25.5), a1=D(17.4))

        # rear notch (paper path): u_behind 5.2-33.3 at the back plane, narrowing to 10.3-32.2 at 3.5 cm depth
        def notch_cutter(name):
            prof = fillet([(U(W - 33.3), -1), (U(W - 5.2), -1), (U(W - 5.2), 7.6), (U(W - 33.3), 7.6)], [0, 0, 1.3, 1.3])
            c = extrude(name, None, prof, axis="y", a0=YB - 3.5, a1=YB + 1)
            plan = [(U(W - 33.5), YB + 1.2), (U(W - 4.8), YB + 1.2), (U(W - 5.2), YB), (U(W - 10.3), YB - 3.5),
                    (U(W - 10.3), YB - 4), (U(W - 32.2), YB - 4), (U(W - 32.2), YB - 3.5), (U(W - 33.3), YB)]
            return inter(c, extrude(name + "_plan", None, plan, axis="z", a0=-2, a1=9))

        def side_recess(name, sx):
            if sx > 0:      # right side: d 1.5-18.8, z 1.0-9.8 (the door wraps the front corner)
                prof = rrect(17.3, 8.8, 1.3, cx=(D(1.5) + D(18.8)) / 2, cy=5.4)
            else:           # left side: d 6.9-23.0, z 1.0-9.3
                prof = rrect(16.1, 8.3, 1.3, cx=(D(6.9) + D(23.0)) / 2, cy=5.15)
            a0, a1 = (WC / 2 - 0.12, WC / 2 + 1) if sx > 0 else (-WC / 2 - 1, -WC / 2 + 0.12)
            return extrude(name, None, prof, axis="x", a0=a0, a1=a1)

        def port_recess(name):
            prof = fillet([(U(2.55), 8.2), (U(14.15), 8.2), (U(14.15), 10.8), (U(2.55), 10.8)], 0.5)
            return extrude(name, None, prof, axis="y", a0=YB - 0.3, a1=YB + 1)

        for c in (opening_cutter("open_cut"), notch_cutter("notch_cut"), side_recess("srec_r", 1),
                  side_recess("srec_l", -1), port_recess("port_rec"),
                  box("hole_l", None, U(9.4), U(10.2), D(25), D(22.9), 1.6, 2.8),
                  box("hole_r", None, U(33.8), U(34.6), D(25), D(22.9), 1.6, 2.8),
                  # the dark hinge frame dips into the cream back: u_behind 8-39.3, z 12.2-12.8
                  box("frame_cut", None, U(W - 39.3), U(W - 8.0), YB - 0.25, YB + 1, 12.2, 13.0)):
            cut(base, c)
        self.add("body", base)

        # ---------------------------------------------------------------- front access door (dark)
        # u 7.0 -> right edge, z 4.3 -> seam; wraps the front-right corner onto the right side to d 21.6
        dsec = []
        for z in (4.3, Z_SEAM):
            yf = D(base_front(z) + 0.08)
            dsec.append((z, fillet([(U(6.0), yf), (W / 2, yf), (W / 2, D(21.6)), (U(6.0), D(21.6))], [0.01, 2.1, 0.3, 0.01])))
        door = loft("door", dark, dsec)
        dmask = fillet([(U(7.0), 4.3), (W / 2 + 1, 4.3), (W / 2 + 1, Z_SEAM + 1), (U(7.0), Z_SEAM + 1)], [2.8, 0, 0, 0])
        inter(door, extrude("door_mask", None, dmask, axis="y", a0=D(26), a1=D(20)))
        cut(door, opening_cutter("open_cut2"))
        self.add("body", door)

        # inside the paper opening: dark liner, serrated top strip, white star wheels
        y_in = D(18.0)
        self.add("body", box("cav_back", darker, U(10.6), U(33.8), y_in - 0.3, y_in + 0.2, 1.3, 6.5))
        self.add("body", box("cav_top", black, U(10.6), U(33.8), D(23.4), y_in, 5.7, 6.45))
        self.add("body", box("cav_l", black, U(10.55), U(10.72), D(23.3), y_in, 2.9, 6.4))
        self.add("body", box("cav_r", black, U(33.68), U(33.85), D(23.3), y_in, 4.2, 6.4))
        self.add("body", box("cav_floor", darker, U(10.6), U(33.8), D(23.0), y_in, 1.2, 1.36))
        for u in (12.4, 15.3, 18.7, 22.2, 25.4, 28.2, 30.9):
            self.add("body", box("star", roller, U(u - 0.45), U(u + 0.45), D(23.55), D(23.2), 4.95, 5.2))
            self.add("body", box("star_arm", darker, U(u - 0.6), U(u + 0.6), D(23.5), D(22.6), 5.2, 5.75))
        # Energy Star sticker
        self.add("body", box("estar", estar, U(1.6), U(3.4), D(base_front(2.75) + 0.03), D(base_front(2.75) - 0.2), 1.8, 3.7))

        # rear notch interior: dark paper-path wall and rollers
        self.add("body", box("notch_wall", darker, U(W - 32.2), U(W - 10.3), YB - 3.75, YB - 3.45, 0.9, 7.5))
        for ub in (13.0, 18.3, 24.3, 28.6):
            self.add("body", cyl("rr", black, (U(W - ub), YB - 3.2, 4.4), "x", 0.55, 1.6, seg=14))

        # back: label, port panel sockets
        self.add("body", box("label", white, U(18.05), U(24.75), YB - 0.1, YB - 0.01, 8.6, 10.6))
        self.add("body", box("barcode", darker, U(18.4), U(23.2), YB - 0.1, YB - 0.005, 9.45, 10.0))
        # USB-B socket in a small raised collar that comes back up to the back plane (u_behind 31.4, z 9.5)
        ux, uz = U(W - 31.4), 9.5
        self.add("body", box("usb_collar", cream, ux - 0.7, ux + 0.7, YB - 0.35, YB - 0.01, uz - 0.7, uz + 0.7, bevel=0.06, seg=1))
        self.add("body", box("usb_hole", black, ux - 0.45, ux + 0.45, YB - 0.4, YB - 0.003, uz - 0.42, uz + 0.42))
        # HP purple 3-pin DC socket (u_behind 33.9, z 9.35), flush with the panel floor
        px, pz = U(W - 33.9), 9.35
        self.add("body", box("dc", purple, px - 0.8, px + 0.8, YB - 0.4, YB - 0.22, pz - 0.55, pz + 0.55))
        # RJ11 pair 1-LINE / 2-EXT (u_behind 38.8, z 8.9-10.2)
        fx = U(W - 38.8)
        self.add("body", box("rj11", black, fx - 1.2, fx + 1.2, YB - 0.4, YB - 0.2, 8.9, 10.2))
        self.add("body", box("rj11_plug", white, fx + 0.2, fx + 1.0, YB - 0.38, YB - 0.12, 9.1, 10.0))

        # feet: rear pair at u_behind 2.1 and 39.8 (back photo), front pair set back from the front edge (photo 25)
        for u, d in ((3.55, 3.6), (41.25, 3.6), (4.5, 21.3), (38.85, 21.3)):
            self.add("body", cyl("foot", rubber, (U(u), D(d), Z_FOOT / 2 + 0.01), "z", 0.85, Z_FOOT + 0.02, seg=16))

        # ---------------------------------------------------------------- scanner base (dark) + glass
        def shell_plan(d_front, d_back=0.0):
            return fillet([(-W / 2, D(d_front)), (W / 2, D(d_front)), (W / 2, D(d_back)), (-W / 2, D(d_back))],
                          [1.6, 2.1, 1.5, 1.5], n=8)

        scan = extrude("scanner", dark, shell_plan(D_SCAN), axis="z", a0=Z_SEAM, a1=Z_SCAN, bevel=0.1, seg=2)
        self.add("body", scan)
        # seam filler (reads as the dark groove between the scanner base and the lid)
        self.add("body", extrude("seam", darker, fillet([(-W / 2 + 0.2, D(D_SCAN - 0.2)), (W / 2 - 0.2, D(D_SCAN - 0.2)),
                                                         (W / 2 - 0.2, D(0.2)), (-W / 2 + 0.2, D(0.2))], 1.4, n=6),
                                 axis="z", a0=Z_SCAN - 0.3, a1=Z_SCAN + 0.02))
        self.add("body", box("glass", glass, U(6.5), U(37.3), D(23.1), D(1.3), Z_SCAN, Z_SCAN + 0.05))
        self.add("body", box("adf_glass", glass, U(4.2), U(6.0), D(23.1), D(1.3), Z_SCAN, Z_SCAN + 0.05))
        # dark hinge frame on the back (u_behind 8-39.3, z 12.2-13.0), filling the cut in the cream base
        fr = fillet([(U(W - 39.3), 12.2), (U(W - 8.0), 12.2), (U(W - 8.0), 13.0), (U(W - 39.3), 13.0)], [0.6, 0.6, 0, 0])
        self.add("body", extrude("hinge_frame", dark, fr, axis="y", a0=YB - 0.3, a1=YB))

        # ---------------------------------------------------------------- control panel (static)
        prof = fillet([(D(23.0), P_UNDER), (D(26.7), P_UNDER), (D(D_PANEL), 10.72), (D(P_LIP[0]), P_LIP[1]),
                       (D(P_TOP[0]), P_TOP[1]), (D(23.0), P_TOP[1])], [0, 0.3, 0.3, 0.2, 0, 0])
        panel = extrude("panel", cream, prof, axis="x", a0=-W / 2, a1=U(22.1))
        # right end: swept up in the front view (r 3.2) and swept back in plan (r 3.4)
        emask = fillet([(-W / 2 - 1, P_UNDER - 0.05), (U(22.1), P_UNDER - 0.05), (U(22.1), 17), (-W / 2 - 1, 17)], [0, 3.2, 0, 0], n=10)
        inter(panel, extrude("panel_emask", None, emask, axis="y", a0=D(29), a1=D(21)))
        pmask = fillet([(-W / 2 - 1, D(D_PANEL + 0.2)), (U(22.1), D(D_PANEL + 0.2)), (U(22.1), D(21)), (-W / 2 - 1, D(21))],
                       [0, 3.6, 0, 0], n=10)
        inter(panel, extrude("panel_pmask", None, pmask, axis="z", a0=8, a1=18))
        self.add("body", panel)
        # the panel's left end is dark above the cream lip (photos 05, 22)
        lcap = fillet([(D(23.0), 11.0), (D(26.9), 11.0), (D(P_LIP[0] - 0.05), P_LIP[1]), (D(P_TOP[0] - 0.05), P_TOP[1] - 0.02),
                       (D(23.0), P_TOP[1] - 0.02)], [0, 0.2, 0.2, 0, 0])
        self.add("body", extrude("panel_lcap", gloss, lcap, axis="x", a0=-W / 2 - 0.03, a1=-W / 2 + 0.25))
        # dark cap where the panel meets the feeder front
        self.add("body", box("panel_cap", gloss, U(0.3), U(21.6), D(P_TOP[0] + 0.08), D(D_LID - 0.1), P_TOP[1] - 0.05, P_TOP[1] + 0.06))

        def on_face(u, z, off=0.0):
            d = P_LIP[0] - (z - P_LIP[1]) * (P_LIP[0] - P_TOP[0]) / (P_TOP[1] - P_LIP[1])
            return np.array([U(u), D(d), z]) + PN * off

        def face_plate(name, mat, poly_uz, h=0.08, off=0.0):
            P = np.asarray(poly_uz, float)
            n = len(P)
            verts = [on_face(u, z, off) for u, z in P] + [on_face(u, z, off + h) for u, z in P]
            faces = [list(range(n))[::-1], list(range(n, 2 * n))] + \
                    [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
            return mesh_obj(name, verts, faces, mat)

        # dark glossy face (u 0.3-21.5, z 11.7-15.2); lower-right corner swept with r 3.0
        self.add("body", face_plate("panel_face", gloss, fillet([(0.3, 11.72), (21.5, 11.72), (21.5, 15.2), (0.3, 15.2)],
                                                                 [0.9, 3.0, 0.25, 0.25], n=10), h=0.07, off=-0.02))
        # LCD (u 7.7-14.3, z 13.4-14.4)
        self.add("body", face_plate("lcd", lcd, rrect(6.6, 1.0, 0.1, cx=11.0, cy=13.9), h=0.04, off=0.05))
        # keypad 3 x 4
        for i, u in enumerate((3.0, 4.65, 6.3)):
            for j, z in enumerate((14.95, 14.3, 13.65, 12.95)):
                self.add("body", face_plate("key%d%d" % (i, j), darker, rrect(1.25, 0.46, 0.12, cx=u, cy=z), h=0.16, off=0.05))
                self.add("body", face_plate("kt%d%d" % (i, j), keytext, rrect(0.5, 0.1, 0.03, cx=u - 0.1, cy=z), h=0.01, off=0.21))
        # power button with its lit ring
        self.add("body", cyl("pwr_ring", led, on_face(1.1, 12.9, 0.06), PNT, 0.45, 0.06, seg=20))
        self.add("body", cyl("pwr", darker, on_face(1.1, 12.9, 0.12), PNT, 0.34, 0.14, seg=20))
        # function icons under the LCD
        for u in (8.2, 9.5, 11.0, 12.5, 13.8):
            self.add("body", face_plate("icon", icon, rrect(0.7, 0.42, 0.08, cx=u, cy=12.75), h=0.01, off=0.05))
        # arrows / OK cluster with its white outline, back, cancel, start, setup
        self.add("body", face_plate("nav_ring", white, rrect(3.7, 0.9, 0.3, cx=17.65, cy=14.5), h=0.03, off=0.05))
        self.add("body", face_plate("nav", darker, rrect(3.45, 0.66, 0.22, cx=17.65, cy=14.5), h=0.1, off=0.07))
        self.add("body", face_plate("ok", keytext, rrect(0.9, 0.5, 0.12, cx=17.65, cy=14.5), h=0.03, off=0.17))
        self.add("body", cyl("back_btn", darker, on_face(15.75, 13.75, 0.1), PNT, 0.3, 0.14, seg=16))
        self.add("body", face_plate("cancel", red, rrect(0.7, 0.6, 0.1, cx=16.2, cy=12.95), h=0.12, off=0.05))
        self.add("body", face_plate("start", blue, rrect(1.9, 0.95, 0.18, cx=18.0, cy=13.05), h=0.14, off=0.05))
        self.add("body", cyl("setup", darker, on_face(20.3, 14.8, 0.08), PNT, 0.24, 0.1, seg=12))
        # model name above the LCD
        lab = text3d("panel_label", white, "HP Officejet J4580 All-in-One", 0.3, (0, 0, 0), "-y", 0.02, font=font)
        tilt = math.atan2(P_LIP[0] - P_TOP[0], P_TOP[1] - P_LIP[1])
        lab.data.transform(Matrix.Rotation(-tilt, 4, "X"))
        lab.data.transform(Matrix.Translation(Vector(on_face(11.4, 14.85, 0.06) * CM)))
        self.add("body", lab)

        # ---------------------------------------------------------------- lid: plate + feeder + feeder tray
        parts = []
        lp = extrude("lid_plate", dark, shell_plan(D_LID), axis="z", a0=Z_LID0, a1=Z_LID1, bevel=0.3, seg=3)
        # recessed hinge bar across the back (u_behind 8.6-36.4, z 13.75-15.0)
        cut(lp, box("hinge_cut", None, U(W - 36.4), U(W - 8.6), YB - 0.5, YB + 1, 13.5, 15.0))
        # shallow document-output well on the lid top, right of the feeder
        well = fillet([(U(22.3), D(22.9)), (U(42.1), D(22.9)), (U(42.1), D(1.3)), (U(22.3), D(1.3))], 1.3)
        cut(lp, extrude("well_cut", None, well, axis="z", a0=Z_LID1 - 0.22, a1=Z_LID1 + 1))
        parts.append(lp)
        parts.append(box("hinge_bar", darker, U(W - 36.4), U(W - 8.6), YB - 0.55, YB - 0.42, 13.7, 15.0))
        parts.append(box("lid_pad", pad, U(6.2), U(37.6), D(23.3), D(1.1), Z_SCAN + 0.06, Z_LID0 + 0.02))

        # document feeder body (left): rounded top-left edge, S-curved right side that runs into the lid
        scurve = [(16.9, 20.7), (17.6, 19.4), (18.3, 18.1), (19.0, 17.1), (19.9, 16.5), (21.5, Z_LID1 + 0.02)]
        fprof = np.array([(U(0.2), Z_LID0 + 0.05), (U(0.75), H), (U(16.0), H)] + [(U(u), z) for u, z in scurve] +
                         [(U(21.5), Z_LID0 + 0.05)])
        fprof = fillet(fprof, [0, 2.2, 1.0, 0.8, 1.5, 1.5, 1.5, 1.0, 0, 0], n=8)
        feeder = extrude("feeder", dark, fprof, axis="y", a0=D(25), a1=YB + 1)
        sprof = fillet([(D(D_LID), Z_LID0), (D(0.05), Z_LID0), (D(0.05), H + 0.001), (D(D_FEED_TOP + 0.03), H + 0.001)],
                       [0, 0, 2.5, 1.3], n=8)
        inter(feeder, extrude("feeder_side", None, sprof, axis="x", a0=-W / 2 - 1, a1=U(23)))
        parts.append(feeder)
        # document slot on the feeder's right face, above the tray
        parts.append(box("slot", black, U(17.0), U(18.3), D(21.9), D(1.7), 19.9, 20.9))
        # HP badge on the feeder front (u 7.8-9.95, z 17.9-19.1)
        bx = U(8.9)
        yb_ = D(D_LID + (18.5 - 15.3) * (D_FEED_TOP - D_LID) / (20.4 - 15.3))
        parts.append(extrude("badge", silver, rrect(2.15, 1.25, 0.25, cx=bx, cy=18.5), axis="y", a0=yb_ - 0.05, a1=yb_ + 0.1))
        parts.append(text3d("hp", darker, "hp", 0.8, (bx, yb_ - 0.06, 18.47), "-y", 0.03, font=font))

        # feeder input tray: thin plate from the feeder (z ~20.6) down to a flat part (z 18.3-18.6), d 1.1-22.1
        TD0, TD1 = 1.1, 22.1
        top = [(38.05, 18.62), (27.0, 18.95), (24.0, 19.1), (21.5, 19.6), (19.5, 20.3), (17.2, 20.9)]
        bot = [(17.2, 20.45), (19.5, 19.85), (21.5, 19.15), (24.0, 18.65), (27.0, 18.5), (37.95, 18.25), (38.15, 18.42)]
        ftray = extrude("feeder_tray", feeder_c, [(U(u), z) for u, z in top + bot], axis="y", a0=D(TD1), a1=D(TD0))
        tplan = fillet([(U(16), D(TD1)), (U(38.2), D(TD1)), (U(38.2), D(TD0)), (U(16), D(TD0))], [0, 2.5, 2.5, 0], n=8)
        inter(ftray, extrude("tray_plan", None, tplan, axis="z", a0=17, a1=22))
        # window in the tray (u 25.5-33.5, d 7.0-16.4)
        cut(ftray, extrude("tray_window", None, rrect(8.0, 9.4, 0.9, cx=U(29.5), cy=D(11.7)), axis="z", a0=17, a1=20))
        parts.append(ftray)
        # cheeks under the tray next to the feeder: dark at the front, tray-coloured at the back
        cheek = [(19.3, Z_LID1 - 0.05), (21.0, 16.2), (22.5, 16.5), (24.0, 17.0), (25.5, 17.7), (27.0, 18.52),
                 (24.0, 18.67), (21.5, 19.17), (19.5, 19.87), (19.3, 19.9)]
        cp = [(U(u), z) for u, z in cheek]
        parts.append(extrude("cheek_f", dark, cp, axis="y", a0=D(TD1 - 0.05), a1=D(TD1 - 0.45)))
        parts.append(extrude("cheek_b", feeder_c, cp, axis="y", a0=D(TD0 + 0.45), a1=D(TD0 + 0.05)))
        # two paper guides at the feeder end of the tray: a fin plus a flat grip tab each
        gfin = fillet([(U(16.8), 20.3), (U(16.8), 21.4), (U(22.0), 21.4), (U(23.0), 20.4), (U(23.0), 19.25)],
                      [0, 0.3, 0.9, 0.6, 0], n=6)
        for dd, s in ((3.9, -1), (19.6, 1)):
            parts.append(extrude("guide_fin", feeder_c, gfin, axis="y", a0=D(dd) - 0.15, a1=D(dd) + 0.15))
            y0, y1 = sorted((D(dd), D(dd + s * 2.0)))
            parts.append(box("guide_tab", feeder_c, U(18.2), U(22.6), y0, y1, 19.55, 19.85, bevel=0.08, seg=1))
        lid = join(parts, "lid")
        self.add("lid", lid, kind="moving", pivot=(0, YB - 0.6, 14.6))

        # ---------------------------------------------------------------- main tray (cassette), extender, stop
        t = []
        tw0, tw1 = U(10.75), U(33.65)
        df, dr = 23.5, 3.7                    # front lip and rear end (closed)
        fl = fillet([(tw0, D(df)), (tw1, D(df)), (tw1, D(dr)), (tw0, D(dr))], [1.2, 1.2, 0.01, 0.01], n=6)
        t.append(extrude("tray_floor", tray_c, fl, axis="z", a0=1.38, a1=1.62))
        t.append(box("tray_wall_l", tray_c, tw0, tw0 + 0.4, D(df - 1.2), D(dr), 1.4, 3.2, bevel=0.1, seg=1))
        t.append(box("tray_wall_r", tray_c, tw1 - 0.4, tw1, D(df - 1.2), D(dr), 1.4, 3.9, bevel=0.1, seg=1))
        # front rim: left and right parts; the middle stays low so the extender can slide out
        for a, b in ((tw0, U(14.5)), (U(29.9), tw1)):
            rim = extrude("tray_rim", tray_c, fl, axis="z", a0=1.4, a1=2.5)
            inter(rim, box("rim_keep", None, a, b, D(df + 0.1), D(df - 1.25), 1, 3))
            t.append(rim)
        t.append(box("tray_rim_mid", tray_c, U(14.5), U(29.9), D(df), D(df - 0.5), 1.4, 1.95))
        # paper-width guide (dark slider at the left)
        t.append(box("width_guide", darker, U(11.3), U(12.9), D(df - 0.6), D(df - 3.2), 1.62, 3.4, bevel=0.1, seg=1))
        self.add("cassette", join(t, "cassette"), kind="moving")

        e = []
        ef = df - 0.2                          # extender front end (closed)
        e.append(box("ext_plate", tray_c, U(14.8), U(29.6), D(ef), D(ef - 12.2), 1.63, 1.85))
        for u in (14.8, 29.6):
            e.append(box("ext_rail", tray_c, U(u) - 0.3, U(u) + 0.3, D(ef), D(ef - 12.2), 1.63, 2.35, bevel=0.1, seg=1))
        self.add("extender", join(e, "extender"), kind="moving")

        # paper stop: hinged at the extender's front end, folded back over it when closed
        flap = box("flap", tray_c, U(15.7), U(28.7), D(ef), D(ef - 5.0), 1.87, 2.1, bevel=0.07, seg=1)
        self.add("flap", flap, kind="moving", pivot=(0, D(ef), 1.98))

        # ---------------------------------------------------------------- cables (plugs on a flat back)
        # Sized so the squashed cables end 4.5 cm behind the back plane, as the user measured on the shelf.
        PLUGS["USB-B"] = (1.2, 1.1, 2.6, 1.05, 0.45, 2.0)     # moulded USB-B plug, into the collar at the back plane
        PLUGS["HP DC"] = (1.7, 1.0, 2.4, 1.55, 0.40, 1.8)     # HP 3-pin DC plug from the 32 V brick, 3 mm into the panel
        self.plug_cable("cable_power", "HP DC", x=px, z=pz, back_y=YB, recess=0.3)
        self.plug_cable("cable_usb", "USB-B", x=ux, z=uz, back_y=YB, recess=0.0, mat=self.mat("usb_cable", "#d9d9d4", 0.5))

        self.base_info = {
            "what": "the cream base, the part that rests on the shelf (the control panel overhangs it)",
            "back_plane_y_cm": round(YB, 3),
            "base_front_at_shelf_y_cm": round(D(D_BASE0), 3),
            "base_depth_at_shelf_cm": D_BASE0,
            "base_front_at_seam_y_cm": round(D(D_BASE1), 3),
            "base_depth_at_seam_cm": D_BASE1,
            "panel_front_y_cm": round(D(D_PANEL), 3),
            "panel_underside_z_cm": P_UNDER,
            "frame": "builder frame: cm, front = -y, back = +y, y = 0 at the middle of the closed depth",
        }
        self.notes.append("Closed = main paper tray pushed in. HP's listed depth (40.15 cm) is with the tray pulled out.")
        self.notes.append("The base rests on the shelf from the back plane to 23.5 cm (user: 24.5 - 4.5 + 3.5); its front "
                          "wall is nearly vertical (23.7 cm at the scanner seam); the control panel reaches 27.0 cm at z 10.3-15.3.")
        self.notes.append("USB-B and the HP DC plug go into a flat back (3 mm panel): 4.5 cm wall-to-back measured on the shelf.")
        self.notes.append("Lid open 75 deg: the document feeder swings about 6.5 cm behind the back plane.")

    def states(self):
        out = (0, -TRAY_OUT, 0)
        ext = (0, -EXT_OUT, 0)
        return {
            "printing": [("move", "cassette", out), ("move", "extender", ext), ("move", "flap", ext),
                         ("rot", "flap", "x", FLAP_UP)],
            "refill": [("move", "cassette", out), ("move", "extender", out), ("move", "flap", out)],
            "lid_open": [("rot", "lid", "x", LID_DEG)],
        }

    def export(self, glb_path=None, json_path=None):
        geom = Printer.export(self, glb_path, json_path)
        json_path = json_path or os.path.join(DATA_DIR, self.id + ".geom.json")
        geom["base"] = self.base_info
        with open(json_path, "w") as f:
            json.dump(geom, f, indent=1)
        return geom
