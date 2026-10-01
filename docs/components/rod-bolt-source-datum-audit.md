# Component contract and handoff: rod-bolt source/datum audit

## Contract

Engine #32; root integration owner; inclined-linkage worker. Baseline combined-motion contract `1440853952cd132e17693c6355c38bcb0f9276b4`, current branch `engine/timing-drive-fit`. Research only. Own this new handoff and `reference/engine/rod-bolt-source-datum-review.json`. No geometry, frozen report, shared viewer or inventory edits. Preserve all stable rod/bolt/nut occurrence IDs, millimeter units, crank journal centers, rod length, piston-pin center and corrected pose convention. Any later candidate needs a separate bounded contract.

The actual combined-motion diagnostic finds six inherited bolt-head/block conflicts. Source replay proves the current bolt is an estimated cylinder plus regular hexagonal prism. The original block and original motion reproduce the same conflict exactly; it is not caused by the corrected crank rotation. See `inventory/engine/engine-corrected-rod-bolt-conflict-validation.json` and the frozen combined handoff.

## Evidence ledger

| Claim | Evidence class / datum | Source and limit |
|---|---|---|
| Current bolt shank diameter 8 mm, stock Z−31..23; head circumradius 7 mm, Z22..27 | Existing illustrative estimate | `first_assembly.py`; exact actual STEP replay difference0. Hex across flats12.124356 mm is derived, not a Ford dimension. |
| Current rod bosses at Y±34.5, split Z0, boss height44, hole diameter8.4 | Existing estimates | `first_assembly.py` rod construction / dimensions; no physical press shoulder modeled. Nominal smooth shank has0.4 mm diametral clearance. |
| Exactyear rod orientation | Exactyear manual diagram, qualitative | Image292722974: piston notch toward front; numbered rod side toward camshaft. Figure viewed. Low head silhouettes in elevation cannot establish three-dimensional head shape or scaled dimensions. |
| Service rod assembly E3TZ6200ERM | Exactyear parts listing | Service assembly identity; does not identify an individual bolt or original engineering number. |
| ARP152-6002 applies to Ford4.9L inline6 | Replacement comparison | Manufacturer kit page and manufacturer-authored instructions. Exact year/OEM equivalence not established. |
| Press-fit bolt architecture; rod hole must clear under-head radius; mating rod requires attention when bolts change | Replacement comparison | ARP152-6002 instructions, p1. Does not provide shoulder diameter, press fit, head dimensions or bolt length. No ARP torque is adopted as Ford production guidance. |
| Catalog distinguishes 240–300cid kit152-6001 styleG from4.9L kit152-6002 styleM | Replacement comparison | ARP2026 catalog p49; manufacturer explicitly asks users to verify head style against p46 images. Text retrieved, image not inspected, so no geometric shape claim is made for styleM. |
| Crankcase R98 | Existing estimate | Existing generator; witness radius98.179965 mm. No measured block contour establishes that R98 is correct. |

Public primary-author sources: [ARP kit152-6002](https://arp-bolts.com/kit/152-6002), [ARP-authored instructions, distributor-hosted PDF](https://www.tzr-motorsport.de/WebRoot/Store20/Shops/61911476/MediaGallery/PDF/ARP/Ford/152-6002.pdf), [ARP2026 catalog p49](https://arpcatalog.com/49/), [head-style reference p46](https://arpcatalog.com/46/). Reviewed 2026-10-01. The instruction summary is limited to architecture; factory tightening procedures are outside scope.

Exactyear local paths and hashes are in the accompanying JSON. Purchased/manual artwork remains ignored and is not redistributed. The public catalog PDF fetches exceeded tool size limits; a smaller mirrored excerpt timed out. Accessible manufacturer HTML provides application/style distinctions but not usable bolt dimensions. Retailer descriptions and forum guesses are not dimensional authority.

## Decision and next contract

**No dimensional replacement is justified yet.** The current generic hex bolt is unsupported, but neither the actual replacement head envelope nor the original rod boss/bolt dimensions is established. Choosing a shorter head simply because it clears the estimated block would substitute one assumption for another. The exactyear elevation and ARP press-fit architecture support auditing the bolt and mating rod together.

A defensible future candidate needs: verified physical head type and plan outline/orientation; head thickness and under-head radius; press-shoulder diameter/length and matching rod seat; smooth grip and threaded portions; nut bearing plane; rod boss width/height, split plane and edge distances; and an actual crankcase section or explicit continued cavity estimate. Protect the journal/bearing and piston-pin datums and full rod length. Demonstrate source replay of the old shape, unchanged protected regions, actual bolt/rod seating, positive head support, rigid-stack motion and block clearance throughout a declared continuous range or honestly sampled range. No clearance-only block cut and no automatic adoption of a replacement part as factory geometry.

## Delivery and gates

Research candidate only, no asset release or CAD build. Existing diagnostic CAD is referenced unchanged. Application/coverage PASS for a scoped unresolved audit; dimensions UNKNOWN for replacement hardware; CAD/export N/A; source/visual review PARTIAL (exactyear drawing viewed, catalog style photo not viewed); installed interface FAIL inherited; motion FAIL inherited; learning N/A; browser NOT RUN; reproduction uses source URLs plus exact local hashes. No geometry check is claimed passed by this research.

Root owns issue/PR integration. #32 remains open. Next action is a manufacturer dimensional drawing or measured applicable bolt-and-rod sample, followed by a bounded source-informed replacement contract; if unavailable, retain an explicitly estimated research candidate rather than claim resolution. No running process. Model/usage unavailable.
