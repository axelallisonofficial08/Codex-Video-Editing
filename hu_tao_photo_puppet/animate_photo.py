"""Animate the supplied JPEG as a 2D puppet in a fresh Blender scene."""
from pathlib import Path
import math
import sys
import bpy

HERE = Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 760
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.fps = 12
scene.frame_start = 1
scene.frame_end = 454
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = False
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'Medium High Contrast'

def emission(name, color):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    shader = nodes.new('ShaderNodeEmission')
    shader.inputs['Color'].default_value = (*color, 1)
    m.node_tree.links.new(shader.outputs[0], out.inputs['Surface'])
    return m, shader

# Original JPEG pixels, with only the neutral stage background made transparent.
im = bpy.data.images.load(str(HERE / 'character_cutout.png'))
mat = bpy.data.materials.new('Original JPEG pixels')
mat.use_nodes = True
mat.surface_render_method = 'DITHERED'
nodes = mat.node_tree.nodes
nodes.clear()
out = nodes.new('ShaderNodeOutputMaterial')
tex = nodes.new('ShaderNodeTexImage')
tex.image = im
transparent = nodes.new('ShaderNodeBsdfTransparent')
lit = nodes.new('ShaderNodeEmission')
mix = nodes.new('ShaderNodeMixShader')
links = mat.node_tree.links
links.new(tex.outputs['Color'], lit.inputs['Color'])
links.new(tex.outputs['Alpha'], mix.inputs[0])
links.new(transparent.outputs[0], mix.inputs[1])
links.new(lit.outputs[0], mix.inputs[2])
links.new(mix.outputs[0], out.inputs['Surface'])

cols, rows = 22, 52
width, height = 1.08, 2.62
verts, uvs, faces = [], [], []
for j in range(rows + 1):
    v = j / rows
    for i in range(cols + 1):
        u = i / cols
        verts.append(((u - .5) * width, 0, v * height))
        uvs.append((u, v))
for j in range(rows):
    for i in range(cols):
        a = j * (cols + 1) + i
        faces.append((a, a + 1, a + cols + 2, a + cols + 1))
mesh = bpy.data.meshes.new('Subdivided JPEG puppet mesh')
mesh.from_pydata(verts, [], faces)
mesh.update()
uvlayer = mesh.uv_layers.new(name='Source image coordinates')
for polygon in mesh.polygons:
    for loop_index in polygon.loop_indices:
        vi = mesh.loops[loop_index].vertex_index
        uvlayer.data[loop_index].uv = uvs[vi]
puppet = bpy.data.objects.new('Hu Tao - actual JPEG puppet', mesh)
bpy.context.collection.objects.link(puppet)
mesh.materials.append(mat)
puppet.shape_key_add(name='Source photograph', from_mix=False)

def ease(x):
    x = max(0, min(1, x))
    return x*x*(3-2*x)

def deform(x, z, p):
    head, tilt, left, right, sway, bob = p
    xn = x + sway * ease(z / 2.5)
    zn = z + bob * ease(z / 2.5)
    hw = ease((z - 1.68) / .46)
    hw *= math.exp(-((x / .53) ** 4))
    angle = tilt * hw
    px, pz = 0, 1.84
    dx, dz = xn - px, zn - pz
    xn = px + dx * math.cos(angle) - dz * math.sin(angle) + head * hw
    zn = pz + dx * math.sin(angle) + dz * math.cos(angle)
    # Small hand/sleeve gestures, keeping the torso readable.
    lw = math.exp(-((x + .39) / .20) ** 2 - ((z - 1.30) / .46) ** 2)
    rw = math.exp(-((x - .39) / .20) ** 2 - ((z - 1.30) / .46) ** 2)
    xn += -.05 * left * lw + .05 * right * rw
    zn += .23 * left * lw + .23 * right * rw
    # A gentle swing in long coat tails and hair.
    hem = (1 - ease(z / .85)) * abs(x / .55)
    xn += .025 * math.sin((z * 3) + sway * 8) * hem
    return xn, zn

# Motion beats follow the warm introduction and bright closing section.
poses = [
    (1,   (0, 0, 0, 0, 0, 0)),
    (29,  (0, 0, 0, 0, 0, 0)),
    (50,  (-.035, -.055, 0, .22, -.020, .010)),
    (72,  (.025, .035, .16, 0, .015, -.004)),
    (96,  (-.030, -.025, .28, .06, -.018, .010)),
    (119, (.018, .030, .05, .35, .012, -.005)),
    (146, (.030, .055, .13, .08, .015, .008)),
    (171, (-.028, -.050, .35, .05, -.015, 0)),
    (199, (.015, .020, .08, .32, .012, .012)),
    (225, (-.018, -.015, .20, .15, -.010, -.004)),
    (252, (.035, .045, .03, .34, .020, .010)),
    (281, (-.028, -.035, .32, .05, -.012, 0)),
    (310, (.018, .025, .08, .23, .010, .014)),
    (341, (-.022, -.030, .30, .08, -.014, -.004)),
    (371, (.026, .037, .07, .34, .015, .008)),
    (404, (-.018, -.025, .27, .08, -.012, 0)),
    (433, (.015, .015, .10, .23, .008, .008)),
    (454, (0, 0, 0, 0, 0, 0)),
]
for idx, (frame, params) in enumerate(poses):
    key = puppet.shape_key_add(name=f'Performance pose {idx:02d}', from_mix=False)
    for i, (x, y, z) in enumerate(verts):
        xx, zz = deform(x, z, params)
        key.data[i].co = (xx, y, zz)
    if idx:
        key.value = 0
        key.keyframe_insert(data_path='value', frame=poses[idx-1][0])
    key.value = 1
    key.keyframe_insert(data_path='value', frame=frame)
    if idx < len(poses)-1:
        key.value = 0
        key.keyframe_insert(data_path='value', frame=poses[idx+1][0])

blink = puppet.shape_key_add(name='Eye blink', from_mix=False)
for i, (x, y, z) in enumerate(verts):
    influence = math.exp(-((x / .21) ** 4) - (((z - 2.20) / .072) ** 4))
    blink.data[i].co = (x, y, z + (2.20 - z) * .80 * influence)
blink.value = 0
blink.keyframe_insert(data_path='value', frame=1)
for b in (58, 112, 168, 232, 307, 354, 407):
    for f, value in ((b-2,0),(b,1),(b+2,0)):
        blink.value = value
        blink.keyframe_insert(data_path='value', frame=f)

# A tiny mouth overlay opens and closes to give the still face singing motion.
mouth_mat, _ = emission('mouth - dark plum', (.18, .065, .072))
bpy.ops.mesh.primitive_circle_add(vertices=24, radius=1, fill_type='NGON')
mouth = bpy.context.object
mouth.name = 'Animated singing mouth'
mouth.data.materials.append(mouth_mat)
mouth.rotation_euler.x = math.pi / 2
mouth.location = (.024, -.012, 2.095)
for frame in range(1, 455, 3):
    singing = frame > 44 and frame < 438
    pulse = abs(math.sin(frame * .37) * math.sin(frame * .12)) if singing else 0
    mouth.scale = (.010, .003 + .009 * pulse, 1)
    mouth.keyframe_insert(data_path='scale', frame=frame)
for frame, params in poses:
    x, z = deform(.024, 2.095, params)
    mouth.location = (x, -.012, z)
    mouth.keyframe_insert(data_path='location', frame=frame)

# Light and color progression from the reference, without reusing its girl.
bgmat, bgshader = emission('animated background', (.015, .019, .030))
for frame, color in [
    (1, (.012, .016, .028, 1)),
    (28, (.012, .016, .028, 1)),
    (35, (.52, .34, .32, 1)),
    (120, (.67, .44, .40, 1)),
    (204, (.53, .39, .42, 1)),
    (212, (.98, .98, .97, 1)),
    (454, (.98, .98, .97, 1)),
]:
    bgshader.inputs['Color'].default_value = color
    bgshader.inputs['Color'].keyframe_insert(data_path='default_value', frame=frame)
bpy.ops.mesh.primitive_plane_add(size=200, location=(0, .5, 1.3))
background = bpy.context.object
background.name = 'warm to white background'
background.rotation_euler.x = math.pi/2
background.data.materials.append(bgmat)

# Two title cards precede the character reveal.
white, _ = emission('title white', (1, 1, 1))
for text, first, last in [('Falling...', 1, 14), ('in Love', 16, 28)]:
    font = bpy.data.curves.new(text, 'FONT')
    font.body = text
    font.align_x = 'CENTER'
    font.align_y = 'CENTER'
    font.size = .19
    label = bpy.data.objects.new(text + ' title', font)
    bpy.context.collection.objects.link(label)
    label.location = (0, -.4, 2.2)
    label.rotation_euler.x = math.pi/2
    font.materials.append(white)
    for f, hide in ((1, first>1), (first, False), (last, False), (last+1, True)):
        label.hide_render = hide
        label.keyframe_insert(data_path='hide_render', frame=f)
for obj in (puppet, mouth):
    for f, hide in ((1, True), (28, True), (29, False)):
        obj.hide_render = hide
        obj.keyframe_insert(data_path='hide_render', frame=f)

camera_data = bpy.data.cameras.new('reference inspired close-up camera')
camera = bpy.data.objects.new('reference inspired close-up camera', camera_data)
bpy.context.collection.objects.link(camera)
scene.camera = camera
camera_data.type = 'ORTHO'
camera.rotation_euler.x = math.pi/2
for f, scale, target_z, x in [
    (1, 2.7, 2.10, 0), (29, 1.55, 2.12, 0),
    (62, 1.37, 2.11, -.03), (95, 1.68, 2.03, .02),
    (128, 1.22, 2.12, .02), (164, 1.10, 2.13, -.03),
    (202, 1.38, 2.08, .02), (224, 1.15, 2.13, 0),
    (260, 1.30, 2.10, .04), (300, 1.12, 2.14, -.03),
    (340, 1.25, 2.10, .03), (385, 1.08, 2.15, -.03),
    (424, 1.12, 2.13, 0), (454, 1.30, 2.08, 0),
]:
    camera.location = (x, -5, target_z)
    camera.data.ortho_scale = scale
    camera.keyframe_insert(data_path='location', frame=f)
    camera.data.keyframe_insert(data_path='ortho_scale', frame=f)

scene.frame_set(1)
im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(HERE / 'hu_tao_photo_performance.blend'))
if '--still' in sys.argv:
    scene.frame_set(100 if '--warm' in sys.argv else 255)
    scene.render.filepath = str(HERE / 'preview.png')
    bpy.ops.render.render(write_still=True)
else:
    (HERE / 'frames').mkdir(exist_ok=True)
    scene.render.filepath = str(HERE / 'frames' / 'frame_')
    if '--benchmark' in sys.argv:
        scene.frame_start = 250
        scene.frame_end = 255
    bpy.ops.render.render(animation=True)
