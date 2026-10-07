# Codex Video Editing — Hu Tao performance

This repository backs up the video editing work, reference breakdowns, Blender scripts, renders, and working frames for the Hu Tao performance project.

## Contents

- `source_media/` — the three files supplied for the project: the full performance reference, the Hu Tao image, and the ten-second example.
- `hu_tao_photo_puppet/reference_halfsec/` — reference frames sampled every half second from the full video.
- `hu_tao_photo_puppet/reference_sheet_*.jpg` — contact sheets used to study poses and shot timing.
- `hu_tao_photo_puppet/white_stage_frames/` — individual frames of the white-stage render.
- `hu_tao_photo_puppet/Hu_Tao_Refined.mp4` — the 37.79-second hand-keyed render with the original soundtrack.
- `hu_tao_photo_puppet/Hu_Tao_White_Stage_1080p.mp4` — the later white-stage export.
- `hu_tao_photo_puppet/*.py` — scripts for character preparation, animation, backplates, and reference review.
- `hutao_blender/` — the earlier handmade Blender study and its project files.
- `skills/` — reusable Codex skills for Blender performance matching and agentic video editing, analysis, localization, quality review, and delivery metadata.

The other previews, logs, stills, frame checks, and intermediate media in these folders are retained so the work can be reviewed in full.

## Rebuilding

The scripts were developed with Blender 5.2.2 on Windows. Install Blender separately; the 1.3 GB portable Blender installation and installer archive are tooling, so they are not stored in this repository. The `hu_tao_photo_puppet/addons/` directory contains the MMD import extension used during development.

Some scripts use fonts from `C:/Windows/Fonts`. The original media is in `source_media/`. To recreate a render that uses the official character rig, obtain the model from its original publisher, import it locally, and run the relevant animation script from `hu_tao_photo_puppet/` with Blender.

## Model distribution restriction

The official Hu Tao PMX model's readme prohibits redistribution. Consequently, the PMX archive, extracted model files, and Blender projects containing the complete imported model are kept only in the local workspace and are **not included in this public repository**. Rendered videos, working frames, reference breakdowns, and scripts are included. Please keep this restriction in mind before publishing any additional project files.
