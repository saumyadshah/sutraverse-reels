#!/usr/bin/env python3
"""Check a Reel's shot list for story flow and continuity BEFORE building scenes (CONTENT_STANDARDS §17).

  python shotlist_lint.py <project_id>            # reads projects/<id>/artifacts/shotlist.json (+ timing.json)
  python shotlist_lint.py path/to/shotlist.json [--timing timing.json]

FAIL = fix the shot list first. WARN = judge it and write why in the shot's "continuity" note.
Checks: timing coverage, every shot tied to narration with a purpose and a key visual, cast only from
the registry, story elements visible when they are spoken, world changes on signature transitions,
screen direction and panel style kept within a location, no jump cuts, explainer shots that teach,
and on-screen text limits.
"""
import argparse, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
SIGNATURE = {"thread", "portal", "bloom"}
WITHIN = {"cut", "match", "push", "rack", "dissolve", "thread", "portal", "bloom"}
SIZES = ["ECU", "CU", "MCU", "MS", "WS", "EWS", "INSERT", "OTS", "POV"]
EXPR_MODERN = {"neutral", "smile", "hopeful", "sad", "worried", "shock", "angry", "tired"}


def load_registry(extra=None):
    reg = {}
    for p in [HERE.parents[3] / "cast" / "cast.json", pathlib.Path.home() / "sutraverse-reels/toolkit/cast/cast.json",
              pathlib.Path("/root/sutraverse-reels/toolkit/cast/cast.json")]:
        if p.is_file():
            reg = json.loads(p.read_text())["characters"]; break
    if extra and pathlib.Path(extra).is_file():
        reg.update(json.loads(pathlib.Path(extra).read_text()).get("characters", {}))
    return reg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target"); ap.add_argument("--timing")
    a = ap.parse_args()
    t = pathlib.Path(a.target)
    if t.suffix == ".json":
        sl_path, art = t, t.parent
    else:
        sys.path.insert(0, str(HERE)); from _common import project_dir  # noqa
        art = project_dir(a.target) / "artifacts"; sl_path = art / "shotlist.json"
    if not sl_path.is_file():
        sys.exit(f"FAIL no shot list at {sl_path} (write it from templates/shotlist.example.json)")
    SL = json.loads(sl_path.read_text())
    tp = pathlib.Path(a.timing) if a.timing else art / "timing.json"
    T = json.loads(tp.read_text()) if tp.is_file() else None
    reg = load_registry(art / "cast_local.json")
    out = []
    F = lambda sid, m: out.append(("FAIL", sid, m))
    W = lambda sid, m: out.append(("WARN", sid, m))

    shots = SL.get("shots", [])
    if not shots: F("-", "no shots")
    if not SL.get("message"): F("-", "no one-line 'message' at the top")
    locs = SL.get("locations", {})
    lines_t = (T or {}).get("lines", {})
    if isinstance(lines_t, list): lines_t = {l["id"]: l for l in lines_t}  # timing.json stores lines as a list
    total = (T or {}).get("total_duration")

    # --- cast ---
    for n in SL.get("cast", []):
        if n not in reg: F("-", f"cast '{n}' is not in toolkit/cast/cast.json or artifacts/cast_local.json: define it once, then reuse")

    # --- timing coverage ---
    shots = sorted(shots, key=lambda s: s.get("start", 0))
    prev_end = 0.0
    for s in shots:
        sid = s.get("id", "?"); st, en = s.get("start"), s.get("end")
        if st is None or en is None: F(sid, "missing start/end"); continue
        if abs(st - prev_end) > 0.06: F(sid, f"gap/overlap of {st - prev_end:+.2f}s before this shot")
        d = en - st
        if d < 1.2 and s.get("beat") != "hook": W(sid, f"very short shot ({d:.2f}s): will it read?")
        if d > 5.0 and s.get("world") != "verse": F(sid, f"shot holds {d:.1f}s (> 5 s): split it or add a camera move/new action (§2)")
        prev_end = en
    if total and shots and abs(prev_end - total) > 0.3: F("-", f"shots end at {prev_end:.2f}s but narration is {total:.2f}s")

    # --- per-shot story + continuity ---
    last_by_loc = {}
    for i, s in enumerate(shots):
        sid = s.get("id", f"#{i}")
        purpose = s.get("purpose", "")
        if len(purpose.split()) < 4: F(sid, "no clear 'purpose' (what this shot tells the viewer, in a sentence)")
        if not s.get("key_visual"): F(sid, "no 'key_visual' (the one thing the viewer must see)")
        if not s.get("lines") and s.get("world") != "brand" and (s.get("end", 0) - s.get("start", 0)) > 1.2: F(sid, "not tied to any narration line")
        for ln in s.get("lines", []):
            if lines_t and ln not in lines_t: F(sid, f"line {ln} not in timing.json")
            elif ln in lines_t:
                lt = lines_t[ln]
                if lt["end"] <= s["start"] - 0.05 or lt["start"] >= s["end"] + 0.05:
                    F(sid, f"line {ln} ({lt['start']:.1f}-{lt['end']:.1f}s) is not spoken during this shot")
        world = s.get("world")
        if world not in {"modern", "mithila", "explainer", "verse", "diorama", "brand"}: F(sid, f"world '{world}' unknown")
        if s.get("size") and s["size"] not in SIZES: W(sid, f"size '{s['size']}' not one of {SIZES}")
        loc = s.get("location")
        if world in {"modern", "mithila", "diorama"}:
            if not loc: F(sid, "no 'location'")
            elif loc not in locs: W(sid, f"location '{loc}' not described in 'locations' (describe it once so every shot matches)")
        names = []
        for c in s.get("characters", []):
            n = c.get("name"); names.append(n)
            if n not in reg: F(sid, f"character '{n}' not in the cast registry")
            elif n not in SL.get("cast", []): W(sid, f"'{n}' missing from the top-level 'cast' list")
            rig = reg.get(n, {}).get("rig", "modern")
            if rig == "modern" and c.get("expression") and c["expression"] not in EXPR_MODERN:
                W(sid, f"{n}: expression '{c['expression']}' is not a CAST expression {sorted(EXPR_MODERN)}")
            if not c.get("action"): W(sid, f"{n}: no 'action' (what they DO in this shot)")
        if len(s.get("text", [])) > 2: F(sid, "more than 2 text elements")
        for tx in s.get("text", []):
            if len(tx) > 64: W(sid, f"on-screen text is long ({len(tx)} chars): '{tx[:30]}…'")
        # transitions
        if i > 0:
            p = shots[i - 1]; tr = s.get("transition_in", "cut")
            if tr not in WITHIN: F(sid, f"transition '{tr}' is not a house transition {sorted(WITHIN)}")
            pw, w = p.get("world"), world
            story_worlds = {"modern", "mithila", "diorama"}
            if pw in story_worlds and w in story_worlds and pw != w and tr not in SIGNATURE:
                F(sid, f"world change {pw}→{w} needs a signature transition (thread / portal / bloom), not '{tr}'")
            if p.get("location") == loc and loc and p.get("size") == s.get("size") and sorted(names) == sorted(c.get("name") for c in p.get("characters", [])) and tr == "cut":
                W(sid, "jump cut: same location, size and characters as the previous shot; change the size or angle")
        # within-location continuity
        if loc:
            q = last_by_loc.get(loc)
            if q:
                if world == "mithila" and q.get("panel") and s.get("panel") and q["panel"] != s["panel"]:
                    F(sid, f"panel style changes in '{loc}' ({q['panel']}→{s['panel']}): keep one panel frame per location")
                qs = {c["name"]: c.get("side") for c in q.get("characters", [])}
                for c in s.get("characters", []):
                    if c["name"] in qs and qs[c["name"]] and c.get("side") and qs[c["name"]] != c["side"] and "center" not in (qs[c["name"]], c["side"]) and not s.get("reverse"):
                        W(sid, f"{c['name']} jumps screen side ({qs[c['name']]}→{c['side']}) in '{loc}': keep screen direction or mark \"reverse\": true with a motivated move")
            last_by_loc[loc] = s
        if world == "mithila" and not s.get("panel"): W(sid, "mithila shot without 'panel' (full | framed): pick one per location")
        if world == "explainer":
            if not s.get("teaches"): F(sid, "explainer shot without 'teaches' (the concept this diagram makes clear)")
            if not s.get("diagram"): F(sid, "explainer shot without 'diagram' (components, labels, data source)")
    # story elements visible when spoken
    for e in SL.get("story_elements", []):
        for ln in e.get("must_show_at", []):
            cover = [s for s in shots if ln in s.get("lines", [])]
            if not cover: F("-", f"story element '{e['name']}': no shot covers {ln}"); continue
            hit = any(e["name"] in [c.get("name") for c in s.get("characters", [])] or e["name"] in s.get("props", []) or e["name"].lower() in s.get("key_visual", "").lower() for s in cover)
            if not hit: F(",".join(s["id"] for s in cover), f"'{e['name']}' is spoken in {ln} but not shown in the shot(s) covering it")
    # size rhythm
    for i in range(2, len(shots)):
        trio = shots[i - 2:i + 1]
        if len({x.get("size") for x in trio}) == 1 and len({x.get("location") for x in trio}) == 1 and trio[0].get("size"):
            W(trio[2]["id"], f"three {trio[0]['size']} shots in a row in one location: vary the framing")

    fails = [o for o in out if o[0] == "FAIL"]
    for lvl, sid, m in out:
        print(f"{lvl:4} {sid:8} {m}")
    print(f"\nshot list: {len(shots)} shots, {len(fails)} FAIL, {len(out) - len(fails)} WARN -> {'FAIL' if fails else 'PASS'}")
    (art / "shotlist_lint.txt").write_text("\n".join(f"{a} {b} {c}" for a, b, c in out) + f"\n{'FAIL' if fails else 'PASS'}\n")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
