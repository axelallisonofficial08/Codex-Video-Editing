# Hu Tao character study

This is an editable Blender character study created from the supplied front-view JPEG. It is a handmade interpretation, not the original Genshin Impact mesh or the model from a prior animation.

## Files

- `hutao_character_study.blend` — editable model, simple animation controls, camera, lighting, and white stage.
- `build_hutao.py` — Blender Python script that rebuilds the project and renders `preview.png`.
- `preview.png` — first-frame render.

The portable Blender executable is in `../tools/blender-5.2.2-windows-x64/blender.exe` after this folder is moved into its own project.

## Rebuild

From PowerShell in this folder:

```powershell
& '..\tools\blender-5.2.2-windows-x64\blender.exe' -b -t 4 --python '.\build_hutao.py'
```

## Finished performance

- `Hu_Tao_Falling_in_Love.mp4` — 37.78-second, 1520 × 1080 H.264 video with the reference clip's AAC audio.
- `hutao_performance.blend` — editable Blender scene with character, camera, background, title cards, and performance keyframes.
- `animate_performance.py` — builds and renders the complete performance from `hutao_character_study.blend`.
- `frames/` — rendered 760 × 540 image sequence used for the final encode.

The rig has independent head and arm controls plus a mouth control. The performance is a handmade stylized interpretation of the supplied Hu Tao image, animated to follow the reference video's dark opening, warm close shots, and bright final section. The final video was upscaled from the rendered image sequence and uses the supplied reference audio.

To re-render the sequence from PowerShell in this folder:

```powershell
& '..\tools\blender-5.2.2-windows-x64\blender.exe' -b '.\hutao_character_study.blend' -t 4 --python '.\animate_performance.py'
```
