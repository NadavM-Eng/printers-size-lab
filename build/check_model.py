#!/usr/bin/env python3
"""
Checks a model for two things a still render does not show. Plain Python (numpy, Pillow); no Blender.

    python build/check_model.py <model.glb | file.printer.json>     # same-plane overlaps
    python build/check_model.py --colour <image> [x0,y0,x1,y1]      # the colour of part of a photo or render

Same-plane overlaps: two surfaces of DIFFERENT materials that lie in the same plane, face the same way
and overlap (a panel drawn flush on the body, glass lying exactly on a scanner bed). Neither is in front,
so they flicker ("z-fighting") as the camera turns. A still image shows one of them and looks fine.
Fix each one that can be seen: move one surface 0.05 cm in or out, or cut the surface under it.

Colour: prints the median colour of a region of an image as #rrggbb. The region is given as fractions
of the image (0,0 = top left, 1,1 = bottom right); the default is the middle fifth. Take each part's
colour from the maker's photos this way, then run it on the same spot of your render and compare.
"""
import base64
import json
import struct
import sys

import numpy as np

CT = {5120: "i1", 5121: "u1", 5122: "<i2", 5123: "<u2", 5125: "<u4", 5126: "<f4"}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


# --------------------------------------------------------------------------------------------
# reading a GLB (or the GLB inside a printer file)
# --------------------------------------------------------------------------------------------
def glb_bytes(path):
    if path.lower().endswith(".json"):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        b64 = (d.get("model") or {}).get("glb_base64")
        if not b64:
            raise SystemExit("%s has no model.glb_base64 (a shape recipe has nothing to check here)" % path)
        return base64.b64decode(b64)
    with open(path, "rb") as f:
        return f.read()


def parse_glb(b):
    if b[:4] != b"glTF":
        raise SystemExit("not a binary glTF file")
    off, js, bn = 12, None, None
    while off < len(b):
        ln, typ = struct.unpack_from("<I4s", b, off)
        chunk = b[off + 8: off + 8 + ln]
        if typ == b"JSON":
            js = json.loads(chunk)
        elif typ == b"BIN\x00":
            bn = chunk
        off += 8 + ln
    return js, bn


def _accessor(js, bn, i):
    a = js["accessors"][i]
    bv = js["bufferViews"][a["bufferView"]]
    n, dt = NC[a["type"]], np.dtype(CT[a["componentType"]])
    start = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    stride = bv.get("byteStride") or dt.itemsize * n
    if stride == dt.itemsize * n:
        arr = np.frombuffer(bn, dt, a["count"] * n, start).reshape(a["count"], n)
    else:
        arr = np.stack([np.frombuffer(bn, dt, n, start + k * stride) for k in range(a["count"])])
    return arr.astype(np.float64 if dt.kind == "f" else np.int64)


def _node_matrix(nd):
    if "matrix" in nd:
        return np.array(nd["matrix"], float).reshape(4, 4).T
    T, R, S = np.eye(4), np.eye(4), np.eye(4)
    if "translation" in nd:
        T[:3, 3] = nd["translation"]
    if "rotation" in nd:
        x, y, z, w = nd["rotation"]
        R[:3, :3] = [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]
    if "scale" in nd:
        S[0, 0], S[1, 1], S[2, 2] = nd["scale"]
    return T @ R @ S


def glb_prims(js, bn):
    """[(node name, material name, triangles[n, 3, 3] in metres, world space), ...]"""
    out = []

    def walk(i, M):
        nd = js["nodes"][i]
        M2 = M @ _node_matrix(nd)
        if "mesh" in nd:
            for pr in js["meshes"][nd["mesh"]]["primitives"]:
                if pr.get("mode", 4) != 4:
                    continue
                P = _accessor(js, bn, pr["attributes"]["POSITION"])
                P = (np.c_[P, np.ones(len(P))] @ M2.T)[:, :3]
                idx = _accessor(js, bn, pr["indices"]).reshape(-1, 3) if "indices" in pr else np.arange(len(P)).reshape(-1, 3)
                mat = js["materials"][pr["material"]].get("name", "material %d" % pr["material"]) if "material" in pr else "none"
                out.append((nd.get("name", "?"), mat, P[idx]))
        for c in nd.get("children", []):
            walk(c, M2)

    for r in js["scenes"][js.get("scene", 0)]["nodes"]:
        walk(r, np.eye(4))
    return out


# --------------------------------------------------------------------------------------------
# same-plane overlaps
# --------------------------------------------------------------------------------------------
def _raster(tris2d, lo, W, H, cell):
    """Boolean grid of the cells whose centre lies inside any of the 2D triangles."""
    mk = np.zeros((W, H), bool)
    for tri in tris2d:
        t0 = np.clip(np.floor((tri.min(0) - lo) / cell).astype(int), 0, [W - 1, H - 1])
        t1 = np.clip(np.ceil((tri.max(0) - lo) / cell).astype(int), 0, [W - 1, H - 1])
        xs = lo[0] + (np.arange(t0[0], t1[0] + 1) + 0.5) * cell
        ys = lo[1] + (np.arange(t0[1], t1[1] + 1) + 0.5) * cell
        X, Y = np.meshgrid(xs, ys, indexing="ij")
        p0, p1, p2 = tri
        den = (p1[1] - p2[1]) * (p0[0] - p2[0]) + (p2[0] - p1[0]) * (p0[1] - p2[1])
        if abs(den) < 1e-15:
            continue
        l1 = ((p1[1] - p2[1]) * (X - p2[0]) + (p2[0] - p1[0]) * (Y - p2[1])) / den
        l2 = ((p2[1] - p0[1]) * (X - p2[0]) + (p0[0] - p2[0]) * (Y - p2[1])) / den
        mk[t0[0]:t1[0] + 1, t0[1]:t1[1] + 1] |= (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
    return mk


def overlaps(prims, step=0.0001, cell=0.001, min_area_cm2=0.3, skip=("cable",)):
    """Surfaces of different materials in the same plane (within `step` metres), facing the same way and
    overlapping by at least `min_area_cm2`. Parts whose node name contains a word in `skip` are left out.
    Returns [{"a", "b", "normal", "offset_cm", "area_cm2"}, ...], largest first."""
    T, mat_id, names = [], [], []
    for node, mat, tris in prims:
        if any(s in node for s in skip) or not len(tris):
            continue
        if mat not in names:
            names.append(mat)
        T.append(np.asarray(tris, float))
        mat_id.append(np.full(len(tris), names.index(mat)))
    if not T:
        return []
    T, mat_id = np.concatenate(T), np.concatenate(mat_id)
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    ok = np.linalg.norm(n, axis=1) > 2e-9
    T, mat_id, n = T[ok], mat_id[ok], n[ok]
    n /= np.linalg.norm(n, axis=1, keepdims=True)
    d = (n * T[:, 0]).sum(1)
    found = {}
    for shift in (0.0, 0.5):          # two passes, so planes on either side of a bucket edge still meet
        key = np.c_[np.round(n * 100), np.floor(d / step + shift)].astype(np.int64)
        _, inv = np.unique(key, axis=0, return_inverse=True)
        inv = inv.ravel()
        order = np.argsort(inv, kind="stable")
        for grp in np.split(order, np.flatnonzero(np.diff(inv[order])) + 1):
            mats = np.unique(mat_id[grp])
            if len(mats) < 2:
                continue
            nn = n[grp[0]]
            a = np.cross(nn, [1.0, 0, 0] if abs(nn[0]) < 0.9 else [0, 1.0, 0])
            a /= np.linalg.norm(a)
            b = np.cross(nn, a)
            uv = np.stack([T[grp] @ a, T[grp] @ b], -1)
            lo, hi = uv.reshape(-1, 2).min(0), uv.reshape(-1, 2).max(0)
            W, H = (np.ceil((hi - lo) / cell).astype(int) + 1)
            if W * H > 4_000_000:
                continue
            masks = {m: _raster(uv[mat_id[grp] == m], lo, W, H, cell) for m in mats}
            ml = list(masks)
            for i in range(len(ml)):
                for j in range(i + 1, len(ml)):
                    cm2 = float((masks[ml[i]] & masks[ml[j]]).sum()) * cell * cell * 1e4
                    if cm2 >= min_area_cm2:
                        k = (names[ml[i]], names[ml[j]], tuple(round(float(x), 2) + 0.0 for x in nn), round(float(d[grp[0]]) * 100, 1))
                        found[k] = max(found.get(k, 0.0), cm2)
    return [{"a": k[0], "b": k[1], "normal": k[2], "offset_cm": k[3], "area_cm2": round(v, 1)}
            for k, v in sorted(found.items(), key=lambda x: -x[1])]


def facing(normal, frame="gltf"):
    """'up', 'front', ... for an axis-aligned normal, else the vector. frame: 'gltf' (Y up, front +Z)
    or 'blender' (Z up, front -Y)."""
    words = ({(0, 1, 0): "up", (0, -1, 0): "down", (0, 0, 1): "front", (0, 0, -1): "back", (1, 0, 0): "right", (-1, 0, 0): "left"}
             if frame == "gltf" else
             {(0, 0, 1): "up", (0, 0, -1): "down", (0, -1, 0): "front", (0, 1, 0): "back", (1, 0, 0): "right", (-1, 0, 0): "left"})
    key = tuple(int(round(x)) for x in normal)
    return words[key] if key in words and max(abs(x - k) for x, k in zip(normal, key)) < 0.02 else "(%.2f, %.2f, %.2f)" % tuple(normal)


def print_overlaps(res, frame="gltf", limit=12, indent="  "):
    if not res:
        print(indent + "no same-plane overlaps")
        return
    print(indent + "! %d same-plane overlaps, %.0f cm2 in total. They flicker when the camera turns. For each one that"
          % (len(res), sum(r["area_cm2"] for r in res)))
    print(indent + "  can be seen, move one surface 0.05 cm in or out, or cut the surface under it:")
    for r in res[:limit]:
        print(indent + "  %7.1f cm2  %-18s x %-18s facing %s, plane at %.1f cm" % (
            r["area_cm2"], r["a"][:18], r["b"][:18], facing(r["normal"], frame), r["offset_cm"]))
    if len(res) > limit:
        print(indent + "  ... and %d smaller ones" % (len(res) - limit))


# --------------------------------------------------------------------------------------------
# colour of a region of an image
# --------------------------------------------------------------------------------------------
def image_colour(path, box=None):
    """Median colour of a region as '#rrggbb'. box = (x0, y0, x1, y1) as fractions of the image."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    x0, y0, x1, y1 = box or (0.4, 0.4, 0.6, 0.6)
    w, h = im.size
    crop = np.asarray(im.crop((int(x0 * w), int(y0 * h), max(int(x0 * w) + 1, int(x1 * w)), max(int(y0 * h) + 1, int(y1 * h)))))
    r, g, b = (int(round(float(v))) for v in np.median(crop.reshape(-1, 3), axis=0))
    return "#%02x%02x%02x" % (r, g, b)


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] in ("--colour", "--color"):
        if len(argv) < 2:
            raise SystemExit("usage: check_model.py --colour <image> [x0,y0,x1,y1]")
        box = tuple(float(v) for v in argv[2].split(",")) if len(argv) > 2 else None
        if box and (len(box) != 4 or not all(0 <= v <= 1 for v in box) or box[0] >= box[2] or box[1] >= box[3]):
            raise SystemExit("the region is x0,y0,x1,y1 as fractions between 0 and 1, top left first")
        print(image_colour(argv[1], box))
        return 0
    bad = 0
    for path in argv:
        js, bn = parse_glb(glb_bytes(path))
        res = overlaps(glb_prims(js, bn))
        print(path)
        print_overlaps(res, "gltf")
        bad += len(res)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
