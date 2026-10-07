import bpy
from pathlib import Path
s=bpy.context.scene; p=Path(__file__).resolve().parent
for t in (2,5.5,8.5,10,13.5,15.5,18.5,20.5,22.5,24.5,28.5,31.5,35.5):
    s.frame_set(round(t*s.render.fps)+1)
    s.render.filepath=str(p/f'refined_check_{t:04.1f}.png')
    bpy.ops.render.render(write_still=True)
