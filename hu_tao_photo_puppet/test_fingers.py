exec(open(__file__.replace('test_fingers.py','test_ik.py'),encoding='utf8').read().replace("s.render.filepath=str(p/'test_ik.png'); bpy.ops.render.render(write_still=True)",""))
import math
for axis in ('X','Y','Z'):
    for n in ('人指１.L','人指２.L','中指１.L','中指２.L','薬指１.L','薬指２.L','小指１.L','小指２.L'):
        b=a.pose.bones[n]; b.rotation_mode='XYZ'; b.rotation_euler=(0,0,0); setattr(b.rotation_euler,axis.lower(),math.radians(50))
    s.render.filepath=str(p/f'finger_{axis}.png'); bpy.ops.render.render(write_still=True)
