import bpy
import math
from pathlib import Path
from mathutils import Vector

# A hand-built, editable character study based on the supplied front-view image.
# It is an interpretation, not an extracted or original game mesh.

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def mat(name, color, roughness=0.7):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*color, 1)
    bs.inputs['Roughness'].default_value = roughness
    return m

skin = mat('warm pale skin', (0.91, 0.79, 0.72))
hair = mat('deep plum brown hair', (0.18, 0.115, 0.14))
hair_light = mat('hair highlights', (0.28, 0.18, 0.20))
coat = mat('dark brown coat', (0.105, 0.07, 0.075))
coat_trim = mat('coat embroidery bronze', (0.45, 0.31, 0.22))
black = mat('soft black', (0.035, 0.025, 0.03))
red = mat('red collar and tassels', (0.64, 0.10, 0.075))
gold = mat('muted gold', (0.74, 0.59, 0.31), 0.4)
white = mat('warm white', (0.95, 0.93, 0.88))
eye = mat('amber eyes', (0.62, 0.37, 0.16), 0.25)
eye_dark = mat('eye and mouth outline', (0.13, 0.075, 0.075))
sock = mat('gray socks', (0.64, 0.63, 0.61))
shoe = mat('black shoes', (0.075, 0.045, 0.045))

def sphere(name, loc, scale, material, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: o.data.materials.append(material)
    if parent:
        o.parent = parent
        o.matrix_parent_inverse = parent.matrix_world.inverted()
    for p in o.data.polygons: p.use_smooth = True
    return o

def cube(name, loc, scale, material, bevel=0, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod=o.modifiers.new('soft edges','BEVEL'); mod.width=bevel; mod.segments=2
        o.modifiers.new('weighted normals','WEIGHTED_NORMAL')
    if material: o.data.materials.append(material)
    if parent:
        o.parent=parent
        o.matrix_parent_inverse=parent.matrix_world.inverted()
    return o

def cone(name, loc, radius1, radius2, depth, material, parent=None, verts=24):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=radius1, radius2=radius2, depth=depth, location=loc)
    o=bpy.context.object; o.name=name
    if material: o.data.materials.append(material)
    if parent:
        o.parent=parent
        o.matrix_parent_inverse=parent.matrix_world.inverted()
    for p in o.data.polygons: p.use_smooth=True
    return o

def path(name, points, radius, material, parent=None):
    curve=bpy.data.curves.new(name,'CURVE'); curve.dimensions='3D'; curve.bevel_depth=radius; curve.bevel_resolution=3
    spline=curve.splines.new('BEZIER'); spline.bezier_points.add(len(points)-1)
    for bp, xyz in zip(spline.bezier_points, points):
        bp.co=xyz; bp.handle_left_type='AUTO'; bp.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,curve); bpy.context.collection.objects.link(o)
    o.data.materials.append(material)
    if parent:
        o.parent=parent
        o.matrix_parent_inverse=parent.matrix_world.inverted()
    return o

def empty(name, loc, parent=None):
    o=bpy.data.objects.new(name,None); bpy.context.collection.objects.link(o); o.location=loc
    if parent:
        o.parent=parent
        o.matrix_parent_inverse=parent.matrix_world.inverted()
    return o

root=empty('Character root: move entire Hu Tao study',(0,0,0))
torso=empty('Upper body rig',(0,0,1.6),root)
head_rig=empty('Head rig: tilt and turn',(0,0,2.18),torso)
left_arm=empty('Left arm rig: gesture',(-0.37,0,1.78),torso)
right_arm=empty('Right arm rig: gesture',(0.37,0,1.78),torso)

# Legs remain planted. The negative-Y side is the camera-facing side.
for side, x in [('L',-0.18),('R',0.18)]:
    sphere(side+' thigh',(x,0,0.88),(0.105,0.115,0.36),skin,root)
    sphere(side+' knee',(x,0,0.57),(0.102,0.105,0.11),skin,root)
    cone(side+' sock',(x,0,0.34),0.098,0.083,0.43,sock,root)
    cube(side+' red sock band',(x,-0.005,0.55),(0.22,0.20,0.055),red,0.018,root)
    sphere(side+' shoe',(x,-0.085,0.095),(0.125,0.22,0.085),shoe,root)
    path(side+' shoe gold loop',[(x-0.05,-0.23,0.13),(x,-0.24,0.17),(x+0.05,-0.23,0.13)],0.007,gold,root)

cube('black shorts',(0,0,1.11),(0.54,0.30,0.33),black,0.05,root)
for x in (-0.15,0.15): cube('short hem',(x,-0.02,0.98),(0.27,0.34,0.06),coat_trim,0.01,root)

# Coat body and split hanging tails.
sphere('coat fitted torso',(0,0,1.67),(0.34,0.215,0.49),coat,torso)
cone('coat peplum',(0,0,1.26),0.32,0.23,0.24,coat,torso)
for side,x in [('L',-0.28),('R',0.28)]:
    tail=cube(side+' long coat tail',(x,0.10,0.91),(0.26,0.14,0.77),coat,0.03,root)
    tail.rotation_euler[1]=(-1 if x<0 else 1)*0.06
    cube(side+' tail hem',(x,0.03,0.54),(0.25,0.16,0.045),coat_trim,0.01,root)
    path(side+' tail ornament',[(x,0.0,0.54),(x,0.0,0.40)],0.014,gold,root)
    sphere(side+' tassel',(x,0.0,0.37),(0.025,0.025,0.07),white,root)

# Central decorative fasteners and coat embroidery.
for z in (1.52,1.67,1.82):
    sphere('frog closure center',(0,-0.224,z),(0.055,0.014,0.023),black,torso)
    for sign in (-1,1):
        path('frog closure loop',[(0,-0.23,z),(sign*0.08,-0.23,z+0.027),(sign*0.11,-0.225,z)],0.010,coat_trim,torso)
for sign in (-1,1):
    path('coat gold line',[(sign*0.08,-0.226,1.35),(sign*0.10,-0.229,1.20),(sign*0.15,-0.225,1.12)],0.009,gold,torso)
    path('coat flourish',[(sign*0.20,-0.219,1.45),(sign*0.28,-0.18,1.40),(sign*0.31,-0.17,1.49)],0.012,coat_trim,torso)

# Arms with oversized sleeves and small pale hands.
for side,arm,x,s in [('L',left_arm,-0.37,-1),('R',right_arm,0.37,1)]:
    sleeve=sphere(side+' flowing sleeve',(x+s*0.12,0,1.48),(0.19,0.20,0.36),coat,arm)
    cuff=cube(side+' dark cuff',(x+s*0.17,-0.005,1.22),(0.33,0.27,0.16),black,0.025,arm)
    hand=sphere(side+' hand',(x+s*0.17,-0.005,1.09),(0.082,0.058,0.13),skin,arm)
    for i in range(4):
        xx=x+s*(0.12+i*0.035)
        sphere(side+' finger '+str(i),(xx,-0.045,1.01),(0.016,0.025,0.065),skin,arm)
    path(side+' sleeve embroidery',[(x+s*0.24,-0.21,1.40),(x+s*0.33,-0.18,1.36),(x+s*0.27,-0.20,1.31)],0.008,coat_trim,arm)

# Collar and red bow.
cone('neck',(0,0,2.02),0.10,0.10,0.20,skin,torso)
cube('white collar',(0,-0.18,2.01),(0.28,0.07,0.12),white,0.025,torso)
sphere('red neck bow',(0,-0.24,1.98),(0.18,0.035,0.075),red,torso)
sphere('gold bow clasp',(0,-0.278,1.98),(0.028,0.012,0.028),gold,torso)

# Hair back before face, with curved tapering locks.
sphere('back hair cap',(0,0.075,2.24),(0.32,0.22,0.35),hair,head_rig)
for x in (-0.27,-0.19,0.18,0.27):
    path('long back hair',[(x,0.12,2.27),(x*1.15,0.11,1.98),(x*1.28,0.11,1.55)],0.09,hair,head_rig)
face=sphere('face',(0,-0.035,2.22),(0.275,0.18,0.325),skin,head_rig)
for x in (-0.25,0.25):
    path('face framing hair',[(x*0.72,-0.13,2.48),(x,-0.12,2.16),(x*1.10,-0.10,1.91)],0.075,hair,head_rig)
for x in (-0.18,-0.08,0.05,0.16):
    path('swept bangs',[(x*0.85,-0.17,2.49),(x,-0.20,2.39),(x+0.035,-0.20,2.29)],0.061,hair,head_rig)

for side,x in [('L',-0.112),('R',0.112)]:
    sphere(side+' white eye',(x,-0.201,2.235),(0.057,0.013,0.055),white,head_rig)
    sphere(side+' amber iris',(x,-0.217,2.235),(0.031,0.012,0.041),eye,head_rig)
    sphere(side+' pupil',(x,-0.228,2.235),(0.010,0.008,0.025),eye_dark,head_rig)
    sphere(side+' glint',(x-0.011,-0.235,2.250),(0.007,0.005,0.009),white,head_rig)
    path(side+' upper lash',[(x-0.052,-0.205,2.275),(x,-0.218,2.294),(x+0.055,-0.202,2.271)],0.008,eye_dark,head_rig)
    path(side+' eyebrow',[(x-0.042,-0.198,2.345),(x+0.03,-0.199,2.350)],0.006,hair,head_rig)
mouth=sphere('Mouth control: scale for lip sync',(0,-0.216,2.095),(0.037,0.009,0.012),eye_dark,head_rig)

# Iconic flat dark hat, talisman plate and flower accents.
cone('hat brim',(0,0,2.50),0.34,0.36,0.05,black,head_rig,32)
cone('hat crown',(0,0,2.62),0.28,0.23,0.22,black,head_rig,32)
cube('gold hat talisman',(0,-0.264,2.64),(0.13,0.023,0.16),gold,0.012,head_rig)
path('hat talisman mark',[(-0.025,-0.279,2.68),(0.018,-0.279,2.63),(-0.02,-0.279,2.60)],0.008,black,head_rig)
for i,(x,z) in enumerate(((0.22,2.69),(0.28,2.64),(0.27,2.73))):
    sphere('red plum flower '+str(i),(x,-0.18,z),(0.045,0.023,0.042),red,head_rig)
for s in (-1,1):
    path('hat side ribbon',[(s*0.26,0.0,2.54),(s*0.39,-0.02,2.34),(s*0.47,-0.02,2.28)],0.035,hair,head_rig)

# White cyclorama and soft shadows.
floor=cube('white floor',(0,0,-0.03),(200,200,0.06),white)
world=bpy.context.scene.world
world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=0.8
for name,loc,power,size in [('key',(-3,-4,6),350,5),('fill',(3,-2,4),120,4)]:
    data=bpy.data.lights.new(name,'AREA'); data.energy=power; data.shape='DISK'; data.size=size
    obj=bpy.data.objects.new(name,data); bpy.context.collection.objects.link(obj); obj.location=loc
    direction=Vector((0,0,1.5))-obj.location; obj.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()

camera_data=bpy.data.cameras.new('front portrait camera'); camera=bpy.data.objects.new('front portrait camera',camera_data)
bpy.context.collection.objects.link(camera); camera.location=(0,-8,1.38)
direction=Vector((0,0,1.38))-camera.location; camera.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
camera_data.type='ORTHO'; camera_data.ortho_scale=5.8
bpy.context.scene.camera=camera

# Opening acting controls: shy glance, then determined look. These are editable keyframes.
head_rig.rotation_euler[2]=0.0; head_rig.keyframe_insert(data_path='rotation_euler',frame=1)
head_rig.rotation_euler[2]=0.14; head_rig.keyframe_insert(data_path='rotation_euler',frame=28)
head_rig.rotation_euler[2]=0.0; head_rig.keyframe_insert(data_path='rotation_euler',frame=61)
head_rig.rotation_euler[0]=0.04; head_rig.keyframe_insert(data_path='rotation_euler',frame=70)
head_rig.rotation_euler[0]=0.0; head_rig.keyframe_insert(data_path='rotation_euler',frame=130)
for frame,sy,sz in [(1,0.009,0.012),(43,0.009,0.012),(49,0.012,0.025),(55,0.009,0.012),(66,0.009,0.012),(99,0.009,0.012),(107,0.012,0.023),(117,0.009,0.012)]:
    mouth.scale.y=sy/0.009; mouth.scale.z=sz/0.012
    mouth.keyframe_insert(data_path='scale',frame=frame)
camera_data.ortho_scale=5.8; camera_data.keyframe_insert(data_path='ortho_scale',frame=1)
camera_data.ortho_scale=5.8; camera_data.keyframe_insert(data_path='ortho_scale',frame=140)
camera_data.ortho_scale=3.4; camera_data.keyframe_insert(data_path='ortho_scale',frame=190)

scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1280; scene.render.resolution_y=720; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.render.fps=30; scene.frame_start=1; scene.frame_end=190
scene.view_settings.view_transform='Standard'
scene.view_settings.look='Medium High Contrast'
scene.view_settings.exposure=-0.65
scene.frame_set(1)

out_dir=Path(__file__).resolve().parent
bpy.ops.wm.save_as_mainfile(filepath=str(out_dir/'hutao_character_study.blend'))
scene.render.filepath=str(out_dir/'preview.png')
bpy.ops.render.render(write_still=True)
