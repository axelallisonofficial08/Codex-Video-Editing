---
name: blender-face-performance
description: Match a character's gaze, blink, mouth, and facial expressions to a video performance in Blender. Use when body animation exists but the face looks static, off beat, or unlike the reference.
---

# Blender face performance

Read expressions from the reference at gesture peaks and lyric or speech beats. Map those observations to the rig's actual shape keys or facial bones; inspect the rig before assuming conventional morph names.

- Place gaze shifts slightly ahead of, or with, head turns according to the reference. Keep the eyes aimed deliberately between shifts.
- Give blinks an observable close and reopen phase. Avoid equally spaced automatic blinks when the reference has distinct expression timing.
- Make mouth shapes follow audio or reference mouth openings. Preserve quiet moments and closed-mouth poses rather than oscillating constantly.
- Check combined morphs for clipping, overclosed eyes, and expressions that accidentally cancel each other.
- Review at native delivery size; subtle morphs that look useful in a close viewport may disappear in a full-body shot.

For the Hu Tao rig, inspect the shape key names in the imported local model and the keyed values in `animate_refined_hutao.py`. Do not publish the model or Blender files containing it.
