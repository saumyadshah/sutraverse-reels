# SutraVerse knowledge base

The memory of the channel: what has been told, which sources, characters and ideas each Reel used, and what is waiting to be made. The weekly planner reads it so stories never repeat and arcs continue (numbered rules, episodes, files).

- `episodes.md`: every published Reel with its series, the named idea, sources, cast and results. The weekly review appends one line per Reel.
- `ideas.md`: the backlog by series, each idea with a hook seed, the named idea and sources to verify.
- `../brand2/cast2.json`: the characters (one entry each).
- `sources.md`: editions and references we trust, and how to cite them.

**Graphify (optional index).** `pip install graphifyy && graphify update toolkit/kb` builds `graphify-out/` (graph.json, GRAPH_REPORT.md, graph.html) for free from the file and heading structure; a semantic pass (concept links across files) needs a model: run `/graphify toolkit/kb` inside an agent session, or set GEMINI_API_KEY for its Gemini backend. Use it to see clusters (which ideas, sources and characters connect) when planning a month; it is not part of video production. Tested 7 Nov 2026 (graphifyy 0.9.103): the structural pass maps headings only, so links between episodes come from the semantic pass or from the planner reading these files.
