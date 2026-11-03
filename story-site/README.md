# Juicebuilder story study

A first, responsive scrollytelling page for the agreed Juicebuilder concept: an industrial kitchen, seven ingredients, a gathering swirl, blending and a final bottle. Scroll drives the story; this is not a recipe configurator.

## Run locally

This starter uses plain HTML, CSS and browser JavaScript, so it has no dependency install step. From this folder, run:

```powershell
py -m http.server 3001
```

Then open `http://localhost:3001`. Stop the local server with Ctrl+C.

To scroll through the Blender animation study, open `http://localhost:3001/?animatic=1`. It scrubs a compressed 45-frame Blender sequence continuously with page scroll; with reduced-motion enabled it advances one representative frame per chapter. The normal URL keeps the generated art-direction still.

Run the data and progress checks with:

```powershell
node --test tests/story.test.mjs
```

`package.json` also exposes the same check as `npm test`; no packages need to be installed.

## What this version demonstrates

The separate [`kiwi-lookdev.html`](./kiwi-lookdev.html) page shows the detailed kiwi pilot as a still and short motion review, including an open glass blender and the kiwi-to-juice handoff. It uses the same industrial kitchen direction and is a visual study for the eventual rendered story.

[`kiwi-scroll.html`](./kiwi-scroll.html) presents the same 72 denoised rendered frames as a reversible scroll story, with five chapter captions ending in a two-bottle pour. The compressed frame set totals about 1.02 MiB. Reduced-motion visitors see representative still frames at chapter changes; the transcript below the visual sequence contains the complete text.

- The full editorial sequence and provisional copy, with the requested ingredient order.
- A sticky cinematic frame whose crop, scale, captions and progress change as chapters pass.
- An optional Blender blockout view (`?animatic=1`) that scrubs the 45-frame optimized sequence as the story scrolls.
- A mobile layout, semantic chapter headings, skip link, keyboard-native page navigation, reduced-motion support, a readable no-script story and a no-WebGL image fallback.
- A compact WebP concept key visual. It is art direction, not a final animated render or a scanned product asset.

The scene is a visual timing and storytelling prototype. It does **not** yet contain the final photoreal 3D animation. The generated key visual and Blender assets are not evidence that each ingredient, liquid or product has been physically validated.

## Customise the sequence

Edit `src/story-data.js` to change the chapter order, copy, labels, stage names or `sequenceFrame` values. Those frame values align each scroll chapter with its position in the Blender timeline. Each chapter has a small typed-by-documentation schema (`StoryChapter`). `src/story.js` builds the semantic text and connects the active chapter to the stage. `styles.css` controls responsive art direction and the stage treatment.

## Move from concept to final imagery

1. Approve the story beats and copy before producing every shot.
2. Build or source licensed, production-quality ingredient and bottle assets. The Hi3D aloe model is only a first test; check the tool's license and inspect it before commercial use.
3. Assemble and animate the set in Blender. Keep ingredients, liquid, glass and kitchen details as separate objects where possible. Use Blender's camera and lighting for the finished sequence.
4. Export a numbered image sequence or video from Blender. For frame-by-frame scroll, encode an image sequence as AVIF/WebP and load the nearby frames based on scroll progress; for lower bandwidth, use a short video with `currentTime` driven by scroll and a poster fallback. Respect reduced-motion and provide a no-script final still.
5. Replace the concept image and stage animation in this site. Preserve the text chapters as real HTML for accessibility and search.

## Performance and licensing

Keep the first screen lightweight, lazy-load below-the-fold sequences, offer a still-frame fallback, and test on a mid-range phone. Avoid shipping large uncompressed PNGs, unnecessary 8K textures, or full-resolution source GLBs to the page. Prefer original client-approved assets or assets with explicit commercial rights; keep license/source notes alongside each imported asset. Do not use reference-site imagery or proprietary assets without permission.
