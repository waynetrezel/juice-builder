# JuiceBuilder — Graphic Print World

## Concept

A personalised drink moves from an idea to a designed, made and enjoyed object. The world looks like a premium printed campaign brought to life: cut paper, imperfect ink registration, halftone texture and small physical shadows. It should feel tactile and confident, with no glossy CGI or floating liquid effects.

The stills in this folder are **visual keyframes**, not animation-ready layers or final packaging artwork. Keep typography as live website text rather than baking it into the imagery.

## Four scroll scenes

| Scene | Keyframe | Story beat | Motion on scroll |
| --- | --- | --- | --- |
| 01 — Imagine | `01-idea.png` | A person imagines their own drink. Fruit, botanical shapes and bottle studies appear inside the paper profile. | Printed shapes register into place one by one; a bottle study becomes the visual bridge to scene 02. |
| 02 — Make | `02-drink-forms.png` | The imagined bottle becomes the drink. | The bottle outline scales up from the study card. Orange and red ink layers rise inside it in successive print passes; slight registration offsets settle. |
| 03 — Design | `03-design-applied.png` | A bespoke label completes the bottle. | Label proofs slide in from the side. The chosen botanical design folds around the bottle; unused proofs slip away. |
| 04 — Enjoy | `04-sip.png` → `05-final-bottle.png` | A person takes a sip and sets the bottle down. The bottle remains as the final frame. | The cut-paper hand lifts and tilts the **uncapped** bottle to the mouth, lowers it, replaces the cap, sets it on the cobalt strip, then exits. The final frame holds for the call to action. |

## Visual rules

- Warm off-white paper background; deep cobalt, vermilion, citrus orange and botanical green inks.
- Flat printed forms with real paper fibres, rough edges, halftone and slight ink misregistration.
- Space on the left for live headings and short copy; keep the bottle comfortably within the frame on mobile.
- Human movement is represented with articulated paper cutouts, never photoreal footage.
- No liquid ribbon, floating gemstones, robotic assembly, neon lighting or ornate glass.
- Maintain one recognisable bottle silhouette, cap colour and label motif across scenes.

## Production approach

Build an initial scroll animatic from the keyframes, then recreate each moving part as a separate SVG or transparent raster layer. A pinned stage with scroll-linked transforms, masks and paper-texture overlays can carry most of the motion. Use a short pre-rendered segment only where the sip or label wrap needs more intricate hand animation. Keep scene text in HTML for accessibility and responsive layout. Provide a reduced-motion version showing the four keyframes without scrubbed animation.

## Next production pass

1. Lock the bottle silhouette and a temporary label mark in a single source design.
2. Separate the profile, ingredients, bottle, fill passes, label proofs, hand and paper background into layers.
3. Assemble a low-fidelity scroll animatic with the four scenes and test its pacing on desktop and mobile.
4. Refine hand motion, print texture and final call to action after the animatic feels right.
