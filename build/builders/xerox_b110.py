"""
Xerox B110 (B110V_BI) - compact mono laser printer, print only, USB + Wi-Fi.

Every number comes from references/xerox-b110/MEASUREMENTS.md (official 33.1 x 21.5 x 18.8 cm, photo
proportions from the Xerox catalogue photo, the B110 user guide drawings and frames of Xerox's own
"Xerox B110 Unbox and Assemble" video).

Frame: cm, Z up, FRONT = -Y, BACK = +Y, +X = the printer's right seen from the front (control-panel
side), x = 0 centre of the width, y = 0 centre of the depth, z = 0 under the feet.

Moving parts
  input_tray   Tray 1: the LOWER front panel (about 7 cm tall) folds down 90 deg (hinge near its bottom edge);
               the upper front panel with the logo stays (B110 video frame 13, drawing 05, Phaser 3020 photo 16)
  tray_ext     the tray's fold-out extension: hidden when closed, shown lying in front of the open door so the
               open tray reaches 13.5 cm in front of the body (HP's 350 mm maximum depth for the twin HP 107)
  support      output support flap, hinged at the front of the output tray, flips forward and up
  support_ext  its extension, slides out along the flap
  paper        an A4 stack lying on the open Tray 1 (hidden when closed)
"""
import math

import numpy as np

W, D, H = 33.1, 21.5, 18.8
YF, YB = -D / 2, D / 2                      # front / back of the closed outline (-10.75 / +10.75)
FOOT = 0.3                                  # feet height
ZW = 15.9                                   # top of the white body
ZC0 = 15.7                                  # bottom of the top cover
WHITE_IN = 0.1                              # the white body is inset under the top cover (each side)
Y_WF = YF + 0.2                             # white front face (the cover lip overhangs 0.2)
Y_WB = YB - 0.2                             # white back face (the rib at the far corner reaches YB)
Y_CB = YB - 0.1                             # back of the top cover

# Tray 1 door (front panel between the side columns)
DOOR_X0, DOOR_X1 = -12.05, 11.85
DOOR_Z0, DOOR_Z1 = 0.45, 7.3                  # lower front panel only
PANEL_Z1 = 15.75                            # top of the fixed upper front panel
TRAY_REACH = 13.5                           # open tray tip in front of the body
DOOR_T = 1.0
DOOR_PIVOT = (0.0, Y_WF + DOOR_T - 0.05, 2.2)
DOOR_OPEN = 90.0

# output tray recess in the top cover (side profile, y-z) and the support flap
REC_X0, REC_X1 = -12.5, 11.7
FLOOR_A = (-7.1, 17.9)                      # front of the tray floor
FLOOR_B = (-0.4, 16.4)                      # back of the tray floor, start of the exit chute
FLOOR_SLOPE = math.degrees(math.atan2(FLOOR_A[1] - FLOOR_B[1], FLOOR_B[0] - FLOOR_A[0]))   # ~12.6 deg
HOOD_Y0, HOOD_Y1, HOOD_TOP = 1.6, 8.6, 18.6
SUP_W, SUP_L, SUP_T = 13.0, 6.4, 0.25
SUP_PIVOT = (0.0, FLOOR_A[0] + 0.05, FLOOR_A[1] + 0.02)
SUP_ANGLE = 30.0                            # flap angle above horizontal when extended (video 10, 13; 3020 photo 18)
SUP_ROT = 180.0 - SUP_ANGLE + FLOOR_SLOPE
EXT_SLIDE = 5.0

# back port strip (seen from behind it is the LEFT end of the back, i.e. the printer's right side)
STRIP_X0 = W / 2 - 4.5
STRIP_RECESS = 0.5
USB_X, USB_Z = W / 2 - 2.3, 10.2
PWR_X, PWR_Z = W / 2 - 3.2, 2.8

# an upright IEC C7 "figure-8" plug: face 0.95 wide x 1.8 tall
PLUGS["C7v"] = (0.95, 1.8, 2.8, 1.8, 0.60, 2.4)


def rounded_slab(name, mat, w, d, cx, cy, z0, z1, R, r_top=0.0, r_bot=0.0, n_arc=5, n_corner=6):
    """A rounded-rectangle plan (w x d, corner radius R) extruded from z0 to z1, with its top and bottom
    outer edges rounded by r_top / r_bot (quarter circles, made of rings of inset outlines)."""
    rings = []

    def ring(inset, z):
        P = rrect(w - 2 * inset, d - 2 * inset, max(R - inset, 0.05), cx, cy, n=n_corner)
        rings.append([(u, v, z) for u, v in P])

    if r_bot > 0:
        for k in range(n_arc + 1):
            th = math.radians(90.0 * k / n_arc)
            ring(r_bot * (1 - math.sin(th)), z0 + r_bot * (1 - math.cos(th)))
    else:
        ring(0.0, z0)
    if r_top > 0:
        for k in range(n_arc + 1):
            th = math.radians(90.0 * k / n_arc)
            ring(r_top * (1 - math.cos(th)), z1 - r_top * (1 - math.sin(th)))
    else:
        ring(0.0, z1)
    n = len(rings[0])
    V = [p for r in rings for p in r]
    F = [list(range(n))[::-1]]
    for i in range(len(rings) - 1):
        a, b = i * n, (i + 1) * n
        F += [[a + j, a + (j + 1) % n, b + (j + 1) % n, b + j] for j in range(n)]
    F.append([(len(rings) - 1) * n + j for j in range(n)])
    return mesh_obj(name, V, F, mat)


class Builder(Printer):

    def build(self):
        white = self.mat("white", "#ebebed", 0.42)
        navy = self.mat("navy", "#273d6f", 0.36)
        tab_m = self.mat("tab", "#415078", 0.4)
        dark = self.mat("dark", "#242425", 0.6)
        inner = self.mat("inner", "#3a3a3c", 0.7)
        roller = self.mat("roller", "#151516", 0.5)
        panel = self.mat("panel", "#343b5f", 0.22)
        btn = self.mat("button", "#2c3152", 0.3)
        badge = self.mat("badge", "#3c3c3e", 0.28)
        txt = self.mat("text", "#f2f2f2", 0.4)
        txt_grey = self.mat("text_grey", "#b9bdc8", 0.4)
        label = self.mat("label", "#d8d8d6", 0.75)
        rubber = self.mat("rubber", "#1c1c1c", 0.9)
        metal = self.mat("metal", "#9a9a9a", 0.35, metal=0.8)
        led_g = self.mat("led_green", "#35d36f", 0.3, emit="#35d36f", emit_strength=2.5)
        led_o = self.mat("led_toner", "#5a3a1c", 0.4)
        paper_m = self.mat("paper", "#f7f7f4", 0.8)
        font_b = find_font("DejaVuSans-Bold")
        font = find_font("DejaVuSans.ttf") or find_font("DejaVuSans")

        # ---- feet ------------------------------------------------------------------------------
        for sx in (-1, 1):
            for sy in (-1, 1):
                self.add("body", cyl("foot", rubber, (sx * 13.0, sy * 7.6, FOOT / 2), "z", 1.0, FOOT, seg=16))

        # ---- white body (sides, back, front columns) --------------------------------------------
        bw, bd = W - 2 * WHITE_IN, Y_WB - Y_WF
        body = rounded_slab("white_body", white, bw, bd, 0.0, (Y_WB + Y_WF) / 2, FOOT, ZW, 1.5,
                            r_top=0.0, r_bot=0.5)
        # cavity behind the Tray 1 door (seen only when the door is open)
        cut(body, box("door_cavity", None, DOOR_X0 - 0.1, DOOR_X1 + 0.1, Y_WF - 1, Y_WF + 3.0, DOOR_Z0 - 0.1, DOOR_Z1 - 0.1))
        # recessed port strip at the back corner on the control-panel side
        cut(body, box("strip_cut", None, STRIP_X0, W / 2 + 1, Y_WB - STRIP_RECESS, YB + 1, 0.7, 15.45))
        # back vents: a band of slots along the top of the back
        for i in range(6):
            z = 12.3 + 0.45 * i
            cut(body, box("bvent%d" % i, None, -8.0, 10.0, Y_WB - 0.25, YB + 1, z, z + 0.22))
        # right-side vents: two groups of slots in the back half
        for z0 in (4.6, 11.2):
            for i in range(5):
                z = z0 + 0.45 * i
                cut(body, box("svent", None, W / 2 - 0.25 - WHITE_IN, W / 2 + 1, 2.0, 7.4, z, z + 0.22))
        # power inlet and USB port openings in the strip
        ys = Y_WB - STRIP_RECESS
        cut(body, box("pwr_cut", None, PWR_X - 0.65, PWR_X + 0.65, ys - 0.7, ys + 0.1, PWR_Z - 1.15, PWR_Z + 1.15))
        cut(body, box("usb_cut", None, USB_X - 0.6, USB_X + 0.6, ys - 0.9, ys + 0.1, USB_Z - 0.55, USB_Z + 0.55))
        self.add("body", body)
        # dark back wall of the door cavity (paper path), dark socket bodies, screw
        self.add("body", box("cavity_back", inner, DOOR_X0, DOOR_X1, Y_WF + 2.95, Y_WF + 3.05, 1.3, DOOR_Z1 - 0.15))
        self.add("body", box("feed_slot", roller, -10.5, 10.5, Y_WF + 2.8, Y_WF + 2.95, 1.6, 2.4))
        self.add("body", box("pwr_inlet", dark, PWR_X - 0.6, PWR_X + 0.6, ys - 0.65, ys - 0.45, PWR_Z - 1.1, PWR_Z + 1.1))
        self.add("body", box("pwr_pins", metal, PWR_X - 0.08, PWR_X + 0.08, ys - 0.45, ys - 0.25, PWR_Z - 0.55, PWR_Z + 0.55))
        self.add("body", box("usb_port", dark, USB_X - 0.55, USB_X + 0.55, ys - 0.85, ys - 0.65, USB_Z - 0.5, USB_Z + 0.5))
        self.add("body", box("usb_tongue", white, USB_X - 0.3, USB_X + 0.3, ys - 0.65, ys - 0.35, USB_Z - 0.2, USB_Z + 0.2))
        self.add("body", cyl("screw", metal, (W / 2 - 1.9, ys + 0.03, 14.0), "y", 0.28, 0.08, seg=12))
        # vertical rib at the far back corner (left side seen from the front)
        self.add("body", box("rib", white, -W / 2 + WHITE_IN + 0.15, -W / 2 + 1.9, Y_WB - 0.3, YB, 0.8, ZW - 0.2,
                             bevel=0.12, seg=2))
        # rating label on the back
        self.add("body", box("label", label, -6.5, 4.0, Y_WB - 0.01, Y_WB + 0.02, 5.0, 9.0))

        # ---- top cover --------------------------------------------------------------------------
        cov = rounded_slab("cover", navy, W, Y_CB - YF, 0.0, (Y_CB + YF) / 2, ZC0, H, 2.0, r_top=1.0, r_bot=0.15)
        # output tray recess: side profile extruded across the recess width
        prof = [(-7.8, H + 1.0), (-7.8, H), FLOOR_A, FLOOR_B, (1.4, 15.95), (3.2, 15.95), (3.2, 16.7),
                (HOOD_Y0, 16.7), (HOOD_Y0, HOOD_TOP), (HOOD_Y1, HOOD_TOP), (HOOD_Y1, H + 1.0)]
        cut(cov, extrude("tray_cut", None, prof, axis="x", a0=REC_X0, a1=REC_X1))
        # finger notch in the front rim for the output support
        cut(cov, box("notch", None, -3.2, 3.0, YF - 1, -7.6, 18.2, H + 1))
        self.add("body", cov)
        # rounded edge of the hood (a thin navy lip over the exit slot)
        self.add("body", cyl("hood_lip", navy, (0.5 * (REC_X0 + REC_X1), HOOD_Y0 + 0.02, 16.85), "x", 0.18,
                             REC_X1 - REC_X0 - 0.1, seg=10))
        # dark paper-exit chute and rollers
        chute = [(-1.2, 16.62), (1.4, 15.99), (3.2, 15.99), (3.2, 16.04), (1.4, 16.04), (-1.2, 16.67)]
        self.add("body", extrude("chute", dark, chute, axis="x", a0=REC_X0 + 0.02, a1=REC_X1 - 0.02))
        for x in (-8.5, -2.9, 2.7, 8.3):
            self.add("body", cyl("roller", roller, (x, 2.1, 16.3), "x", 0.32, 3.6, seg=14))

        # control panel pill on the right rim, buttons, LEDs, "B110"
        pcx, pcy = 14.2, -2.0
        pill = extrude("panel", panel, rrect(2.4, 7.5, 1.15, pcx, pcy, n=8), axis="z", a0=H - 0.25, a1=H + 0.02)
        self.add("body", pill)
        for y, sym in ((pcy + 1.0, "wps"), (pcy - 1.6, "pwr")):
            self.add("body", cyl("btn_" + sym, btn, (pcx, y, H + 0.04), "z", 0.72, 0.06, seg=20))
        self.add("body", cyl("led_status", led_g, (pcx, pcy - 3.0, H + 0.03), "z", 0.13, 0.04, seg=10))
        self.add("body", cyl("led_toner", led_o, (pcx, pcy + 2.75, H + 0.03), "z", 0.13, 0.04, seg=10))
        self.add("body", text3d("model_txt", txt_grey, "B110", 0.55, (pcx, -7.3, H + 0.005), "+z", 0.01, font))

        # ---- Tray 1 door (moving) ---------------------------------------------------------------
        # fixed upper front panel (between the side columns, above the tray door) with the logo badge
        self.add("body", box("front_panel", white, DOOR_X0, DOOR_X1, Y_WF - 0.02, Y_WF + DOOR_T, DOOR_Z1 + 0.06, PANEL_Z1,
                             bevel=0.12, seg=2))
        bz = 11.7
        self.add("body", extrude("badge", badge, rrect(4.8, 1.4, 0.3, -0.1, bz, n=5), axis="y", a0=Y_WF - 0.12,
                                 a1=Y_WF + 0.01))
        self.add("body", text3d("logo", txt, "xerox", 0.9, (-0.1, Y_WF - 0.13, bz - 0.05), "-y", 0.02, font_b))
        door = box("door", white, DOOR_X0, DOOR_X1, Y_WF, Y_WF + DOOR_T, DOOR_Z0, DOOR_Z1, bevel=0.12, seg=2)
        cut(door, box("door_in", None, DOOR_X0 + 1.0, DOOR_X1 - 1.0, Y_WF + DOOR_T - 0.35, Y_WF + DOOR_T + 1,
                      DOOR_Z0 + 2.2, DOOR_Z1 - 0.6))
        parts = [door]
        # paper width guides on the inner face (lie flat when the door is open)
        for gx in (-10.6, 10.4):
            parts.append(box("guide", self.mat("guide", "#d6d6d8", 0.5), gx - 0.4, gx + 0.4, Y_WF + DOOR_T - 0.35,
                             Y_WF + DOOR_T + 0.9, 2.6, 6.6, bevel=0.1, seg=1))
        self.add("input_tray", join(parts, "door_all"), kind="moving", pivot=DOOR_PIVOT)

        # ---- output support flap + extension (moving) ------------------------------------------
        ang = math.radians(FLOOR_SLOPE)
        dirv = np.array([0.0, math.cos(ang), -math.sin(ang)])      # along the floor, toward the back
        nrmv = np.array([0.0, math.sin(ang), math.cos(ang)])       # floor normal
        p0 = np.array(SUP_PIVOT)

        def plate(name, mat, w, L, t, lift, start=0.0):
            a = p0 + dirv * start + nrmv * lift
            b = a + dirv * L
            prof2 = [(a[1], a[2]), (b[1], b[2]), (b[1] + nrmv[1] * t, b[2] + nrmv[2] * t),
                     (a[1] + nrmv[1] * t, a[2] + nrmv[2] * t)]
            return extrude(name, mat, prof2, axis="x", a0=-w / 2, a1=w / 2, bevel=0.06, seg=1)

        sup = plate("support", navy, SUP_W, SUP_L, SUP_T, 0.03)
        # finger tab that sits in the notch of the front rim
        tab = box("tab", tab_m, -3.0, 2.8, YF + 0.35, SUP_PIVOT[1] + 0.3, 18.25, 18.45, bevel=0.06, seg=1)
        self.add("support", join([sup, tab], "support_all"), kind="moving", pivot=SUP_PIVOT)
        ext = plate("support_ext", tab_m, 11.0, 5.6, 0.18, 0.03 + SUP_T, start=0.4)
        self.add("support_ext", ext, kind="moving", pivot=SUP_PIVOT)

        # ---- A4 paper on the open tray (hidden when closed) ------------------------------------
        y_tip = DOOR_PIVOT[1] - (DOOR_Z1 - DOOR_PIVOT[2])          # front edge of the open door
        z_in = DOOR_PIVOT[2] + 0.06                                # inner face of the open door
        y_ext = Y_WF - 0.2 - TRAY_REACH                            # tip of the extended tray
        ext = box("tray_ext", self.mat("tray_ext", "#e4e4e6", 0.5), -11.0, 11.0, y_ext, y_tip + 1.5,
                  z_in - 0.55, z_in - 0.05, bevel=0.1, seg=1)
        self.add("tray_ext", ext, kind="moving", hidden=True)
        p_front = y_ext + 1.0
        self.add("paper", box("paper", paper_m, -10.5, 10.5, p_front, p_front + 29.7, z_in + 0.05, z_in + 0.65),
                 kind="moving", hidden=True)

        # ---- cables: plug + cable squashed against the wall --------------------------------------
        self.plug_cable("cable_power", "C7v", x=PWR_X, z=PWR_Z, back_y=Y_WB, recess=STRIP_RECESS)
        self.plug_cable("cable_usb", "USB-B", x=USB_X, z=USB_Z, back_y=Y_WB, recess=STRIP_RECESS)
        self.notes.append("Ports on a strip at the back corner on the control-panel side, set in ~0.5 cm: "
                          "both plugs stick out behind the printer (flat back).")

    def states(self):
        d = math.radians(SUP_ANGLE)
        slide = (0.0, -EXT_SLIDE * math.cos(d), EXT_SLIDE * math.sin(d))
        open_tray = [("rot", "input_tray", "x", DOOR_OPEN), ("show", "tray_ext"), ("show", "paper")]
        return {
            "printing": open_tray + [("rot", "support", "x", SUP_ROT), ("rot", "support_ext", "x", SUP_ROT),
                                     ("move", "support_ext", slide)],
            "refill": list(open_tray),
        }
