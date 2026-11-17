"""
Example builder (not a real printer). It shows the printer_kit API; copy it to start a real one.

Every number in a real builder must trace back to references/<id>/MEASUREMENTS.md (photo
measurements scaled to the official size). Build in cm, Blender frame: Z up, FRONT = -Y, BACK = +Y,
x = 0 centre of width, y = 0 centre of depth, z = 0 underside of the feet.

Run:  python3 build/build_printer.py example --render front,34fl,back
"""


class Builder(Printer):
    W, D, H = 36.0, 36.0, 18.3        # closed body: width, depth, height (cm)

    def build(self):
        W, D, H = self.W, self.D, self.H
        body = self.mat("body", "#2b2b2c", 0.55)          # matte dark plastic
        dark = self.mat("dark", "#18181a", 0.45)
        rubber = self.mat("rubber", "#101010", 0.9)
        light = self.mat("label", "#e8e8e6", 0.4)
        led = self.mat("led", "#2bd16b", 0.3, emit="#2bd16b", emit_strength=3.0)

        # 1. Body: a side profile (u = y from front to back, v = z) extruded across the width.
        #    fillet() rounds individual corners; bevel rounds every edge of the extrusion.
        prof = fillet([(-D / 2, 0.8), (D / 2, 0.8), (D / 2, H), (-D / 2 + 7, H), (-D / 2, H - 3.5)],
                      [0.5, 0.5, 1.5, 4.0, 1.2])
        shell = extrude("shell", body, prof, axis="x", a0=-W / 2, a1=W / 2, bevel=0.5)

        # 2. A recessed output tray on top: boolean cutters are removed after baking.
        cut(shell, box("well_cut", None, -W / 2 + 4.5, W / 2 - 4.5, -D / 2 + 9, D / 2 - 7, H - 2.2, H + 1))
        # a shallow seam line around the front cover
        cut(shell, box("seam_cut", None, -W / 2 - 1, W / 2 + 1, -D / 2 - 1, -D / 2 + 0.15, 7.3, 7.45))
        self.add("body", shell)

        # 3. Feet (rubber pads under the four corners)
        for sx in (-1, 1):
            for sy in (-1, 1):
                self.add("body", cyl("foot", rubber, (sx * (W / 2 - 3), sy * (D / 2 - 3), 0.4), "z", 1.1, 0.8))

        # 4. Paper cassette: a separate moving part so the site can slide it out (refill state)
        cas = box("cassette", body, -W / 2 + 0.6, W / 2 - 0.6, -D / 2 - 0.15, D / 2 - 5, 0.9, 7.2, bevel=0.3)
        cut(cas, box("grip_cut", None, -5, 5, -D / 2 - 1, -D / 2 + 1.2, 0.5, 2.0))
        self.add("cassette", cas, kind="moving", pivot=(0, -D / 2, 0.9))

        # 5. Output support flap hinged at its front edge (printing state stands it up)
        flap = box("flap", dark, -6, 6, -D / 2 + 9.5, -D / 2 + 17, H - 2.2, H - 1.9, bevel=0.1)
        self.add("flap", flap, kind="moving", pivot=(0, -D / 2 + 9.5, H - 2.05))

        # 6. Control panel details: buttons, an LED and raised text
        for i, x in enumerate((W / 2 - 9, W / 2 - 6.5, W / 2 - 4)):
            self.add("body", cyl("btn%d" % i, dark, (x, -D / 2 + 4, H - 1.55), (0, -0.55, 0.83), 0.8, 0.3))
        self.add("body", cyl("led", led, (W / 2 - 11.5, -D / 2 + 4, H - 1.6), (0, -0.55, 0.83), 0.25, 0.2))
        self.add("body", text3d("logo", light, "brand", 1.6, (-W / 2 + 6.5, -D / 2 - 0.03, H - 5.5), "-y"))

        # 7. Back connectors: plug + cable as one 'cable' part each. A recessed socket lets the
        #    plug sink into the outline; a flat back makes it stick out fully.
        self.plug_cable("cable_power", "C13", x=W / 2 - 6, z=6.0, back_y=D / 2, recess=1.5)
        self.plug_cable("cable_usb", "USB-B", x=-W / 2 + 8, z=9.0, back_y=D / 2, recess=0.0)

    def states(self):
        return {
            "printing": [("rot", "flap", "x", 70)],
            "refill": [("move", "cassette", (0, -24, 0))],
        }
