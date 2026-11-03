# Liquid Ribbon

This is a separate prototype workspace for the next Juicebuilder direction. The completed kiwi pilot remains at the parent `story-site` level and is linked from the shell; nothing in that prototype has been replaced.

## Current state

- Prototype name: `liquid-ribbon`
- Status: neutral shell ready for the new brief
- Entry point: `index.html`
- Styling: `src/styles.css`
- Refined concept brief: `PRODUCTION-BRIEF.md`
- Reserved folders: `assets/` for supplied/generated media and `src/` for the experience code
- Kling handoff folder: `assets/source/kling/` for original exports; processed web assets will go in `assets/processed/`

The first concept refinement is now captured in `PRODUCTION-BRIEF.md`. It defines the 18-second Liquid Ribbon storyboard, the jug handoff, ingredient choreography, transparency strategy and production limitations without generating final media. This prototype can receive its own Blender scene, rendered sequence, scroll choreography and responsive treatment without changing the kiwi work.

The supplied Kling generations are preserved in `assets/source/kling/`. The latest black-background export is `assets/source/kling/liquid-ribbon-kling-v2.mp4` (25.04 seconds), with a silent browser copy and poster in `assets/processed/`. The current `kling-scroll.html` route uses that latest video inside the earlier scroll-story layout with a black presentation background. Its timeline is scrubbed directly by page scroll, without easing. The previous frame-scrub comparison is preserved at `kling-scroll-frames.html`.

The black-background still reference is saved as `assets/processed/liquid-ribbon-hero-black-v1.png` for use in image-to-video generation tools that cannot accept the reference video.

The black-background storyboard sheet is saved as `assets/processed/liquid-ribbon-storyboard-black-v1.png`.

The separate two-chapter **Impossible Delivery** concept is ready in `IMPOSSIBLE-DELIVERY-HANDOFF.md`, with three generated reference stills under `assets/concept/impossible-delivery/`. It supplies the two Kling prompts, their shared bottle handoff image, safe-area rules and the planned scroll-page transition. No new Kling footage has been generated yet.

## First blockout

The initial Blender timing blockout is now saved at the project root as `liquid-ribbon-blockout-v1.blend`. It uses simple procedural shapes and a dark inspection background to validate composition only. Checkpoint frames are in `renders/liquid-ribbon-blockout/` at frames 001, 088, 124 and 180. The scene is 24fps over 180 frames and is explicitly marked as not final media.
