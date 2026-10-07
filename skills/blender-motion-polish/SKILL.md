---
name: blender-motion-polish
description: Improve the smoothness of an existing Blender character performance while preserving pose timing and shot cuts. Use for jerky hands, head tilts, body motion, IK pops, and uneven keyframe curves.
---

# Blender motion polish

Smoothness means coherent timing and believable motion paths, not simply more frames or blanket curve smoothing.

1. Inspect the rendered motion and locate the exact frames of pops, sudden stops, hand path corners, and unwanted drift. Identify whether the cause is a pose key, F-curve, IK solver, constraint, or cut.
2. Preserve intentional gesture accents and the times of reference poses. Add in-between poses where a straight interpolation changes the silhouette or sends a hand through the body. Keep hand paths as arcs when the reference supports them.
3. Use Bezier curves with Auto Clamped handles for ordinary continuous channels, then adjust individual handles where acceleration still looks wrong. Blender's Auto handles can overshoot. Use linear or constant interpolation for cuts, visibility, and other discontinuities.
4. For IK arms, inspect elbows and shoulder deformation over the whole path. Stabilize pole direction or change solver settings only when a real flip occurs. Verify the wrist does not stretch past the arm's reach.
5. Add restrained overlap to hair, sleeves, and torso only after the primary gesture is matched. Keep contact poses fixed; secondary motion must not pull hands off the face or desk.
6. Render short checks around each repaired moment at delivery frame rate. Compare the same timestamps before a full export.

In this project, `animate_refined_hutao.py` creates wrist IK targets and keyed head rotations. Its camera and background visibility keys also contain hard shot boundaries; never smooth those blindly. If replacing a prior refined video, verify the new render before removing the old one, consistent with the user's storage preference.
