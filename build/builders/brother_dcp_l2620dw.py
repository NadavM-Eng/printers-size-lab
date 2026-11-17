"""
Brother DCP-L2620DW: mono laser all-in-one with a flatbed scanner (no document feeder).

Every number comes from printers/Brother DCP-L2620DW/measurements/MEASUREMENTS.md: Brother's
orthographic outline drawing (photo 91) for the side profile and the heights, the studio and marketplace
photos for widths and details, all scaled to the official 41.0 x 39.9 x 27.2 cm.

Frame: cm, Z up, FRONT = -Y, BACK = +Y, x = 0 centre of the width, y = 0 centre of the closed depth,
z = 0 under the feet. Depth "from the front" d maps to y = d - 19.95.
"""

from mathutils import Matrix  # noqa: F401  (also injected by the kit)
import printer_kit as _K

# The kit's studio lights are much brighter than the reference studio photos; dim them for the
# photo comparisons only (affects renders, not the exported model).
_K.LIGHT_GAIN = 0.28

W, D, H = 41.0, 39.9, 27.2
YF, YR = -D / 2, D / 2              # front face of the lower body / rear-most line (scanner unit)
FOOT = 0.3                          # feet height; the body starts here
Z_SEAM = 8.9                        # paper tray / front cover seam
Z_KINK = 14.2                       # lower side wall / upper band (also the underside of the rear overhang)
Z_LIP = 18.65                       # top of the front cover (front edge of the output tray)
Z_BASE = 20.5                       # underside of the grey scanner base
Z_BLK = 23.4                        # grey scanner base / black scanner frame
Z_LID = 25.5                        # scanner top / lid underside
D_WRAP = 2.2                        # tray front and front cover wrap this far around the sides
D_COL = 6.5                         # front of the upper band (the columns beside the paper exit)
D_SC = 6.0                          # front face of the scanner unit and the lid
D_LB = 35.4                         # lower back face: both sockets are on it
D_UB = 38.6                         # rear face of the upper block (the "ears" above the sockets)
Y_LB, Y_UB, Y_SC, Y_COL = YF + D_LB, YF + D_UB, YF + D_SC, YF + D_COL
S_LOW = 0.065                       # lean of the lower side walls (cm per cm of height)
EXIT_X0, EXIT_X1 = -16.5, 13.2      # paper exit opening
PAN_X0, PAN_X1 = -19.5, 7.1         # control panel
PAN_TILT = 8.0                      # panel top falls toward the front (deg)


def hw_low(z):
    """Half width of the lower body (tray, front cover, engine) at height z: 35.7 cm at the feet, 37.5 at 14.2."""
    return 17.85 + S_LOW * (z - FOOT)


def hw_band(z):
    """Half width of the upper band: 37.5 cm at its foot, 39.0 cm under the scanner base."""
    return hw_low(Z_KINK) + (19.5 - hw_low(Z_KINK)) * (z - Z_KINK) / (Z_BASE - Z_KINK)


S_BAND = (19.5 - hw_low(Z_KINK)) / (Z_BASE - Z_KINK)


def xform(ob, M):
    ob.data.transform(M)
    ob.data.update()
    return ob


def rot_about(ob, axis, deg, pivot):
    """Rotate an object's mesh about an axis through pivot (cm)."""
    p = Vector(np.asarray(pivot, float) * CM)
    M = Matrix.Translation(p) @ Matrix.Rotation(math.radians(deg), 4, axis) @ Matrix.Translation(-p)
    return xform(ob, M)


def loft(name, mat, levels, n=6):
    """A solid made of rounded rectangles stacked in z.
    levels (bottom to top): (z, x0, x1, y0, y1, r) with r one radius or four
    (front-left, front-right, rear-right, rear-left)."""
    rings = []
    for (z, x0, x1, y0, y1, r) in levels:
        P = fillet([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], r, n)
        rings.append([(u, v, z) for u, v in P])
    m = len(rings[0])
    assert all(len(r) == m for r in rings), "loft rings differ in size"
    verts = [p for ring in rings for p in ring]
    faces = [list(range(m))[::-1], [(len(rings) - 1) * m + i for i in range(m)]]
    for k in range(len(rings) - 1):
        for i in range(m):
            a, b = k * m + i, k * m + (i + 1) % m
            faces.append([a, b, b + m, a + m])
    return mesh_obj(name, verts, faces, mat)


def side_box(name, mat, side, y0, y1, z0, z1, depth, proud=0.0, band=False):
    """A thin box lying on a leaning side wall (side = +1 right, -1 left).
    depth: thickness into the wall; proud: how far it stands out of the wall surface.
    band=True puts it on the upper band, otherwise on the lower side wall."""
    zc = (z0 + z1) / 2
    xs = hw_band(zc) if band else hw_low(zc)
    slope = S_BAND if band else S_LOW
    if side > 0:
        ob = box(name, mat, xs - depth, xs + proud, y0, y1, z0, z1)
    else:
        ob = box(name, mat, -xs - proud, -xs + depth, y0, y1, z0, z1)
    ang = math.degrees(math.atan(slope)) * (1 if side > 0 else -1)
    return rot_about(ob, "Y", ang, (side * xs, 0, zc))


class Builder(Printer):

    def build(self):
        # ---------------------------------------------------------------- materials
        body = self.mat("body", "#3f4044", 0.62)
        black = self.mat("black", "#232427", 0.5)
        lidm = self.mat("lid", "#222326", 0.45)
        paneltop = self.mat("panel_top", "#33363b", 0.6)
        trim = self.mat("trim", "#54575b", 0.55)
        dark = self.mat("dark", "#0d0e0f", 0.8)
        seam = self.mat("seam", "#18191a", 0.7)
        silver = self.mat("logo", "#c4c6c8", 0.35, metal=0.3)
        lcd = self.mat("lcd", "#8db4cc", 0.25, emit="#8db4cc", emit_strength=0.35)
        key = self.mat("key", "#1b1c1e", 0.5)
        legend = self.mat("legend", "#a9abad", 0.5)
        start = self.mat("start", "#2fbf4f", 0.35, emit="#2fbf4f", emit_strength=1.2)
        stop = self.mat("stop", "#d23a3a", 0.35, emit="#d23a3a", emit_strength=0.9)
        plate = self.mat("plate", "#a9acb2", 0.5)
        green = self.mat("green", "#58c043", 0.45)
        rubber = self.mat("rubber", "#111111", 0.9)
        glass = self.mat("glass", "#1b2a33", 0.08)
        white = self.mat("white", "#e9e9e6", 0.6)
        padm = self.mat("pad", "#2c2e31", 0.85)

        # ---------------------------------------------------------------- lower body (engine)
        # two tapered solids that meet at the columns: the front slab (tray front + front cover, with the
        # rounded "pillow" top) and the engine behind it up to the lower back
        def chamfer_levels(y0, y1, r):
            return [(FOOT, -hw_low(FOOT) + 0.7, hw_low(FOOT) - 0.7, y0, y1, r),
                    (FOOT + 0.3, -hw_low(FOOT) + 0.25, hw_low(FOOT) - 0.25, y0, y1, r),
                    (FOOT + 0.9, -hw_low(1.2), hw_low(1.2), y0, y1, r)]

        def front_solid(name):
            r = [1.8, 1.8, 0.05, 0.05]
            lv = chamfer_levels(YF, Y_COL + 0.1, r)
            # front top edge r 2.0, side top edges r 1.0
            for z in (16.65, 17.2, 17.65, 18.0, 18.3, 18.5, 18.6, Z_LIP):
                zf, zs = Z_LIP - 2.0, Z_LIP - 1.0
                dy = 0.0 if z <= zf else 2.0 - math.sqrt(max(0.0, 4.0 - (z - zf) ** 2))
                dx = 0.0 if z <= zs else 1.0 - math.sqrt(max(0.0, 1.0 - (z - zs) ** 2))
                h = hw_low(z) - dx
                lv.append((z, -h, h, YF + dy, Y_COL + 0.1, r))
            return loft(name, body, lv)

        r_rear = [0.05, 0.05, 1.0, 1.0]
        lower = loft("lower", body, chamfer_levels(Y_COL + 0.1, Y_LB, r_rear) + [
            (Z_KINK + 0.05, -hw_low(Z_KINK), hw_low(Z_KINK), Y_COL + 0.1, Y_LB, r_rear)])
        front = front_solid("front")
        # the tray front (a separate moving part) leaves the body; 0.1 cm seam above it
        cut(front, box("c_trayfront", None, -30, 30, YF - 2, YF + D_WRAP, -1, Z_SEAM + 0.05))
        # tray bay behind it
        c_bay = box("c_bay", None, -17.2, 17.2, YF, YF + 34.6, 0.9, 8.6)
        cut(front, c_bay)
        cut(lower, c_bay)
        # recessed name plate on the front cover
        cut(front, box("c_plate", None, -14.8, 14.8, YF - 1, YF + 0.15, 10.5, 15.5, bevel=0.08, seg=1))
        # manual feed slot just above the name plate
        cut(front, box("c_mf", None, -5.0, 5.0, YF - 1, YF + 0.7, 15.7, 16.4))
        # back: bezel of the power inlet, USB channel, lever recess (all shallow: the lower back is flat)
        cut(lower, box("c_pwr", None, 14.6, 17.5, Y_LB - 0.3, Y_LB + 2, 9.9, 13.5))
        cut(lower, box("c_pwr_in", None, 15.25, 16.85, Y_LB - 1.9, Y_LB + 2, 10.3, 12.9))
        cut(lower, box("c_usb", None, -17.4, -15.2, Y_LB - 0.4, Y_LB + 2, 6.1, 13.1, bevel=0.3, seg=2))
        cut(lower, box("c_lever", None, -2.5, 4.6, Y_LB - 0.9, Y_LB + 2, 3.4, 5.9, bevel=0.3, seg=2))
        self.add("body", lower)
        self.add("body", front)
        self.add("body", box("mf_slit", dark, -4.9, 4.9, YF + 0.62, YF + 0.72, 15.72, 16.38))

        # ---------------------------------------------------------------- upper band + rear overhang
        band = loft("band", body, [
            (Z_KINK, -hw_band(Z_KINK), hw_band(Z_KINK), Y_COL, Y_UB, [0.05, 0.05, 1.5, 1.5]),
            (Z_BASE + 0.05, -hw_band(Z_BASE), hw_band(Z_BASE), Y_COL, Y_UB, [0.05, 0.05, 1.5, 1.5])])
        # paper exit: opening under the scanner, floor falling toward the back
        cut(band, box("c_exit", None, EXIT_X0, EXIT_X1, Y_COL - 1, YF + 27.0, Z_LIP, Z_BASE + 1))
        ramp = extrude("c_ramp", None, [(Y_COL - 1, Z_LIP + 0.2), (Y_COL - 1, Z_LIP - 0.1), (YF + 27.0, 14.6),
                                        (YF + 27.0, Z_LIP + 0.2)], axis="x", a0=EXIT_X0, a1=EXIT_X1)
        cut(band, ramp)
        # rear: between the two ears the block ends higher (the back cover shows below it)
        cut(band, box("c_rear_mid", None, -15.3, 14.2, Y_LB, Y_UB + 1, Z_KINK - 1, 17.7))
        # dark cavity in the upper back
        cut(band, box("c_cav", None, -5.4, 11.3, Y_UB - 2.0, Y_UB + 1, 18.5, Z_BASE + 1))
        # carrying grips: a pocket on each side near the top
        for s in (-1, 1):
            cut(band, side_box("c_grip", None, s, YF + 17.1, YF + 26.4, 16.7, 19.3, 1.6, proud=2, band=True))
        self.add("body", band)
        self.add("body", box("exit_dark", dark, EXIT_X0 + 0.05, EXIT_X1 - 0.05, YF + 26.9, YF + 26.98, 14.7, Z_BASE))
        self.add("body", box("cav_in", dark, -5.3, 11.2, Y_UB - 2.05, Y_UB - 1.95, 18.6, Z_BASE))
        for s in (-1, 1):
            self.add("body", side_box("grip_in", dark, s, YF + 17.3, YF + 26.2, 16.85, 19.15, 1.65, proud=-1.5,
                                      band=True))

        # ---------------------------------------------------------------- scanner unit
        base = loft("scan_base", body, [
            (Z_BASE, -19.5, 19.5, Y_SC, YR, 1.0),
            (Z_BLK, -20.4, 20.4, Y_SC, YR, 1.0)])
        # the paper exit opening reaches up into the base
        cut(base, box("c_exit_base", None, EXIT_X0, EXIT_X1, Y_SC - 1, Y_SC + 2.5, Z_BASE - 1, 21.9,
                      bevel=0.4, seg=2))
        cut(base, box("c_cav_b", None, -5.4, 11.3, YR - 2.6, YR + 1, Z_BASE - 1, 21.4))
        self.add("body", base)
        self.add("body", box("cav_in_b", dark, -5.3, 11.2, YR - 2.65, YR - 2.55, Z_BASE, 21.35))

        frame = extrude("scan_frame", black, rrect(W, YR - Y_SC, 1.0, cx=0, cy=(Y_SC + YR) / 2), axis="z",
                        a0=Z_BLK, a1=Z_LID, bevel=0.15, seg=2)
        cut(frame, box("c_notch_s", None, -4.9, 4.9, Y_SC - 1, Y_SC + 1.2, Z_LID - 0.5, Z_LID + 1))
        self.add("body", frame)
        # glass and the scan-head strip (seen with the lid up)
        self.add("body", box("glass", glass, -12.0, 19.2, YF + 7.6, YF + 34.0, Z_LID - 0.05, Z_LID + 0.004))
        self.add("body", box("strip", dark, -17.5, -12.4, YF + 7.6, YF + 34.0, Z_LID - 0.05, Z_LID + 0.004))
        self.add("body", box("strip_w", white, -13.6, -12.9, YF + 8.0, YF + 33.6, Z_LID - 0.05, Z_LID + 0.008))

        # ---------------------------------------------------------------- lid (document cover)
        lid_back = YR - 0.3
        lv = []
        for z, ins in ((Z_LID + 0.02, 0.06), (Z_LID + 0.15, 0.0), (H - 0.6, 0.0), (H - 0.3, 0.12), (H - 0.1, 0.33),
                       (H, 0.6)):
            lv.append((z, -W / 2 + ins, W / 2 - ins, Y_SC + ins, lid_back - ins, 1.0))
        lid = loft("lid", lidm, lv)
        cut(lid, box("c_notch_l", None, -4.9, 4.9, Y_SC - 1, Y_SC + 1.2, Z_LID - 1, Z_LID + 1.1))
        lid_parts = [lid]
        # "DCP" badge near the middle of the lid
        yb = YF + 24.5
        for (x0, x1, y0, y1) in [(-1.8, 1.8, yb - 0.5, yb - 0.44), (-1.8, 1.8, yb + 0.44, yb + 0.5),
                                 (-1.8, -1.74, yb - 0.5, yb + 0.5), (1.74, 1.8, yb - 0.5, yb + 0.5)]:
            lid_parts.append(box("badge", silver, x0, x1, y0, y1, H - 0.01, H + 0.012))
        lid_parts.append(text3d("dcp", silver, "DCP", 0.62, (0, yb, H + 0.005), "+z",
                                depth_cm=0.02, font=find_font("DejaVuSans-Bold")))
        # document pad under the lid: dark grey (photo 13 shows the lid's underside dark, not white)
        lid_parts.append(box("pad", padm, -12.0, 19.2, YF + 7.8, YF + 33.8, Z_LID - 0.005, Z_LID + 0.05))
        self.add("lid", join(lid_parts, "lid_join"), kind="moving", pivot=(0, YR - 0.6, Z_LID + 0.2))
        # hinge blocks on the back of the lid (static)
        for hx in (-9.2, 16.1):
            self.add("body", box("hinge", black, hx - 1.1, hx + 1.1, YR - 1.3, YR, Z_LID - 0.5, H - 0.25,
                                 bevel=0.15))

        # ---------------------------------------------------------------- control panel
        y0p, y1p = YF + 1.0, Y_SC + 0.3
        z_back = Z_LID                                       # panel top where it meets the scanner
        plan = fillet([(PAN_X0, y0p), (PAN_X1, y0p), (PAN_X1, y1p), (PAN_X0, y1p)], [2.0, 2.5, 0, 0])
        pan = extrude("panel", paneltop, plan, axis="z", a0=22.85, a1=z_back + 0.4, bevel=0.45)
        cutter = box("c_pan_top", None, -30, 30, -40, 10, 0, 10)
        xform(cutter, Matrix.Translation(Vector((0, Y_SC * CM, z_back * CM))))
        rot_about(cutter, "X", PAN_TILT, (0, Y_SC, z_back))
        cut(pan, cutter)
        self.add("body", pan)
        # lighter lower band, set back a little
        band_l = fillet([(PAN_X0 + 0.25, y0p + 0.3), (PAN_X1 - 0.3, y0p + 0.3), (PAN_X1 - 0.3, y1p),
                         (PAN_X0 + 0.25, y1p)], [1.8, 2.3, 0, 0])
        self.add("body", extrude("pan_low", trim, band_l, axis="z", a0=21.9, a1=22.9, bevel=0.12))

        def on_face(ob, yc, zlift=0.0):
            """ob built flat at z = 0 around (x, yc); move it onto the inclined panel top."""
            ztop = z_back - (Y_SC - yc) * math.tan(math.radians(PAN_TILT))
            xform(ob, Matrix.Translation(Vector((0, 0, (ztop + zlift) * CM))))
            rot_about(ob, "X", PAN_TILT, (0, yc, ztop))
            return ob

        def fy(d):                # d = cm behind the panel's front edge
            return y0p + d

        # LCD bezel and screen
        self.add("body", on_face(box("bezel", dark, -18.3, -10.9, fy(1.0), fy(3.9), -0.05, 0.05), fy(2.45)))
        self.add("body", on_face(box("screen", lcd, -17.4, -11.7, fy(1.5), fy(3.4), -0.05, 0.07), fy(2.45)))
        r_front, r_back = fy(1.55), fy(3.0)
        kx = {"clear": -9.4, "pad": -6.6, "scan": -3.7, "opt": -1.3, "go": 1.45, "power": 4.25}

        def keycap(name, m, x, yc, w=1.15, d=0.78, bar=None, bw=0.22):
            self.add("body", on_face(box(name, m, x - w / 2, x + w / 2, yc - d / 2, yc + d / 2, -0.05, 0.13,
                                         bevel=0.1, seg=2), yc))
            if bar is not None:
                self.add("body", on_face(box(name + "_bar", bar, x - w * bw, x + w * bw, yc - 0.07, yc + 0.07,
                                             0.0, 0.145), yc))

        keycap("k_clear", key, kx["clear"], r_back, bar=legend)
        keycap("k_menu", key, kx["clear"] - 0.25, r_front, bar=legend)
        keycap("k_up", key, kx["pad"] + 0.2, r_back + 0.35, w=0.75, d=0.9)
        keycap("k_ok", key, kx["pad"], (r_front + r_back) / 2, w=1.0, d=0.75, bar=legend)
        keycap("k_down", key, kx["pad"] - 0.2, r_front - 0.35, w=0.75, d=0.9)
        keycap("k_scan", key, kx["scan"], r_back, bar=legend)
        keycap("k_id", key, kx["scan"] - 0.2, r_front)
        keycap("k_opt", key, kx["opt"], r_back, bar=legend)
        keycap("k_wifi", plate, kx["opt"] - 0.15, r_front)
        keycap("k_stop", key, kx["go"], r_back, w=1.6, d=0.85, bar=stop, bw=0.3)
        keycap("k_start", key, kx["go"] - 0.15, r_front, w=1.6, d=0.85, bar=start, bw=0.3)
        pw = cyl("power", key, (kx["power"], (r_front + r_back) / 2, 0.04), "z", 0.5, 0.18)
        self.add("body", on_face(pw, (r_front + r_back) / 2))

        # ---------------------------------------------------------------- paper tray (moving)
        cfront = front_solid("cas_front")
        cut(cfront, box("c_cas_keep", None, -30, 30, YF - 2, YF + D_WRAP - 0.02, -1, Z_SEAM - 0.07), op="INTERSECT")
        notch = extrude("c_grip_notch", None, fillet([(-5.2, FOOT - 1), (5.2, FOOT - 1), (4.7, 3.0), (-4.7, 3.0)],
                                                     [0, 0, 0.5, 0.5]), axis="y", a0=YF - 1, a1=YF + 1.7)
        cut(cfront, notch)
        tray = box("cas_tray", body, -17.0, 17.0, YF + D_WRAP - 0.1, YF + 34.4, 1.0, 8.4)
        cut(tray, box("c_tray_in", None, -16.3, 16.3, YF + 2.8, YF + 33.8, 1.6, 9.5))
        paper = box("paper", white, -10.5, 10.5, YF + 3.4, YF + 33.1, 1.6, 3.8)
        gshadow = box("grip_shadow", dark, -4.9, 4.9, YF + 1.66, YF + 1.74, FOOT + 0.05, 2.95)
        self.add("cassette", join([cfront, tray, paper, gshadow], "cas_join"), kind="moving", pivot=(0, YF, FOOT))

        # ---------------------------------------------------------------- output support flap (moving)
        hinge_y, hinge_z = YF + 1.5, 18.58
        flap = box("flap", body, -4.0, 4.0, hinge_y, hinge_y + 4.5, Z_LIP - 0.02, Z_LIP + 0.14, bevel=0.06, seg=2)
        self.add("flap", flap, kind="moving", pivot=(0, hinge_y, hinge_z))
        # thin dark outline of the flap's pocket in the cover top
        for (x0, x1, y0, y1) in [(-4.15, -4.05, hinge_y + 0.5, hinge_y + 4.6), (4.05, 4.15, hinge_y + 0.5, hinge_y + 4.6)]:
            self.add("body", box("flap_gap", seam, x0, x1, y0, y1, Z_LIP - 0.05, Z_LIP + 0.012))
        # two paper guide fins on the cover top
        for s in (-1, 1):
            fin = extrude("fin", body, fillet([(YF + 1.2, 18.2), (YF + 4.4, 18.5), (YF + 4.4, 19.7), (YF + 3.5, 19.7)],
                                              [0, 0, 0.25, 0.25]), axis="x", a0=s * 7.5 - 0.5, a1=s * 7.5 + 0.5,
                          bevel=0.15, seg=2)
            self.add("body", fin)

        # ---------------------------------------------------------------- front details
        self.add("body", text3d("logo", silver, "brother", 1.8, (0, YF + 0.13, 13.0), "-y",
                                depth_cm=0.05, font=find_font("DejaVuSans-Bold")))
        # dark line behind the tray / front cover seam
        self.add("body", box("seam_front", seam, -hw_low(Z_SEAM) + 1.0, hw_low(Z_SEAM) - 1.0, YF + 0.5, YF + 0.6,
                             Z_SEAM - 0.2, Z_SEAM + 0.1))

        # ---------------------------------------------------------------- side details
        for s in (-1, 1):
            # tray / front cover wrap seam, and the seam between tray and cover on the wrap
            self.add("body", side_box("seam_v", seam, s, YF + D_WRAP - 0.05, YF + D_WRAP + 0.05, FOOT + 0.4, Z_KINK,
                                      0.02, proud=0.03))
            # seam between the lower side wall and the upper band
            self.add("body", side_box("seam_k", seam, s, YF + D_WRAP, Y_LB - 0.6, Z_KINK - 0.05, Z_KINK + 0.05,
                                      0.02, proud=0.03))
        # right side: vent grille under the grip (grid of square holes)
        gy0, gy1, gz0, gz1 = YF + 18.6, YF + 25.8, 8.6, 16.2
        self.add("body", side_box("vent_r", dark, 1, gy0, gy1, gz0, gz1, 0.02, proud=0.03))
        for k in range(8):
            yv = gy0 + k * (gy1 - gy0) / 7.0 - 0.11
            self.add("body", side_box("vbar", body, 1, yv, yv + 0.22, gz0, gz1, 0.02, proud=0.06))
        for k in range(9):
            zv = gz0 + k * (gz1 - gz0) / 8.0 - 0.11
            self.add("body", side_box("hbar", body, 1, gy0, gy1, zv, zv + 0.22, 0.02, proud=0.06))
        # left side: vent grille low, just behind the front wrap
        ly0, ly1, lz0, lz1 = YF + 3.2, YF + 8.6, 4.4, 11.6
        self.add("body", side_box("vent_l", dark, -1, ly0, ly1, lz0, lz1, 0.02, proud=0.03))
        for k in range(7):
            yv = ly0 + k * (ly1 - ly0) / 6.0 - 0.1
            self.add("body", side_box("vbar", body, -1, yv, yv + 0.2, lz0, lz1, 0.02, proud=0.06))
        for k in range(10):
            zv = lz0 + k * (lz1 - lz0) / 9.0 - 0.1
            self.add("body", side_box("hbar", body, -1, ly0, ly1, zv, zv + 0.2, 0.02, proud=0.06))

        # ---------------------------------------------------------------- back details (lower back face)
        yb = Y_LB
        # back cover outline (opens down) and its pull tab
        for (x0, x1, z0, z1) in [(-14.5, 14.4, 16.7, 16.8), (-14.5, 14.4, 7.2, 7.3),
                                 (-14.5, -14.4, 7.2, 16.8), (14.3, 14.4, 7.2, 16.8)]:
            self.add("body", box("bc_line", seam, x0, x1, yb - 0.03, yb + 0.03, z0, z1))
        self.add("body", box("bc_tab", body, -2.0, 2.1, yb - 0.1, yb + 0.5, 15.1, 16.3, bevel=0.15, seg=2))
        # 2-sided tray rear edge (a band standing a little proud) and the tray rear below it
        self.add("body", box("dx_band", body, -13.0, 13.4, yb - 0.2, yb + 0.3, 5.05, 7.2, bevel=0.1, seg=2))
        for (x0, x1, z0, z1) in [(-11.0, 12.8, 4.85, 4.95), (-11.0, -10.9, 1.5, 4.9), (12.7, 12.8, 1.5, 4.9)]:
            self.add("body", box("tr_line", seam, x0, x1, yb - 0.03, yb + 0.03, z0, z1))
        # green 2-sided tray lever in its dark recess
        self.add("body", box("lever_bg", dark, -2.4, 4.5, yb - 0.92, yb - 0.85, 3.5, 5.8))
        self.add("body", box("lever", green, -0.9, 2.7, yb - 0.9, yb - 0.4, 4.1, 4.9, bevel=0.1, seg=2))
        # power inlet (C14 turned 90 deg: long side vertical), its rim 0.3 cm inside the back face
        self.add("body", box("inlet", dark, 14.9, 17.2, yb - 0.32, yb - 0.28, 10.1, 13.3))
        self.add("body", box("inlet_in", dark, 15.3, 16.8, yb - 1.92, yb - 1.85, 10.35, 12.85))
        for pz in (11.0, 11.6, 12.2):
            self.add("body", box("pin", plate, 15.95, 16.15, yb - 1.85, yb - 0.9, pz - 0.2, pz + 0.2))
        # USB channel: light plate (blank where network models have the LAN socket) with the USB-B socket low
        self.add("body", box("usb_plate", plate, -17.3, -15.3, yb - 0.42, yb - 0.37, 6.2, 13.0))
        self.add("body", box("usb", dark, -16.7, -15.5, yb - 0.4, yb - 0.33, 7.0, 8.0))
        # corner vents (seen from behind at the left = the printer's right)
        for k in range(6):
            z0 = 2.1 + k * 0.62
            self.add("body", box("rvent", dark, 13.7, 14.9, yb - 0.02, yb + 0.03, z0, z0 + 0.3))
        for k in range(5):
            x0 = 13.9 + k * 0.68
            self.add("body", box("rvent2", dark, x0, x0 + 0.36, yb - 0.02, yb + 0.03, 1.2, 1.9))

        # ---------------------------------------------------------------- feet
        for fx in (-15.0, 15.0):
            for fy_ in (YF + 3.2, Y_LB - 3.2):
                self.add("body", cyl("foot", rubber, (fx, fy_, FOOT / 2 + 0.03), "z", 0.9, FOOT + 0.06))

        # ---------------------------------------------------------------- cables
        # C13 plug: the inlet is turned 90 deg, so the plug face is 1.6 wide x 2.2 tall
        PLUGS["C13v"] = (1.6, 2.2, 3.4, 2.4, 0.75, 3.0)
        # both sockets are on the lower back, 4.5 cm in front of the rear line (side outline 91: lower back
        # at 35.5 cm, overhang block to 39.9 cm); the inlet sits in a ~1 cm pocket, the USB-B at the
        # bottom of a ~0.6 cm channel (back photo 03 shadows)
        self.plug_cable("cable_power", "C13v", x=16.05, z=11.6, back_y=Y_LB, recess=1.0)
        self.plug_cable("cable_usb", "USB-B", x=-16.1, z=7.5, back_y=Y_LB, recess=0.6)

        self.notes += [
            "Official 41.0 x 39.9 x 27.2 cm; depth runs from the front cover / tray face to the rear of the "
            "scanner unit. The lower back with both sockets is 4.5 cm in front of that line (rear overhang).",
            "Lower body narrower than the scanner (35.7 cm at the feet, 37.5 cm at 14 cm up, 39 cm under the "
            "scanner; sides lean in toward the bottom).",
            "No Ethernet: USB-B only. Power inlet C14 (C13 cord), turned 90 deg, flush on the lower back.",
        ]

    def states(self):
        return {
            # flip the support flap up and forward over the front edge
            "printing": [("rot", "flap", "x", 150)],
            # paper tray slides straight out of the front (Brother: pull it completely out)
            "refill": [("move", "cassette", (0, -30.0, 0))],
            # scanner lid raised on its rear hinges
            "lid_open": [("rot", "lid", "x", -80)],
        }
