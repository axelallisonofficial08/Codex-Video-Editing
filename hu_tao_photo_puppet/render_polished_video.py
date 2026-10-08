"""Render the polished Blender performance to numbered frames for FFmpeg."""
import bpy
from pathlib import Path

p = Path(__file__).resolve().parent
s = bpy.context.scene
s.frame_start = 1
s.frame_end = 907
s.render.fps = 24
s.render.resolution_x = 1280
s.render.resolution_y = 720
s.render.resolution_percentage = 100
s.render.image_settings.file_format = 'PNG'
s.render.image_settings.color_mode = 'RGB'
(p/'polished_frames').mkdir(exist_ok=True)
s.render.filepath = str(p/'polished_frames'/'frame_')
bpy.ops.render.render(animation=True)
print('FRAMES', s.render.filepath)
