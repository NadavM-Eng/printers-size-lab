#!/usr/bin/env python3
"""
Merge the research (specs, box contents, prices) and each model's geometry into docs/printers.json,
the single data file the site reads.

    python3 build/assemble.py

Inputs:  printers/<printer name>/specs.json  (the research)
         docs/data/<id>.geom.json            (written by build/build_printer.py)
"""
import json
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths import specs_path  # noqa: E402

ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")

ORDER = [
    ("hp-officejet-j4580", "Your printer"),
    ("brother-dcp-l2620dw", "Candidates"),
    ("brother-hl-l2445dw", "Candidates"),
    ("brother-hl-l2400dw", "Candidates"),
    ("pantum-bp2300nw", "Candidates"),
    ("hp-laserjet-m110w", "Candidates"),
    ("xerox-b230", "Candidates"),
    ("xerox-b110", "Candidates"),
]
FALLBACK_NAMES = {
    "hp-officejet-j4580": ("HP OfficeJet J4580", "HP"),
    "brother-dcp-l2620dw": ("Brother DCP-L2620DW", "Brother"),
    "brother-hl-l2445dw": ("Brother HL-L2445DW", "Brother"),
    "brother-hl-l2400dw": ("Brother HL-L2400DW", "Brother"),
    "pantum-bp2300nw": ("Pantum BP2300NW", "Pantum"),
    "hp-laserjet-m110w": ("HP LaserJet M110w", "HP"),
    "xerox-b230": ("Xerox B230", "Xerox"),
    "xerox-b110": ("Xerox B110", "Xerox"),
}


# Official sizes (W, D, H mm) already confirmed while scoping, used only until the research lands.
# Measured on the user's shelf (ruler photos, 17 Nov 2026). Takes priority over model estimates.
ON_SHELF = {
    "hp-officejet-j4580": {"cable_back_gap_cm": 4.5, "base_overhang_cm": 3.5,
                           "note": "Wall to the back of the printer 4.5 cm (cables); the base sticks out about 3.5 cm "
                                   "past the shelf edge; the shelf is 24.5 cm deep."},
}

KNOWN_DIMS = {
    "hp-officejet-j4580": (433.5, 401.5, 216.7),
    "brother-dcp-l2620dw": (410, 399, 272),
    "brother-hl-l2445dw": (356, 360, 183),
    "brother-hl-l2400dw": (356, 360, 183),
    "pantum-bp2300nw": (337, 220, 179),
    "hp-laserjet-m110w": (346, 189, 158),
}


def load_json(*paths):
    for p in paths:
        if p and os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    return None


def g(d, *keys, default=None):
    for k in keys:
        if not isinstance(d, dict) or k not in d or d[k] is None:
            return default
        d = d[k]
    return d


def fmt_num(v, nd=1):
    if v is None:
        return None
    s = ("%." + str(nd) + "f") % float(v)
    return s.rstrip("0").rstrip(".") if "." in s else s


def dims_cm(dm):
    if not dm or not all(dm.get(k) for k in ("w", "d", "h")):
        return None
    return "%s × %s × %s cm" % (fmt_num(dm["w"] / 10), fmt_num(dm["d"] / 10), fmt_num(dm["h"] / 10))


def money(v, cur):
    if v is None:
        return None
    if cur == "ils":
        return "₪%s" % ("{:,.0f}".format(float(v)))
    return "$%s" % ("{:,.0f}".format(float(v)))


def you(text):
    """The research notes say "the user's shelf"; on the site they speak to the reader."""
    if not isinstance(text, str):
        return text
    return text.replace("the user's", "your").replace("The user's", "Your")


def sentences(text):
    """Split text after each '. ' that is followed by a capital letter or a digit, never inside brackets.
    Only the space between sentences is dropped; no other text is lost."""
    s = str(text).strip()
    out, start, depth = [], 0, 0
    for i, ch in enumerate(s):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif ch == "." and depth == 0 and s[i + 1:i + 2] == " " and (s[i + 2:i + 3].isupper() or s[i + 2:i + 3].isdigit()):
            out.append(s[start:i + 1].strip())
            start = i + 2
    out.append(s[start:].strip())
    return [x for x in out if x]


def paras(text):
    """One `more` paragraph per sentence of the text."""
    return [{"p": x} for x in sentences(text)] if text else []


def tidy_rows(rows):
    """Last pass over every row: a visible note longer than 110 characters moves into `more`, as one
    paragraph per " · " part (or per sentence). Rows that already have a `more` keep their note.
    Also drops keys whose value is None."""
    for r in rows:
        note = r.get("note")
        if "more" not in r and isinstance(note, str) and len(note) > 110:
            parts = [x.strip() for x in note.split(" · ")] if " · " in note else sentences(note)
            r["more"] = [{"p": x} for x in parts if x]
            del r["note"]
        for k in [k for k, v in r.items() if v is None]:
            del r[k]
    return rows


def rows_for(s):
    rows = []

    def add(label, value, href=None, note=None, more=None):
        if value in (None, "", [], "null"):
            return
        r = {"label": label, "value": value}
        if href:
            r["href"] = href
        if note:
            r["note"] = note
        if more:
            r["more"] = more
        rows.append(r)

    notes = you(s.get("notes"))
    if isinstance(notes, str) and notes.strip():   # first sentence visible, the rest in pairs under "More"
        first, *rest = sentences(notes)
        add("Notes", first, more=[{"p": " ".join(rest[i:i + 2])} for i in range(0, len(rest), 2)])
    else:
        add("Notes", notes)
    add("Type", s.get("type"))
    fn = s.get("functions") or []
    add("Functions", ", ".join(f.capitalize() if i == 0 else f for i, f in enumerate(fn)) if fn else None)
    add("Size closed (W × D × H)", dims_cm(g(s, "dims_mm", "closed")), g(s, "dims_mm", "closed", "source"))
    mx = g(s, "dims_mm", "max")
    if mx and dims_cm(mx):
        add("Size in use (W × D × H)", dims_cm(mx), mx.get("source"), mx.get("what"))
    cs = s.get("cable_space") or {}
    if cs.get("behind_body_cm") is not None:
        src = cs.get("source")
        add("Cable space behind", "%s cm" % fmt_num(cs["behind_body_cm"]),
            src if isinstance(src, str) and src.startswith("http") else None, more=paras(you(cs.get("why"))))
    w = g(s, "weight_kg", "value")
    if w:
        add("Weight", "%s kg" % fmt_num(w), g(s, "weight_kg", "source"), g(s, "weight_kg", "what"))
    sp = s.get("print_speed_ppm") or {}
    if sp.get("a4") or sp.get("letter"):
        parts = []
        if sp.get("a4"):
            parts.append("%s pages/min (A4)" % fmt_num(sp["a4"], 0))
        if sp.get("letter"):
            parts.append("%s (Letter)" % fmt_num(sp["letter"], 0))
        add("Print speed", ", ".join(parts), sp.get("source"))
    elif sp.get("black_max"):
        add("Print speed", "Up to %s pages/min black, %s colour" % (fmt_num(sp["black_max"], 0), fmt_num(sp.get("colour_max"), 0)), sp.get("source"))
    dup = s.get("duplex")
    if dup:
        add("Two-sided printing", {"automatic": "Automatic", "manual": "Manual (turn the pages yourself)", "none": "No"}.get(dup, dup))
    c = s.get("connectivity") or {}
    names = [("usb", "USB"), ("wifi", "Wi-Fi"), ("ethernet", "Ethernet"), ("wifi_direct", "Wi-Fi Direct"), ("bluetooth", "Bluetooth")]
    have = [n for k, n in names if c.get(k)]
    if have:
        add("Connections", ", ".join(have), c.get("source"))
    p = s.get("paper") or {}
    if p.get("input_sheets"):
        add("Paper in", "%s sheets%s" % (fmt_num(p["input_sheets"], 0), (", " + p["input_type"]) if p.get("input_type") else ""), p.get("source"))
    if p.get("output_sheets"):
        add("Paper out", "%s sheets%s" % (fmt_num(p["output_sheets"], 0), (", " + p["output_type"]) if p.get("output_type") else ""))
    add("Manual feed", p.get("manual_feed"))
    sc = s.get("scanner")
    if sc:
        txt = (sc.get("type") or "Scanner").capitalize()
        if sc.get("adf"):
            txt += ", document feeder" + (" (%s sheets)" % fmt_num(sc["adf_sheets"], 0) if sc.get("adf_sheets") else "")
        add("Scanner", txt, sc.get("source"))
    else:
        add("Scanner", "None")
    add("Display", s.get("display"))
    t = s.get("toner") or {}
    if t:
        bits = []
        if t.get("starter_pages"):
            bits.append("starter %s pages" % "{:,}".format(int(t["starter_pages"])))
        if g(t, "standard", "code"):
            bits.append("%s (%s pages)" % (t["standard"]["code"], "{:,}".format(int(t["standard"]["pages"])) if t["standard"].get("pages") else "?"))
        if g(t, "high", "code"):
            bits.append("%s (%s pages)" % (t["high"]["code"], "{:,}".format(int(t["high"]["pages"])) if t["high"].get("pages") else "?"))
        add("Toner", "; ".join(bits) if bits else None, t.get("source"))
        if g(t, "drum", "code"):
            add("Drum", "%s (%s pages)" % (t["drum"]["code"], "{:,}".format(int(t["drum"]["pages"])) if t["drum"].get("pages") else "?"))
    ink = s.get("ink") or {}
    if ink.get("cartridges"):
        add("Ink", ", ".join(ink["cartridges"]), ink.get("source"))
    box = s.get("in_the_box") or {}
    if box.get("items"):
        add("In the box", box["items"], box.get("source"), ("As listed for %s. " % box["region"] if box.get("region") else "") + (box.get("notes") or ""))
    pi = g(s, "price", "ils") or {}
    if pi.get("value") is not None:
        add("Price in Israel", money(pi["value"], "ils"), pi.get("url"), " · ".join(x for x in (pi.get("where"), pi.get("date"), pi.get("note")) if x))
    pu = g(s, "price", "usd") or {}
    if pu.get("value") is not None:
        add("Price international", money(pu["value"], "usd"), pu.get("url"), " · ".join(x for x in (pu.get("where"), pu.get("date"), pu.get("note")) if x))
    hp = s.get("hp_plus")
    if hp:
        add("HP+", hp.get("m110we") if isinstance(hp, dict) else hp, hp.get("source") if isinstance(hp, dict) else None)
    return rows


# --------------------------------------------------------------------------------------------
# running cost and software reputation: printers/<name>/ownership.json (see helper-instructions/RESEARCH_BRIEF.md)
# --------------------------------------------------------------------------------------------
OWNERSHIP_FROM = {"brother-hl-l2445dw": "brother-hl-l2400dw"}   # same machine, same cartridges and software
RATING_WORD = {"good": "Good", "mixed": "Mixed", "poor": "Poor", "unknown": "Not enough evidence"}


def impersonal(text):
    """The researchers wrote some remarks in the first person ("no page I opened says"); the site doesn't."""
    if not isinstance(text, str):
        return text
    import re
    t = re.sub(r"\bI have\b", "the research has", text)
    t = re.sub(r"\bI\b", "the research", t)
    t = re.sub(r"(^|[.!?] )the research", lambda m: m.group(1) + "The research", t)
    return t


def load_ownership(pid):
    """ownership.json, with the Windows and owner-opinion parts replaced by the second pass (reviews.json)
    wherever that pass reached a rating or the first one had none."""
    for p in (pid, OWNERSHIP_FROM.get(pid)):
        if not p:
            continue
        folder = os.path.dirname(specs_path(p))
        o = load_json(os.path.join(folder, "ownership.json"))
        if not o:
            continue
        rev = load_json(os.path.join(folder, "reviews.json")) or {}
        for key in ("windows", "forums"):
            new, old = rev.get(key), o.get(key) or {}
            if isinstance(new, dict) and new.get("rating") and (new["rating"] != "unknown" or old.get("rating", "unknown") == "unknown"):
                seen = {x.get("url") for x in (new.get("sources") or []) if isinstance(x, dict)}
                new = dict(new, sources=(new.get("sources") or []) + [x for x in (old.get("sources") or [])
                                                                     if isinstance(x, dict) and x.get("url") not in seen])
                o[key] = new
        return o
    return None


def per_page(v, cur):
    """A cost per page as text: two decimals, three when it is under 0.10."""
    sign = {"ils": "₪", "usd": "$"}[cur]
    return "%s%.*f" % (sign, 2 if v >= 0.1 else 3, v)


def price_of(c, cur):
    p = c.get("price_" + cur)
    v = p.get("value") if isinstance(p, dict) else None
    return float(v) if isinstance(v, (int, float)) and v > 0 else None


def cost_per_page(o):
    """Cheapest cost per black page with original cartridges, and with compatible ones, per currency.
    A separate drum's cost per page is added. Starter cartridges are left out (they aren't sold)."""
    cons = [c for c in (o.get("consumables") or []) if isinstance(c, dict) and isinstance(c.get("pages"), (int, float)) and c["pages"] > 0]
    out = {}
    for cur in ("ils", "usd"):
        drums = [(price_of(c, cur) / c["pages"], c) for c in cons
                 if c.get("kind") == "drum" and c.get("original", True) and price_of(c, cur)]
        drum = min(drums, key=lambda x: x[0]) if drums else None
        res = {}
        for key, original in (("original", True), ("compatible", False)):
            carts = [(price_of(c, cur) / c["pages"], c) for c in cons
                     if c.get("kind") in ("toner", "ink") and c.get("role") not in ("starter", "colour", "color", "drum")
                     and bool(c.get("original", True)) == original and price_of(c, cur)]
            if not carts:
                continue
            cpp, c = min(carts, key=lambda x: x[0])
            res[key] = {"value": round(cpp + (drum[0] if drum else 0), 4), "cartridge": c, "drum": drum[1] if drum else None}
        if res:
            out[cur] = res
    return out


def cart_text(c, cur):
    p = c.get("price_" + cur) or {}
    return "%s (%s pages, %s%s%s)" % (c.get("code") or "cartridge", "{:,}".format(int(c["pages"])), money(p.get("value"), cur),
                                      (" at " + short_shop(p["where"])) if p.get("where") else "",
                                      (", " + p["availability"]) if p.get("availability") else "")


def short_shop(where):
    """'Beit HaFax (lowest original of 12 offers on zap.co.il)' -> 'Beit HaFax'."""
    w = str(where).split(" (")[0].split(", ")[0].strip()
    for cut in (" via ", " offer on", " listed on"):
        w = w.split(cut)[0]
    return w.replace("zap.co.il offer: ", "").strip() or str(where)


def ownership_rows(o):
    """Spec rows and the per-page figures the site compares."""
    rows, fields = [], {}
    if not o:
        return rows, fields
    cpp = cost_per_page(o)
    for cur, label in (("ils", "Cost per page in Israel"), ("usd", "Cost per page international")):
        r = (cpp.get(cur) or {}).get("original")
        if not r:
            comp = (cpp.get(cur) or {}).get("compatible")
            if comp:   # no original cartridge found on sale: say so, and give the compatible figure
                fields["page_compatible_" + cur] = comp["value"]
                note = "No original cartridge was found on sale. Compatible " + cart_text(comp["cartridge"], cur) + "."
                rows.append({"label": label, "value": per_page(comp["value"], cur) + " per page, compatible cartridge only",
                             "more": paras(note),
                             "href": (comp["cartridge"].get("price_" + cur) or {}).get("url")})
            continue
        fields["page_" + cur] = r["value"]
        note = "Original " + cart_text(r["cartridge"], cur)
        if r["drum"]:
            note += " plus drum " + cart_text(r["drum"], cur)
        comp = (cpp.get(cur) or {}).get("compatible")
        if comp:
            fields["page_compatible_" + cur] = comp["value"]
            note += ". With a compatible cartridge: %s per page, %s" % (per_page(comp["value"], cur), cart_text(comp["cartridge"], cur))
        rows.append({"label": label, "value": per_page(r["value"], cur) + " per page", "more": paras(note + "."),
                     "href": (r["cartridge"].get("price_" + cur) or {}).get("url")})
    cons = [c for c in (o.get("consumables") or []) if isinstance(c, dict)]
    items = []
    for c in cons:
        bits = []
        for cur in ("ils", "usd"):
            if price_of(c, cur):
                p = c["price_" + cur]
                bits.append(money(p["value"], cur) + ((" at " + short_shop(p["where"])) if p.get("where") else "")
                            + ((", " + p["availability"]) if p.get("availability") else ""))
        if not bits:
            continue
        pages = ("%s pages" % "{:,}".format(int(c["pages"]))) if isinstance(c.get("pages"), (int, float)) else "yield not listed"
        items.append("%s%s, %s: %s" % (c.get("code") or c.get("role") or "cartridge", "" if c.get("original", True) else " (compatible)",
                                       pages, "; ".join(bits)))
    if items:
        rows.append({"label": "Cartridge prices", "value": items})
    tp = o.get("third_party_cartridges") or {}
    if tp.get("summary"):
        word = {"yes": "Allowed", "nags": "Allowed, with warnings", "blocked": "Blocked", "unknown": "Not clear"}.get(tp.get("allowed"), "")
        rows.append({"label": "Compatible cartridges", "value": word or tp["summary"],
                     "more": [{"p": tp["summary"]}] if word else None,
                     "href": tp.get("source") if str(tp.get("source") or "").startswith("http") else None})
    for key, label in (("windows", "Software on Windows"), ("forums", "What owners say")):
        b = o.get(key) or {}
        if not b.get("rating"):
            continue
        fields[key + "_rating"] = b["rating"]
        more = []   # labelled blocks, shown under "More"
        if key == "windows":
            if b.get("driver"):
                more.append({"label": "Driver", "p": b["driver"].rstrip(".") + "."})
            if b.get("app_required") and b["app_required"] != "no":
                more.append({"label": "App required", "p": b["app_required"]})
            if b.get("problems"):
                more.append({"label": "Known problems", "items": list(b["problems"])})
            if b.get("scanning"):
                more.append({"label": "Scanning", "p": b["scanning"].rstrip(".") + "."})
        else:
            stars = ["%s of %s from %s reviews at %s" % (fmt_num(x["score"]), fmt_num(x.get("out_of") or 5, 0),
                                                         "{:,}".format(int(x["reviews"])), str(x.get("where") or "a shop").split(" (")[0])
                     for x in (b.get("stars") or [])
                     if isinstance(x, dict) and isinstance(x.get("score"), (int, float))
                     and isinstance(x.get("reviews"), (int, float)) and x["reviews"] >= 3]
            if stars:
                more.append({"label": "Ratings", "items": stars})
            if b.get("praise"):
                more.append({"label": "Praise", "items": list(b["praise"])})
            if b.get("complaints"):
                more.append({"label": "Complaints", "items": list(b["complaints"])})
            if b.get("sources_read"):
                more.append({"p": "%s sources read." % b["sources_read"]})
        src = next((x.get("url") for x in (b.get("sources") or []) if isinstance(x, dict) and str(x.get("url") or "").startswith("http")), None)
        word, why = RATING_WORD.get(b["rating"], b["rating"]), (b.get("why") or "").rstrip(".")
        note = why + "." if why else None
        if note and len(note) > 140:   # a long reason opens the drop-down instead of sitting under the rating
            more.insert(0, {"p": note})
            note = None
        rows.append({"label": label, "value": word, "note": note, "more": more or None, "href": src})
    for r in rows:
        for k in [k for k, v in r.items() if v is None]:
            del r[k]
        for k in ("value", "note"):
            if isinstance(r.get(k), str):
                r[k] = impersonal(r[k])
        for blk in r.get("more") or []:
            if isinstance(blk.get("p"), str):
                blk["p"] = impersonal(blk["p"])
            if isinstance(blk.get("items"), list):
                blk["items"] = [impersonal(x) for x in blk["items"]]
    return rows, fields


def collect_sources(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("source", "url", "page") and isinstance(v, str) and v.startswith("http"):
                out.add(v)
            else:
                collect_sources(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_sources(v, out)


def main():
    printers = []
    for pid, group in ORDER:
        s = load_json(specs_path(pid)) or {}
        if not g(s, "dims_mm", "closed", "w") and pid in KNOWN_DIMS:
            w, d, h = KNOWN_DIMS[pid]
            s.setdefault("dims_mm", {})["closed"] = {"w": w, "d": d, "h": h}
        geom = load_json(os.path.join(DOCS, "data", pid + ".geom.json"))
        name, brand = FALLBACK_NAMES[pid]
        srcs = set()
        collect_sources(s, srcs)
        own = load_ownership(pid)
        own_rows, own_fields = ownership_rows(own)
        collect_sources(own, srcs)
        rows = rows_for(s)
        # running cost and software go right after the notes, ahead of the hardware specs
        at = 1 if rows and rows[0]["label"] == "Notes" else 0
        rows[at:at] = own_rows
        tidy_rows(rows)
        glb = os.path.join(DOCS, "models", pid + ".glb")
        printers.append({
            "id": pid,
            "name": s.get("name") or name,
            "brand": s.get("brand") or brand,
            "group": group,
            "current": group == "Your printer",
            "type": s.get("type"),
            "has_model": os.path.exists(glb),
            "dims_mm": s.get("dims_mm") or {},
            "weight_kg": g(s, "weight_kg", "value"),
            "price_ils": g(s, "price", "ils", "value"),
            "price_usd": g(s, "price", "usd", "value"),
            "scanner": bool(s.get("scanner")),
            "rows": rows,
            **own_fields,
            "notes": you(s.get("notes")),
            "sources": sorted(srcs),
            "geom": geom,
            "measured": ON_SHELF.get(pid),
        })
    scene = load_json(os.path.join(DOCS, "data", "scene.json"))   # the shelf and the wardrobe
    out = {"generated": date.today().isoformat(), "printers": printers, "scene": scene}
    with open(os.path.join(DOCS, "printers.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("wrote docs/printers.json:", ", ".join("%s%s" % (p["id"], "" if p["has_model"] else " (no model yet)") for p in printers))


if __name__ == "__main__":
    main()
