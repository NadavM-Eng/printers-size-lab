#!/usr/bin/env python3
"""
Pack one printer into a single printer file for the "Add your printer" panel of Printers Size Lab
(format printers-size-lab/printer@2, see docs/ai-instructions.md). Plain Python 3, no Blender needed.

    python3 build/export_printer_file.py <id>
    python3 build/export_printer_file.py <id> --research path/to/<id>.research.json --out path/to/<id>.printer.json

It reads
    docs/models/<id>.glb             the mesh (written by build/build_printer.py)
    docs/data/<id>.geom.json         its parts, pivots and states (written by build/build_printer.py)
    the research, the first that exists of:
      --research <file>                                  printer-file fields (everything but "format" and "model")
      printers/<folder>/specs.json (+ ownership.json)    this repo's research files, or printer-file fields
and writes <id>.printer.json (default: work/export/<id>.printer.json) with model.glb_base64 and model.geom.

The research may be in either of two shapes:
  - printer-file fields (what an outside assistant writes): name, brand, type, functions, buyer_country,
    dims_mm, weight_kg, specs [...], price {value, currency, ...}, running_cost, software, cable_space,
    notes, made_with. They are copied as they are.
  - this repo's own research (specs.json with price.ils / price.usd, print_speed_ppm, connectivity ...,
    and ownership.json): converted to printer-file fields here.
"""
import argparse
import base64
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths import specs_path  # noqa: E402

ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
FORMAT = "printers-size-lab/printer@2"
MAX_GLB = 8 * 1024 * 1024        # the page refuses larger meshes
MAX_TRIS = 300000
SPEC_LABELS = ("Print speed", "Two-sided printing", "Connections", "Paper in", "Paper out", "Manual feed",
               "Scanner", "Display", "Toner", "Drum", "Ink", "In the box")
FIELDS = ("id", "name", "brand", "type", "functions", "buyer_country", "dims_mm", "weight_kg", "specs", "price",
          "running_cost", "software", "cable_space", "notes", "sources", "made_with")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def is_printer_fields(s):
    """True when the research is already in printer-file fields rather than this repo's specs.json shape."""
    pr = s.get("price")
    return ("format" in s or "buyer_country" in s or "made_with" in s or isinstance(s.get("specs"), list)
            or (isinstance(pr, dict) and "currency" in pr))


# --------------------------------------------------------------------------------------------
# this repo's research -> printer-file fields
# --------------------------------------------------------------------------------------------
def from_repo_research(pid, s):
    import assemble as A   # rows_for / load_ownership know this repo's research shape
    out = {k: s[k] for k in ("name", "brand", "type", "functions") if s.get(k)}
    dm = s.get("dims_mm") or {}
    out["dims_mm"] = {k: {kk: v for kk, v in dm[k].items() if kk in ("w", "d", "h", "source", "includes", "what")}
                      for k in ("closed", "max") if isinstance(dm.get(k), dict)}
    if isinstance(s.get("weight_kg"), dict) and s["weight_kg"].get("value"):
        out["weight_kg"] = {k: v for k, v in s["weight_kg"].items() if k in ("value", "what", "source")}
    specs = []
    for r in A.rows_for(s):
        if r["label"] in SPEC_LABELS:
            row = {"label": r["label"], "value": r["value"]}
            if r.get("href"):
                row["source"] = r["href"]
            if r.get("note"):
                row["note"] = r["note"]
            specs.append(row)
    out["specs"] = specs
    # one price: Israel when there is a shekel price (the built-in printers were researched for Israel)
    price = (s.get("price") or {})
    cur, country = ("ils", "Israel") if (price.get("ils") or {}).get("value") is not None else ("usd", "United States")
    p = price.get(cur) or {}
    out["buyer_country"] = country
    if p.get("value") is not None:
        out["price"] = {"value": p["value"], "currency": cur.upper(), "where": p.get("where"), "url": p.get("url"),
                        "date": p.get("date"), "note": p.get("note")}
        out["price"] = {k: v for k, v in out["price"].items() if v is not None}
    own = A.load_ownership(pid)
    if own:
        carts = []
        for c in own.get("consumables") or []:
            if not isinstance(c, dict) or c.get("role") == "starter":
                continue
            pc = c.get("price_" + cur)
            if not isinstance(pc, dict) or not pc.get("value"):
                continue
            carts.append({k: v for k, v in {
                "code": c.get("code"), "kind": c.get("kind"), "role": c.get("role"), "pages": c.get("pages"),
                "price": pc["value"], "currency": cur.upper(), "original": bool(c.get("original", True)),
                "where": A.short_shop(pc["where"]) if pc.get("where") else None, "url": pc.get("url")}.items() if v is not None})
        rc = {}
        if carts:
            rc["cartridges"] = carts
        tp = own.get("third_party_cartridges") or {}
        if tp.get("allowed") or tp.get("summary"):
            rc["compatible"] = {k: v for k, v in {"allowed": tp.get("allowed"), "note": A.impersonal(tp.get("summary")),
                                                  "source": tp.get("source")}.items() if v}
        if rc:
            out["running_cost"] = rc
        sw = {}
        for key, name in (("windows", "windows"), ("forums", "owners")):
            b = own.get(key) or {}
            if b.get("rating"):
                src = next((x.get("url") for x in (b.get("sources") or [])
                            if isinstance(x, dict) and str(x.get("url") or "").startswith("http")), None)
                sw[name] = {k: v for k, v in {"rating": b["rating"], "why": A.impersonal(b.get("why")), "source": src}.items() if v}
        if sw:
            out["software"] = sw
    cs = s.get("cable_space") or {}
    if cs.get("why"):
        out["cable_space"] = {"why": A.you(cs["why"])}
    if s.get("notes"):
        out["notes"] = A.you(s["notes"])
    srcs = set()
    A.collect_sources(s, srcs)
    A.collect_sources(own, srcs)
    out["sources"] = sorted(srcs)[:40]
    return out


def default_made_with(pid):
    """For this repo's own printers (the process in helper-instructions/AGENT_BRIEF.md). Rounds and photos are
    counted from the local comparison sheets and photo index when they exist (both are git-ignored)."""
    import re
    from paths import WORK, photos_dir
    out = {"route": "A", "tools": ["Blender 5.2 (bpy)", "Printers Size Lab toolkit (build/printer_kit.py)", "web search", "vision"]}
    try:
        idx = load(os.path.join(photos_dir(pid), "index.json"))
        n = len(idx if isinstance(idx, list) else idx.get("photos") or [])
        if n:
            out["photos_used"] = n
    except Exception:
        pass
    rounds = [int(m.group(1)) for f in (os.listdir(os.path.join(WORK, "compare", pid)) if os.path.isdir(os.path.join(WORK, "compare", pid)) else [])
              for m in [re.match(r"round(\d+)", f)] if m]
    if rounds:
        out["comparison_rounds"] = max(rounds)
    out["verified_from_photos"] = ["front", "back", "top"]
    out["notes"] = ("Built-in printer of Printers Size Lab, modelled from reference photos of the exact model and compared with "
                    "them side by side. The measurements and the model's status are in the project's repository.")
    return out


# --------------------------------------------------------------------------------------------
# the mesh
# --------------------------------------------------------------------------------------------
def glb_json(data):
    """Return the JSON chunk of a GLB, after the checks the page also makes."""
    if len(data) < 20 or data[:4] != b"glTF":
        raise SystemExit("not a binary glTF (GLB) file")
    version, length = struct.unpack("<II", data[4:12])
    if version != 2 or length != len(data):
        raise SystemExit("GLB header is wrong (version %d, length %d of %d bytes)" % (version, length, len(data)))
    clen, ctype = struct.unpack("<II", data[12:20])
    if ctype != 0x4E4F534A:
        raise SystemExit("the first GLB chunk is not JSON")
    return json.loads(data[20:20 + clen].decode("utf-8"))


def check_glb(data):
    j = glb_json(data)
    for kind in ("buffers", "images"):
        for i, b in enumerate(j.get(kind) or []):
            if "uri" in b:
                raise SystemExit("%s[%d] points to an outside file or URI (%r); export a self-contained GLB" % (kind, i, str(b["uri"])[:60]))
    acc = j.get("accessors") or []
    tris = 0
    for n in j.get("nodes") or []:
        if "mesh" not in n:
            continue
        for prim in j["meshes"][n["mesh"]].get("primitives") or []:
            if prim.get("mode", 4) != 4:
                continue
            a = prim.get("indices")
            cnt = acc[a]["count"] if a is not None else acc[prim["attributes"]["POSITION"]]["count"]
            tris += cnt // 3
    return j, tris


def pack_geom(geom, j):
    """The parts of a geom.json the page needs; it measures sizes, envelopes and cable space itself."""
    names = {n.get("name") for n in j.get("nodes") or []}
    parts = {}
    for part, info in (geom.get("parts") or {}).items():
        node = info.get("node")
        if node not in names and not any(str(x).startswith(node + ".") for x in names if x):
            print("  ! part %s: node %s is not in the GLB" % (part, node))
        parts[part] = {"node": node, "kind": info.get("kind", "body"), "hidden": bool(info.get("hidden"))}
        if info.get("pivot_m") is not None:
            parts[part]["pivot_m"] = info["pivot_m"]
    return {"frame": "glTF: metres, Y up, front +Z, origin at the bottom centre of the closed body",
            "parts": parts, "states": geom.get("states") or {}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id")
    ap.add_argument("--research", help="printer-file fields (JSON) to use instead of printers/<folder>/specs.json")
    ap.add_argument("--made-with", help="JSON file with the made_with block (overrides the research's own)")
    ap.add_argument("--glb", help="default docs/models/<id>.glb")
    ap.add_argument("--geom", help="default docs/data/<id>.geom.json")
    ap.add_argument("--out", help="default work/export/<id>.printer.json")
    a = ap.parse_args()
    pid = a.id
    glb = a.glb or os.path.join(DOCS, "models", pid + ".glb")
    gpath = a.geom or os.path.join(DOCS, "data", pid + ".geom.json")
    for p in (glb, gpath):
        if not os.path.exists(p):
            raise SystemExit("missing %s (run build/build_printer.py %s first)" % (p, pid))

    rpath = a.research or specs_path(pid)
    if not os.path.exists(rpath):
        raise SystemExit("missing research %s (give --research <file> with the printer-file fields)" % rpath)
    research = load(rpath)
    if is_printer_fields(research):
        fields = {k: research[k] for k in FIELDS if k in research}
        made_default = None
    else:
        fields = from_repo_research(pid, research)
        made_default = default_made_with(pid)
    if a.made_with:
        fields["made_with"] = load(a.made_with)
    elif "made_with" not in fields and made_default:
        fields["made_with"] = made_default
    if "made_with" not in fields:
        print("  ! no made_with block: add one to the research file (see the instructions), or pass --made-with")

    data = open(glb, "rb").read()
    if len(data) > MAX_GLB:
        raise SystemExit("the GLB is %.1f MB; the page accepts at most 8 MB. Use fewer segments or bevels." % (len(data) / 1e6))
    j, tris = check_glb(data)
    if tris > MAX_TRIS:
        raise SystemExit("the GLB has %d triangles; the page accepts at most %d." % (tris, MAX_TRIS))
    geom = pack_geom(load(gpath), j)

    out = {"format": FORMAT, "id": pid}
    out.update({k: v for k, v in fields.items() if k != "id"})
    out["model"] = {"glb_base64": base64.b64encode(data).decode("ascii"), "geom": geom}
    dst = a.out or os.path.join(ROOT, "work", "export", pid + ".printer.json")
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    gs = geom["states"]
    print("wrote %s (%.2f MB; GLB %.2f MB, %d triangles; parts: %s; states: %s)" % (
        dst, os.path.getsize(dst) / 1e6, len(data) / 1e6, tris, ", ".join(geom["parts"]), ", ".join(gs) or "none"))


if __name__ == "__main__":
    main()
