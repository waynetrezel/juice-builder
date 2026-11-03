# Juicebuilder visual development

## Start here: current website

From this repository's root, run `npm run dev` with Node.js 22 or newer, then open <http://127.0.0.1:3002/>. No dependency installation is needed. The root URL opens the latest four-film graphic print story at `/graphic-print-world/kling-four/`, including all four approved videos, the editorial panels and the inspiration filmstrip. Video byte-range requests are supported for forward and reverse scroll seeking. The server listens on this computer only and marks responses non-indexable.

Run `npm run check` for JavaScript syntax and current-page asset references, and `npm test` for the existing story checks. This is a static website; there is no build step. The earlier studies remain accessible under `/story-site/` and `/graphic-print-world/`.

Large PNG, MP4, GLB and Blender source files use Git LFS. Install Git LFS before cloning and run `git lfs pull` if media appears as pointer text. Blender auto-backups (`*.blend1`, etc.) are preserved in the local copy but ignored by Git.

## Scroll-story preview

The first website prototype is in [`story-site/`](./story-site/README.md). It demonstrates the agreed story and responsive scrollytelling layout, using a compact generated concept still. Its optional `?animatic=1` mode continuously scrubs a 45-frame Blender blockout sequence as the story scrolls. The image and Blender assets are art-direction/look-development work; this is not the finished photoreal animation. Run it locally with `py -m http.server 3001` from `story-site/` and open `http://localhost:3001`.

This is a fresh project for the fixed, scroll-led juice-making story. The current visual reference is `references/industrial-kitchen-styleframe.png`. The Blender sequence is still an animatic blockout, not the final hyper-real production render.

## Current files

- `references/sunlit-juice-styleframe.png` is the superseded first AI-generated **2D art-direction reference**. It is not a Blender model or final production asset.
- `references/industrial-kitchen-styleframe.png` is the current art-direction reference: exposed brick, charcoal cabinetry, steel framing and focused overhead downlights. It supersedes the earlier sunlit studio look.
- `blender/create_styleframe.py` builds an editable Blender look-development scene with the industrial kitchen set and overhead lights.
- `juicebuilder-industrial-lookdev.blend` is the latest scene saved by that script.
- `renders/aloe-industrial-look-test.png` is a procedural render. It is a geometry and lighting blockout; its organic forms are intentionally not considered final because they do not yet meet the photoreal target.
- `assets/aloe/aloe-skin-albedo.png` is an AI-generated 2D color texture for an aloe-surface test, not a scanned texture or 3D asset.
- `blender/create_aloe_pilot.py` builds a more detailed aloe leaf pilot with that texture in the industrial lighting setup.
- `aloe-asset-pilot-v2.blend` and `renders/aloe-asset-pilot-v2.png` are the editable pilot and its latest render. The mesh is still a procedural look-development model, not the final photoreal asset.
- `assets/aloe/Hi3D_Untitled_allparts_20261026_014833.glb` is the original Hi3D-generated aloe asset. Its download is preserved unchanged.
- `assets/aloe/aloe-leaf-web.glb` is the web copy: about 3.2 MB, 175k triangles, 2K textures and Draco mesh compression. It was imported back into Blender successfully.
- `blender/create_aloe_story_shot.py` stages the generated leaf in the kitchen scene. `aloe-story-shot-v2.blend` and `renders/aloe-story-shot-v2.png` are the latest working scene and still.
- The user confirmed the generated Hi3D leaf is okay to use for this project. It remains a first asset test; its render still shows texture and shape artifacts, so it is not yet a final hyper-real production model.
- `blender/create_story_animatic.py` builds the reversible 264-frame Blender blockout with 11 timeline markers and renders one image per web chapter. It uses 2K scanned lemon, lime, apple, kiwi and single dandelion plant assets from Poly Haven (CC0), plus the user's optimized Hi3D aloe GLB. The late ingredient motion now rises and gathers toward the blender. Asset sources and licensing notes are in `assets/ingredients/ASSET_SOURCES.md`.
- `juicebuilder-story-animatic.blend` is the editable animation scene; `renders/juicebuilder-animatic-contact-sheet-v2.png` is the latest review sheet.
- `blender/make_animatic_contact_sheet.py` makes the chapter contact sheet and compressed stills in `story-site/assets/animatic/`.
- `blender/render_scroll_sequence.py` renders 45 intermediate images from the reversible timeline, and `blender/package_scroll_sequence.py` compresses them into `story-site/assets/sequence/` and makes `renders/juicebuilder-scroll-sequence-contact.png`. The website scrubs this compressed sequence from scroll, with a chapter-based reduced-motion mode.

## Kiwi look test

- `blender/create_kiwi_lookdev.py` creates an isolated ingredient pilot in the industrial kitchen. It uses the Poly Haven CC0 kiwi scan for the whole fruit, a modeled cut half with procedural skin and short fibres, a generated cut-face texture, and separate juice beads. The editable Blender scene is `kiwi-lookdev-v1.blend`.
- `assets/materials/brick_wall_001/` holds the Poly Haven CC0 2K brick colour, normal, and roughness maps used by the kiwi scene. Its source and license are recorded in `ASSET_SOURCE.md`.
- `assets/lookdev/kiwi-cut-surface-v1.png` is an original AI-generated texture used only on the cut plane. It is not a physical scan or a mesh.
- `renders/kiwi-lookdev/kiwi-lookdev-hero-v1.png` is the full resolution Cycles still. `blender/render_kiwi_motion.py` renders 72 review frames over a six-second beat, and `blender/package_kiwi_lookdev.py` creates the version 6 compressed still and MP4 for `story-site/kiwi-lookdev.html`.
- The pilot includes a faceted open glass pitcher with a pouring lip, a metal blade assembly, a detailed motor base, a lid resting on the counter, individually keyed chopped kiwi pieces, a shaped juice volume, and two temporary bottles receiving the pour. The liquid, fruit pieces, stream and blade motion are visual approximations rather than physical simulations. The scene still needs art direction and production refinement before a final photoreal sequence.
- `blender/package_kiwi_scroll.py` compresses the 72 denoised pilot frames to about 1.02 MiB in `story-site/assets/kiwi/scroll/`. `story-site/kiwi-scroll.html` lets the same scene play forward and backward with scrolling; it shows five editorial beats and uses discrete representative frames for reduced-motion visitors.

Rebuild the kiwi pilot from the project root (the MP4 step requires `ffmpeg`):

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python blender\create_kiwi_lookdev.py
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python blender\render_kiwi_motion.py
py blender\package_kiwi_lookdev.py
py blender\package_kiwi_scroll.py
```

## Re-render the blockout

With Blender 5.2 installed at the standard Windows location:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python blender\create_styleframe.py
```

Render the current ingredient pass and update the website stills with:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python blender\create_story_animatic.py
py blender\make_animatic_contact_sheet.py
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python blender\render_scroll_sequence.py
py blender\package_scroll_sequence.py
```

Render the aloe asset pilot with:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python blender\create_aloe_pilot.py
```

Create the compact web copy from the original Hi3D file with:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python blender\optimize_aloe_glb.py
```

Render the generated aloe ingredient shot with:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python blender\create_aloe_story_shot.py
```

## Agreed visual direction

- Industrial-style kitchen with exposed brick, charcoal cabinetry, black steel framing and a substantial island.
- Warm focused pendant/ceiling downlights, with soft fill; no direct sunlight.
- Ingredient order: lemon, lime, apple, aloe vera leaf, kiwi, whole dandelion above ground (no roots), okra.
- Temporary unbranded bottle.
- Scroll tells the story; no ingredient configurator or user-controlled 3D viewer.
- Rendered 3D sequence is the target website format. Realistic ingredient assets still need to be sourced, generated, or modeled and refined before the production animation.
- This pass adds scanned fruit and one root-free dandelion, a ribbed procedural okra pod with seed-bearing slices, and more complete Blender glassware: a handled, tilting pitcher, clear bottles, an opened pour bottle, and a curved juice stream. The pitcher and bottles use procedural geometry and the liquid is a visual approximation; chopped-ingredient motion and the blender's internal mechanics still need production treatment. The website remains a chapter-keyframe animatic, not a continuous rendered sequence.
