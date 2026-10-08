"""Retime a 24 fps Blender performance to 30 fps and render PNG frames."""
import bpy
import sys
from pathlib import Path

scene = bpy.context.scene
root = Path(__file__).resolve().parent
factor = 30 / 24

for action in bpy.data.actions:
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    for key in curve.keyframe_points:
                        key.co.x = 1 + (key.co.x - 1) * factor
                        key.handle_left.x = 1 + (key.handle_left.x - 1) * factor
                        key.handle_right.x = 1 + (key.handle_right.x - 1) * factor
                    curve.update()

scene.render.fps = 30
scene.render.fps_base = 1
scene.frame_start = 1
scene.frame_end = 1134
scene.render.resolution_x = 1520
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(root / 'natural_frames' / 'frame_')
scene.render.use_file_extension = True
scene.render.film_transparent = False
scene.render.image_settings.color_mode = 'RGB'

bpy.ops.wm.save_as_mainfile(filepath=str(root / 'Hu_Tao_Reference_Matched.blend'))
if '--desk-only' in sys.argv:
    scene.frame_start = 372
    scene.frame_end = 496
bpy.ops.render.render(animation=True)
