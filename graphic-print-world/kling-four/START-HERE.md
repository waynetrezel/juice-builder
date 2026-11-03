# JuiceBuilder — four Kling films + editorial panels

The current direction uses **four short Kling videos** separated by editorial story panels. The earlier layered study remains at the parent folder's `index.html`; this is a separate production path.

**Current status:** All four clips are installed and connected. Clip 03 is the woman-drinks-and-sets-down action; the earlier label-only export is preserved as `videos/03-design-replaced-backup.mp4`. Clip 04 is the quiet final hero/CTA hold. The original Kling exports and their silent scroll-ready versions are kept together in `videos/`. Three new text-and-image interludes live in `panels/`.

## The handoff plan

| Clip | Story | Start image | End image | Target length |
| --- | --- | --- | --- | --- |
| 01 | Imagine a personal drink | `stills/01-opening.png` | `stills/02-empty-bottle.png` | ~5 s |
| 02 | The drink fills the bottle | `stills/02-empty-bottle.png` | `stills/03-filled-bottle.png` | ~5 s |
| 03 | Someone enjoys it; the bottle remains | `stills/03-filled-bottle.png` | `stills/05-final-hero.png` | ~5 s |
| 04 | Final hero / completion hold | `stills/05-final-hero.png` | `stills/05-final-hero.png` | ~5 s |

The same file at each handoff must be used as the previous clip's last-frame reference and the next clip's first-frame reference when the selected Kling mode offers both inputs. If it only accepts one reference image, use the listed start image and describe the listed end image in the prompt, then select a generation whose final frame is closest. Keep the camera locked, 16:9 landscape, all objects clear of the top/bottom frame boundaries, and the same off-white paper background in all four clips. Do not add text or logos to the videos; the website will supply readable live text.

These images are **generated concept references**, not guaranteed pixel-matched production frames. Kling can change the bottle, print texture or framing. Inspect every handoff before accepting a clip. If frames do not align, use the actual final frame of the approved clip as the next clip's start reference, or create a deliberate paper wipe between clips. Do not hide a visual jump with a crossfade.

## Make the clips

1. Clips 01–04 are complete and connected. If a clip is regenerated, preserve the same start/end handoff images and keep the scroll-ready filename alongside the source export.
2. Generate the final landscape video at the same resolution, frame rate and style settings.
3. Review each result for the handoff frame, bottle silhouette, cap, label, paper texture, frame boundaries and absence of lettering. Regenerate a failed clip before making the next one.
4. Save the accepted files here as `videos/01-imagine.mp4` through `videos/04-hero.mp4`. Keep the original Kling downloads separately too.
5. Send me the four MP4 files. I will fit each scene to its scroll range, test reverse scrolling and mobile playback, and choose the best delivery format based on the actual exports. The local page at `index.html` is the four-chapter layout; until MP4s exist it shows the start stills. `videos/manifest.json` lists only approved, installed clips so missing files are never requested by the preview.

## Editorial panels

The panels are deliberately text-free artwork so the live website typography stays sharp and accessible:

| Panel | Story beat | Artwork |
| --- | --- | --- |
| Discover | A trend or recipe catches the customer's eye | `panels/discover-board-landscape-v2.webp` |
| Decide | Flavour, function and ingredient choices become a direction | `panels/build-constellation-remade.webp` |
| On its way | The finished parcel travels to the customer | `panels/delivery-map-remade.webp` |

The sequence is **Imagine → Discover → Decide → Make → On its way → Enjoy → Complete**. All three panels now use landscape artwork with textured-paper breathing room and finished top and bottom torn-paper edges. They are connected directly without extra flat-colour canvas extensions or spacer sections. Discover was recomposed as a 1672 × 941 landscape image, preserving the glass, smartphone, citrus, mint, arrows and colour swatches while painting generous paper margins into the asset itself. Its visible objects occupy approximately source rows 270–708, leaving more than 400px above and below when displayed at the target 3800px desktop width. The complete artwork retains its native aspect ratio as the page scales; the former portrait-specific fit rules have been removed. On mobile, copy sits above the complete artwork. A shared paper grain and soft blending confined to blank paper at the image boundaries avoid abrupt panel edges. Video playback remains scroll-driven; the inspiration filmstrip performs one automatic entrance when it comes into view, and copy retains its viewport-triggered entrances. Small uppercase scene labels and the title shadow have been removed. Each orange chapter progress line remains visible at 100%.

The paired `*-remade.png` files are unchanged copies of the approved generated images. WebP files are delivery encodes of those images, with no padding, cropping, or regeneration:

- Discover landscape: `exec-2f14d104-ef87-4fef-bb16-f048afefbc1e.png` (1672 × 941), saved as `panels/discover-board-landscape-v2.png` and encoded as WebP. Full generation prompts are in `review/discover-landscape-generation.md`. The earlier portrait `exec-e1702851-553c-4e6f-ade0-a49098cac043.png` (1024 × 1536) is preserved as a backup.
- Decide: `exec-0308e45d-e4fc-4839-b23a-27d889b25d39.png` (1672 × 941).
- On its way: `exec-7cf7333a-41ea-4fd6-a788-801eff4d65f2.png` (1672 × 941).

Older `*-400margin.*` versions are retained as backups but are no longer referenced by the page.

## Scroll treatment

The paper gap between Discover and Decide now contains a long cobalt filmstrip of original drink-recipe inspiration images. It has textured torn-paper edges, transparent sprocket holes and subtle reel markers. Its 24 frames use six generated images saved in `panels/reels/`. The roll sweeps right to left once in 2.2 seconds with `cubic-bezier(.65,0,.35,1)` ease-in-out, then settles. Motion is handled by `inspiration-film.js` and does not modify film scrubbing. On desktop it overlays the existing gap; smaller screens give the roll its own row so it cannot cover the copy. Reduced-motion mode shows the settled strip immediately. Full prompts and source details are in `review/inspiration-film-generation.md`.

The ingredient trail remains saved for future placement in the `#saved-ingredient-trail` template, with its transparent assets, CSS and `ingredient-trail.js` preserved. It is not displayed and its script is not loaded in the current layout. Sources and prompts remain in `review/ingredient-trail-generation.md`.

Each video gets its own scroll chapter and its own readable heading. The visual stays pinned while the chapter scrolls. Forward scroll advances the clip; reverse scroll rewinds it. Editorial panels sit between the relevant clips and animate their copy once on entry. On reduced-motion devices, show the stills without animated video or copy transitions. Final optimization will follow playback tests with the real files; direct MP4 seeking and a compressed frame sequence are both possible.

The five stills were made for this concept and are safe to use as generation references. They are not final client product branding or print-ready packaging art.
