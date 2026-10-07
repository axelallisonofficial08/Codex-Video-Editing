---
name: blender-motion-qa
description: Review a Blender character animation for motion pops, reference timing errors, camera cuts, facial continuity, and export defects before delivering a video.
---

# Blender motion QA

Review the actual rendered frames and audio, not only the Blender viewport.

1. Compare reference and output at matched timestamps around every camera cut, gesture peak, hand contact, facial change, and the opening and ending.
2. Play each problem interval continuously at normal speed, then frame by frame. Look for wrist or elbow flips, head snapping, hand penetration, drifting contact, frozen holds, and unwanted camera easing.
3. Use frame-difference or landmark plots to locate abrupt changes, but judge flagged frames visually: cuts and fast intentional gestures are valid discontinuities.
4. Confirm duration, frame rate, resolution, soundtrack sync, black frames, and final file playability. A higher frame rate cannot repair badly timed source keys.
5. Keep the previous accepted render until the new one passes review; then apply the user's instruction to remove the superseded video and conserve space.

In the Hu Tao project, consult `reference_halfsec/`, `reference_sheet_*.jpg`, the latest render, and short check-render scripts. The reference is the movement target; smoothness must not erase its gesture accents.
