# Hu Tao JPEG puppet performance

## White-stage version (2026-10-07)

- `Hu_Tao_White_Stage_1080p.mp4`: 42.72-second video, 1920 × 1080, 18 fps. The white-background opening, camera push, red curtains, and song performance are present. The song audio begins at 9 seconds, using the singing section of the supplied reference video.
- `Hu_Tao_White_Stage.blend`: editable scene with the existing Hu Tao model and animation, white stage, curtains, camera, lyric presentation, and song audio strip.
- `make_white_stage.py` and `add_song_to_blend.py`: source scripts for the updated scene.

The two requested opening dialogue lines have keyed mouth movement but **no audible speech**. Local speech synthesis failed, and the connected voice service had no available credits. Mouth shapes during the song follow audio loudness and keyframed acting rather than phoneme-level alignment. The existing model also has visible hand/finger artifacts in some close shots. The 1080p file is upscaled from 1280 × 720 rendered frames.

This is a fresh Blender project built from the supplied JPEG. It does not load or reuse the earlier handmade Hu Tao Blender character. The character's visible pixels come from `original_reference.jpeg`; Blender deforms a subdivided image mesh to animate them.

## Deliverables

- `Hu_Tao_JPEG_Animated.mp4` — finished 37.78-second, 1520 × 1080 H.264 video with the reference video's audio.
- `hu_tao_photo_performance.blend` — editable Blender scene with the image puppet, shape-key acting, mouth motion, eye blinks, background, titles, and camera.
- `character_cutout.png` — transparent cutout made from the supplied JPEG.
- `prepare_photo.py` and `animate_photo.py` — scripts used to build the assets and Blender scene.

The Blender scene packs the cutout image. The original JPEG is included separately for provenance and rebuilding.

The source character occupies only about 250 pixels of width in the JPEG, so close shots are softer than a high-resolution illustration. The performance follows the reference video's dark opening, warm first half, bright second half, and approximate gesture rhythm, while preserving the pictured character.
