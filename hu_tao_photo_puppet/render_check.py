import bpy
from pathlib import Path
s=bpy.context.scene
p=Path(__file__).resolve().parent
for t in (2,6,9,14,22,27,33):
    s.frame_set(round(t*s.render.fps)+1)
    s.render.filepath=str(p/f'check_{t:02}.png')
    bpy.ops.render.render(write_still=True)
