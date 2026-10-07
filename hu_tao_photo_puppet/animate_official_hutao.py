"""Full-length Hu Tao performance, timed against the supplied reference video."""
import bpy, math, struct, wave
from pathlib import Path
from mathutils import Vector

HERE=Path(__file__).resolve().parent
FPS=18
DURATION=37.78
END=math.ceil(DURATION*FPS)
s=bpy.context.scene
s.render.engine='BLENDER_EEVEE'
s.render.resolution_x=848; s.render.resolution_y=478; s.render.resolution_percentage=100
s.render.film_transparent=False
s.render.image_settings.file_format='PNG'; s.render.image_settings.color_mode='RGBA'
s.render.fps=FPS; s.frame_start=1; s.frame_end=END
s.view_settings.view_transform='Standard'; s.view_settings.look='Medium High Contrast'
s.world.use_nodes=True
s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.45,.36,.33,1)
s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8

arm=bpy.data.objects['胡桃_arm']
mesh=bpy.data.objects['胡桃_mesh']
shapes=mesh.data.shape_keys.key_blocks
for n in ['腕.L','腕.R','ひじ.L','ひじ.R','手首.L','手首.R','頭','首','上半身','上半身2','肩.L','肩.R']:
    arm.pose.bones[n].rotation_mode='XYZ'

def mat(name,color,rough=.9):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1)
    m.use_nodes=True; bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1); bs.inputs['Roughness'].default_value=rough
    return m
wood=mat('Warm rosewood panels',(.16,.075,.065))
trim=mat('Gold warm trim',(.28,.13,.09))
tablemat=mat('Wooden desk',(.28,.13,.1))
white=mat('White lyric backdrop',(.95,.96,.95))
ink=mat('Black title',(.005,.004,.008))

def cube(name,loc,scale,material):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(material); return o

wall=cube('Warm interior wall',(0,1.0,1.5),(12,.08,5),wood)
for z in (.78,1.75,2.65):
    cube('Interior horizontal wood trim',(0,.89,z),(12,.035,.025),trim)
for x in (-3,-1.5,0,1.5,3):
    cube('Interior vertical panel',(x,.9,1.5),(.025,.03,3),trim)
desk=cube('Performance desk',(0,-.65,.83),(5,.62,.06),tablemat)
white_wall=cube('White lyric background',(0,.6,1.4),(15,.08,6),white)
title_wall=cube('Black title background',(0,-.2,1.4),(15,.08,6),ink)

cd=bpy.data.cameras.new('Performance camera'); cam=bpy.data.objects.new('Performance camera',cd); s.collection.objects.link(cam)
cam.location=(0,-4.2,1.23); cd.type='ORTHO'; cd.ortho_scale=1.30
cam.rotation_euler=(Vector((0,0,1.23))-cam.location).to_track_quat('-Z','Y').to_euler(); s.camera=cam
for name,pos,power,size,color in [('soft key',(-2,-3,4),650,4,(1,.77,.66)),('soft fill',(2,-2,3),370,3,(.77,.83,1))]:
    d=bpy.data.lights.new(name,'AREA'); d.energy=power; d.size=size; d.color=color
    o=bpy.data.objects.new(name,d); s.collection.objects.link(o); o.location=pos
    o.rotation_euler=(Vector((0,0,1.1))-o.location).to_track_quat('-Z','Y').to_euler()

def frame(t): return max(1,round(t*FPS)+1)
def rot(bone,t,x=0,y=0,z=0):
    b=arm.pose.bones[bone]; b.rotation_euler=tuple(math.radians(v) for v in (x,y,z)); b.keyframe_insert('rotation_euler',frame=frame(t))
def shape(name,t,v):
    if name in shapes:
        shapes[name].value=v; shapes[name].keyframe_insert('value',frame=frame(t))
def place(o,t,loc=None,scale=None,hide=None):
    f=frame(t)
    if loc is not None: o.location=loc; o.keyframe_insert('location',frame=f)
    if scale is not None: o.scale=scale; o.keyframe_insert('scale',frame=f)
    if hide is not None: o.hide_render=hide; o.keyframe_insert('hide_render',frame=f)

# Opening cards recreate the source's timing and restrained typography.
def text_obj(name,content,size=.10,at=(0,-.31,1.4),color=(1,1,1,1)):
    cu=bpy.data.curves.new(name,'FONT'); cu.body=content; cu.align_x='CENTER'; cu.align_y='CENTER'; cu.size=size
    o=bpy.data.objects.new(name,cu); s.collection.objects.link(o); o.location=at
    o.rotation_euler[0]=math.radians(90)
    m=bpy.data.materials.new(name+' lettering'); m.diffuse_color=color; m.use_nodes=True
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=color
    cu.materials.append(m); return o

cards=[('Falling..',1.25,2.12),('Falling',2.13,2.88),('In',2.90,3.68),('Love',3.70,4.75)]
for i,(word,a,b) in enumerate(cards):
    o=text_obj('Opening title '+str(i),word,.08)
    place(o,0,hide=True); place(o,a,hide=False); place(o,b,hide=True)

# Shot/background edits. These are stepped to match the source's hard cuts.
place(wall,0,hide=True); place(wall,4.80,hide=False); place(wall,20.86,hide=True)
place(desk,0,hide=True); place(desk,12.9,hide=False); place(desk,18.1,hide=True)
for o in (white_wall,):
    place(o,0,hide=True); place(o,20.86,hide=False); place(o,37.55,hide=True)
place(title_wall,0,hide=False); place(title_wall,4.80,hide=True)
place(arm,0,loc=(0,0,-4)); place(arm,4.80,loc=(0,0,0)); place(arm,37.50,loc=(0,0,0)); place(arm,37.55,loc=(0,0,-4))

# Camera crops and offsets follow the original: close singing shots, wider desk,
# then tighter lyric-section close-ups.
camera=[(0,1.4,1.23,0),(4.80,1.27,1.23,0),(6,1.27,1.23,-.07),(8.6,1.35,1.23,.07),
        (12.4,1.42,1.22,-.02),(13,1.65,1.15,0),(17.8,1.58,1.17,.02),
        (20.86,1.38,1.27,.07),(23,1.26,1.24,0),(27,1.30,1.25,-.03),
        (31,1.20,1.27,.01),(35,1.16,1.28,0),(37.55,1.25,1.24,0)]
for t,sc,z,x in camera:
    cd.ortho_scale=sc; cd.keyframe_insert('ortho_scale',frame=frame(t))
    cam.location=(x,-4.2,z); cam.keyframe_insert('location',frame=frame(t))

# Poses: upper arms/forearms, wrists, torso, head. Times are sampled at major
# gestures in the 37-second reference rather than driven by a generic loop.
# arm.L is on screen right; arm.R is on screen left.
poses=[
 # t, head nod/turn/tilt, torso tilt, L upper/elbow/wrist, R upper/elbow/wrist
 (4.8,(12,-7,-5),(-3,0,0),(-20,-12,22),(-8,0,-5)),
 (5.7,(4,-2,-2),(0,0,0),(-24,-12,15),(-8,0,-8)),
 (6.8,(-3,4,5),(0,0,0),(-18,-15,18),(-8,0,-8)),
 (7.7,(8,-9,-5),(-2,0,0),(-18,-10,12),(-48,-70,-15)),
 (8.6,(-8,10,8),(0,0,0),(-20,-12,17),(-65,-78,-8)),
 (9.6,(13,3,-7),(0,0,0),(-18,-15,17),(-52,-60,-18)),
 (10.6,(5,-5,1),(0,0,0),(-45,-60,12),(-18,-12,-10)),
 (11.7,(-8,7,4),(0,0,0),(-55,-76,10),(-20,-17,-8)),
 (12.7,(8,-12,-8),(4,0,-5),(-50,-70,15),(-18,-10,-8)),
 (13.4,(16,-12,-8),(18,0,-7),(-10,-15,8),(-70,-85,-12)),
 (14.5,(13,-8,-7),(18,0,-7),(-8,-12,8),(-75,-85,-12)),
 (15.7,(10,-5,-5),(17,0,-5),(-8,-12,8),(-72,-82,-12)),
 (16.8,(18,-10,-8),(18,0,-7),(-8,-12,8),(-68,-80,-12)),
 (17.9,(14,0,-4),(10,0,-2),(-12,-20,8),(-46,-60,-10)),
 (19.0,(1,6,3),(0,0,0),(-48,-55,10),(-30,-40,-8)),
 (20.0,(-1,8,3),(0,0,0),(-55,-64,10),(-20,-15,-8)),
 (20.86,(10,-8,-5),(-1,0,0),(-10,-12,9),(-8,0,-8)),
 (21.8,(-2,4,5),(0,0,0),(-18,-14,12),(-16,-8,-8)),
 (22.8,(-8,8,8),(0,0,0),(-45,-60,8),(-18,-10,-10)),
 (23.8,(7,-4,-6),(0,0,0),(-50,-68,5),(-10,-8,-8)),
 (24.9,(-4,-5,8),(0,0,0),(-63,-82,-5),(-13,-10,-8)),
 (25.9,(-3,5,-5),(0,0,0),(-58,-80,0),(-15,-8,-8)),
 (26.9,(5,-6,6),(0,0,0),(-18,-12,10),(-48,-70,-12)),
 (28.0,(-7,4,-4),(0,0,0),(-10,-8,8),(-55,-66,-8)),
 (29.0,(-2,5,6),(0,0,0),(-18,-10,10),(-40,-45,-8)),
 (30.0,(2,-6,-5),(0,0,0),(-25,-25,12),(-55,-65,-5)),
 (31.0,(-4,2,5),(0,0,0),(-50,-65,8),(-25,-30,-7)),
 (32.1,(8,-5,-6),(0,0,0),(-55,-75,10),(-35,-48,-9)),
 (33.2,(-3,4,7),(0,0,0),(-45,-62,8),(-50,-66,-10)),
 (34.2,(5,-5,-4),(0,0,0),(-35,-46,8),(-55,-70,-10)),
 (35.2,(-3,4,5),(0,0,0),(-55,-70,8),(-45,-55,-8)),
 (36.2,(4,-3,-4),(0,0,0),(-60,-76,4),(-47,-62,-6)),
 (37.5,(0,0,0),(0,0,0),(-18,-12,12),(-18,-12,-10)),
]
for t,head,torso,left,right in poses:
    rot('頭',t,*head); rot('上半身',t,*torso)
    rot('腕.L',t,z=left[0]); rot('ひじ.L',t,x=left[1],z=left[2]); rot('手首.L',t,z=8)
    rot('腕.R',t,z=-right[0]); rot('ひじ.R',t,x=right[1],z=right[2]); rot('手首.R',t,z=-8)

# Expression points mirror the original's closed-eye phrases, winks and smiles.
expressions=[
 (4.8,1,0,0),(5.7,.1,.05,0),(6.6,0,.12,0),(7.8,.65,.05,0),
 (8.8,.15,.2,0),(9.7,.82,0,0),(10.7,.1,.1,0),(11.8,.1,.1,0),
 (13.4,.65,0,0),(14.5,.1,0,0),(15.7,.15,0,0),(16.8,.9,0,0),
 (18.0,.05,.1,0),(20.0,0,.13,0),(21.0,.8,.05,0),(22.0,0,.28,0),
 (23.0,.05,.4,0),(24.0,.65,.24,0),(25.0,.1,.42,.75),(26.0,.6,.36,0),
 (27.0,.9,.30,0),(28.0,.9,.32,0),(29.0,.08,.40,0),(30.0,.82,.33,0),
 (31.0,.05,.36,0),(32.0,.05,.40,0),(33.0,.85,.40,0),(34.0,.05,.48,0),
 (35.0,.08,.40,0),(36.0,.04,.35,0),(37.5,.2,.1,0)]
for t,blink,smile,wink in expressions:
    shape('まばたき',t,blink); shape('笑い',t,smile); shape('ウィンク',t,wink)

# Source-song amplitude drives the imported MMD vowel morphs, with the
# hand-authored facial marks above keeping the phrasing expressive.
raw=(HERE/'original_audio.f32').read_bytes()
samples=struct.unpack('<'+str(len(raw)//4)+'f',raw)
for i in range(frame(4.8),END+1,2):
    t=(i-1)/FPS; c=int(t*8000); section=samples[max(0,c-400):min(len(samples),c+400)]
    rms=(sum(v*v for v in section)/max(1,len(section)))**.5
    mouth=min(.78,max(0,(rms-.015)*5.8))
    shape('あ',t,mouth)
    shape('口角上げ',t,.10 if t>20.86 else .03)

# Simple translated lyric cards on the bright half, matching the source layout.
lyrics=[('Because I love you',21,25.7),('Just to make you happy',26.0,30.7),
        ('Your smile',31.0,34.0),('Your laugh',34.1,37.55)]
for k,(line,a,b) in enumerate(lyrics):
    o=text_obj('Lyric '+str(k),line,.042,(-.56,-.26,1.48),(.05,.04,.05,1))
    o.data.align_x='LEFT'; place(o,0,hide=True); place(o,a,hide=False); place(o,b,hide=True)

# Sound stays with the editable Blender project; final encoder also copies the
# original audio losslessly from the reference video.
source=HERE.parent/'source_media'/'Falling in Love 💙 - Monolithia (1080p).mp4'
if not source.exists():
    source=Path('C:/Users/reage/Downloads/Falling in Love 💙 - Monolithia (1080p).mp4')
try:
    if source.exists():
        s.sequence_editor_create(); snd=s.sequence_editor.strips.new_sound('Original performance audio',str(source),channel=1,frame_start=1)
except Exception as exc: print('Audio strip skipped:',exc)
s.frame_set(1)
s.render.filepath=str(HERE/'official_frames'/'frame_')
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'Hu_Tao_Full_Performance.blend'))
print('SAVED SCENE',END,'frames')
