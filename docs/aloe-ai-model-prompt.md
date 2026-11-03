# Aloe Vera single-leaf asset prompt

Use this with an image-to-3D tool such as Tripo. Start from the user-provided aloe reference image. Choose a high-detail output with PBR textures; export GLB or FBX for Blender.

> A single mature Aloe vera leaf, detached from the plant. One long, thick, fleshy lance-shaped leaf with a broad cut base, a gently tapering pointed tip, a natural shallow cup through its length, subtle longitudinal ridges, tiny irregular pale-green flecks, and small realistic serrations along both margins. The freshly cut base must be visible as a clean cross-section with a thin darker rind surrounding moist translucent pale-green gel. Botanical proportions and asymmetry; photoreal natural surface, no stylisation. Model the outer rind and gel face as separate material regions if supported. Isolated object, centred, neutral reference lighting. No plant rosette, no pot, no soil, no roots, no table, no labels, no text, no watermark.

## Check the generated model before using it

- Confirm it is one leaf rather than a potted aloe plant.
- Inspect the base cross-section and both serrated edges from multiple views.
- Check the mesh and texture for pinching, melted spots, broken tips and stretched pixels.
- Preserve the supplied reference image with the asset and check the generation service's commercial-use terms before launch.

The model can then replace the procedural leaf in `blender/create_aloe_pilot.py`; Blender remains the place to correct its shape, materials, camera, lighting and animation.
