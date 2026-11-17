#!/usr/bin/env python3
"""
Reference-photo helper for the modelling agents. Photos stay outside the repo (they belong to
their owners and are git-ignored): printers/<printer name>/photos/<name>.png plus index.json.

    python3 build/photos.py add <id> <captured.png> --name 03_back --view back \
        --url <image url> --page <page url> --source manufacturer --evidence "rule b: brother.co.uk product page"
    python3 build/photos.py list <id>
    python3 build/photos.py contact <id>          # contact sheet of all photos -> printers/<printer name>/photos/_contact.png

`add` trims flat borders (the white or dark margins around a browser screenshot) before saving.
"""
import argparse
import json
import os
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import photos_dir  # noqa: E402


def trim(im, tol=10):
    a = np.asarray(im.convert("RGB"), int)
    corners = [a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]]
    keep = np.zeros(a.shape[:2], bool)
    for c in corners:
        keep |= np.abs(a - c).max(2) > tol
    # a pixel is content if it differs from every corner colour
    content = np.ones(a.shape[:2], bool)
    for c in corners:
        content &= np.abs(a - c).max(2) > tol
    ys, xs = np.where(content)
    if len(xs) < 50:
        return im
    pad = 6
    x0, x1 = max(0, xs.min() - pad), min(a.shape[1], xs.max() + pad + 1)
    y0, y1 = max(0, ys.min() - pad), min(a.shape[0], ys.max() + pad + 1)
    return im.crop((x0, y0, x1, y1))


def index_path(pid):
    return os.path.join(photos_dir(pid), "index.json")


def photo_file(pid, entry):
    """The photo's path on this machine (older index files hold paths from another machine)."""
    return os.path.join(photos_dir(pid), entry["name"] + ".png")


def load(pid):
    p = index_path(pid)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save(pid, idx):
    os.makedirs(photos_dir(pid), exist_ok=True)
    with open(index_path(pid), "w", encoding="utf-8") as f:
        json.dump(idx, f, indent=1)


def cmd_add(a):
    os.makedirs(photos_dir(a.id), exist_ok=True)
    im = Image.open(a.src)
    if not a.no_trim:
        im = trim(im)
    out = os.path.join(photos_dir(a.id), a.name + ".png")
    im.convert("RGB").save(out)
    idx = [e for e in load(a.id) if e["name"] != a.name]
    idx.append({"name": a.name, "file": a.name + ".png", "size": list(im.size), "view": a.view, "url": a.url,
                "page": a.page, "source_kind": a.source, "model_evidence": a.evidence, "notes": a.notes})
    idx.sort(key=lambda e: e["name"])
    save(a.id, idx)
    print("saved", out, im.size)


def cmd_list(a):
    for e in load(a.id):
        print("%-28s %-22s %4dx%-4d %s" % (e["name"], e["view"], e["size"][0], e["size"][1], e["model_evidence"][:60]))


def cmd_contact(a):
    idx = load(a.id)
    if not idx:
        print("no photos")
        return
    th = 260
    tiles = []
    font = ImageFont.load_default()
    for e in idx:
        im = Image.open(photo_file(a.id, e)).convert("RGB")
        im.thumbnail((th, th))
        t = Image.new("RGB", (th, th + 18), "white")
        t.paste(im, ((th - im.width) // 2, 18 + (th - im.height) // 2))
        ImageDraw.Draw(t).text((3, 3), "%s  %s" % (e["name"], e["view"]), fill="black", font=font)
        tiles.append(t)
    cols = 5
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (th + 6), rows * (th + 24)), "#dddddd")
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * (th + 6), (i // cols) * (th + 24)))
    out = os.path.join(photos_dir(a.id), "_contact.png")
    sheet.save(out)
    print(out)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add")
    s.add_argument("id")
    s.add_argument("src")
    s.add_argument("--name", required=True)
    s.add_argument("--view", required=True)
    s.add_argument("--url", default="")
    s.add_argument("--page", default="")
    s.add_argument("--source", default="")
    s.add_argument("--evidence", default="")
    s.add_argument("--notes", default="")
    s.add_argument("--no-trim", action="store_true")
    s = sub.add_parser("list")
    s.add_argument("id")
    s = sub.add_parser("contact")
    s.add_argument("id")
    a = ap.parse_args()
    {"add": cmd_add, "list": cmd_list, "contact": cmd_contact}[a.cmd](a)


if __name__ == "__main__":
    main()
