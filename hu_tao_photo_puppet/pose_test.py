import bpy, math
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent
s=bpy.context.scene
s.render.engine='BLENDER_EEVEE'; s.render.resolution_x=848; s.render.resolution_y=478
s.world.color=(.35,.3,.28)
cd=bpy.data.cameras.new('cam'); cam=bpy.data.objects.new('cam',cd); s.collection.objects.link(cam)
cam.location=(0,-4,1.16); cam.rotation_euler=(Vector((0,0,1.16))-cam.location).to_track_quat('-Z','Y').to_euler(); cd.type='ORTHO'; cd.ortho_scale=1.45; s.camera=cam
for x in (-2,2):
 d=bpy.data.lights.new('area','AREA'); d.energy=650; d.size=4; o=bpy.data.objects.new('area',d); s.collection.objects.link(o); o.location=(x,-3,4); o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
a=bpy.data.objects['胡桃_arm']
for n,v in [('腕.L',-.7),('腕.R',.7)]:
 b=a.pose.bones[n]; b.rotation_mode='XYZ'; b.rotation_euler.z=v
for n,v in [('ひじ.L',-.55),('ひじ.R',.55)]:
 b=a.pose.bones[n]; b.rotation_mode='XYZ'; b.rotation_euler.z=v
s.render.filepath=str(P/'pose_test.png'); bpy.ops.render.render(write_still=True)
