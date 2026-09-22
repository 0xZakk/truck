Legacy whole-truck prototype archived at `archive/2026-09-22-legacy-truck/`.
`/viewer/` is now the current project home; engine development remains active.
Do not resume the archived modeling pipeline. Manuals, BOM and KB remain available.

Latest implementation (2026-09-22): engine atlas at /viewer/engine.html, individual
pages at /viewer/part.html?id=<occurrence-id>, original study at /viewer/piston-study.html.
53 definitions / 399 occurrences. Engine remains unfinished and provisional.
Read [ENGINE-COMPLETION.md](ENGINE-COMPLETION.md),
[cad/engine/README.md](../cad/engine/README.md) and [ENGINE-AUDIT.md](ENGINE-AUDIT.md) first.

Current restart guidance (2026-09-22): see [RESTART.md](RESTART.md).
The following is historical and describes the removed 2D app.

 Resume note — Phase 2 (FSM → app)

## The actual vision (clarified by user)
A web app covering **every system → every part** of the truck. Each system page has:
1. **🩻 Interactive "x-ray" graphic** — cutaway of the truck with that system
   highlighted; click a part to jump to its explanation.
2. **⚙️ Part-by-part "how it works"** walkthrough (scrollable, narrated).
3. **🔧 Common issues & fixes** linked to each part.
User wants help: **mapping each system, creating the graphics, building the site.**
Plan: build the **shell first (done)**, then deep-build **Starting System** as the
exemplar, then replicate.

## Status: systems shell ✅ (+ manual search ✅)
Front-end moved to static files in `web/`; Python server (`app/server.py`) now
serves them + JSON APIs. Run: `./scripts/run-app.sh` → http://127.0.0.1:8080/
- `app/systems.json` — taxonomy: 6 categories, 25 systems (data-driven; add a
  system/part = edit JSON). `starting-system` has a 7-part list as the template demo.
- `web/index.html` — systems home (grid by category, status badges).
- `web/system.html` — per-system page; renders 3 placeholder sections from JSON.
- `web/search.html` — manual search UI (client-side, calls /api/search).
- `web/style.css` — shared styles.
- Server routes: `/`, `/system/<slug>`, `/search`, `/api/systems`, `/api/search`,
  `/page?path=` (FSM viewer, server-rendered), `/fsm/<ondisk>` (images), `/<asset>`.

## Starting System: BUILT ✅ (the exemplar)
Live at `/system/starting-system`. Decisions used: BOTH graphics (compare), and
authored-but-clearly-labeled narration (💬 plain vs 📖 factory, with cited links).
- Content: `app/content/starting-system.json` — overview, 7 parts (each plain +
  factory excerpt + source link), specs, 5 common issues w/ factory test links,
  safety note. Grounded in real FSM pages (Description & Operation, Specs,
  Locations, R&R, pinpoint test TA5, Service Precautions).
- Graphics (inline SVG, clickable, hover-synced w/ part cards):
  `web/diagrams/starting-system-cutaway.svg` (truck profile, parts in physical
  locations, numbered) and `…-schematic.svg` (electrical flow: blue signal switches
  red heavy current). Toggle on the page switches between them.
- Backend: `/api/system/<slug>` merges systems.json meta + content/<slug>.json.
- `web/system.html` renders the full experience when content exists, else placeholder.
- Validate styled SVGs: inline the diagram CSS into the svg + `qlmanage -t` (qlmanage
  ignores external CSS, so render shows black without inlining).

## PIVOT (user feedback): drop hand-drawn SVG → use REAL FSM diagrams
User found the hand-drawn SVGs "toy"; wants polished, well-designed, and pointed at
the real factory illustrations (e.g. the starter exploded view). Done:
- Deleted the toy SVGs. Starter page now shows a **factory-diagram viewer**: hero
  figure + thumbnail gallery (Component / Wiring / Location) + click-to-zoom lightbox.
- Curated diagrams live in `app/content/starting-system.json` → `diagrams:[{type,
  caption,img,source}]`. Images served via `/fsm/<ondisk>`; source links via `/page`.
- The 4 starter diagrams: exploded view 1187056411, wiring sheets 1197008238 &
  1197039564, engine-bay location 78517664.

## Diagram inventory (whole FSM)
- **2,947 unique content images.** ~136 wiring schematics, 122+ exploded/component
  illustrations (on "Description and Operation" pages), 116 connector/pinouts, 59
  location diagrams, 117 spec charts. EVERY system has diagrams.
- Best hero sources by page-type: "Description and Operation" (component/exploded),
  "Diagrams/Electrical Diagrams/<sys>/System Diagram" (wiring), "Locations", and
  "Service and Repair" (R&R exploded views).

## DIRECTION LOCKED (after 2 misses): scrollytelling + whole-truck x-ray
User confirmed via AskUserQuestion:
- **Interaction = scrollytelling**: truck visual pinned (sticky), part explanations
  scroll beside it, visual tracks the active part. BUILT on the starter page
  (`web/system.html`: `.scrolly` + IntersectionObserver; sticky `.stage` swaps to the
  active part's factory illustration via `part.focus` index into `diagrams[]`).
- **Central artwork = "we'll do it together"** → see `docs/xray-art-brief.md`.
  Plan: generate ONE base whole-truck x-ray image; ALL highlighting done in code
  (overlay glow on per-part `{x,y,w,h}` regions). Drop image in `web/assets/`,
  then I wire + calibrate regions. Awaiting the base image.
- Interim (now): stage shows the most-relevant REAL factory diagram per part (no toy
  art), with a banner that the unified x-ray is in progress.

## When the base x-ray image arrives
1. Save to `web/assets/truck-xray.png`; add region boxes per part to content JSON.
2. Replace stage `<img>` swap with: fixed base image + absolutely-positioned glow
   overlay driven by active part's region. Keep scroll-sync + zoom.
3. Calibrate coordinates against the actual image.

## Older options (still relevant later)
1. **Scale diagrams to all systems** — auto-gather candidate images per system from
   the page-types above, then curate a hero set into each content JSON. Biggest win.
2. **Interactive hotspots on the real diagram** — overlay clickable regions on the
   exploded view that link to part explanations (the labeled callouts are at fixed
   positions). More work; do only if user wants the click-to-explain interaction.
3. **Design polish pass** — typography/layout/overall look (user wants "polished").
   Get a reference or specifics.

## Status: working app ✅ (history)
`app/` holds a stdlib-only Python web app. Run it:
```
./scripts/run-app.sh [port]      # default 8080, builds index if missing
# open http://127.0.0.1:8080/   (opens via cmux browser forwarding)
```
- `app/build_index.py` → indexes all 12,110 pages into `app/fsm.db` (SQLite FTS5,
  porter tokenizer). Rebuildable in ~2s. DB is gitignored.
- `app/server.py` → routes: `/` search UI, `/api/search?q=`, `/page?path=<ondisk>`
  clean viewer, `/fsm/<ondisk>` static (images). ThreadingHTTPServer.
- Verified: ranked search w/ highlighted snippets; promo-free page viewer with
  breadcrumbs; internal cross-links rewritten & working (DTC chart → pinpoint
  tests); diagram images serve as image/png.

## Decisions chosen (via AskUserQuestion)
- First feature: **full-text search** ✅ done.
- App style: **clean local web app** ✅.

## FSM data facts (for building more features)
Root: `manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/`
- On-disk section dir names literally contain `%20` (e.g. `Repair%20and%20Diagnosis`);
  in-HTML hrefs double-encode to `%2520`. Decode exactly ONCE to get on-disk path.
  (Helpers: `resolve_ondisk`, `extract_main`, `rewrite` in server.py.)
- Leaf pages: `<div class='main'>…</div>` then `<div class="theme-colors footer"`.
  Content is `<h1>` + `<b>/<br>/<span class=indent-N>/<a>/<img class='big-img'>`.
- Key sections to mine next:
  - DTCs: `…/A L L  Diagnostic Trouble Codes ( DTC )/Testing and Inspection/
    Manufacturer Code Charts/<range>/` — codes w/ descriptions + pinpoint-test links.
  - Specs: `…/Specifications/{Capacity,Electrical,Mechanical} Specifications/…`
  - Wiring: `…/Diagrams/` and `…/Power and Ground Distribution/`.

## Next candidate features (not yet built)
1. DTC lookup page (parse the code charts into code→meaning→test).
2. Quick-reference specs page (aggregate Specifications section).
3. System explainer / symptom→diagnosis flows.
4. Maintenance tracker.

## Access / Tailscale
- App binds **127.0.0.1:8080** (localhost only; not on raw LAN).
- Fronted for the tailnet via `tailscale serve` (HTTPS, tailnet-only, not Funnel):
  `https://zakks-mac-mini.bluebuck-pineapplefish.ts.net/`
- Re-enable: `tailscale serve --bg --https=443 http://127.0.0.1:8080`
  · disable: `tailscale serve --https=443 off`
- The serve config persists, but it proxies to the local app, so `run-app.sh` must
  be running. Not yet a launchd service (would survive reboots / session end).

## Notes
- Background server may be running (port 8080). Re-run via run-app.sh if not.
- Haynes/Chilton owned in print only; OCR pipeline offered, not built.
- Large files gitignored; manuals reproducible via scripts/fetch-manuals.sh.
