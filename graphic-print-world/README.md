# Graphic Print World preview

An isolated scroll-driven JuiceBuilder concept. It preserves the earlier JuiceBuilder prototypes.

## Four Kling-film direction

The new four-chapter film layout is at <http://127.0.0.1:3002/kling-four/>. The production pack, five handoff stills and four copy-ready Kling prompts are in [`kling-four/START-HERE.md`](./kling-four/START-HERE.md). This preview shows stills until approved video exports are added. The layered study below remains available for comparison.

## View locally

The current **layered scroll preview** is served at <http://127.0.0.1:3002/>. The earlier still-image animatic remains at <http://127.0.0.1:3002/animatic.html>. To start the server again later from PowerShell:

```powershell
python -m http.server 3002 --directory 'C:\Coding\Applications\Ideas\juicebuilder\graphic-print-world'
```

Then open <http://127.0.0.1:3002/>.

## Files

- `STORYBOARD.md`: four-scene story and motion notes.
- `01-idea.png` to `05-final-bottle.png`: generated concept keyframes.
- `layers/*.png`: transparent source cutouts for the profile, fruit, person, hands and bottle.
- `layers/*.webp`: compressed runtime versions of those cutouts (about 2.5 MB total instead of more than 14 MB of PNGs).
- `index.html`, `layered.css`, `layered.js`, `style.css`: the current layered scroll preview.
- `animatic.html`, `app.js`: the earlier still-image crossfade preview.

The current version animates independent paper cutouts, print proofs, a rising ink fill, a label, an uncapped sip and the bottle-only end frame directly from scroll position. Text stays in HTML and a reduced-motion setting changes the sequence to discrete states. This is still a **design study**: the bottle-fill silhouette and label application need the same final art finish as the textured cutouts before release.
