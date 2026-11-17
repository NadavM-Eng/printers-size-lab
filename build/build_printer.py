#!/usr/bin/env python3
"""
Build one printer model and (optionally) render photo-matched views.

    python3 build/build_printer.py <id>                         # GLB -> docs/models/<id>.glb, geometry -> docs/data/<id>.geom.json
    python3 build/build_printer.py <id> --render front,back,left,right,top,34fl
    python3 build/build_printer.py <id> --render 34fl --state printing
    python3 build/build_printer.py <id> --view photo07:-35:18:60   # custom view name:azimuth:elevation:lens
    python3 build/build_printer.py <id> --render front --cables     # include cables in the renders

The builder lives in build/builders/<id with - replaced by _>.py and defines `class Builder(Printer)`.
Every name in printer_kit is available inside builder modules without importing.
Renders go to work/renders/<id>/<state>_<view>.png (git-ignored).
"""
import argparse
import importlib.util
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import printer_kit as K  # noqa: E402
from mathutils import Quaternion, Vector  # noqa: E402


load_builder = K.load_builder


def official(pid):
    p = K.specs_path(pid)
    try:
        with open(p, encoding="utf-8") as f:
            c = json.load(f)["dims_mm"]["closed"]
        return {"w": c["w"], "d": c["d"], "h": c["h"]}
    except Exception:
        return {}


def apply_state(printer, state):
    """Pose the Blender objects in a state (for renders)."""
    ops = printer._state_ops().get(state, []) if state != "closed" else []
    vis = {p: not m["hidden"] for p, m in printer.meta.items()}
    for part, ob in printer.parts.items():
        ob.rotation_mode = "QUATERNION"
        ob.rotation_quaternion = Quaternion()
    base = {part: Vector(ob.location) for part, ob in printer.parts.items()}
    for o in ops:
        ob = printer.parts[o["part"]]
        if "rot" in o:
            q = Quaternion(Vector(o["rot"]), math.radians(o["deg"]))
            ob.rotation_quaternion = q @ ob.rotation_quaternion
        if "move" in o:
            base[o["part"]] = base[o["part"]] + Vector(o["move"]) * K.CM
        if o.get("show"):
            vis[o["part"]] = True
        if o.get("hide"):
            vis[o["part"]] = False
    for part, ob in printer.parts.items():
        ob.location = base[part]
    return vis


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--render", default="", help="comma-separated view names: " + ",".join(K.VIEWS))
    ap.add_argument("--view", action="append", default=[], help="custom view name:azimuth:elevation:lens")
    ap.add_argument("--state", default="closed")
    ap.add_argument("--samples", type=int, default=32)
    ap.add_argument("--size", type=int, default=900)
    ap.add_argument("--out", default=None)
    ap.add_argument("--cables", action="store_true", help="include cables in renders")
    ap.add_argument("--no-export", action="store_true")
    a = ap.parse_args()

    K.reset_scene()
    B = load_builder(a.id)
    p = B(a.id, official(a.id))
    print("building", a.id)
    p.build()
    p.finish()
    if not a.no_export:
        p.export()
    jobs = [(v, None, None, None) for v in a.render.split(",") if v]
    for spec in a.view:
        name, az, el, lens = spec.split(":")
        jobs.append((name, float(az), float(el), float(lens)))
    if jobs:
        out = a.out or os.path.join(K.WORK, "renders", a.id)
        os.makedirs(out, exist_ok=True)
        vis = apply_state(p, a.state)
        parts = [ob.name for part, ob in p.parts.items()
                 if vis[part] and (a.cables or p.meta[part]["kind"] != "cable")]
        for name, az, el, lens in jobs:
            path = os.path.join(out, "%s_%s.png" % (a.state, name))
            K.render_view(path, name, parts, size=a.size, samples=a.samples, az=az, el=el, lens=lens)
            print("  render", path)


if __name__ == "__main__":
    main()
