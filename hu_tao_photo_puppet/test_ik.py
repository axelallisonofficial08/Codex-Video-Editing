import bpy
from pathlib import Path
from mathutils import Vector
p=Path(__file__).resolve().parent
s=bpy.context.scene
s.render.engine='BLENDER_EEVEE'; s.render.resolution_x=848; s.render.resolution_y=478
a=bpy.data.objects['胡桃_arm']
for side,xyz in [('L',(.25,-.18,1.37)),('R',(-.10,-.20,1.10))]:
    target=bpy.data.objects.new('target.'+side,None); s.collection.objects.link(target); target.location=xyz
    c=a.pose.bones['手首.'+side].constraints.new('IK'); c.target=target; c.chain_count=3; c.use_stretch=False
cd=bpy.data.cameras.new('cam'); cam=bpy.data.objects.new('cam',cd); s.collection.objects.link(cam)
cam.location=(0,-4,1.30); cam.rotation_euler=(Vector((0,0,1.30))-cam.location).to_track_quat('-Z','Y').to_euler(); cd.type='ORTHO'; cd.ortho_scale=1.0; s.camera=cam
for x in (-2,2):
 d=bpy.data.lights.new('light','AREA'); d.energy=600; d.size=4; o=bpy.data.objects.new('light',d); s.collection.objects.link(o); o.location=(x,-3,4); o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler()
s.render.filepath=str(p/'test_ik.png'); bpy.ops.render.render(write_still=True)
