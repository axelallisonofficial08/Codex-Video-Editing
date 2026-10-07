"""Create and render a Hu Tao performance inspired by the supplied reference clip."""
import bpy
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
scene = bpy.context.scene
fps = 12
frames = 454
scene.render.fps = fps
scene.frame_start = 1
scene.frame_end = frames
scene.render.resolution_x = 760
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(HERE / 'frames' / 'frame_')
scene.render.engine = 'BLENDER_EEVEE'
scene.render.image_settings.color_mode = 'RGB'
scene.render.film_transparent = False
scene.view_settings.exposure = -0.25

root = bpy.data.objects['Character root: move entire Hu Tao study']
torso = bpy.data.objects['Upper body rig']
head = bpy.data.objects['Head rig: tilt and turn']
left = bpy.data.objects['Left arm rig: gesture']
right = bpy.data.objects['Right arm rig: gesture']
mouth = bpy.data.objects['Mouth control: scale for lip sync']
camera = scene.camera
camera.data.animation_data_clear()
camera.animation_data_clear()
head.animation_data_clear()
torso.animation_data_clear()
left.animation_data_clear()
right.animation_data_clear()
mouth.animation_data_clear()
head.location.y = -0.32

# Keep the model centered while varying between full, medium, and face shots.
shots = [
    (1, 2.8, 2.18, 0.00), (25, 2.8, 2.18, 0.00),
    (38, 2.0, 2.21, -0.08), (78, 2.05, 2.18, -0.05),
    (110, 2.5, 2.04, 0.06), (145, 1.76, 2.24, 0.07),
    (181, 2.2, 2.18, -0.05), (213, 1.66, 2.24, 0.04),
    (248, 2.28, 2.10, 0.04), (285, 1.8, 2.23, -0.04),
    (326, 2.15, 2.17, 0.04), (370, 1.72, 2.24, 0.00),
    (420, 1.63, 2.22, -0.04), (454, 1.83, 2.17, 0.00),
]
for frame, scale, z, x in shots:
    camera.data.ortho_scale = scale
    camera.data.keyframe_insert(data_path='ortho_scale', frame=frame)
    camera.location = (x, -8, z)
    camera.keyframe_insert(data_path='location', frame=frame)

# A flat stage backdrop switches from the reference's dark/warm opening to white.
mat = bpy.data.materials.new('performance background')
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()
out = nodes.new('ShaderNodeOutputMaterial')
emission = nodes.new('ShaderNodeEmission')
mat.node_tree.links.new(emission.outputs[0], out.inputs['Surface'])
for frame, color in [
    (1, (0.008, 0.010, 0.022, 1)),
    (28, (0.008, 0.010, 0.022, 1)),
    (33, (0.42, 0.23, 0.22, 1)),
    (125, (0.63, 0.37, 0.32, 1)),
    (185, (0.47, 0.31, 0.34, 1)),
    (211, (0.96, 0.96, 0.94, 1)),
    (454, (0.96, 0.96, 0.94, 1)),
]:
    emission.inputs['Color'].default_value = color
    emission.inputs['Color'].keyframe_insert(data_path='default_value', frame=frame)
bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 2.5, 2))
backdrop = bpy.context.object
backdrop.name = 'Animated performance backdrop'
backdrop.rotation_euler.x = math.pi / 2
backdrop.data.materials.append(mat)

# Opening title cards are native Blender text, so they remain editable.
title_mat = bpy.data.materials.new('white title lettering')
title_mat.use_nodes = True
title_nodes = title_mat.node_tree.nodes
title_nodes.clear()
title_output = title_nodes.new('ShaderNodeOutputMaterial')
title_emission = title_nodes.new('ShaderNodeEmission')
title_emission.inputs['Color'].default_value = (1, 1, 1, 1)
title_mat.node_tree.links.new(title_emission.outputs[0], title_output.inputs['Surface'])
for label, first, last in [('Falling...', 1, 14), ('in Love', 16, 28)]:
    curve = bpy.data.curves.new(label + ' title', 'FONT')
    curve.body = label
    curve.align_x = 'CENTER'
    curve.align_y = 'CENTER'
    curve.size = .19
    obj = bpy.data.objects.new(label + ' title card', curve)
    bpy.context.collection.objects.link(obj)
    obj.location = (0, -4, 2.19)
    obj.rotation_euler.x = math.pi / 2
    curve.materials.append(title_mat)
    for f, hidden in ((1, first > 1), (first, False), (last, False), (last + 1, True)):
        obj.hide_render = hidden
        obj.keyframe_insert(data_path='hide_render', frame=f)

for obj in bpy.data.objects:
    ancestor = obj.parent
    while ancestor is not None and ancestor != root:
        ancestor = ancestor.parent
    if ancestor == root:
        for f, hidden in ((1, True), (28, True), (29, False)):
            obj.hide_render = hidden
            obj.keyframe_insert(data_path='hide_render', frame=f)

# Deliberate performance beats: bashful glances, a lowered gaze, then direct singing.
beats = [
    (1, 0, 0, 0, 0, 0), (28, 0, 0, 0, 0, 0),
    (40, 0.06, -0.18, -0.04, 0.10, -0.10),
    (68, 0.05, 0.13, 0.04, -0.20, 0.17),
    (95, -0.10, -0.12, -0.03, -0.45, 0.21),
    (120, -0.06, 0.08, 0.02, -0.13, 0.38),
    (147, 0.10, -0.19, -0.04, 0.25, -0.42),
    (175, 0.04, 0.13, 0.03, -0.44, -0.08),
    (210, -0.08, 0.0, 0.01, -0.03, 0.20),
    (238, 0.11, -0.11, -0.04, 0.25, -0.49),
    (267, 0.05, 0.10, 0.02, -0.18, -0.15),
    (302, -0.06, 0.13, 0.04, -0.50, 0.15),
    (335, 0.08, -0.14, -0.03, -0.08, 0.40),
    (370, -0.08, 0.02, 0.0, -0.36, -0.28),
    (404, 0.04, -0.10, 0.03, 0.02, 0.12),
    (435, -0.03, 0.07, -0.02, -0.20, -0.15),
    (454, 0.02, 0.0, 0.0, 0, 0),
]
for frame, tilt, turn, lean, la, ra in beats:
    head.rotation_euler = (tilt, 0, turn)
    head.keyframe_insert(data_path='rotation_euler', frame=frame)
    torso.rotation_euler = (0, lean, 0)
    torso.keyframe_insert(data_path='rotation_euler', frame=frame)
    left.rotation_euler = (0, la, -la * .35)
    right.rotation_euler = (0, ra, -ra * .35)
    left.keyframe_insert(data_path='rotation_euler', frame=frame)
    right.keyframe_insert(data_path='rotation_euler', frame=frame)

# Syllabic mouth movement timed broadly to the musical phrases.
for frame in range(1, frames + 1, 3):
    active = frame >= 46 and frame < 440
    wave = abs(math.sin(frame * 0.54) * math.sin(frame * 0.14)) if active else 0
    mouth.scale = (1, 1, 1 + wave * 1.6)
    mouth.keyframe_insert(data_path='scale', frame=frame)

# Brief blinks at several expressive beats.
for b in (59, 113, 168, 230, 307, 353, 407):
    for side in ('L', 'R'):
        for part in ('white eye', 'amber iris', 'pupil', 'glint'):
            obj = bpy.data.objects.get(side + ' ' + part)
            if obj:
                for f, factor in ((b-2, 1), (b, .12), (b+2, 1)):
                    obj.scale.z = factor
                    obj.keyframe_insert(data_path='scale', frame=f)

# The opening is genuinely dark, with the character revealed as the camera fades in.
for name in ('key', 'fill'):
    light = bpy.data.objects[name].data
    base = 350 if name == 'key' else 120
    for frame, multiplier in ((1, .015), (23, .015), (36, 1), (454, 1)):
        light.energy = base * multiplier
        light.keyframe_insert(data_path='energy', frame=frame)

scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE / 'hutao_performance.blend'))
if '--still' in sys.argv:
    scene.frame_set(255)
    scene.render.filepath = str(HERE / 'performance_preview.png')
    bpy.ops.render.render(write_still=True)
else:
    (HERE / 'frames').mkdir(exist_ok=True)
    if '--titles' in sys.argv:
        scene.frame_start = 1
        scene.frame_end = 30
    elif '--benchmark' in sys.argv:
        scene.frame_start = 255
        scene.frame_end = 260
    bpy.ops.render.render(animation=True)
