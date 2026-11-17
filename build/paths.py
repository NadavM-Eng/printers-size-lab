"""
Where things live on disk. No Blender import, so every script can use it.

    printers/<printer name>/specs.json                    research (sizes, box contents, prices, cable space)
    printers/<printer name>/photos/                       reference photos + index.json (never committed)
    printers/<printer name>/measurements/MEASUREMENTS.md  measurements taken from the photos
    work/renders/<id>/, work/compare/<id>/                renders and photo-vs-model sheets (never committed)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRINTERS_DIR = os.path.join(ROOT, "printers")
WORK = os.environ.get("PSL_WORK") or os.path.join(ROOT, "work")

# printer id (used in file names and on the site) -> folder name under printers/
FOLDERS = {
    "hp-officejet-j4580": "HP OfficeJet J4580 (current printer)",
    "brother-dcp-l2620dw": "Brother DCP-L2620DW",
    "brother-hl-l2445dw": "Brother HL-L2445DW",
    "brother-hl-l2400dw": "Brother HL-L2400DW",
    "pantum-bp2300nw": "Pantum BP2300NW",
    "hp-laserjet-m110w": "HP LaserJet M110w",
    "xerox-b230": "Xerox B230",
    "xerox-b110": "Xerox B110V",
}


def printer_dir(pid):
    return os.path.join(PRINTERS_DIR, FOLDERS.get(pid, pid))


def specs_path(pid):
    return os.path.join(printer_dir(pid), "specs.json")


def photos_dir(pid):
    return os.path.join(printer_dir(pid), "photos")
