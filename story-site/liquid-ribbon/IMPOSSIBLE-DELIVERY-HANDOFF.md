# Impossible Delivery — two-chapter production handoff

This is a new, separate Liquid Ribbon concept. The existing Kling scroll prototype is unchanged. The film tells the Juicebuilder service story through one recognisable bottle: choices shape it, then an impossible delivery brings it to a floating doorway. The two videos are generated separately and become two independent scroll-controlled sections, divided by a short text section.

## Reference stills

All three concept stills were generated for this project. They are 1672 × 941 PNGs (approximately 16:9) and contain no third-party product artwork. They are visual guidance, not a guarantee that Kling will reproduce every object exactly.

| Still | File | Use in Kling |
| --- | --- | --- |
| Chapter 1 opening | `assets/concept/impossible-delivery/chapter-1-start.png` | First frame of Chapter 1 |
| Shared bottle handoff | `assets/concept/impossible-delivery/shared-bottle-handoff.png` | Last frame of Chapter 1 **and** first frame of Chapter 2; use the same file for both |
| Chapter 2 arrival | `assets/concept/impossible-delivery/chapter-2-end.png` | Last frame of Chapter 2 |

If the selected Kling mode permits first and last frame references, use the paired stills above. If it only permits a first frame, use the first still for each chapter and describe the desired ending in the corresponding prompt. Do not use the old multi-panel moodboard as a start frame.

## Shared production rules

- Landscape 16:9; target roughly 10–15 seconds per chapter, using the duration offered by the selected Kling mode. A final hold of 1–2 seconds gives the scroll page a stable end frame.
- One continuous shot per chapter. Fixed camera, no zoom or vertical pan. Objects float with no floor, horizon or supporting surface.
- Uniform jet-black `#000000` background. Every illuminated pixel, including shadows, glow and reflections, stays within the middle 60% of the frame height where possible. The top and bottom 20% are empty black in generation. The website master will enforce a final 15% pure-black band on each edge after the footage is approved.
- Motion may cross the left or right edge. Never let a bottle, carton, doorway, particle or its lighting cross the upper or lower safe limits.
- Preserve one bottle identity: rounded clear glass, coral-red cap, amber-to-ruby drink, condensation, and the coral/gold/violet swirl emblem. No words on the label.
- No captions, logos, cards or storyboard panels inside the generated video. Website copy belongs in the separate transition section.

## Chapter 1 — Made for you

**Story:** Four abstract floating choices converge and sculpt a single personalised drink bottle. The completed bottle holds centred as the shared handoff frame.

**Kling prompt — paste as one prompt:**

> Premium pop-surrealist 3D commercial, one continuous fixed-camera shot on uniform jet-black #000000. Begin from the supplied first frame: a floating golden crescent, violet cloud, coral starburst and translucent green spiral, each a glossy sculptural symbol for a different mood or taste. The symbols drift horizontally toward the centre in graceful, playful motion. Their colours weave together into a luminous amber-to-ruby liquid and resolve into one sealed, rounded clear-glass drink bottle with a coral-red cap, subtle condensation and a bold coral/gold/violet abstract swirl emblem, with no lettering. End on the supplied last-frame image of that exact bottle, stationary and centred, and hold it for the final 1–2 seconds. Smooth coherent transformation, rich jewel-like reflections, clean graphic silhouettes, no cuts, no extra bottles. Keep the camera still. Every object, particle, reflection, glow and shadow remains within the central 60% of frame height. The top and bottom 20% stay completely empty, unlit and pure #000000 for every frame. Horizontal entry and exit is permitted; vertical entry, exit or clipping is forbidden. No floor, horizon, gradient, vignette, text, logo or storyboard layout.

## Between the chapters

After Chapter 1 completes, keep its final bottle frame visible briefly, then scroll to a separate black editorial section with the line:

> Made around you. On its way to you.

Do not place this copy over the moving bottle. The next scroll section starts with the **same shared bottle still** at matching scale and position, so the story reconnects cleanly. The transition section can be short; its job is to make the shift from creation to delivery legible.

## Chapter 2 — The impossible delivery

**Story:** Packaging forms around the same bottle. The visible drink travels sideways through suspended surreal spaces and arrives beside a floating doorway. The carton remains open-sided so viewers always recognise it as a drink delivery.

**Kling prompt — paste as one prompt:**

> Premium pop-surrealist 3D commercial, one continuous fixed-camera shot on uniform jet-black #000000. Begin with the supplied first-frame image: the same single rounded clear-glass bottle, coral-red cap, amber-to-ruby drink, condensation and coral/gold/violet swirl emblem, centred and floating. Keep the bottle's shape, cap, label emblem and liquid colour consistent throughout. Warm coral and golden-orange folded panels assemble around it into a playful open-sided delivery carton with a broad front cutout; the bottle remains visible at all times. The packaged bottle glides horizontally through a few brief, abstract floating colour portals, suggesting an impossible journey without showing a floor or landscape. It arrives beside a small suspended doorway that opens to reveal violet and gold light. End on the supplied last-frame image: the complete visible bottle in its open-sided carton beside the doorway, held still for the final 1–2 seconds. Elegant coherent motion, jewel-like materials, no cuts, no duplicate bottle. Keep the camera still. Every object, particle, reflection, glow and shadow remains within the central 60% of frame height. The top and bottom 20% stay completely empty, unlit and pure #000000 for every frame. Horizontal entry and exit is permitted; vertical entry, exit or clipping is forbidden. No floor, horizon, gradient, vignette, captions, text, logo or storyboard layout.

## Review and website integration

1. Generate Chapter 1 with its opening and handoff references. Check the completed bottle against the handoff still before generating Chapter 2.
2. Generate Chapter 2 using the **exact Chapter 1 handoff image** as its first-frame reference. If Kling changes the bottle too much, use a frame exported from the approved Chapter 1 clip as the new first-frame reference for Chapter 2.
3. Review both exports from first frame to last. Reject or regenerate any shot with top/bottom clipping, coloured background, off-frame glass or bottle, visible floor, inconsistent bottle identity, or the package hiding the drink.
4. Once approved, prepare silent browser copies and posters. The website uses two separate sticky scroll sections, each mapping its own scroll progress directly to its clip time, with the copy section between them. Lazy-load Chapter 2 until the user approaches it; keep the fallback stills for reduced-motion and video failure.
5. Composite final pure-black 15% top/bottom guard bands only after approving the motion. The bands guarantee clean website edges but cannot recover content already cropped or conceal important action that strays into them.

The stills are concept references generated with the built-in ImageGen tool. The final film remains subject to Kling generation and visual review.
