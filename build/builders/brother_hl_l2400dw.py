"""
Brother HL-L2400DW -- and the shared body of the HL-L2445DW (builders/brother_hl_l2445dw.py subclasses this).

Numbers come from printers/Brother HL-L2400DW/measurements/MEASUREMENTS.md (photos scaled to the official
356 W x 360 D x 183 H mm). Frame: cm, Z up, FRONT = -Y, BACK = +Y, z = 0 under the feet.

Everything is built around the centre of the BODY (35.3 cm wide). The louvred vent on the right side sticks
out 0.3 cm, so the official 35.6 cm is body + vent; build() ends with recentre(), which shifts every part by
XSHIFT so that x = 0 is the centre of that overall width.

Back, seen from behind, left to right:
  AC inlet (C14, upright) in a housing that stands 0.5 cm proud of the flat left column  -> plug sticks out
  back cover (face-up tray door) with its handle tab (rearmost point, official depth)
  port niche: a corner notch 1.1 cm deep with a light-grey I/O plate
      HL-L2400DW: USB-B only (the plate is plain where the 2445DW has its RJ45)   -> cable_power + cable_usb
      HL-L2445DW: RJ45 above the USB-B                                             -> cable_power + cable_eth

To make a sibling model, subclass Builder and change MODEL / ETHERNET (or override build_back_io, which calls
build_ports and build_cables).

Run:  .venv/Scripts/python.exe build/build_printer.py brother-hl-l2400dw --render front,34fl,back
"""
import os
import sys

# The renders are only used for the photo comparison; the default lights wash out a dark printer.
if "printer_kit" in sys.modules:
    sys.modules["printer_kit"].LIGHT_GAIN = 0.3

# The kettle inlet is mounted upright, so the C13 plug stands on its narrow side (face 1.6 W x 2.2 H).
PLUGS.setdefault("C13v", (1.6, 2.2, 3.4, 2.4, 0.75, 3.0))


class Builder(Printer):
    MODEL = "HL-L2400DW"
    ETHERNET = False

    HW = 17.65      # half width of the body (35.3); the right-side vent adds 0.3 -> 35.6 overall
    VENT_OUT = 0.3
    XSHIFT = -0.15  # applied at the end so x = 0 is the centre of the overall width
    H = 18.25       # lid top (the buttons stand 0.05 above it -> 18.3)
    YF = -18.0      # front face (paper tray front and front cover)
    YS = -16.3      # side seam of the front cover / tray front (they wrap around the front corners)
    YLOW = 17.1     # flat back: side columns, lower corner blocks, 2-sided tray
    YB = 16.95      # back cover, 0.15 behind the columns
    YP = 16.6       # rear edge of the raised lid top
    YL = 17.4       # rear edge of the lid's rear rim (overhangs the back by 0.3)
    YTAB = 18.0     # back-cover handle tab = rearmost point of the closed body (official depth)
    ZB = 0.3        # underside of the body (feet below)
    ZT = 9.25       # top of the paper tray front
    ZC = 9.4        # bottom of the front cover
    ZLID = 17.0     # lid / body seam = underside of the rear rim
    R_FRONT = 1.4   # vertical front corners
    R_ROLL = 1.0    # front edge of the top

    # port niche (corner notch on the back, at the printer's left = right when seen from behind)
    NICHE_X1, NICHE_Z0, NICHE_Z1, NICHE_DEPTH = -14.78, 7.8, 14.75, 1.1
    PLATE_X0, PLATE_X1, PLATE_Z0, PLATE_Z1 = -17.15, -15.07, 8.75, 14.3
    PORT_X = -16.16
    USB_Z, RJ45_Z = 10.4, 12.5
    # AC inlet housing
    INLET_X, INLET_Z, INLET_OUT = 16.35, 10.8, 0.5

    # ------------------------------------------------------------------------------------------
    def materials(self):
        m = {}
        m["body"] = self.mat("body", "#47484c", 0.62)
        m["dark"] = self.mat("dark", "#141516", 0.75)
        m["trim"] = self.mat("trim", "#2a2b2d", 0.55)
        m["plate"] = self.mat("plate", "#64656b", 0.45)
        m["tab"] = self.mat("tab", "#606166", 0.55)
        m["lever"] = self.mat("lever", "#4cc24a", 0.45)
        m["grip"] = self.mat("grip", "#b4b6ba", 0.5)
        m["bezel"] = self.mat("bezel", "#101112", 0.2)
        m["lcd"] = self.mat("lcd", "#a3aaa4", 0.2, emit="#a3aaa4", emit_strength=0.12)
        m["led"] = self.mat("led", "#3fd46a", 0.3, emit="#3fd46a", emit_strength=3.0)
        m["logo"] = self.mat("logo", "#d4d5d7", 0.4)
        m["rubber"] = self.mat("rubber", "#111111", 0.9)
        m["metal"] = self.mat("metal", "#b9bcc0", 0.35, metal=0.8)
        m["paper"] = self.mat("paper", "#f4f4f2", 0.85)
        m["label"] = self.mat("label", "#2a2b2e", 0.4)
        m["labeltxt"] = self.mat("labeltxt", "#9a9b9e", 0.5)
        m["button"] = self.mat("button", "#2b2c2f", 0.4)
        m["btntxt"] = self.mat("btntxt", "#c9cacc", 0.5)
        m["inlet"] = self.mat("inlet", "#0e0e0f", 0.6)
        self.m = m
        return m

    # ------------------------------------------------------------------------------------------
    def fit_text(self, ob, width_cm, axis=0):
        """Scale a text mesh about its own centre so its extent along `axis` is width_cm."""
        V = mesh_world_verts(ob) / CM
        c = (V.min(0) + V.max(0)) / 2
        s = width_cm / max(V[:, axis].max() - V[:, axis].min(), 1e-6)
        T = Matrix.Translation(Vector(c * CM))
        S = Matrix.Diagonal((s, s, s, 1.0))
        ob.data.transform(T @ S @ T.inverted())
        ob.data.update()
        return ob

    def vent_png(self, name, nx, ny, hole=0.62, color=(15, 15, 16, 255)):
        """Texture for a perforated vent: nx x ny dark square holes on a transparent background."""
        from PIL import Image, ImageDraw
        path = os.path.join(TMP, name + ".png")
        cw = 16
        im = Image.new("RGBA", (nx * cw, ny * cw), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        a = int(cw * (1 - hole) / 2)
        for i in range(nx):
            for j in range(ny):
                d.rectangle([i * cw + a, j * cw + a, (i + 1) * cw - a - 1, (j + 1) * cw - a - 1], fill=color)
        im.save(path)
        return path

    # ------------------------------------------------------------------------------------------
    def build(self):
        self.materials()
        self.build_shell()
        self.build_cassette()
        self.build_flap()
        self.build_back_io()
        self.recentre()
        self.notes.append("Shared body of the HL-L2400DW and HL-L2445DW (the 2445DW adds an RJ45 above the USB-B).")
        self.notes.append("Official width = 35.3 cm body + 0.3 cm louvred vent on the right side; "
                          "official depth = front panel to the back-cover handle tab.")

    def recentre(self):
        """Shift every part so x = 0 is the centre of the overall width (body + the vent on the right)."""
        dx = self.XSHIFT
        T = Matrix.Translation(Vector((dx * CM, 0, 0)))
        for part, ob in self.parts.items():
            bake(ob)
            ob.data.transform(T)
            ob.data.update()
            piv = self.meta[part]["pivot"]
            if piv is not None:
                piv[0] += dx
        for s in self.sockets:
            s["x"] = round(s["x"] + dx, 2)

    # ------------------------------------------------------------------------------------------
    def plan(self, y1, r_back):
        """Plan outline (x, y) of the body from the front face to y1, with rounded corners."""
        hw, YF = self.HW, self.YF
        return fillet([(-hw, YF), (hw, YF), (hw, y1), (-hw, y1)], [self.R_FRONT, self.R_FRONT, r_back, r_back], n=8)

    def cover_poly(self, inset=0.0, z_top=None):
        """Back cover outline (x, z): a rectangle with a short leg at each bottom corner."""
        i = inset
        zt = (self.ZLID if z_top is None else z_top) - i
        return [(-14.28 + i, 5.0 + i), (-13.1 - i, 5.0 + i), (-13.1 - i, 6.1 + i), (13.4 + i, 6.1 + i),
                (13.4 + i, 5.0 + i), (14.43 - i, 5.0 + i), (14.43 - i, zt), (-14.28 + i, zt)]

    def build_shell(self):
        m = self.m
        hw, H = self.HW, self.H
        YF, YS, YLOW, YB, YP, YL = self.YF, self.YS, self.YLOW, self.YB, self.YP, self.YL
        ZB, ZLID = self.ZB, self.ZLID
        body, dark, trim = m["body"], m["dark"], m["trim"]

        # 1. lower body + raised lid top + the lid's rear rim, joined into one solid
        shell = extrude("shell", body, self.plan(YLOW, 0.45), axis="z", a0=ZB, a1=ZLID + 0.3, bevel=0.25, seg=3)
        bake(shell)
        lid = extrude("lid_u", None, self.plan(YP, 0.8), axis="z", a0=ZLID - 0.6, a1=H, bevel=0.3, seg=4)
        bake(lid)
        rim = box("rim_u", None, -hw, hw, 15.7, YL, ZLID, H - 0.25, bevel=0.1, seg=2)
        bake(rim)
        cut(shell, lid, "UNION")
        cut(shell, rim, "UNION")
        # 2. the front edge of the top rolls over (R_ROLL)
        r = self.R_ROLL
        roll = [(YF - 1, H - r)] + [tuple(p) for p in arc(YF + r, H - r, r, 180, 90, n=10)] + [(YF + r, H + 1), (YF - 1, H + 1)]
        cut(shell, extrude("roll_cut", None, roll, axis="x", a0=-hw - 1, a1=hw + 1))
        bake(shell)

        cuts = []
        # 3. the paper tray front (a separate part) and the tray tunnel behind it
        cuts.append(box("cas_cut", None, -hw - 1, hw + 1, YF - 1, YS, ZB - 1, self.ZC - 0.07))
        cuts.append(box("tunnel_cut", None, -16.9, 16.9, YS - 0.1, YS + 1.2, ZB + 0.3, 9.0))
        # 4. manual-feed cover: shallow pocket, the cover plate goes back in with a groove around it
        cuts.append(extrude("mf_cut", None, rrect(29.36, 5.1, 0.35, cx=0, cy=12.65), axis="y", a0=YF - 1, a1=YF + 0.22))
        # 5. grip slot above the manual-feed cover
        cuts.append(box("grip_cut", None, -5.0, 5.0, YF - 1, YF + 0.9, 15.2, 15.95))
        # 6. seams: front cover across the lid and down the lid's edge, lid / body, front shell / side panels
        ys = -10.5
        cuts.append(box("seam_top", None, -hw - 1, hw + 1, ys - 0.06, ys + 0.06, H - 0.09, H + 1))
        for sx in (-1, 1):
            x0, x1 = sorted((sx * (hw - 0.07), sx * (hw + 1)))
            cuts.append(box("seam_lid_side", None, x0, x1, ys - 0.06, ys + 0.06, ZLID, H + 1))
            cuts.append(box("seam_lid", None, x0, x1, YS, 15.7, ZLID - 0.05, ZLID + 0.05))
            cuts.append(box("seam_front", None, x0, x1, YS - 0.06, YS + 0.06, self.ZC - 0.07, ZLID))
        # 7. output tray pit and the paper exit under the rear of the lid
        cuts.append(extrude("pit_cut", None, rrect(23.3, 12.1, [1.0, 1.0, 0.9, 0.9], cx=1.05, cy=4.25),
                            axis="z", a0=15.9, a1=H + 1))
        cuts.append(box("exit_cut", None, -10.1, 12.2, 10.2, 12.3, 15.9, 17.45))
        # 8. support-flap recess with a finger slot at each rear corner
        cuts.append(extrude("flap_cut", None, [(-3.95, -16.42), (3.95, -16.42), (4.42, -13.44), (-4.42, -13.44)],
                            axis="z", a0=H - 0.3, a1=H + 1))
        for sx in (-1, 1):
            x0, x1 = sorted((sx * 4.3, sx * 5.4))
            cuts.append(box("ear_cut", None, x0, x1, -14.05, -13.44, H - 0.45, H + 1))
        # 9. back: cover pocket, 2-sided tray pocket, port niche (open to the side), notches in the rim
        cuts.append(extrude("cover_cut", None, self.cover_poly(), axis="y", a0=YLOW - 0.35, a1=YLOW + 1))
        cuts.append(box("tray_cut", None, -10.9, 12.73, YLOW - 0.4, YLOW + 1, ZB - 1, 3.9))
        cuts.append(box("niche_cut", None, -hw - 1, self.NICHE_X1, YLOW - self.NICHE_DEPTH, YLOW + 1,
                        self.NICHE_Z0, self.NICHE_Z1, bevel=0.12, seg=2))
        ix, iz = self.INLET_X, self.INLET_Z            # room for the C14 cup behind the inlet housing
        cuts.append(box("inlet_cut_s", None, ix - 1.1, ix + 1.1, YLOW + self.INLET_OUT - 1.72, YLOW + 1, iz - 1.52, iz + 1.52))
        cuts.append(box("lever_cut_s", None, -2.58, 4.56, YLOW - 1.2, YLOW + 1, 2.3, 4.7))
        for x in (-14.35, 14.35):
            cuts.append(box("rim_notch", None, x - 0.07, x + 0.07, YL - 0.45, YL + 1, H - 0.6, H + 1))
        for c in cuts:
            cut(shell, c)

        objs = [shell]
        # dark insides
        objs.append(box("tunnel_back", dark, -16.85, 16.85, YS + 0.9, YS + 1.3, ZB + 0.35, 8.95))
        objs.append(box("grip_back", dark, -4.98, 4.98, YF + 0.5, YF + 0.9, 15.22, 15.93))
        objs.append(box("grip_lip", body, -4.95, 4.95, YF + 0.03, YF + 0.5, 15.2, 15.45, bevel=0.05, seg=1))
        objs.append(box("exit_back", dark, -10.05, 12.15, 12.1, 12.3, 15.9, 17.45))
        for sx in (-1, 1):
            x0, x1 = sorted((sx * 4.33, sx * 5.37))
            objs.append(box("ear_floor", dark, x0, x1, -14.02, -13.47, H - 0.46, H - 0.4))
        objs.append(extrude("flap_floor", trim, [(-3.93, -16.4), (3.93, -16.4), (4.4, -13.46), (-4.4, -13.46)],
                            axis="z", a0=H - 0.31, a1=H - 0.295))
        # manual-feed cover plate (flush) and the logo
        objs.append(extrude("mf_plate", body, rrect(29.14, 4.88, 0.28, cx=0, cy=12.65), axis="y", a0=YF, a1=YF + 0.3,
                            bevel=0.05, seg=2))
        logo = text3d("logo", m["logo"], "brother", 1.6, (0.1, YF - 0.02, 12.45), "-y", depth_cm=0.04,
                      font=find_font("DejaVuSans.ttf") or find_font("DejaVuSans"))
        objs.append(self.fit_text(logo, 4.9))
        objs += self.output_tray()
        objs += self.panel()
        objs += self.back_details()
        objs += self.side_details()
        # feet
        for sx in (-1, 1):
            for sy in (-1, 1):
                objs.append(cyl("foot", m["rubber"], (sx * 15.2, sy * 14.6 - 0.4, ZB / 2), "z", 0.9, ZB, seg=16))
        self.add("body", join(objs, "body_tmp"))

    # ------------------------------------------------------------------------------------------
    def output_tray(self):
        """Floor of the output pit (ribbed, deepest at the exit), exit rollers and the model label."""
        m, H = self.m, self.H
        o = []
        y0, y1, z0, z1 = -1.75, 10.3, H - 0.55, 16.0     # floor line: front (shallow) -> rear (deep)
        o.append(extrude("tray_floor", m["body"], [(y0, 15.85), (y0, z0), (y1, z1), (y1, 15.85)], axis="x",
                         a0=-10.55, a1=12.65))
        k = (z1 - z0) / (y1 - y0)
        for i in range(27):                               # ribs on the front half of the floor
            x = -9.9 + i * 0.84
            ya, yb = y0 + 0.25, 4.6
            za, zb = z0 + k * (ya - y0), z0 + k * (yb - y0)
            o.append(extrude("rib", m["body"], [(ya, za - 0.02), (ya, za + 0.09), (yb, zb + 0.09), (yb, zb - 0.02)],
                             axis="x", a0=x, a1=x + 0.22))
        for i, x in enumerate((-7.6, -2.4, 3.6, 8.9)):
            o.append(cyl("roller%d" % i, m["trim"], (x, 11.25, 16.55), "x", 0.45, 3.0, seg=16))
        o.append(cyl("shaft", m["metal"], (1.05, 11.25, 16.55), "x", 0.14, 21.5, seg=10))
        # model label on the lid behind the exit
        o.append(extrude("label", m["label"], rrect(3.95, 1.6, 0.25, cx=1.0, cy=12.4), axis="z", a0=H - 0.02, a1=H + 0.02))
        lab = text3d("label_txt", m["labeltxt"], self.MODEL, 0.3, (1.0, 12.4, H + 0.025), "+z", depth_cm=0.01,
                     font=find_font("DejaVuSans-Bold"))
        o.append(self.fit_text(lab, 2.7))
        return o

    def panel(self):
        """Control panel on the lid, front-left (top photo 15, close-ups 10 and 16)."""
        m, H = self.m, self.H
        up = 0.05
        o = []
        o.append(extrude("lcd_bezel", m["bezel"], rrect(6.0, 1.15, 0.42, cx=-14.1, cy=-3.0), axis="z", a0=H - 0.03, a1=H + 0.015))
        o.append(extrude("lcd", m["lcd"], rrect(5.5, 0.7, 0.12, cx=-14.1, cy=-3.0), axis="z", a0=H, a1=H + 0.03))
        o.append(cyl("btn_power", m["button"], (-16.23, -5.18, H + up / 2), "z", 0.5, up, seg=24))
        o.append(cyl("btn_power_ring", m["btntxt"], (-16.23, -5.18, H + up + 0.004), "z", 0.2, 0.008, seg=16))
        o.append(cyl("btn_power_dot", m["button"], (-16.23, -5.18, H + up + 0.008), "z", 0.13, 0.012, seg=16))
        o.append(cyl("btn_wifi", m["button"], (-16.23, -6.71, H + up / 2), "z", 0.5, up, seg=24))
        o.append(cyl("led_wifi", m["led"], (-16.23, -6.71, H + up + 0.005), "z", 0.4, 0.01, seg=20))
        for nm, x, y in (("back", -14.09, -5.18), ("ok", -12.46, -5.18), ("down", -14.09, -6.71), ("up", -12.46, -6.71)):
            o.append(extrude("btn_" + nm, m["button"], rrect(1.5, 0.85, 0.36, cx=x, cy=y), axis="z", a0=H - 0.02, a1=H + up))
            o.append(box("mark_" + nm, m["btntxt"], x - 0.22, x + 0.22, y - 0.05, y + 0.05, H + up, H + up + 0.008))
        o.append(extrude("btn_go", m["button"], rrect(3.15, 0.9, 0.42, cx=-13.33, cy=-8.54), axis="z", a0=H - 0.02, a1=H + up))
        o.append(extrude("go_led", m["led"], rrect(2.35, 0.24, 0.11, cx=-13.33, cy=-8.54), axis="z", a0=H + up, a1=H + up + 0.01))
        return o

    def back_details(self):
        m = self.m
        hw = self.HW
        YB, YLOW, ZB = self.YB, self.YLOW, self.ZB
        body, dark, trim = m["body"], m["dark"], m["trim"]
        o = []
        # back cover plate, 0.15 behind the columns, with a groove all round
        o.append(extrude("back_cover", body, self.cover_poly(0.07, z_top=self.ZLID + 0.05), axis="y", a0=YLOW - 0.4, a1=YB))
        o.append(box("cover_gap", dark, -14.3, 14.45, YLOW - 0.36, YLOW - 0.33, 4.98, self.ZLID))
        # handle tab: rearmost point of the body (official depth)
        tab = extrude("tab", body, fillet([(YB - 0.1, 13.95), (self.YTAB, 13.95), (self.YTAB, 14.75), (YB + 0.25, 15.35),
                                          (YB - 0.1, 15.35)], [0, 0.2, 0.25, 0.1, 0], n=4), axis="x", a0=-2.08, a1=2.08,
                      bevel=0.12, seg=2)
        o.append(tab)
        o.append(box("tab_shadow", trim, -1.9, 1.9, YB - 0.02, YB + 0.02, 13.7, 13.95))
        # 2-sided tray: rear panel (slightly sunk), upper flange (slightly proud), lever recess with the green lever
        tray = box("duplex_tray", body, -10.83, 12.66, YLOW - 0.45, YLOW - 0.1, ZB, 3.83, bevel=0.06, seg=2)
        bake(tray)
        flange = box("duplex_flange", body, -13.1, 13.4, YLOW - 0.2, YLOW + 0.1, 4.0, 6.0, bevel=0.07, seg=2)
        bake(flange)
        lx0, lx1, lz0, lz1 = -2.58, 4.56, 2.3, 4.7
        for ob in (tray, flange):
            cut(ob, extrude("lever_cut", None, rrect(lx1 - lx0, lz1 - lz0, 0.35, cx=(lx0 + lx1) / 2, cy=(lz0 + lz1) / 2),
                            axis="y", a0=YLOW - 1.2, a1=YLOW + 1))
        o += [tray, flange]
        o.append(box("tray_gap", dark, -10.92, 12.75, YLOW - 0.5, YLOW - 0.44, ZB - 0.02, 4.0))
        o.append(box("lever_back", dark, lx0 + 0.02, lx1 - 0.02, YLOW - 1.2, YLOW - 1.1, lz0 + 0.02, lz1 - 0.02))
        o.append(box("lever", m["lever"], -0.84, 2.87, YLOW - 1.0, YLOW - 0.35, 3.1, 3.85, bevel=0.08, seg=2))
        o.append(box("lever_grip", m["grip"], -0.9, 2.95, YLOW - 0.95, YLOW - 0.2, 2.4, 3.1, bevel=0.08, seg=2))
        # AC inlet (IEC C14, upright) in a housing that stands proud of the column
        ix, iz, yh = self.INLET_X, self.INLET_Z, YLOW + self.INLET_OUT
        hous = box("inlet_housing", body, ix - 1.2, ix + 1.2, YLOW - 0.3, yh, iz - 1.8, iz + 1.8, bevel=0.14, seg=2)
        bake(hous)
        cav = fillet([(ix - 1.08, iz - 1.5), (ix + 0.6, iz - 1.5), (ix + 1.08, iz - 1.02), (ix + 1.08, iz + 1.02),
                      (ix + 0.6, iz + 1.5), (ix - 1.08, iz + 1.5)], 0.08, n=2)
        cut(hous, extrude("inlet_cut", None, cav, axis="y", a0=YLOW - 1, a1=yh + 1))
        o.append(hous)
        cup = extrude("inlet_cup", m["inlet"], cav, axis="y", a0=yh - 1.7, a1=yh - 0.1)   # black C14 cup, 1.6 deep
        bake(cup)
        cut(cup, box("cup_cut", None, ix - 0.93, ix + 0.93, yh - 1.55, yh + 1, iz - 1.35, iz + 1.35))
        o.append(cup)
        for dx, dz in ((-0.3, 0.7), (-0.3, -0.7), (0.35, 0.0)):
            o.append(box("pin", m["metal"], ix + dx - 0.05, ix + dx + 0.05, yh - 1.55, yh - 0.35, iz + dz - 0.2, iz + dz + 0.2))
        o.append(box("inlet_latch", m["inlet"], 14.47, ix - 1.15, YLOW - 0.3, YLOW + 0.3, iz - 1.1, iz + 1.4, bevel=0.06, seg=1))
        # vents on the lower corner block next to the inlet (seen from behind: bottom left)
        for k in range(7):
            z = 1.35 + 0.45 * k
            o.append(box("vslot%d" % k, dark, 13.62, 14.55, YLOW - 0.02, YLOW + 0.015, z, z + 0.22))
        for r in range(3):
            for c in range(4):
                x = 13.62 + c * 0.83
                z = 0.42 + r * 0.4
                o.append(box("vgrid", dark, x, x + 0.68, YLOW - 0.02, YLOW + 0.015, z, z + 0.22))
        # seam of the corner blocks beside the 2-sided tray flange
        for x in (-13.15, 13.45):
            o.append(box("blk_seam", dark, x - 0.04, x + 0.04, YLOW - 0.02, YLOW + 0.012, 3.9, 5.0))
        return o

    def side_details(self):
        m = self.m
        hw, out = self.HW, self.VENT_OUT
        body, dark = m["body"], m["dark"]
        o = []
        # left side: perforated grille near the front, under the lid seam
        o.append(decal("vent_left", self.vent_png("vent_grid", 40, 28, hole=0.55, color=(17, 17, 19, 255)), (-hw - 0.012, -10.9, 12.9), 10.2, 7.2,
                       facing="-x", mats=self.mats))
        # right side: louvred vent box that stands 0.3 cm proud of the side (it shows in the top photo)
        y0, y1, z0, z1 = 0.0, 8.1, 9.3, 16.4
        o.append(box("louvre_back", dark, hw - 0.02, hw + 0.03, y0 + 0.2, y1 - 0.2, z0 + 0.2, z1 - 0.2))
        for (a0, a1, b0, b1) in ((y0, y1, z0, z0 + 0.3), (y0, y1, z1 - 0.3, z1), (y0, y0 + 0.3, z0, z1), (y1 - 0.3, y1, z0, z1)):
            o.append(box("louvre_frame", body, hw - 0.05, hw + out, a0, a1, b0, b1, bevel=0.05, seg=1))
        for yv in (y0 + 2.6, y0 + 5.2):
            o.append(box("louvre_div", body, hw - 0.05, hw + out - 0.03, yv - 0.1, yv + 0.1, z0 + 0.2, z1 - 0.2))
        n = 9
        for i in range(n):
            zc = z0 + 0.3 + (i + 0.5) * (z1 - z0 - 0.6) / n
            o.append(extrude("louvre_fin", body, [(hw, zc + 0.3), (hw + 0.03, zc + 0.36), (hw + out - 0.03, zc - 0.12),
                                                  (hw + out - 0.06, zc - 0.18)], axis="y", a0=y0 + 0.25, a1=y1 - 0.25))
        # small perforated patch low on the right side, near the front
        o.append(decal("vent_dots", self.vent_png("vent_dots", 9, 9, hole=0.45), (hw + 0.012, -14.4, 2.2), 2.6, 2.6,
                       facing="+x", mats=self.mats))
        # lighter latch strip just behind the front seam on both sides
        for sx in (-1, 1):
            x0, x1 = sorted((sx * (hw - 0.02), sx * (hw + 0.025)))
            o.append(box("side_latch", m["tab"], x0, x1, self.YS + 0.1, self.YS + 0.42, 11.6, 14.4))
        return o

    # ------------------------------------------------------------------------------------------
    def build_cassette(self):
        """Paper tray: its front wraps around the front corners; the tray slides out along -y."""
        m = self.m
        YF, YS, hw, ZB = self.YF, self.YS, self.HW, self.ZB
        prof = fillet([(-hw, YS + 0.05), (-hw, YF), (hw, YF), (hw, YS + 0.05)], [0, self.R_FRONT, self.R_FRONT, 0], n=8)
        front = extrude("cas_front", m["body"], prof, axis="z", a0=ZB + 0.03, a1=self.ZT, bevel=0.22, seg=3)
        bake(front)
        notch = fillet([(-4.75, -1), (4.75, -1), (4.4, 2.4), (-4.4, 2.4)], [0, 0, 0.35, 0.35], n=4)
        cut(front, extrude("notch_cut", None, notch, axis="y", a0=YF - 1, a1=YS + 1))
        o = [front]
        o.append(box("notch_roof", m["trim"], -4.7, 4.7, YF + 0.25, YS + 0.3, 2.38, 2.6))
        o.append(box("notch_back", m["trim"], -4.7, 4.7, YS + 0.05, YS + 0.3, ZB + 0.2, 2.5))
        o.append(box("tray_floor", m["trim"], -16.5, 16.5, YS, YF + 33.0, ZB + 0.1, ZB + 0.4))
        for sx in (-1, 1):
            x0, x1 = sorted((sx * 16.5, sx * 16.2))
            o.append(box("tray_side", m["trim"], x0, x1, YS, YF + 33.0, ZB + 0.1, 8.3))
        o.append(box("tray_back", m["trim"], -16.5, 16.5, YF + 32.7, YF + 33.0, ZB + 0.1, 8.3))
        o.append(box("paper", m["paper"], -10.5, 10.5, YF + 2.2, YF + 31.9, ZB + 0.4, 2.9))
        self.add("cassette", join(o, "cas_tmp"), kind="moving", pivot=(0, YF, ZB))

    def build_flap(self):
        """Output support flap lying in the front strip of the lid, hinged at its front edge."""
        H = self.H
        f = extrude("flap", self.m["body"], [(-3.85, -16.35), (3.85, -16.35), (4.32, -13.52), (-4.32, -13.52)],
                    axis="z", a0=H - 0.28, a1=H - 0.03, bevel=0.07, seg=2)
        self.add("flap", f, kind="moving", pivot=(0, -16.35, H - 0.15))

    # ------------------------------------------------------------------------------------------
    # Back ports and cables: the only things that differ between the HL-L2400DW and the HL-L2445DW.
    def build_back_io(self):
        """Everything model-specific on the back: the jacks in the port niche and the plugged-in cables.
        A sibling model sets ETHERNET (and MODEL for the lid label) or overrides this one method."""
        self.build_ports()
        self.build_cables()

    def port_face_y(self):
        """y of the I/O plate at the back of the port niche (the socket faces)."""
        return self.YLOW - self.NICHE_DEPTH

    def usb_jack(self, z):
        m, y, x = self.m, self.port_face_y(), self.PORT_X
        return [box("usb_shell", m["metal"], x - 0.62, x + 0.62, y, y + 0.12, z - 0.58, z + 0.58, bevel=0.05, seg=1),
                box("usb_hole", m["dark"], x - 0.45, x + 0.45, y + 0.11, y + 0.135, z - 0.42, z + 0.42)]

    def rj45_jack(self, z):
        m, y, x = self.m, self.port_face_y(), self.PORT_X - 0.05
        return [box("rj_shell", m["metal"], x - 0.78, x + 0.78, y, y + 0.12, z - 0.9, z + 0.9, bevel=0.05, seg=1),
                box("rj_hole", m["dark"], x - 0.58, x + 0.58, y + 0.11, y + 0.135, z - 0.62, z + 0.72),
                box("rj_latch", m["dark"], x + 0.58, x + 0.72, y + 0.11, y + 0.135, z - 0.3, z + 0.3)]

    def build_ports(self):
        """The port niche's back wall, the I/O plate and the jacks. USB-B always; RJ45 only if ETHERNET."""
        m, y = self.m, self.port_face_y()
        o = [box("niche_back", m["dark"], -self.HW + 0.02, self.NICHE_X1 - 0.02, y - 0.02, y + 0.012,
                 self.NICHE_Z0 + 0.02, self.NICHE_Z1 - 0.02)]
        o.append(extrude("io_plate", m["plate"], rrect(self.PLATE_X1 - self.PLATE_X0, self.PLATE_Z1 - self.PLATE_Z0, 0.3,
                                                       cx=(self.PLATE_X0 + self.PLATE_X1) / 2,
                                                       cy=(self.PLATE_Z0 + self.PLATE_Z1) / 2), axis="y", a0=y, a1=y + 0.045))
        o += self.usb_jack(self.USB_Z)
        if self.ETHERNET:
            o += self.rj45_jack(self.RJ45_Z)
        self.add("body", join(o, "ports_tmp"))

    def build_cables(self):
        """cable_power always; cable_eth if the model has Ethernet, otherwise cable_usb."""
        self.plug_cable("cable_power", "C13v", x=self.INLET_X, z=self.INLET_Z, back_y=self.YLOW + self.INLET_OUT, recess=0.0)
        if self.ETHERNET:
            self.plug_cable("cable_eth", "RJ45", x=self.PORT_X - 0.05, z=self.RJ45_Z, back_y=self.YLOW, recess=self.NICHE_DEPTH)
        else:
            self.plug_cable("cable_usb", "USB-B", x=self.PORT_X, z=self.USB_Z, back_y=self.YLOW, recess=self.NICHE_DEPTH)

    # ------------------------------------------------------------------------------------------
    def states(self):
        return {
            "printing": [("rot", "flap", "x", 70)],
            "refill": [("move", "cassette", (0, -27.0, 0))],
        }
