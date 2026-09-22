# Site Inspiration — Interactive "How It Works" Explainers

Reference collection for the future **truck systems explainer website**: an interactive
site with visual explainers, diagnostics, and repair/understanding guides for each truck
system (engine, starter, transmission, brakes, etc.). Seeded by the Interlatent robotics
hardware guide (https://interlatent.com/blog/interlatent-robotics-hardware-guide).

Per-part template we like: **history → what it does → how it works**, with an interactive
visual at each step (e.g. the starter motor: Cadillac ~1912 → cranks the engine → coil
creates a magnetic field, etc.).

## The gold standard (most relevant to a truck)

- **[Bartosz Ciechanowski — ciechanow.ski](https://ciechanow.ski/)** — The bar to aim for.
  Real-time WebGL interactives you drag/rotate/tweak. Already has directly-relevant pieces:
  - [Internal Combustion Engine](https://ciechanow.ski/internal-combustion-engine/)
  - [Gears](https://ciechanow.ski/gears/)
  - [Mechanical Watch](https://ciechanow.ski/mechanical-watch/)
  - [Bicycle](https://ciechanow.ski/bicycle/)
  - Note how he layers simple → complex with an interactive at every step.
- **[Animagraffs — animagraffs.com](https://animagraffs.com/)** — Animated cutaway infographics.
  [How a Car Engine Works](https://animagraffs.com/how-a-car-engine-works/) + transmission.
  Guided animated cutaways (different style from drag-to-explore).
- **[How a Car Works — howacarworks.com](https://howacarworks.com/)** — Whole automotive
  teaching site with CGI; tears down & rebuilds a car across systems. Directly our domain.

## The computing one (Zakk was trying to recall — best guess first)

- **[Putting the "You" in CPU — cpu.land](https://cpu.land/)** — How a CPU runs your programs.
- **[nand2tetris](https://www.nand2tetris.org/)** — build a computer from NAND gates up (more course).
- **[Red Blob Games — redblobgames.com](https://www.redblobgames.com/)** — Amit Patel's
  interactive algorithm explainers (pathfinding, hexagons). Stellar interaction design.

## The "explorable explanations" movement (philosophy + more examples)

- **[Explorable Explanations — explorabl.es](https://explorabl.es/)** — Nicky Case's hub; the genre's manifesto.
- **[Nicky Case — ncase.me](https://ncase.me/)** — *The Evolution of Trust*, *Parable of the Polygons*.
- **[Bret Victor — worrydream.com](https://worrydream.com/ExplorableExplanations/)** — the original 2011 essay.
- **[awesome-explorables (GitHub)](https://github.com/blob42/awesome-explorables)** — big curated list to mine.

## Other excellent interactive-essay producers (style/inspiration)

- **[samwho.dev](https://samwho.dev/)** — single-concept deep-dives (load balancing, memory
  allocation, hashing). Close to our "explain the starter motor" idea.
- **[The Pudding — pudding.cool](https://pudding.cool/)** — visual essays; scrollytelling pacing.
- **[Distill.pub](https://distill.pub/)** — interactive ML explainers; clean "interactive figure in prose."

## Strategic notes

1. **Our CAD work is a natural fit.** We already have 3D models of ~21 truck systems.
   Ciechanowski's approach is real-time 3D you can manipulate — our part library could power
   exactly that, a head start most of these sites didn't have.
2. **Standardize the per-part structure** (history → what it does → how it works), the way
   Ciechanowski and samwho.dev structure a single piece.
