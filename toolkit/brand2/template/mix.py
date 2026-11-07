#!/usr/bin/env python3
"""Pilot sound: drone bed + procedural foley from window.EV (events.json). Voice-over Reels add the Gemini VO stem."""
import json, sys, pathlib, numpy as np, soundfile as sf
LIB = pathlib.Path(__import__('os').environ['LIB']); sys.path.insert(0, str(LIB / 'core' / 'audio'))
import sfx
HERE = pathlib.Path(__file__).resolve().parent; ev = json.load(open(HERE / 'events.json'))
SR = sfx.SR; dur = ev['dur']; n = int(dur * SR); L = np.zeros(n); R = np.zeros(n); buf = np.stack([L, R], 1)
t = np.arange(n) / SR
drone = 0.06 * (np.sin(2 * np.pi * 55 * t) + .5 * np.sin(2 * np.pi * 82.5 * t) + .25 * np.sin(2 * np.pi * 110 * t)) * np.minimum(1, t / 2)
quiet = [(e['t'], e['t'] + .7) for e in ev['ev'] if e['type'] == 'silence']
for a, b in quiet: drone[int(a * SR):int(b * SR)] *= 0.08
buf += np.stack([drone, drone], 1)
room = 0.012 * sfx.lp(sfx.noise(dur), 900); buf[:len(room)] += np.stack([room, room], 1)
for e in ev['ev']:
    k = e['type']; at = e['t']
    if k == 'ping': sfx.add(buf, sfx.ding(.5), at, .5, .3)
    elif k == 'freeze': sfx.add(buf, sfx.thump(.8), at, .7)
    elif k == 'card': sfx.add(buf, sfx.click(1.4, .8), at, .6, -.2)
    elif k == 'whoosh': sfx.add(buf, sfx.whoosh(.5, 1), at, .7)
    elif k == 'paper': sfx.add(buf, sfx.whoosh(.3, .6), at, .5, .2)
    elif k == 'stamp': sfx.add(buf, sfx.thump(1, 55), at, .9)
    elif k == 'ding': sfx.add(buf, sfx.ding(.7), at, .6)
buf = sfx.limit(buf / max(1e-6, np.abs(buf).max()) * .8)
(HERE / 'out').mkdir(exist_ok=True); sf.write(HERE / 'out' / 'mix.wav', buf, SR); print('mix ok', round(dur, 2), 's')
