# Inspiration filmstrip

Six original drink-recipe inspiration images were created with the built-in image generation tool. They are concept photographs, not screenshots of real social-media accounts. Source PNGs and 600px-wide WebP delivery images are saved in `panels/reels/`.

The current filmstrip has 24 frames, using all six images in a repeating sequence. It enters from the right, travels left in 2.2 seconds with `cubic-bezier(.65,0,.35,1)` ease-in-out, then settles. The movement is triggered once on viewport entry and is independent of scrolling. Refresh the page to replay it. Reduced-motion mode shows the settled strip immediately.

The cobalt paper, ragged edges and transparent sprocket holes are native HTML/CSS/SVG. `panels/film-paper-mask.svg` provides the torn silhouette and cut-out holes. The strip is clipped horizontally, with sufficient vertical space for the visible frames. On desktop it occupies the existing paper gap; on smaller screens it takes its own row to avoid the text.

The earlier ingredient trail is preserved in the `#saved-ingredient-trail` template in `index.html`, along with its assets, CSS and `ingredient-trail.js`. That script is not loaded by the current page. Its placement selectors will need adapting when the new section is chosen.

## Source files

- `panels/reels/reel-citrus.png` and `panels/reels/reel-citrus.webp`, from `exec-c66c9e0f-624e-4e22-9506-1f093278f033.png`.
- `panels/reels/reel-green.png` and `panels/reels/reel-green.webp`, from `exec-88dde969-ff11-4be0-9841-1d1f0b5f207b.png`.
- `panels/reels/reel-berry.png` and `panels/reels/reel-berry.webp`, from `exec-b6971be8-7762-4d6c-b0b9-a8ebcc162efe.png`.
- `panels/reels/reel-tropical.png` and `panels/reels/reel-tropical.webp`, from `exec-28ce3979-f579-4b9c-8a10-eac560509c93.png`.
- `panels/reels/reel-ginger.png` and `panels/reels/reel-ginger.webp`, from `exec-b0d2f957-8a8c-4be7-b31c-0f015128665e.png`.
- `panels/reels/reel-watermelon.png` and `panels/reels/reel-watermelon.webp`, from `exec-baa62b3e-fded-454d-aa49-7b9014ee5a5b.png`.

## Full generation prompts

### reel-citrus

Subject: a short clear glass of vivid orange citrus juice and sparkling ice, fresh orange slices and mint leaves. One hand gently placing a fresh orange wedge onto the glass rim, recipe-creator viewpoint. Use case: photorealistic-natural. Asset type: a full-bleed PORTRAIT drink-recipe inspiration image for a camera-film strip on a premium JuiceBuilder website. Vertical 9:16 reel-style framing. A richly coloured, convincing editorial food photograph with subtle tactile printed grain, natural fresh ingredients, soft directional studio light, warm cream paper-toned surroundings and a small cobalt-blue linen accent. One clear hero glass, fully inside the central 70% of the composition, with no part of the glass cut off. Strong simple composition that reads at thumbnail size, appetising real texture, clean daylight highlights. No lettering, labels, logos, watermark, interface, border, filmstrip, collage panels or typography. A single complete photograph, not a contact sheet.

### reel-green

Subject: a tall clear glass of fresh bright green juice, a kiwi slice on the rim, green apple, cucumber ribbons and a small lime half arranged loosely nearby. Refined overhead three-quarter recipe photograph. Use case: photorealistic-natural. Asset type: a full-bleed PORTRAIT drink-recipe inspiration image for a camera-film strip on a premium JuiceBuilder website. Vertical 9:16 reel-style framing. A richly coloured, convincing editorial food photograph with subtle tactile printed grain, natural fresh ingredients, soft directional studio light, warm cream paper-toned surroundings and a small cobalt-blue linen accent. One clear hero glass, fully inside the central 70% of the composition, with no part of the glass cut off. Strong simple composition that reads at thumbnail size, appetising real texture, clean daylight highlights. No lettering, labels, logos, watermark, interface, border, filmstrip, collage panels or typography. A single complete photograph, not a contact sheet.

### reel-berry

Subject: a chilled clear glass of deep crimson berry juice with ice, raspberries, blueberries and a tiny sprig of fresh mint, a few scattered berries nearby, a small ribbed glass carafe in the far soft-focus background. Use case: photorealistic-natural. Asset type: a full-bleed PORTRAIT drink-recipe inspiration image for a camera-film strip on a premium JuiceBuilder website. Vertical 9:16 reel-style framing. A richly coloured, convincing editorial food photograph with subtle tactile printed grain, natural fresh ingredients, soft directional studio light, warm cream paper-toned surroundings and a small cobalt-blue linen accent. One clear hero glass, fully inside the central 70% of the composition, with no part of the glass cut off. Strong simple composition that reads at thumbnail size, appetising real texture, clean daylight highlights. No lettering, labels, logos, watermark, interface, border, filmstrip, collage panels or typography. A single complete photograph, not a contact sheet.

### reel-tropical

Subject: a clear glass filled with sunny golden pineapple juice and ice, a pineapple wedge and lime wheel on its rim, a cropped pineapple crown softly out of focus behind it, inviting tropical drink recipe scene. Use case: photorealistic-natural. Asset type: a full-bleed PORTRAIT drink-recipe inspiration image for a camera-film strip on a premium JuiceBuilder website. Vertical 9:16 reel-style framing. A richly coloured, convincing editorial food photograph with subtle tactile printed grain, natural fresh ingredients, soft directional studio light, warm cream paper-toned surroundings and a small cobalt-blue linen accent. One clear hero glass, fully inside the central 70% of the composition, with no part of the glass cut off. Strong simple composition that reads at thumbnail size, appetising real texture, clean daylight highlights. No lettering, labels, logos, watermark, interface, border, filmstrip, collage panels or typography. A single complete photograph, not a contact sheet.

### reel-ginger

Subject: one clear glass of fresh pale golden lemon-and-ginger juice with tiny bubbles, a thin lemon wheel, sliced ginger root and a small metal juicing tool nearby, close-up recipe preparation moment. Use case: photorealistic-natural. Asset type: a full-bleed PORTRAIT drink-recipe inspiration image for a camera-film strip on a premium JuiceBuilder website. Vertical 9:16 reel-style framing. A richly coloured, convincing editorial food photograph with subtle tactile printed grain, natural fresh ingredients, soft directional studio light, warm cream paper-toned surroundings and a small cobalt-blue linen accent. One clear hero glass, fully inside the central 70% of the composition, with no part of the glass cut off. Strong simple composition that reads at thumbnail size, appetising real texture, clean daylight highlights. No lettering, labels, logos, watermark, interface, border, filmstrip, collage panels or typography. A single complete photograph, not a contact sheet.

### reel-watermelon

Subject: a clear glass of coral-pink watermelon juice and clear ice, garnished with a slim watermelon triangle and green mint, a small lime wedge nearby, one hand pouring the last small stream of pink juice from a simple unlabelled glass jug. Use case: photorealistic-natural. Asset type: a full-bleed PORTRAIT drink-recipe inspiration image for a camera-film strip on a premium JuiceBuilder website. Vertical 9:16 reel-style framing. A richly coloured, convincing editorial food photograph with subtle tactile printed grain, natural fresh ingredients, soft directional studio light, warm cream paper-toned surroundings and a small cobalt-blue linen accent. One clear hero glass, fully inside the central 70% of the composition, with no part of the glass cut off. Strong simple composition that reads at thumbnail size, appetising real texture, clean daylight highlights. No lettering, labels, logos, watermark, interface, border, filmstrip, collage panels or typography. A single complete photograph, not a contact sheet.

