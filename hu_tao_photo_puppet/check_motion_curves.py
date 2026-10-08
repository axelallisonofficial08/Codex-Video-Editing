"""List the largest frame-to-frame changes in the polished performance."""
import bpy
from math import sqrt, pi

s = bpy.context.scene
def fcmap(obj, path):
    a = obj.animation_data.action
    return {c.array_index:c for l in a.layers for strip in l.strips
            for bag in strip.channelbags for c in bag.fcurves if c.data_path == path}

def changes(name, path, multiplier=1):
    obj = bpy.data.objects[name]
    fc = fcmap(obj, path)
    result = []
    prev = None
    for f in range(s.frame_start, s.frame_end+1):
        pos = tuple(fc[i].evaluate(f) for i in sorted(fc))
        if prev is not None:
            delta = sqrt(sum((a-b)**2 for a,b in zip(pos,prev)))*multiplier
            result.append((round(delta,3), f, round((f-1)/s.render.fps,3)))
        prev=pos
    print(name,path,'MAX_DELTA',sorted(result,reverse=True)[:14])

for side in ('L','R'):
    changes('Wrist IK '+side,'location')
changes('胡桃_arm','pose.bones["頭"].rotation_euler',180/pi)
