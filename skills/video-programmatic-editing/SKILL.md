---
name: video-programmatic-editing
description: Assemble and render video reproducibly with available command-line or code tools such as FFmpeg, Remotion, or Blender. Use for timed cuts, overlays, compositing, format conversion, and batch exports.
---

# Video programmatic editing

Probe each source's duration, frame rate, resolution, pixel format, and audio streams. Select the simplest available tool that can deliver the requested composition. FFmpeg suits cuts, transcodes, filters, and muxing; Remotion suits code-driven layouts; Blender suits 3D animation. Verify tool versions and supported options before scripting.

Represent the edit as explicit timecoded inputs and transformations. Preserve source audio sync and expected aspect ratio. For cuts, map source and output timestamps; for overlays, render a short composite check before a full export. Keep intermediate files only while needed for review or recovery.

After rendering, probe the output and play representative intervals including cuts and the ending. Reconcile actual duration, frame count, resolution, audio, and file playability with the brief. In this project's Blender workflow, validate a replacement render before deleting the previous version to conserve space.
