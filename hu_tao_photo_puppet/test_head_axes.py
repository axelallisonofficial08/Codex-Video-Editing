import bpy,math
from pathlib import Path
from mathutils import Vector
p=Path(__file__).resolve().parent; s=bpy.context.scene
s.render.engine='BLENDER_EEVEE'; s.render.resolution_x=424; s.render.resolution_y=478
a=bpy.data.objects['胡桃_arm']; head=a.pose.bones['頭']; head.rotation_mode='XYZ'
cd=bpy.data.cameras.new('cam'); cam=bpy.data.objects.new('cam',cd); s.collection.objects.link(cam)
cam.location=(0,-4,1.32); cam.rotation_euler=(Vector((0,0,1.32))-cam.location).to_track_quat('-Z','Y').to_euler(); cd.type='ORTHO'; cd.ortho_scale=.55; s.camera=cam
for x in (-2,2):
 d=bpy.data.lights.new('light','AREA'); d.energy=600; d.size=4; o=bpy.data.objects.new('light',d); s.collection.objects.link(o); o.location=(x,-3,4); o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler()
for name,xyz in [('neutral',(0,0,0)),('xpos',(20,0,0)),('ypos',(0,20,0)),('zpos',(0,0,20))]:
 head.rotation_euler=tuple(math.radians(v) for v in xyz)
 s.render.filepath=str(p/f'head_{name}.png'); bpy.ops.render.render(write_still=True)
