"""
printer_kit: shared toolkit for building printer models headlessly with Blender's Python module (bpy).

Conventions (inside Blender)
- Units in the builder API: centimetres. Meshes are stored in metres.
- Z is up. The printer's FRONT faces -Y, its BACK faces +Y, width runs along X
  (+X is on your right when you stand in front of the printer).
- Origin: x = 0 at the centre of the width, y = 0 at the centre of the closed body's depth,
  z = 0 at the underside of the feet (the shelf surface).

Export: GLB in metres, glTF Y-up (export_yup). In glTF space the front faces +Z, up is +Y,
the back is at -Z. Every object becomes one node named "<id>_<part>".

A builder is a module with `class Builder(Printer)` that implements build() and optionally states().
See builders/_example.py.
"""
import json
import math
import os
import sys
import tempfile

import numpy as np
import bpy
import bmesh
from mathutils import Matrix, Vector

CM = 0.01
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import paths  # noqa: E402
from paths import printer_dir, specs_path, photos_dir  # noqa: E402,F401

ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
MODELS_DIR = os.path.join(DOCS, "models")
DATA_DIR = os.path.join(DOCS, "data")
WORK = paths.WORK
TMP = tempfile.mkdtemp(prefix="pkit_")
# build/fonts holds the DejaVu fonts the builders ask for, so logos look the same on every machine
FONT_DIRS = [os.path.join(HERE, "fonts"), "/usr/share/fonts", r"C:\Windows\Fonts"]
# Cycles threads per process. Several builds may run at once, so don't take every core.
THREADS = int(os.environ.get("PSL_THREADS") or min(8, os.cpu_count() or 2))


# --------------------------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------------------------
def nrm(v):
    v = np.asarray(v, float)
    return v / max(np.linalg.norm(v), 1e-12)


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)])


def srgb2lin(c):
    c = np.asarray(c, float)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin(hexcol):
    """sRGB hex -> linear RGBA tuple for Principled BSDF (forgetting this makes black look grey)."""
    return (*srgb2lin(hexrgb(hexcol)), 1.0)


def find_font(*names):
    """Return the first font file whose name contains one of `names` (case-insensitive)."""
    for font_dir in FONT_DIRS:
        for root, _, files in os.walk(font_dir):
            for f in sorted(files):
                for n in names:
                    if n.lower() in f.lower() and f.lower().endswith((".ttf", ".otf")):
                        return os.path.join(root, f)
    return None


# --------------------------------------------------------------------------------------------
# 2D profile helpers (all in cm). Profiles are closed polygons [(u, v), ...].
# --------------------------------------------------------------------------------------------
def fillet(poly, r, n=6):
    """Round the corners of a closed polygon. r: one radius or one per vertex (0 = sharp)."""
    P = np.asarray(poly, float)
    m = len(P)
    R = np.broadcast_to(np.asarray(r, float), (m,))
    out = []
    for i in range(m):
        p0, p1, p2 = P[i - 1], P[i], P[(i + 1) % m]
        ri = float(R[i])
        a, b = p0 - p1, p2 - p1
        la, lb = np.linalg.norm(a), np.linalg.norm(b)
        if ri <= 0 or la < 1e-9 or lb < 1e-9:
            out.append(p1)
            continue
        a, b = a / la, b / lb
        ang = math.acos(float(np.clip(np.dot(a, b), -1, 1)))
        if ang < 1e-3 or abs(ang - math.pi) < 1e-3:
            out.append(p1)
            continue
        t = min(ri / math.tan(ang / 2), 0.49 * la, 0.49 * lb)
        re = t * math.tan(ang / 2)
        q0, q2 = p1 + a * t, p1 + b * t
        c = p1 + nrm(a + b) * (re / math.sin(ang / 2))
        a0 = math.atan2(q0[1] - c[1], q0[0] - c[0])
        a2 = math.atan2(q2[1] - c[1], q2[0] - c[0])
        d = (a2 - a0 + math.pi) % (2 * math.pi) - math.pi
        for k in range(n + 1):
            th = a0 + d * k / n
            out.append(c + re * np.array([math.cos(th), math.sin(th)]))
    return np.array(out)


def rrect(w, h, r, cx=0.0, cy=0.0, n=6):
    """Rounded rectangle centred at (cx, cy)."""
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
    return fillet(pts, r, n)


def arc(cx, cy, r, a0_deg, a1_deg, n=12):
    """Points on an arc (useful inside hand-made profiles)."""
    a = np.radians(np.linspace(a0_deg, a1_deg, n + 1))
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)


# --------------------------------------------------------------------------------------------
# scene + materials
# --------------------------------------------------------------------------------------------
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


class Mats:
    """Principled BSDF materials keyed by name. Colours are sRGB hex; converted to linear."""

    def __init__(self):
        self.cache = {}

    def get(self, key, color="#808080", rough=0.5, metal=0.0, emit=None, emit_strength=1.5,
            alpha=1.0, coat=0.0, image=None):
        if key in self.cache:
            return self.cache[key]
        m = bpy.data.materials.new(key)
        try:
            m.use_nodes = True
        except Exception:
            pass
        nt = m.node_tree
        b = nt.nodes.get("Principled BSDF")
        b.inputs["Base Color"].default_value = lin(color)
        b.inputs["Roughness"].default_value = rough
        b.inputs["Metallic"].default_value = metal
        if coat:
            b.inputs["Coat Weight"].default_value = coat
        if emit:
            b.inputs["Emission Color"].default_value = lin(emit)
            b.inputs["Emission Strength"].default_value = emit_strength
        if image is not None:
            img = bpy.data.images.load(image)
            img.pack()
            tex = nt.nodes.new("ShaderNodeTexImage")
            tex.image = img
            nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
            nt.links.new(tex.outputs["Alpha"], b.inputs["Alpha"])
            try:
                m.surface_render_method = "BLENDED"
            except Exception:
                m.blend_method = "BLEND"
        elif alpha < 1.0:
            b.inputs["Alpha"].default_value = alpha
            try:
                m.surface_render_method = "BLENDED"
            except Exception:
                m.blend_method = "BLEND"
        self.cache[key] = m
        return m


# --------------------------------------------------------------------------------------------
# mesh primitives (cm in, metres stored)
# --------------------------------------------------------------------------------------------
def _link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob


def mesh_obj(name, verts_cm, faces, mat=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(float(x) * CM for x in v) for v in verts_cm], [], [list(f) for f in faces])
    me.update()
    ob = bpy.data.objects.new(name, me)
    if mat is not None:
        me.materials.append(mat)
    _link(ob)
    recalc_normals(ob)
    return ob


def recalc_normals(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()


def _plane_to3(axis, u, v, a):
    if axis == "x":   # profile in the side plane: u = y (front -, back +), v = z
        return (a, u, v)
    if axis == "y":   # profile in the front plane: u = x, v = z
        return (u, a, v)
    return (u, v, a)  # axis "z": profile in plan: u = x, v = y


def extrude(name, mat, prof, axis="x", a0=-10.0, a1=10.0, bevel=0.0, seg=3, angle=30.0):
    """Extrude a closed 2D profile (cm) along an axis from a0 to a1 (cm).
    axis="x": side profile (u = y, v = z) extruded across the width.
    axis="y": front profile (u = x, v = z) extruded front-to-back.
    axis="z": plan profile (u = x, v = y) extruded upward.
    bevel: edge rounding in cm, applied at bake time with an angle limit."""
    P = np.asarray(prof, float)
    keep = np.ones(len(P), bool)
    keep[1:] = np.linalg.norm(np.diff(P, axis=0), axis=1) > 1e-6
    P = P[keep]
    if np.linalg.norm(P[0] - P[-1]) < 1e-6:
        P = P[:-1]
    n = len(P)
    verts = [_plane_to3(axis, u, v, a0) for u, v in P] + [_plane_to3(axis, u, v, a1) for u, v in P]
    faces = [list(range(n))[::-1], list(range(n, 2 * n))] + [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    ob = mesh_obj(name, verts, faces, mat)
    if bevel > 0:
        ob["bevel"] = [float(bevel), int(seg), float(angle)]
    return ob


def box(name, mat, x0, x1, y0, y1, z0, z1, bevel=0.0, seg=3, angle=30.0):
    """Axis-aligned box from corner coordinates (cm)."""
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    ob = mesh_obj(name, v, f, mat)
    if bevel > 0:
        ob["bevel"] = [float(bevel), int(seg), float(angle)]
    return ob


def cyl(name, mat, center, axis, r, length, seg=24, r2=None, bevel=0.0):
    """Cylinder (or cone if r2 is given) centred at `center` (cm) along axis 'x', 'y', 'z' or a vector."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg,
                          radius1=r * CM, radius2=(r if r2 is None else r2) * CM, depth=length * CM)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    if mat is not None:
        me.materials.append(mat)
    _link(ob)
    ax = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}.get(axis, axis)
    rot = Vector((0, 0, 1)).rotation_difference(Vector(ax)).to_matrix().to_4x4()
    me.transform(rot)
    me.transform(Matrix.Translation(Vector(np.asarray(center, float) * CM)))
    me.update()
    if bevel > 0:
        ob["bevel"] = [float(bevel), 2, 30.0]
    return ob


def tube(name, mat, path_cm, r, n=12):
    """A round tube (cable) along a polyline path (cm), with end caps."""
    P = np.asarray(path_cm, float)
    T = np.gradient(P, axis=0)
    T = T / np.clip(np.linalg.norm(T, axis=1, keepdims=True), 1e-9, None)
    up = np.array([0.0, 0.0, 1.0])
    rings = []
    prevN = None
    for i, t in enumerate(T):
        ref = up if abs(np.dot(up, t)) < 0.9 else np.array([1.0, 0.0, 0.0])
        Nn = ref - np.dot(ref, t) * t
        Nn /= np.linalg.norm(Nn)
        if prevN is not None:   # keep the frame from twisting
            Nn2 = prevN - np.dot(prevN, t) * t
            if np.linalg.norm(Nn2) > 1e-6:
                Nn = Nn2 / np.linalg.norm(Nn2)
        prevN = Nn
        B = np.cross(t, Nn)
        a = np.linspace(0, 2 * np.pi, n, endpoint=False)
        rings.append(P[i] + r * (np.cos(a)[:, None] * Nn + np.sin(a)[:, None] * B))
    V = np.concatenate(rings)
    m = len(P)
    F = []
    for i in range(m - 1):
        for j in range(n):
            F.append([i * n + j, i * n + (j + 1) % n, (i + 1) * n + (j + 1) % n, (i + 1) * n + j])
    F.append(list(range(n))[::-1])
    F.append([(m - 1) * n + j for j in range(n)])
    return mesh_obj(name, V, F, mat)


def bend_path(start, dirs_lengths, radius=3.0, step=0.6):
    """Polyline for a cable: start point (cm) then a list of (direction vector, length) legs.
    Corners between legs are rounded with `radius` (cm). Returns an (N, 3) array."""
    pts = [np.asarray(start, float)]
    for d, L in dirs_lengths:
        pts.append(pts[-1] + nrm(d) * L)
    P = np.array(pts)
    out = [P[0]]
    for i in range(1, len(P) - 1):
        a, b, c = P[i - 1], P[i], P[i + 1]
        u, w = nrm(a - b), nrm(c - b)
        ang = math.acos(float(np.clip(np.dot(u, w), -1, 1)))
        if abs(ang - math.pi) < 1e-3:
            out.append(b)
            continue
        fa = 0.98 if i == 1 else 0.49            # the first and last legs aren't shared with another corner
        fc = 0.98 if i == len(P) - 2 else 0.49
        t = min(radius / math.tan(ang / 2), fa * np.linalg.norm(a - b), fc * np.linalg.norm(c - b))
        re = t * math.tan(ang / 2)
        q0, q2 = b + u * t, b + w * t
        ctr = b + nrm(u + w) * (re / math.sin(ang / 2))
        e1, e2 = q0 - ctr, q2 - ctr
        k = max(3, int(re * (math.pi - ang) / step))
        for s in np.linspace(0, 1, k):   # slerp between e1 and e2 around ctr
            om = math.acos(float(np.clip(np.dot(nrm(e1), nrm(e2)), -1, 1)))
            if om < 1e-6:
                out.append(ctr + e1)
            else:
                out.append(ctr + (math.sin((1 - s) * om) * e1 + math.sin(s * om) * e2) / math.sin(om))
    out.append(P[-1])
    Q = [out[0]]
    for p in out[1:]:
        if np.linalg.norm(p - Q[-1]) > 1e-4:
            Q.append(p)
    return np.array(Q)


def text3d(name, mat, text, size_cm, center_cm, facing="-y", depth_cm=0.05, font=None, align="CENTER"):
    """Raised 3D text (logos, labels). facing: which way the text faces ('-y' = front, '+y' = back,
    '+z' = up, '-x' / '+x' = sides). center_cm is the centre of the text on that face."""
    cu = bpy.data.curves.new(name + "_crv", type="FONT")
    cu.body = text
    cu.size = size_cm * CM
    cu.extrude = depth_cm * CM / 2
    cu.align_x = align
    cu.align_y = "CENTER"
    if font:
        cu.font = bpy.data.fonts.load(font)
    tmp = bpy.data.objects.new(name + "_tmp", cu)
    _link(tmp)
    deps = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(deps), depsgraph=deps)
    bpy.data.objects.remove(tmp)
    bpy.data.curves.remove(cu)
    # text is built in XY facing +Z; rotate it to face the requested direction
    R = {
        "+z": Matrix.Identity(4),
        "-y": Matrix.Rotation(math.radians(90), 4, "X"),
        "+y": Matrix.Rotation(math.radians(90), 4, "X") @ Matrix.Rotation(math.radians(180), 4, "Y"),
        "+x": Matrix.Rotation(math.radians(90), 4, "Z") @ Matrix.Rotation(math.radians(90), 4, "X"),
        "-x": Matrix.Rotation(math.radians(-90), 4, "Z") @ Matrix.Rotation(math.radians(90), 4, "X"),
    }[facing]
    me.transform(R)
    me.transform(Matrix.Translation(Vector(np.asarray(center_cm, float) * CM)))
    ob = bpy.data.objects.new(name, me)
    me.materials.clear()
    if mat is not None:
        me.materials.append(mat)
    _link(ob)
    return ob


def decal(name, image_path, center_cm, w_cm, h_cm, facing="-y", mats=None, rough=0.4):
    """A thin textured plane (control-panel graphics, labels). Place it ~0.03 cm above the surface."""
    m = (mats or Mats()).get("decal_" + os.path.basename(image_path), image=image_path, rough=rough)
    u, v = w_cm / 2, h_cm / 2
    V = [(-u, -v, 0), (u, -v, 0), (u, v, 0), (-u, v, 0)]
    ob = mesh_obj(name, V, [(0, 1, 2, 3)], m)
    me = ob.data
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li, vi in zip(poly.loop_indices, poly.vertices):
            x, y, _ = me.vertices[vi].co
            uvl.data[li].uv = (0.0 if x < 0 else 1.0, 0.0 if y < 0 else 1.0)
    R = {
        "+z": Matrix.Identity(4),
        "-y": Matrix.Rotation(math.radians(90), 4, "X"),
        "+y": Matrix.Rotation(math.radians(90), 4, "X") @ Matrix.Rotation(math.radians(180), 4, "Y"),
        "+x": Matrix.Rotation(math.radians(90), 4, "Z") @ Matrix.Rotation(math.radians(90), 4, "X"),
        "-x": Matrix.Rotation(math.radians(-90), 4, "Z") @ Matrix.Rotation(math.radians(90), 4, "X"),
    }[facing]
    me.transform(R)
    me.transform(Matrix.Translation(Vector(np.asarray(center_cm, float) * CM)))
    me.update()
    return ob


# --------------------------------------------------------------------------------------------
# booleans, baking, shading
# --------------------------------------------------------------------------------------------
def cut(target, cutter, op="DIFFERENCE"):
    """Queue a boolean (applied at bake time). The cutter is removed after baking."""
    m = target.modifiers.new("bool_%d" % len(target.modifiers), "BOOLEAN")
    m.object = cutter
    m.operation = op
    m.solver = "EXACT"
    cutter["cutter"] = True
    cutter.hide_render = True
    return m


def bake(ob):
    """Apply booleans, then the stored bevel, into a plain mesh."""
    if "bevel" in ob.keys():
        w, seg, ang = ob["bevel"]
        m = ob.modifiers.new("bevel", "BEVEL")
        m.width = w * CM
        m.segments = int(seg)
        m.limit_method = "ANGLE"
        m.angle_limit = math.radians(ang)
        m.use_clamp_overlap = True
        m.profile = 0.5
        m.miter_outer = "MITER_ARC"
        del ob["bevel"]
    if not ob.modifiers:
        return
    deps = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(deps), preserve_all_data_layers=True, depsgraph=deps)
    old = ob.data
    ob.modifiers.clear()
    ob.data = me
    if old.users == 0:
        bpy.data.meshes.remove(old)


def smooth_by_angle(ob, deg=32.0):
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    lim = math.radians(deg)
    for f in bm.faces:
        f.smooth = True
    for e in bm.edges:
        if len(e.link_faces) == 2:
            e.smooth = e.calc_face_angle(0.0) <= lim
        else:
            e.smooth = False
    bm.to_mesh(me)
    bm.free()
    me.update()


def join(objs, name):
    """Merge several objects (same part) into one. Bakes each first."""
    objs = [o for o in objs if o is not None]
    for o in objs:
        bake(o)
    base = objs[0]
    deps = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    mats = []
    for o in objs:
        me = o.data
        offset = len(mats)
        for m in me.materials:
            mats.append(m)
        tmp = me.copy()
        tmp.transform(o.matrix_world)
        for p in tmp.polygons:
            p.material_index += offset
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    _link(ob)
    for o in objs:
        bpy.data.objects.remove(o)
    return ob


def mesh_world_verts(ob):
    M = np.array(ob.matrix_world)
    V = np.array([v.co for v in ob.data.vertices], float)
    if len(V) == 0:
        return V
    return (np.c_[V, np.ones(len(V))] @ M.T)[:, :3]


def b2g(v):
    """Blender (x, y, z) -> glTF (x, z, -y)."""
    x, y, z = v
    return [x, z, -y]


# --------------------------------------------------------------------------------------------
# connectors and cables
# --------------------------------------------------------------------------------------------
# Typical connector sizes in cm: (plug face width, plug face height, housing length beyond the
# socket face, strain-relief length, cable diameter, minimum bend radius to the cable centre).
PLUGS = {
    "C13":   (2.2, 1.6, 3.4, 2.4, 0.75, 3.0),   # kettle-style IEC plug (3 pins)
    "C7":    (1.8, 0.95, 2.8, 1.8, 0.60, 2.4),  # "figure 8" 2-pin plug
    "C5":    (2.0, 1.5, 3.0, 2.0, 0.70, 2.8),   # "cloverleaf" 3-pin plug
    "DC":    (1.1, 1.1, 2.6, 1.6, 0.40, 1.8),   # barrel jack plug from an external adapter
    "USB-B": (1.6, 1.1, 3.0, 1.5, 0.45, 2.0),
    "RJ45":  (1.4, 1.25, 2.4, 1.6, 0.55, 2.2),
    "RJ11":  (1.0, 0.9, 2.0, 1.0, 0.40, 1.6),
}


class Printer:
    """Base class for printer builders.

    In build(), create geometry with the helpers and register every object with self.add():
        self.add("body", ob)                       -> node "<id>_body"
        self.add("lid", ob, pivot=(x, y, z))       -> moving part; pivot = hinge point (cm)
        self.add("cable_power", ob, kind="cable")  -> cables are excluded from body dimensions
    In states(), return {"printing": [...], "refill": [...], "lid_open": [...]} where each item is
        ("rot", part, axis, degrees)    axis: 'x', 'y', 'z' or a vector (Blender frame), about the part's pivot
        ("move", part, (dx, dy, dz))    in cm (Blender frame)
        ("show", part) / ("hide", part) parts created hidden-by-default use self.add(..., hidden=True)
    """

    def __init__(self, pid, official=None):
        self.id = pid
        self.official = official or {}
        self.mats = Mats()
        self.parts = {}       # part -> object
        self.meta = {}        # part -> dict(kind, pivot, hidden)
        self.sockets = []     # info about back connectors for the site
        self.notes = []

    # --- materials shortcut -------------------------------------------------------------------
    def mat(self, key, color="#808080", rough=0.5, **kw):
        return self.mats.get(key, color, rough, **kw)

    # --- registration ---------------------------------------------------------------------------
    def add(self, part, ob, kind="body", pivot=None, hidden=False):
        """Register an object as part `part`. Several adds with the same part name are joined."""
        if part in self.parts:
            ob = join([self.parts[part], ob], "%s_%s" % (self.id, part))
        else:
            ob.name = "%s_%s" % (self.id, part)
        self.parts[part] = ob
        m = self.meta.setdefault(part, {"kind": kind, "pivot": None, "hidden": hidden})
        if pivot is not None:
            m["pivot"] = [float(c) for c in pivot]
        m["kind"] = kind if kind != "body" or m["kind"] == "body" else m["kind"]
        m["hidden"] = m["hidden"] or hidden
        return ob

    # --- back connectors ---------------------------------------------------------------------------
    def plug_cable(self, part, kind, x, z, back_y, recess=0.0, exit="down", drop_to=0.4, run=None,
                   angled=False, mat=None, squash=True):
        """Model a plug pushed into a socket on the back plus its cable, as one cable part.
        x, z: socket centre (cm); back_y: y of the back surface at that spot (cm, positive);
        recess: how deep the socket face sits inside the outline (cm, 0 = flush/flat back);
        exit: where the cable heads after the strain relief: 'down' to the shelf, or 'side'.
        run: optional (dx, dy) to lay the cable along the shelf after it drops.
        angled: a right-angle plug (cable leaves sideways right at the plug).
        squash: the printer is pushed back until the cable presses against the wall, so the cable
        bends tightly right after the strain relief (the user's rule: a socket recessed in a pocket
        needs only 1-2 cm for the squashed cable; a plug on a flat back adds its own length, 5-8 cm).
        Returns the cable's furthest y behind the printer (cm)."""
        fw, fh, L, sr, dia, bend = PLUGS[kind]
        if squash:
            bend = max(dia * 1.2, 0.8)
        m = mat or self.mat("cable", "#141414", 0.55)
        y_face = back_y - recess
        objs = [box("plug", m, x - fw / 2, x + fw / 2, y_face, y_face + L, z - fh / 2, z + fh / 2, bevel=0.15, seg=2)]
        if angled:
            start = np.array([x, y_face + L * 0.6, z - fh / 2])
            legs = [((0, 0, -1), max(0.5, z - drop_to - fh / 2))]
        else:
            objs.append(cyl("relief", m, (x, y_face + L + sr / 2, z), "y", dia * 0.85, sr, seg=14, r2=dia * 0.55))
            start = np.array([x, y_face + L + sr - 0.2, z])
            # the cable leaves the strain relief and bends down with its minimum bend radius
            legs = [((0, 1, 0), bend * 1.02), ((0, 0, -1), max(bend * 1.05, z - drop_to))]
        if run is not None:
            legs.append(((run[0], run[1], 0), math.hypot(run[0], run[1])))
        path = bend_path(start, legs, radius=bend)
        objs.append(tube("cable", m, path, dia / 2, n=10))
        ob = join(objs, "%s_%s" % (self.id, part))
        self.add(part, ob, kind="cable")
        far = float(mesh_world_verts(ob)[:, 1].max() / CM)
        self.sockets.append({"part": part, "kind": kind, "x": x, "z": z, "recess": recess,
                             "angled": angled, "far_y_cm": round(far, 2)})
        return far

    # --- to be implemented by builders -------------------------------------------------------
    def build(self):
        raise NotImplementedError

    def states(self):
        return {}

    # --- pipeline ------------------------------------------------------------------------------
    def finish(self):
        """Bake every part, delete cutters, set pivots, shade."""
        for ob in list(bpy.data.objects):
            if ob.get("cutter"):
                continue
            bake(ob)
        for ob in list(bpy.data.objects):
            if ob.get("cutter"):
                bpy.data.objects.remove(ob)
        registered = set(o.name for o in self.parts.values())
        for ob in list(bpy.data.objects):
            if ob.name not in registered:
                print("  ! unregistered object removed:", ob.name)
                bpy.data.objects.remove(ob)
        for part, ob in self.parts.items():
            piv = self.meta[part]["pivot"]
            if piv is not None:
                p = Vector(np.asarray(piv, float) * CM)
                ob.data.transform(Matrix.Translation(-p))
                ob.location = p
            smooth_by_angle(ob)
            ob.data.update()

    def _state_ops(self):
        out = {}
        for st, ops in self.states().items():
            lst = []
            for op in ops:
                if op[0] == "rot":
                    _, part, axis, deg = op
                    ax = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}.get(axis, axis)
                    lst.append({"part": part, "rot": [float(a) for a in ax], "deg": float(deg)})
                elif op[0] == "move":
                    _, part, d = op
                    lst.append({"part": part, "move": [float(a) for a in d]})
                elif op[0] in ("show", "hide"):
                    lst.append({"part": op[1], op[0]: True})
                else:
                    raise ValueError("unknown state op %r" % (op,))
                if lst[-1]["part"] not in self.parts:
                    raise ValueError("state %s uses unknown part %s" % (st, lst[-1]["part"]))
            out[st] = lst
        return out

    def _verts_in_state(self, ops, include_kinds=("body", "moving", "detail"), include_hidden=False):
        """World vertices (cm, Blender frame) of the chosen parts with state ops applied."""
        rot = {}
        move = {}
        vis = {p: not m["hidden"] for p, m in self.meta.items()}
        for o in ops:
            p = o["part"]
            if "rot" in o:
                R = Matrix.Rotation(math.radians(o["deg"]), 4, Vector(o["rot"]))
                rot[p] = R @ rot.get(p, Matrix.Identity(4))
            if "move" in o:
                move[p] = np.asarray(move.get(p, (0, 0, 0))) + np.asarray(o["move"])
            if o.get("show"):
                vis[p] = True
            if o.get("hide"):
                vis[p] = False
        allv = []
        for part, ob in self.parts.items():
            m = self.meta[part]
            if m["kind"] not in include_kinds or not (vis[part] or include_hidden):
                continue
            V = np.array([v.co for v in ob.data.vertices], float)
            if part in rot:
                V = V @ np.array(rot[part].to_3x3()).T
            V = V + np.array(ob.location)
            if part in move:
                V = V + np.asarray(move[part]) * CM
            allv.append(V / CM)
        return np.concatenate(allv) if allv else np.zeros((0, 3))

    def report(self, state_ops):
        V = self._verts_in_state([])
        mn, mx = V.min(0), V.max(0)
        size = mx - mn
        print("  body (closed): W %.1f  D %.1f  H %.1f cm   [x %.1f..%.1f  y %.1f..%.1f  z %.1f..%.1f]" % (
            size[0], size[1], size[2], mn[0], mx[0], mn[1], mx[1], mn[2], mx[2]))
        off = self.official
        if off.get("w"):
            print("  official:      W %.1f  D %.1f  H %.1f cm   (diff %+.1f %+.1f %+.1f)" % (
                off["w"] / 10, off["d"] / 10, off["h"] / 10,
                size[0] - off["w"] / 10, size[1] - off["d"] / 10, size[2] - off["h"] / 10))
        env = {}
        for st, ops in [("closed", [])] + list(state_ops.items()):
            Vs = self._verts_in_state(ops)
            a, b = Vs.min(0), Vs.max(0)
            env[st] = {"min": [round(float(c), 2) for c in a], "max": [round(float(c), 2) for c in b]}
            if st != "closed":
                print("  %-9s     W %.1f  D %.1f  H %.1f cm" % (st, *(b - a)))
        Vc = self._verts_in_state([], include_kinds=("cable",))
        back_gap = None
        if len(Vc):
            back_gap = float(Vc[:, 1].max() - mx[1])
            print("  cables reach %.1f cm behind the back" % back_gap)
        tris = sum(sum(len(p.vertices) - 2 for p in ob.data.polygons) for ob in self.parts.values())
        print("  triangles: %d" % tris)
        return {"size_cm": [round(float(c), 2) for c in size], "min_cm": [round(float(c), 2) for c in mn],
                "max_cm": [round(float(c), 2) for c in mx], "envelopes_cm": env,
                "cable_back_gap_cm": None if back_gap is None else round(back_gap, 2), "triangles": tris}

    def export(self, glb_path=None, json_path=None):
        glb_path = glb_path or os.path.join(MODELS_DIR, self.id + ".glb")
        json_path = json_path or os.path.join(DATA_DIR, self.id + ".geom.json")
        os.makedirs(os.path.dirname(glb_path), exist_ok=True)
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        ops = self._state_ops()
        rep = self.report(ops)
        for o in bpy.data.objects:
            o.select_set(True)
        bpy.ops.export_scene.gltf(filepath=glb_path, export_format="GLB", export_yup=True,
                                  export_apply=True, export_materials="EXPORT", use_selection=False)
        size_mb = os.path.getsize(glb_path) / 1e6
        print("  wrote %s (%.2f MB)" % (glb_path, size_mb))

        def gbox(e):   # Blender-frame cm box -> glTF-frame metres box
            a, b = np.array(e["min"]) * CM, np.array(e["max"]) * CM
            ga, gb = b2g(a), b2g(b)
            return {"min": [round(min(p, q), 4) for p, q in zip(ga, gb)],
                    "max": [round(max(p, q), 4) for p, q in zip(ga, gb)]}

        geom = {
            "id": self.id,
            "frame": "glTF: metres, Y up, front +Z, origin at the bottom centre of the closed body",
            "nodes": {p: "%s_%s" % (self.id, p) for p in self.parts},
            "parts": {p: {"node": "%s_%s" % (self.id, p), "kind": m["kind"], "hidden": m["hidden"],
                          "pivot_m": None if m["pivot"] is None else [round(c, 4) for c in b2g(np.array(m["pivot"]) * CM)]}
                      for p, m in self.meta.items()},
            "states": {st: [dict(o, **({"rot": [round(c, 5) for c in b2g(o["rot"])]} if "rot" in o else {}),
                                 **({"move": [round(c, 4) for c in b2g(np.array(o["move"]) * CM)]} if "move" in o else {}))
                            for o in lst] for st, lst in ops.items()},
            "body_size_cm": rep["size_cm"],
            "envelopes_m": {st: gbox(e) for st, e in rep["envelopes_cm"].items()},
            "cable_back_gap_cm": rep["cable_back_gap_cm"],
            "sockets": self.sockets,
            "triangles": rep["triangles"],
            "glb_mb": round(size_mb, 2),
            "notes": self.notes,
        }
        with open(json_path, "w") as f:
            json.dump(geom, f, indent=1)
        print("  wrote", json_path)
        if size_mb > 6:
            print("  ! GLB is larger than 6 MB")
        if rep["triangles"] > 150000:
            print("  ! more than 150k triangles")
        return geom


def load_builder(pid):
    """Load builders/<pid with - as _>.py with every kit name injected; returns its Builder class.
    Builders can use it to subclass a sibling, e.g. Base = load_builder("brother-hl-l2400dw")."""
    import importlib.util
    mod_name = pid.replace("-", "_")
    path = os.path.join(HERE, "builders", mod_name + ".py")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    g = globals()
    for k, v in g.items():
        if not k.startswith("__"):
            setattr(mod, k, v)
    spec.loader.exec_module(mod)
    return mod.Builder


# --------------------------------------------------------------------------------------------
# rendering (photo-matched views) and comparison sheets
# --------------------------------------------------------------------------------------------
LIGHT_GAIN = 1.0   # scale all render lights (raise if renders look too dark, lower if washed out)

VIEWS = {
    # name: (azimuth deg around Z measured from the front (-Y), elevation deg, lens mm)
    "front": (0, 4, 100), "back": (180, 4, 100), "left": (-90, 4, 100), "right": (90, 4, 100),
    "top": (0, 89.5, 100), "bottom": (0, -89.5, 100),
    "34fl": (-40, 22, 70), "34fr": (40, 22, 70), "34bl": (-140, 22, 70), "34br": (140, 22, 70),
}


def setup_render(size=900, samples=48, bg="#d9d9d6"):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.render.threads_mode = "FIXED"
    sc.render.threads = THREADS
    try:
        sc.cycles.use_denoising = True
    except Exception:
        pass
    sc.render.resolution_x = size
    sc.render.resolution_y = size
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0.0
    w = bpy.data.worlds.new("w")
    sc.world = w
    try:
        w.use_nodes = True
    except Exception:
        pass
    bgn = w.node_tree.nodes.get("Background")
    bgn.inputs[0].default_value = lin(bg)
    bgn.inputs[1].default_value = 0.6


def _light(name, kind, loc, energy, size=1.0, target=(0, 0, 0)):
    ld = bpy.data.lights.new(name, kind)
    ld.energy = energy
    if kind == "AREA":
        ld.size = size
    ob = bpy.data.objects.new(name, ld)
    _link(ob)
    ob.location = Vector(loc)
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return ob


def render_view(out_png, view="front", parts=None, size=900, samples=48, az=None, el=None, lens=None, pad=1.12):
    """Render the current scene from a named view or custom azimuth/elevation/lens."""
    a0, e0, l0 = VIEWS.get(view, (0, 5, 85))
    az = a0 if az is None else az
    el = e0 if el is None else el
    lens = l0 if lens is None else lens
    obs = [o for o in bpy.data.objects if o.type == "MESH" and (parts is None or o.name in parts)]
    V = np.concatenate([mesh_world_verts(o) for o in obs])
    c = (V.min(0) + V.max(0)) / 2
    rad = np.linalg.norm(V - c, axis=1).max()
    setup_render(size, samples)
    for o in list(bpy.data.objects):
        if o.type in ("CAMERA", "LIGHT"):
            bpy.data.objects.remove(o)
    cam_d = bpy.data.cameras.new("cam")
    cam_d.lens = lens
    cam_d.sensor_width = 36
    fov = 2 * math.atan(18 / lens)
    dist = rad * pad / math.sin(fov / 2)
    azr, elr = math.radians(az), math.radians(el)
    dvec = np.array([math.sin(azr) * math.cos(elr), -math.cos(azr) * math.cos(elr), math.sin(elr)])
    cam = bpy.data.objects.new("cam", cam_d)
    _link(cam)
    cam.location = Vector(c + dvec * dist)
    up = "Y"
    q = Vector(-dvec).to_track_quat("-Z", up)
    cam.rotation_euler = q.to_euler()
    if abs(el) > 80:   # keep the printer's front at the bottom of the frame in top/bottom views
        cam.rotation_euler = (Vector(-dvec).to_track_quat("-Z", "Y")).to_euler()
    bpy.context.scene.camera = cam
    s = rad * 4
    k = LIGHT_GAIN * s * s
    _light("key", "AREA", c + np.array([-0.8, -1.2, 1.4]) * s, 160 * k, size=s * 0.9, target=c)
    _light("fill", "AREA", c + np.array([1.3, -0.6, 0.5]) * s, 55 * k, size=s, target=c)
    _light("rim", "AREA", c + np.array([0.2, 1.4, 1.0]) * s, 70 * k, size=s, target=c)
    _light("under", "AREA", c + np.array([0.0, -0.6, -1.2]) * s, 22 * k, size=s, target=c)
    for o in bpy.data.objects:
        if o.type == "MESH":
            o.hide_render = parts is not None and o.name not in parts
    bpy.context.scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    return out_png


def compare_sheet(pairs, out_png, height=640, title=None):
    """pairs: list of (photo_path, render_path, label). Writes one sheet: photo | render per row."""
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(find_font("DejaVuSans.ttf") or find_font("DejaVuSans"), 22)
    rows = []
    for photo, rend, label in pairs:
        ims = []
        for p in (photo, rend):
            im = Image.open(p).convert("RGB")
            im = im.resize((max(1, int(im.width * height / im.height)), height))
            ims.append(im)
        w = ims[0].width + ims[1].width + 30
        row = Image.new("RGB", (w, height + 40), "white")
        row.paste(ims[0], (0, 40))
        row.paste(ims[1], (ims[0].width + 30, 40))
        d = ImageDraw.Draw(row)
        d.text((8, 8), "photo: " + label, fill="black", font=font)
        d.text((ims[0].width + 38, 8), "model", fill="black", font=font)
        rows.append(row)
    W = max(r.width for r in rows)
    H = sum(r.height for r in rows) + (50 if title else 0)
    sheet = Image.new("RGB", (W, H), "white")
    y = 0
    if title:
        ImageDraw.Draw(sheet).text((8, 12), title, fill="black", font=font)
        y = 50
    for r in rows:
        sheet.paste(r, (0, y))
        y += r.height
    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    sheet.save(out_png)
    return out_png
