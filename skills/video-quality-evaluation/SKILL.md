---
name: video-quality-evaluation
description: Evaluate an edited or generated video against its reference and brief using structured visual, motion, audio, and technical checks, then drive targeted revisions.
---

# Video quality evaluation

Build a rubric from the user's actual goal: timing, identity consistency, pose and gesture match, scene continuity, framing, facial expression, audio sync, and delivery format. Compare aligned reference and output frames at cuts and action peaks, plus continuous playback of problem intervals.

Use image-text similarity, embeddings such as SigLIP, optical flow, frame differences, or model judgments only when those tools are available and the measurement addresses a specific question. Metrics can flag anomalies but cannot alone judge whether a gesture feels correct or a cut is intentional. Record timestamps and the visible evidence for each finding.

Revise the highest-impact problems, rerender the affected interval, and compare again. Stop optional evaluation once the remaining risk is understood and the deliverable meets the brief. For the Hu Tao performance, prioritize hand paths, head timing, facial beats, background/camera changes, and the original soundtrack.
