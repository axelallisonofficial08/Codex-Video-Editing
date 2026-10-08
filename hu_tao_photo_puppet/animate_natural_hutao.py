"""Reference-matched close-ups, torso follow-through, and facial timing."""
import bpy
import math
from pathlib import Path

P=Path(__file__).resolve().parent
s=bpy.context.scene
FPS=s.render.fps
F=lambda t:round(t*FPS)+1
arm=bpy.data.objects['胡桃_arm']
mesh=bpy.data.objects['胡桃_mesh']
shapes=mesh.data.shape_keys
cam=bpy.data.objects['Reference matched camera']

def curves(idblock):
    a=idblock.animation_data.action
    return [c for l in a.layers for strip in l.strips for bag in strip.channelbags for c in bag.fcurves]

def change_key(fc,t,value):
    frame=F(t)
    for k in fc.keyframe_points:
        if abs(k.co.x-frame)<.1:
            k.co.y=k.handle_left.y=k.handle_right.y=value
            fc.update()
            return
    raise RuntimeError(f'No key at {t}: {fc.data_path}[{fc.array_index}]')

# The source is a 1520x1080 close-up. Match its aspect and shot scale rather
# than leaving the character small in a 16:9 frame.
scales={4.75:.55,6:.55,7.5:.54,9:.51,10:.54,11.5:.60,12.35:.60,
        12.43:.70,16.38:.70,16.4:.61,17:.60,19.5:.65,19.8:.65,
        19.85:.65,21.92:.65,21.95:.65,23.82:.65,23.85:.65,26.82:.65,
        26.85:.66,29.22:.66,29.25:.62,30.97:.62,31:.69,33.77:.69,
        33.8:.42,37.24:.45}
for fc in curves(cam):
    if fc.data_path=='ortho_scale':
        for t,value in scales.items(): change_key(fc,t,value)
    elif fc.data_path=='location' and fc.array_index==2:
        for t in (12.43,16.38): change_key(fc,t,1.025)

# Observed profile turn, temple gesture, quiet Chinese-lyric expression, and
# final closer look. The head motion is purposeful rather than a loop.
head_changes={
    8.5:(15,0,-3),9:(13,24,1),9.5:(2,51,0),10:(15,43,-3),
    10.5:(10,31,-2),11:(4,21,-1),11.5:(-2,13,0),
    27.5:(2,-12,-3),28:(14,-8,-5),28.5:(3,-2,0),
    34:(2,0,-1),34.5:(3,0,-1),35:(5,0,-2),35.5:(8,0,-2),
    36:(9,0,-1),36.5:(6,0,-1),37.24:(2,0,0)}
for fc in curves(arm):
    if fc.data_path=='pose.bones["頭"].rotation_euler':
        for t,xyz in head_changes.items():
            change_key(fc,t,math.radians(xyz[fc.array_index]))

# Align the two conspicuous hand poses with their half-second reference
# frames: the right fingers meet the temple, then the left hand rests lower
# beside the hat during the desk shot.
for controller in ('Wrist IK R','Wrist IK L'):
    obj=bpy.data.objects[controller]
    for fc in curves(obj):
        if fc.data_path!='location': continue
        if controller=='Wrist IK R':
            if fc.array_index==0:
                for t,x in ((8,-.14),(8.5,-.13)): change_key(fc,t,x)
            elif fc.array_index==2:
                for t,z in ((8,1.34),(8.5,1.36)): change_key(fc,t,z)
        elif fc.array_index==2:
            for t in (12.43,13,14,15,16,16.38): change_key(fc,t,1.00)

# Source shoulders turn with the head and lean into the desk. Small asymmetric
# torso poses keep the upper body from freezing while hands trace their paths.
torso=[
 (4.75,3,-2,-1),(5.5,0,0,1),(6.5,-1,0,-1),(7.5,2,-1,1),
 (8.5,4,-2,-2),(9.5,3,13,0),(10,6,17,-3),(11.5,0,6,0),
 (12.35,0,0,0),(12.43,11,-4,-4),(13,10,-3,-5),(14,8,0,-3),
 (15,6,2,-3),(16.38,10,-3,-4),(16.4,0,0,0),(17,0,0,1),
 (18,3,0,1),(19.5,0,0,0),(19.85,0,-2,0),(20.5,1,-1,-2),
 (21.5,4,0,1),(21.95,-1,1,-2),(22.5,0,2,-1),(23.5,3,-1,2),
 (23.85,0,-1,-1),(24.5,2,-1,1),(25.5,1,0,-1),(26.85,0,1,0),
 (27.5,2,0,-2),(28.5,3,0,1),(29.25,0,0,0),(30,1,0,1),
 (31,3,0,-2),(32,1,0,1),(33,0,0,0),(33.8,0,0,0),
 (35,2,0,1),(36,1,0,-1),(37.24,0,0,0)]
spine=arm.pose.bones['上半身2']
spine.rotation_mode='XYZ'
for t,x,y,z in torso:
    spine.rotation_euler=tuple(map(math.radians,(x,y,z)))
    spine.keyframe_insert('rotation_euler',frame=F(t))

# The original audio-amplitude mouth track opens on instruments as well as
# vocals. Match visible reference mouth shapes at half-second landmarks.
mouth={
 4.75:.03,5:.02,5.5:.05,6:.20,6.5:.15,7:.03,7.5:.03,8:.13,8.5:.02,
 9:.02,9.5:.02,10:.05,10.5:.02,11:.17,11.5:.18,12:.18,
 12.5:.15,13:.03,13.5:.02,14:.02,14.5:.18,15:.04,15.5:.20,
 16:.03,16.5:.08,17:.08,17.5:.20,18:.04,18.5:.16,19:.04,19.5:.03,
 19.85:.14,20:.16,20.5:.04,21:.18,21.5:.04,22:.18,22.5:.02,
 23:.23,23.5:.03,24:.02,24.5:.15,25:.03,25.5:.02,26:.04,26.5:.04,
 27:.17,27.5:.03,28:.02,28.5:.18,29:.11,29.5:.04,30:.15,
 30.5:.18,31:.13,31.5:.03,32:.04,32.5:.15,33:.04,33.5:.04,
 34:.16,34.5:.16,35:.16,35.5:.15,36:.15,36.5:.14,37.24:.04}
for fc in curves(shapes):
    if fc.data_path=='key_blocks["あ"].value':
        while fc.keyframe_points:
            fc.keyframe_points.remove(fc.keyframe_points[0])
        for t,value in mouth.items():
            key=fc.keyframe_points.insert(F(t),value)
            key.interpolation='BEZIER'
            key.handle_left_type=key.handle_right_type='AUTO_CLAMPED'
        fc.update()
    elif fc.data_path=='key_blocks["まばたき"].value':
        points=sorted((float(k.co.x),float(k.co.y)) for k in fc.keyframe_points)
        for (f0,v0),(f1,v1) in zip(points,points[1:]):
            if abs(v1-v0)>.45 and f1-f0>6:
                key=fc.keyframe_points.insert(f1-3,v0)
                key.interpolation='BEZIER'
                key.handle_left_type=key.handle_right_type='AUTO_CLAMPED'
        fc.update()
    elif fc.data_path=='key_blocks["口角上げ"].value':
        while fc.keyframe_points:
            fc.keyframe_points.remove(fc.keyframe_points[0])
        smiles=[(4.75,.23),(5.5,.25),(6.5,.23),(7.5,.14),(8.5,.23),
                (9.5,.05),(10.5,.13),(11.5,.19),(12.43,.09),
                (14,.10),(15,.15),(16,.06),(17,.10),(18,.17),
                (19.5,.20),(20.5,.22),(21.5,.20),(22,.10),
                (23,.22),(24,.25),(25,.22),(26,.20),(27,.29),
                (28,.10),(29,.29),(30,.13),(31,.20),(32,.28),
                (33,.17),(33.8,.04),(37.24,.03)]
        for t,value in smiles:
            key=fc.keyframe_points.insert(F(t),value)
            key.interpolation='BEZIER'
            key.handle_left_type=key.handle_right_type='AUTO_CLAMPED'
        fc.update()

s.render.resolution_x=1520
s.render.resolution_y=1080
s.render.resolution_percentage=100
s.frame_set(F(5))
bpy.ops.wm.save_as_mainfile(filepath=str(P/'Hu_Tao_Natural.blend'))
print('Saved reference-matched natural scene')
