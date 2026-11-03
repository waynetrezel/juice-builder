# Liquid Ribbon — production brief

Status: concept refinement only. No final media has been generated or published.

## Direction already established

- A premium, roughly 18-second scrollytelling sequence for a personalised herbal and fruit drink service.
- Empty-space presentation: no room, kitchen, tabletop, horizon, stars or decorative environment.
- Seven recognisable opening ingredients: coconut, pineapple, cherries, papaya, banana, grapes and lime.
- Ingredients soften into flowing strands, merge into one broad glossy ribbon, gather into a clear jug, pour into a clear glass, then resolve into an appetising finished drink.
- Golden-peach, lightly creamy liquid is the working look; it is not a claim about the final recipe.
- Front three-quarter camera near glass-rim height, glass lower-left, jug upper-right, restrained camera movement.
- The final output should support true transparency if technically practical, with a composited fallback if glass/refraction makes alpha unreliable.
- No audio, baked-in copy, glitter, explosive splash, ice or ornamental foliage.

### Kling source decision

The supplied Kling generation is now the visual source for this prototype pass. All visible ingredients, leaves, ribbons, droplets, glass details and garnish in that generation are retained; the browser preparation removes only the audio track. The visible Kling watermark remains in the review copy until a clean licensed export is available.

## Main risks and the fixes

### 1. Fruit suddenly “melting” into liquid

The weak version is a cross-fade or a generic blob that loses the relationship between ingredient and juice. Keep each fruit anchored at one end while its edible cut surface elongates into a strand. Let the strand inherit the fruit's colour first, then blend towards the golden-peach master liquid. Remove pits, stalks, peel and the coconut shell as separate, quiet exits behind the motion; never turn the coconut shell itself into juice.

### 2. The jug appearing without a handoff

The jug should already be spatially implied before it becomes important. Introduce a faint glass silhouette in the upper-right during the final convergence, then reveal its highlights as the ribbon's leading edge approaches the mouth. The jug rotates into its pouring angle only after the ribbon has entered it. This preserves volume and direction instead of creating a teleporting prop.

### 3. A disconnected or weightless pour

Keep one continuous attachment from jug lip to glass. Use a slightly narrowing, thick stream with a visible rolling fold at impact, restrained droplets and a rising fill level. The stream can be art-directed geometry for the concept pass; a Mantaflow simulation should be reserved for the final shot if the landing wave needs more physical detail.

## Refined 18-second storyboard

| Time | Story beat | Action and transition |
| --- | --- | --- |
| 0.0–1.2 | Establish | Empty glass is already lower-left. The seven ingredients fade in on a loose S-curve with generous negative space. |
| 1.2–3.8 | Recognise | Pineapple wedge and deseeded papaya crescent lead the composition; coconut half and peeled banana balance them; cherries, grape cluster and lime half provide smaller accents. Each turns only enough to reveal texture. |
| 3.8–4.6 | Initiate | The S-curve begins to travel. Cut faces brighten; the glass remains a fixed anchor while the camera stays nearly still. |
| 4.6–7.8 | Transform | Fruit-by-fruit, edible flesh stretches from the cut surface into short strands. Pineapple/papaya read golden-peach, coconut/banana creamy, cherries/grapes darker, lime green. Shell, peel, pits and stalks leave at the outer edge of the curve. |
| 7.8–8.8 | Merge | The strands braid into one broad ribbon with one clear sculptural curl. Keep the curl readable; no tangled particle cloud. |
| 8.8–10.2 | Gather | A clear jug is now visible upper-right. The ribbon enters its mouth, its final tail joins the reservoir, and the jug begins a slow tilt. This is the handoff beat and must not be shortened. |
| 10.2–14.2 | Pour | Jug and glass form the reference diagonal. The stream stays attached to the lip, lands inside the opening, creates one rolling fold and raises the liquid level consistently. |
| 14.2–15.4 | Release | The stream narrows and breaks naturally. The jug lifts out towards the upper-right, leaving the finished glass as the destination. |
| 15.4–18.0 | Hero hold | Camera approaches 3–5%. Surface settles with subtle bubbles; condensation catches the key light. A small lime wheel on the rim is the default garnish. |

## Camera and composition

- Master framing: 16:9, with a protected centre crop for 4:5 and 9:16 mobile versions.
- Use one restrained front three-quarter camera, approximately 70mm equivalent, at or just above the glass rim. Avoid a dramatic orbit; spatial continuity is more valuable than spectacle.
- Keep the glass lower and slightly left of centre throughout. Reserve the upper-right diagonal for the jug and pour. Leave clear negative space around the S-curve so surrounding website copy can coexist.
- The only camera move is the final 3–5% approach during the hero hold.

## Ingredient choreography

- Pineapple wedge: largest golden anchor, its cut plane becoming the longest first ribbon strand.
- Papaya crescent: second large warm shape, deseeded, contributing a softer peach strand.
- Coconut half: white flesh is the edible source; the shell eases out of frame separately and never liquefies.
- Banana section: peeled, creamy, slightly curved; stretches later than the pineapple so the S-curve remains legible.
- Cherries: two or three whole cherries become short burgundy streaks; pits exit with the stems.
- Grape cluster: small cluster separates into a few purple-green beads before joining the ribbon.
- Lime half: bright green accent and eventual rim garnish; flesh contributes a brief green edge before blending.

## Lighting and materials

Use an invisible studio rig rather than an environment: a large soft key above/front-left, a controlled warm rim from upper-right, and narrow black/white reflection cards outside camera view. These cards give glass and liquid readable highlights while preserving an empty background.

- Glass: physically based clear material, clean silhouette, restrained roughness and a visible rim; test refraction against both dark and light composites.
- Liquid: one coherent golden-peach material across strands, jug and glass, with slightly darker edge thickness and a soft internal scattering cue.
- Ribbon: broad, smooth and glossy with deliberate folds; avoid a thin noodle-like stream until the pour stage.
- Fruit: realistic cut surfaces, wet highlights and varied scale. Keep texture detail subordinate to silhouette at scroll distance.
- Preview the transparent render over charcoal, warm ivory and the intended site background before approving the look.

## Final hero frame

The jug has left the frame. The glass sits lower-left/centre, filled roughly 70–75% with the golden-peach drink. A calm surface, a few fine bubbles, soft condensation and one small lime wheel communicate refreshment. The upper-right remains open, allowing the page to place copy or the next scroll cue there. This frame should be strong enough to hold indefinitely.

## Practical production recommendation

1. Build the master in Blender Cycles at 24fps (18 seconds = 432 frames). Use hand-animated curve/mesh deformation for the fruit-to-ribbon transformation because it is more art-directable than trying to simulate every ingredient.
2. Use a small Mantaflow liquid test only for the final glass impact. If it does not materially improve the read, keep the pour as controlled geometry and spend the budget on glass, refraction and condensation.
3. Render a high-quality RGBA EXR/PNG master with Film Transparent, while keeping hidden studio reflection cards for believable glass highlights. A true alpha render does not automatically preserve useful glass/refraction when composited over arbitrary backgrounds.
4. For the website, the most reliable first delivery is a colour-managed video/sequence composited against the chosen site background. If true transparency is mandatory, test WebM alpha and a reduced RGBA frame sequence on the actual target browsers; keep a matte fallback and a static hero frame.
5. Create three web crops from the same camera: desktop 16:9, portrait 4:5 and mobile 9:16. Keep the glass and jug inside the protected crop rather than solving mobile with a second animation.

## Decisions to confirm before keyframe work

The current defaults are golden-peach liquid, true-alpha testing plus a matte fallback, and a small lime-wheel garnish. The only decisions that materially change the next pass are:

1. Must the final website composition remain genuinely transparent, or is a fixed site-background composite acceptable if it gives the glass a more convincing result?
2. Is golden-peach still the right placeholder for the first look-development pass?
3. Should the lime wheel remain in the final hero, or should the drink finish completely ungarnished?
