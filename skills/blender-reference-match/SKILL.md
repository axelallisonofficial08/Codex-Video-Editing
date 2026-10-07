---
name: blender-reference-match
description: Recreate a supplied performance in Blender by measuring shot cuts, body poses, hand paths, head motion, and timing from video reference. Use for reference-matched character animation, not generic animation from a text prompt.
---

# Blender reference match

Treat a rendered reference video as visual evidence, not as animation data. Match the observable result at the same timestamps.

1. Record the reference's frame rate, duration, shot cuts, camera framing, backgrounds, and visible pose landmarks. Use denser samples where hands, head, or face move quickly; half-second samples alone miss short gestures.
2. For each shot, note screen-space head center, shoulders, elbows, wrists, and any hand contact. Include expression and gaze changes. Mark visibility limits instead of guessing hidden joints.
3. Block the Blender rig at the same times. Check camera and character scale before polishing motion; camera errors can look like pose errors.
4. Compare aligned reference and Blender frames at every cut and gesture peak. Correct timing and silhouettes first, then refine arcs and expression.
5. Preserve shot changes as cuts. Do not interpolate camera or visibility through a cut unless the reference shows a transition.

For the Hu Tao project, inspect `hu_tao_photo_puppet/reference_halfsec/`, the contact sheets, and `animate_refined_hutao.py`. These are guides; revisit the source MP4 near fast gestures. The official model is local only because its readme prohibits redistribution.
