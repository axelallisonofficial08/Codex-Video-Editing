"""Build the requested white-stage performance from the existing Hu Tao rig."""
import bpy, math
from pathlib import Path
from mathutils import Vector

P = Path(__file__).resolve().parent
s = bpy.context.scene
fps = 18
offset = round(4.2 * fps)
song_start = 9.0
song_end = 41.98
end = round(42.7 * fps)
s.frame_start, s.frame_end, s.render.fps = 1, end, fps
s.render.engine = 'BLENDER_EEVEE'
s.render.resolution_x, s.render.resolution_y = 1280, 720
s.render.resolution_percentage = 100
s.render.image_settings.file_format = 'PNG'
s.render.image_settings.color_mode = 'RGB'
s.world.node_tree.nodes['Background'].inputs['Color'].default_value = (1, 1, 1, 1)
s.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 1
s.view_settings.exposure = -.45

def f(t): return round(t * fps) + 1
def clear_action(idblock):
    if idblock and idblock.animation_data:
        idblock.animation_data_clear()
def key_hide(o, value):
    clear_action(o)
    o.hide_render = value
    o.hide_viewport = value

def curves(action):
    if hasattr(action, 'fcurves'):
        return list(action.fcurves)
    return [fc for layer in action.layers for strip in layer.strips
            for bag in strip.channelbags for fc in bag.fcurves]

# Preserve the existing hand-keyed performance, facial marks and mouth motion.
for action in bpy.data.actions:
    for fc in curves(action):
        for k in fc.keyframe_points:
            k.co.x += offset
            k.handle_left.x += offset
            k.handle_right.x += offset
        fc.update()

for o in list(bpy.data.objects):
    if o.name.startswith('Opening title') or o.name in (
            'Warm interior wall', 'Performance desk', 'Black title background') or \
            o.name.startswith(('Interior horizontal', 'Interior vertical')):
        key_hide(o, True)
white = bpy.data.objects['White lyric background']
key_hide(white, False)
white.location = (0, 1.0, 1.4)
white.dimensions = (15, .08, 6)

arm = bpy.data.objects['胡桃_arm']
if arm.animation_data and arm.animation_data.action:
    for curve in curves(arm.animation_data.action):
        if curve.data_path == 'location':
            # Assigning constant location below replaces the unwanted keys.
            for k in curve.keyframe_points:
                k.co.y = 0
                k.handle_left.y = 0
                k.handle_right.y = 0
arm.location = (0, 0, 0)
arm.keyframe_insert('location', frame=1)
arm.keyframe_insert('location', frame=end)
for side, deg in (('L', -55), ('R', 55)):
    bone = arm.pose.bones['腕.'+side]
    bone.rotation_mode = 'XYZ'
    for t in (0, 5.7, 8.95):
        bone.rotation_euler.z = math.radians(deg)
        bone.keyframe_insert('rotation_euler', frame=f(t))

for light in [o for o in bpy.data.objects if o.type == 'LIGHT']:
    light.data.energy *= .58

cam = s.camera
clear_action(cam)
clear_action(cam.data)
cam.location = (0, -4.2, 1.17)
cam.rotation_euler = (Vector((0, 0, 1.17))-cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.type = 'ORTHO'
for t, scale, z, x in [
    (0, 3.55, .75, 0), (3.65, 3.55, .75, 0),
    (5.65, 1.48, 1.28, 0), (9.0, 1.48, 1.28, 0),
    (9.02, 1.27, 1.23, 0), (10.2, 1.27, 1.23, -.07),
    (12.8, 1.35, 1.23, .07), (16.6, 1.42, 1.22, -.02),
    (17.2, 1.65, 1.15, 0), (22, 1.58, 1.17, .02),
    (25.06, 1.38, 1.27, .07), (27.2, 1.26, 1.24, 0),
    (31.2, 1.30, 1.25, -.03), (35.2, 1.20, 1.27, .01),
    (39.2, 1.16, 1.28, 0), (42.7, 1.25, 1.24, 0)]:
    cam.data.ortho_scale = scale
    cam.data.keyframe_insert('ortho_scale', frame=f(t))
    cam.location = (x, -4.2, z)
    cam.keyframe_insert('location', frame=f(t))

# Opening acting: feet and torso remain still; gaze and face carry the change.
head = arm.pose.bones['頭']
head.rotation_mode = 'XYZ'
for t, xyz in [(0,(3,0,0)), (.5,(4,0,-8)), (1.35,(5,0,-8)),
               (1.8,(3,0,0)), (2.55,(2,0,0)), (3.15,(0,0,0)),
               (4.25,(0,0,0)), (5.65,(0,0,0))]:
    head.rotation_euler = tuple(math.radians(v) for v in xyz)
    head.keyframe_insert('rotation_euler', frame=f(t))
keys = bpy.data.objects['胡桃_mesh'].data.shape_keys.key_blocks
def morph(name, marks):
    if name not in keys: return
    q = keys[name]
    for t, v in marks:
        q.value = v; q.keyframe_insert('value', frame=f(t))
morph('笑い', [(0,0), (1.0,0), (2.7,0), (3.3,.16), (5.7,.2)])
morph('まばたき', [(0,.08), (.7,0), (1.1,.65), (1.28,0),
                    (2.8,0), (3.0,.7), (3.18,0), (5.7,0)])
morph('あ', [(0,0), (1.78,0), (1.88,.25), (2.05,.46),
             (2.23,.12), (2.37,.42), (2.58,.18), (2.7,0),
             (3.2,0), (3.45,.35), (3.62,.12), (3.8,.46),
             (4.02,.2), (4.16,.40), (4.3,0), (5.7,0)])

# Curtains sit between the fixed camera and the performer. Soft ripples make
# their motion read as fabric while the two edges meet exactly at centre.
red = bpy.data.materials.new('Deep red velvet')
red.diffuse_color = (.36, .018, .029, 1)
red.use_nodes = True
bs = red.node_tree.nodes.get('Principled BSDF')
bs.inputs['Base Color'].default_value = (.36, .018, .029, 1)
bs.inputs['Roughness'].default_value = .78
def curtain(side):
    verts, faces = [], []
    nx = 32
    for j,z in enumerate((-.9, 2.9)):
        for i in range(nx+1):
            x = (i/nx)*2.15
            verts.append((x, -.95 + .035*math.cos(i*math.pi*.8), z))
    for i in range(nx): faces.append((i,i+1,nx+i+2,nx+i+1))
    mesh = bpy.data.meshes.new('Curtain mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(red)
    o = bpy.data.objects.new('Red curtain '+side, mesh)
    s.collection.objects.link(o)
    if side == 'left': o.scale.x = -1
    for t,x in [(0, -3.0 if side=='left' else 3.0),
                (6.25, -3.0 if side=='left' else 3.0),
                (7.28, 0 if side=='left' else 0),
                (8.0, 0), (8.98, -3.0 if side=='left' else 3.0)]:
        o.location.x = x
        o.keyframe_insert('location', frame=f(t))
    o.hide_render = False
    return o
curtain('left'); curtain('right')

# No source-video opening titles, source backgrounds or extra text.
if s.sequence_editor:
    for st in list(s.sequence_editor.strips): s.sequence_editor.strips.remove(st)
s.frame_set(1)
s.render.filepath = str(P/'white_stage_frames'/'frame_')
bpy.ops.wm.save_as_mainfile(filepath=str(P/'Hu_Tao_White_Stage.blend'))
print('WHITE STAGE READY', end)
