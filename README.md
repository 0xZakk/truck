# 1994 F-150 Atlas

An interactive, component-level reconstruction of a **1994 Ford F-150 XLT SuperCab, short bed, 2WD**, with the **4.9L inline-six** and **M5OD-R2 five-speed manual transmission**.

Explore how the truck fits together through individual CAD parts, installed assemblies, mechanical motion, and source-linked engineering notes. The project follows one owner's white F-150, rather than a generic vehicle model.

## Explore the atlas

**[Open the live Truck Explorer](https://truck-atlas.vercel.app/explore)**

The current application includes:

- **3D Truck Explorer:** select and isolate systems and parts, inspect assemblies, use X-ray and cutaway views, and explore assembly explosion, engine motion, gear selection, and clutch movement.
- **Parts catalog:** component and assembly pages with interactive models, functions, dimensions, and related systems.
- **System guides:** explanations connecting the engine, transmission, driveline, suspension, steering, brakes, electrical equipment, and other truck systems.
- **Engineering essays:** illustrated guides and focused piston and valvetrain studies.

The application uses Astro, React, TypeScript, and Three.js. Parametric CAD sources and assembly inventories supply the browser geometry and explicit placement transforms.

## Status and accuracy

**This is an educational reconstruction in progress, not a factory-certified digital twin or a service manual.** Some geometry is source-supported; other details are replacement-part comparisons, estimates, or unresolved candidates. Motion and exploded views can be illustrative rather than validated service procedures.

A successful export, collision check, website build, or deployment does not establish factory fidelity. The owner's truck has no known modifications, but original configuration is not proven for every component. Its emissions calibration remains unconfirmed, and exterior body dimensions and rear frame/bed fit remain provisional.

Read [current state](docs/CURRENT-STATE.md), component handoffs, and [quality requirements](docs/onboarding/QUALITY-STANDARD.md) for the scope and limitations of each checkpoint. Historical completion claims are not a substitute for current evidence.

## Run locally

### Committed engine viewer

This is the starting point for a fresh clone and needs no CAD installation:

```sh
git clone https://github.com/0xZakk/truck.git
cd truck
python3 -m http.server 8081 --bind 127.0.0.1
```

Open [the engine viewer](http://127.0.0.1:8081/viewer/engine.html). Its pinned Three.js CDN imports require internet access.

### Current Astro application

The newer whole-truck application is maintained in the development checkout under `app/`. **Its source and complete current asset set are not yet published on the repository's default branch.** These commands apply to a checkout containing that application and its matching inventory and meshes; cloning the repository alone does not restore the current whole-truck experience.

```sh
cd app
npm ci
npm run dev
```

Open [the Truck Explorer](http://127.0.0.1:4321/explore). Viewing existing meshes does not require running the CAD builders.

## Production build and deployment

In the current application checkout:

```sh
cd app
npm run build:vercel
npx vercel login
npx vercel link
npx vercel deploy --prebuilt --prod --archive=tgz
```

The production build generates static pages and packages only the viewer's required JSON, authored GLB meshes, and legacy study assets. Packaging checks the runtime asset list and rejects unexpected files. Missing meshes fail the build instead of silently shipping an incomplete viewer.

**Do not deploy the local `public/` symlink tree or the entire working directory.** Those development links include manuals and research folders. Purchased manuals, owner photographs, source captures, credentials, and STEP originals are excluded from the production package. See `app/DEPLOYMENT.md` in the application checkout for the full workflow. Automatic deployment from Git requires publishing and restoring the matching source and asset set first.

## Repository map

| Location | Contents |
| --- | --- |
| `app/` | Current Astro/React atlas and Vercel packaging; development checkout only pending source publication |
| `viewer/` | Committed browser viewers and focused mechanical studies |
| `cad/` | Parametric CAD sources and assembly helpers |
| `models/` | Browser geometry, with availability depending on the checkpoint |
| `inventory/` | Part identities, assembly hierarchy, transforms, evidence, and validation records |
| `kb/` | Source-linked knowledge base |
| `docs/` | Onboarding, component handoffs, quality gates, and project status |
| `scripts/` | Export, composition, navigation, and validation utilities |

Large generated CAD checkpoints follow the [artifact restoration policy](docs/CAD-ARTIFACTS.md). Purchased reference originals and owner photographs remain local. Pilot and candidate outputs are not automatically accepted into the installed reconstruction.

## Contribute

Start with [developer and agent onboarding](docs/onboarding/START-HERE.md), then read [CONTRIBUTING.md](CONTRIBUTING.md).

- [Project board](https://github.com/users/0xZakk/projects/2) and [system workstreams](docs/github-workstreams.json)
- [Engine component backlog](docs/engine-parts/README.md)
- [Project workflow](docs/onboarding/PROJECT-WORKFLOW.md) and [component handoff template](docs/templates/COMPONENT-HANDOFF.md)
- [CAD pipeline](cad/engine/README.md) and [efficient modeling workflow](docs/TOKEN-EFFICIENT-BUILD-WORKFLOW.md)
- [Knowledge-base workflow](docs/KNOWLEDGE-BASE-WORKFLOW.md)

Work on a bounded issue, preserve stable part IDs and explicit millimeter transforms, record evidence and unknowns, and run checks appropriate to the change. Lightweight CI verifies navigation and syntax; it does not prove CAD fidelity. Integration review and browser checks are required before an installed component is considered complete.
