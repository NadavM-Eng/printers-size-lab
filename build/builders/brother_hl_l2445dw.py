"""
Brother HL-L2445DW -- the HL-L2400DW body plus a wired Ethernet port.

Both specs.json files give the same 356 x 360 x 183 mm and 7.1 kg, and the photo sets are the same Brother
images (only 04_front differs: each store page's own front shot, same body). The one visible difference is on
the back: photo 07_back (Brother UK, HLL2445DW_1.png) shows an RJ45 jack above the USB-B in the port niche,
where the HL-L2400DW (photo 09_back_l2400dw) has a blank plate. The lid label reads the model name.

So this builder only changes MODEL and ETHERNET; the base's build_back_io() then adds the RJ45 jack and plugs
cable_power + cable_eth (the base plugs cable_power + cable_usb).

Run:  .venv/Scripts/python.exe build/build_printer.py brother-hl-l2445dw --render back --cables
"""
Base = load_builder("brother-hl-l2400dw")


class Builder(Base):
    MODEL = "HL-L2445DW"
    ETHERNET = True

    def build(self):
        super().build()
        self.notes.append("HL-L2445DW: RJ45 jack above the USB-B in the port niche (photo 07_back); "
                          "the Ethernet cable is the data cable.")
