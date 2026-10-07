import bpy
from pathlib import Path
from mathutils import Vector

HERE=Path(__file__).resolve().parent
scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=848
scene.render.resolution_y=478
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='Standard'
scene.view_settings.look='Medium High Contrast'
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.5,0.35,0.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=0.8
cam_data=bpy.data.cameras.new('front camera')
cam=bpy.data.objects.new('front camera',cam_data)
bpy.context.collection.objects.link(cam)
cam.location=(0,-4,1.20)
cam.rotation_euler=(Vector((0,0,1.20))-cam.location).to_track_quat('-Z','Y').to_euler()
cam_data.type='ORTHO'
cam_data.ortho_scale=1.25
scene.camera=cam
for name,pos,power,size in [('key',(-2,-3,4),500,4),('fill',(2,-2,3),250,3)]:
    d=bpy.data.lights.new(name,'AREA')
    d.energy=power
    d.size=size
    o=bpy.data.objects.new(name,d)
    bpy.context.collection.objects.link(o)
    o.location=pos
    o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
scene.render.filepath=str(HERE/'official_model_test.png')
bpy.ops.render.render(write_still=True)
