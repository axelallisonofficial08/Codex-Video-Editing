---
name: video-content-analysis
description: Analyze supplied footage and audio to find usable moments, highlights, pauses, filler words, and edit points before making a video cut. Use for content-led editing and selects, not for replacing a requested performance with a highlights reel.
---

# Video content analysis

Build an evidence-based timeline before cutting. Capture source timecodes, shot boundaries, speech or lyric beats, visible actions, and audio changes. Use transcript or ASR when speech exists, but inspect the actual frames and listen to uncertain segments; text alone misses gestures and visual beats.

Mark candidate highlights and removable material with start/end times, a short reason, and confidence. Distinguish deliberate pauses, reaction shots, music holds, and breathing space from genuine dead time. Check continuity on both sides of any proposed cut.

For reference-matched animation, use the analysis to identify gesture and expression peaks while retaining the reference duration and order unless the user asks for a shorter edit. In the Hu Tao project, compare the original MP4 with `reference_halfsec/` and inspect fast motions more densely than the half-second samples.
