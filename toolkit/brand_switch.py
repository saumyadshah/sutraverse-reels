#!/usr/bin/env python3
"""Flip BRAND.json to the new handles once Saumya has renamed the accounts.

  python3 toolkit/brand_switch.py --ig shlokwise            # after the Instagram username change
  python3 toolkit/brand_switch.py --yt @shlokwise           # after the YouTube handle change
"""
import argparse, json
from pathlib import Path
p = Path(__file__).with_name("BRAND.json")
a = argparse.ArgumentParser(); a.add_argument("--ig"); a.add_argument("--yt"); o = a.parse_args()
b = json.loads(p.read_text())
if o.ig: b["instagram"].update(handle=o.ig.lstrip("@"), switched=True)
if o.yt: b["youtube"].update(handle="@" + o.yt.lstrip("@"), switched=True)
p.write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
print("instagram:", b["instagram"]["handle"], b["instagram"]["switched"], "| youtube:", b["youtube"]["handle"], b["youtube"]["switched"])
