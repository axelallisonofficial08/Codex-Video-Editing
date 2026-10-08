"""Polish the existing reference-timed Blender scene without redistributing its rig."""
import bpy
from pathlib import Path

P = Path(__file__).resolve().parent
s = bpy.context.scene
fps = s.render.fps
frame = lambda t: round(t * fps) + 1

def curves(idblock):
    if not idblock.animation_data or not idblock.animation_data.action:
        return []
    action = idblock.animation_data.action
    return [fc for layer in action.layers for strip in layer.strips
            for bag in strip.channelbags for fc in bag.fcurves]

def replace_key(fc, t, value):
    f = frame(t)
    for key in fc.keyframe_points:
        if abs(key.co.x - f) < 0.1:
            key.co.y = value
            key.handle_left.y = value
            key.handle_right.y = value
            fc.update()
            return
    raise RuntimeError(f'Missing key {fc.data_path}[{fc.array_index}] at {t}s')

# The old root dip made the desk hand fall through the tabletop. Raise the
# character partway, frame the desk near the lower edge, and bring the hand
# beside the hat while the other hand stays at the tabletop.
arm = bpy.data.objects['胡桃_arm']
for fc in curves(arm):
    if fc.data_path == 'location' and fc.array_index == 2:
        replace_key(fc, 12.43, -0.27)
        replace_key(fc, 16.38, -0.27)
        for key in fc.keyframe_points:
            key.interpolation = 'LINEAR'

cam = bpy.data.objects['Reference matched camera']
for fc in curves(cam):
    if fc.data_path == 'location' and fc.array_index == 2:
        replace_key(fc, 12.43, 1.05)
        replace_key(fc, 16.38, 1.05)
    elif fc.data_path == 'ortho_scale':
        replace_key(fc, 12.43, 1.05)
        replace_key(fc, 16.38, 1.05)
    for key in fc.keyframe_points:
        key.interpolation = 'LINEAR'

# Preserve contact and shot timing. Clamp curves only on the continuous
# performance channels so arm paths and facial values cannot overshoot.
for name in ('Wrist IK L', 'Wrist IK R'):
    for fc in curves(bpy.data.objects[name]):
        for key in fc.keyframe_points:
            key.interpolation = 'BEZIER'
            key.handle_left_type = 'AUTO_CLAMPED'
            key.handle_right_type = 'AUTO_CLAMPED'
        fc.auto_smoothing = 'CONT_ACCEL'
        fc.update()

left_wrist = bpy.data.objects['Wrist IK L']
for fc in curves(left_wrist):
    if fc.data_path != 'location':
        continue
    for t in (12.43, 13.0, 14.0, 15.0, 16.0):
        if fc.array_index == 0:
            replace_key(fc, t, 0.23)
        elif fc.array_index == 2:
            replace_key(fc, t, 1.22)
    if fc.array_index in (0, 2):
        val = 0.23 if fc.array_index == 0 else 1.22
        fc.keyframe_points.insert(frame(16.38), val)
        fc.update()

right_wrist = bpy.data.objects['Wrist IK R']
for fc in curves(right_wrist):
    if fc.data_path == 'location' and fc.array_index == 2:
        for t in (12.43, 13.0, 14.0, 15.0, 16.0):
            replace_key(fc, t, 0.91)
        fc.keyframe_points.insert(frame(16.38), 0.91)
        fc.update()
for fc in curves(arm):
    if fc.data_path.startswith('pose.bones['):
        for key in fc.keyframe_points:
            key.interpolation = 'BEZIER'
            key.handle_left_type = 'AUTO_CLAMPED'
            key.handle_right_type = 'AUTO_CLAMPED'
        fc.auto_smoothing = 'CONT_ACCEL'
        fc.update()

wood = bpy.data.objects['Blurred wooden room']
new_image = bpy.data.images.load(str(P/'wood_backplate_polished.png'), check_existing=True)
for material in wood.data.materials:
    for node in material.node_tree.nodes:
        if node.type == 'TEX_IMAGE':
            node.image = new_image
new_image.pack()

s.render.resolution_x = 1280
s.render.resolution_y = 720
s.render.resolution_percentage = 100
s.render.image_settings.file_format = 'PNG'
s.render.film_transparent = False
s.frame_set(frame(13.5))
bpy.ops.wm.save_as_mainfile(filepath=str(P/'Hu_Tao_Polished.blend'))
print('Saved polished scene', s.frame_end, 'frames', s.render.resolution_x, s.render.resolution_y)
