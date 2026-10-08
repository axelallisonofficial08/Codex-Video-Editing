import bpy
from pathlib import Path

s = bpy.context.scene
p = Path(__file__).resolve().parent
for t in (5.5, 9.5, 13.5, 15.5, 20.5, 28.5, 35.0):
    s.frame_set(round(t*s.render.fps)+1)
    s.render.filepath = str(p / f'polished_check_{t:04.1f}.png')
    bpy.ops.render.render(write_still=True)
    print('CHECK', t, s.render.filepath)
