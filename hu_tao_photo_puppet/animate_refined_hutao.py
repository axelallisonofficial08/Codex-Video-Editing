"""Refined, shot-timed Hu Tao recreation of the supplied 37.78 s performance.

The source MP4 is a rendered performance, so these are observed/keyed poses,
not imported animation data. Major poses were annotated at 0.5 s intervals.
"""
import bpy, math, struct
from pathlib import Path
from mathutils import Vector

P=Path(__file__).resolve().parent
FPS=24; DURATION=37.78; END=math.ceil(DURATION*FPS)
s=bpy.context.scene
s.render.engine='BLENDER_EEVEE'
s.render.resolution_x=848; s.render.resolution_y=478; s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG'; s.render.image_settings.color_mode='RGB'
s.render.fps=FPS; s.frame_start=1; s.frame_end=END
s.view_settings.view_transform='Standard'; s.view_settings.look='Medium High Contrast'
s.world.use_nodes=True; s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.25,.2,.2,1)
s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
a=bpy.data.objects['胡桃_arm']; mesh=bpy.data.objects['胡桃_mesh']; keys=mesh.data.shape_keys.key_blocks
for b in a.pose.bones:
    if b.name in ('頭','首','上半身','上半身2','手首.L','手首.R') or any(q in b.name for q in ('親指','人指','中指','薬指','小指')):
        b.rotation_mode='XYZ'
def F(t): return max(1,round(t*FPS)+1)
def sethide(o,t,hidden): o.hide_render=hidden; o.keyframe_insert('hide_render',frame=F(t))
def setshape(n,t,val):
    if n in keys:
        keys[n].value=val; keys[n].keyframe_insert('value',frame=F(t))
def setrot(n,t,vals):
    b=a.pose.bones[n]; b.rotation_euler=tuple(math.radians(v) for v in vals); b.keyframe_insert('rotation_euler',frame=F(t))

# Put the two reference-inspired backplates behind the imported 3D character.
def image_plane(name,path,y):
    bpy.ops.mesh.primitive_plane_add(size=2,location=(0,y,1.18),rotation=(math.pi/2,0,0))
    o=bpy.context.object; o.name=name; o.scale=(.95,.55,1)
    m=bpy.data.materials.new(name+' material'); m.use_nodes=True
    ns=m.node_tree.nodes; ns.clear(); tex=ns.new('ShaderNodeTexImage'); tex.image=bpy.data.images.load(str(path),check_existing=True)
    em=ns.new('ShaderNodeEmission'); out=ns.new('ShaderNodeOutputMaterial')
    m.node_tree.links.new(tex.outputs['Color'],em.inputs['Color']); m.node_tree.links.new(em.outputs['Emission'],out.inputs['Surface'])
    o.data.materials.append(m); return o
wood=image_plane('Blurred wooden room',P/'wood_backplate.png',1.0)
white=image_plane('White and cyan lyric backdrop',P/'white_backplate.png',.92)
def flat_material(name,rgb):
    m=bpy.data.materials.new(name); m.diffuse_color=(*rgb,1); m.use_nodes=True
    ns=m.node_tree.nodes; ns.clear(); em=ns.new('ShaderNodeEmission'); em.inputs['Color'].default_value=(*rgb,1)
    out=ns.new('ShaderNodeOutputMaterial'); m.node_tree.links.new(em.outputs[0],out.inputs['Surface']); return m
blackmat=flat_material('Title black',(.002,.002,.004))
bpy.ops.mesh.primitive_plane_add(size=2,location=(0,-.30,1.18),rotation=(math.pi/2,0,0))
black=bpy.context.object; black.name='Opening and closing black'; black.scale=(3,2,1); black.data.materials.append(blackmat)
deskmat=flat_material('Wood desk',(.25,.115,.09))
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,-.53,.80))
desk=bpy.context.object; desk.name='Desk'; desk.dimensions=(3,.48,.055); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); desk.data.materials.append(deskmat)
for o,a0,b0 in [(wood,4.75,19.85),(white,19.85,37.24),(desk,12.43,16.4)]:
    sethide(o,0,True); sethide(o,a0,False); sethide(o,b0,True)
sethide(black,0,False); sethide(black,4.75,True); sethide(black,37.24,False)
sethide(mesh,0,True); sethide(mesh,4.75,False); sethide(mesh,37.24,True)
for t,z in ((4.75,0),(12.35,0),(12.43,-.42),(16.38,-.42),(16.40,0)):
    a.location.z=z; a.keyframe_insert('location',frame=F(t))

cd=bpy.data.cameras.new('Reference matched camera'); cam=bpy.data.objects.new('Reference matched camera',cd); s.collection.objects.link(cam)
cam.location=(0,-4.1,1.30); cam.rotation_euler=(Vector((0,0,1.30))-cam.location).to_track_quat('-Z','Y').to_euler()
cd.type='ORTHO'; cd.ortho_scale=.95; s.camera=cam
for name,pos,power,size,col in [('Warm key',(-2,-3,4),480,4,(1,.82,.76)),('Cool fill',(2,-2,3),350,3,(.82,.88,1))]:
    d=bpy.data.lights.new(name,'AREA'); d.energy=power; d.size=size; d.color=col
    o=bpy.data.objects.new(name,d); s.collection.objects.link(o); o.location=pos
    o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler()

# Camera centers were read from the half-second reference contact sheets.
# Values are crop width, target height and horizontal offset.
shots=[
 (0,.95,1.30,0),(4.75,.98,1.31,0),(6.0,.96,1.30,0),(7.5,.93,1.30,0),
 (9.0,.88,1.31,0),(10.0,.94,1.31,.03),(11.5,1.0,1.30,0),
 (12.35,1.0,1.30,0),(12.43,1.20,.94,0),(16.38,1.20,.94,0),
 (16.4,1.05,1.27,0),(17.0,1.02,1.30,0),(19.5,1.11,1.30,0),
 (19.80,1.11,1.30,0),(19.85,.86,1.33,-.20),
 (21.92,.86,1.33,-.20),(21.95,.88,1.32,.18),
 (23.82,.88,1.32,.18),(23.85,.86,1.32,-.18),
 (26.82,.86,1.32,-.18),(26.85,.90,1.31,.18),
 (29.22,.90,1.31,.18),(29.25,.86,1.31,0),
 (30.97,.86,1.31,0),(31.0,1.01,1.30,0),
 (33.77,1.01,1.30,0),(33.8,.79,1.33,0),(37.24,.84,1.31,0)]
for t,scale,z,x in shots:
    cd.ortho_scale=scale; cd.keyframe_insert('ortho_scale',frame=F(t))
    cam.location=(x,-4.1,z); cam.keyframe_insert('location',frame=F(t))

# Wrist targets let each hand trace the particular reference movement.  L is
# screen right; R is screen left. A three-bone IK chain drives upper/lower arms.
targets={}
for side in ('L','R'):
    o=bpy.data.objects.new('Wrist IK '+side,None); s.collection.objects.link(o); targets[side]=o
    c=a.pose.bones['手首.'+side].constraints.new('IK'); c.target=o; c.chain_count=5; c.use_stretch=False
def wrist(side,t,xyz):
    if xyz[2]>1.20:
        xyz=(xyz[0],xyz[1],xyz[2]-.18)
    if abs(xyz[0])<=.15 and xyz[2]<1.20:
        xyz=(xyz[0]*.45,xyz[1],xyz[2])
    o=targets[side]; o.location=xyz; o.keyframe_insert('location',frame=F(t))
def fingers(side,t,gesture):
    curls={'open':(0,0,0,0,0),'soft':(18,18,18,18,15),'fist':(48,66,66,66,52),
           'point':(18,0,68,68,65),'shy':(26,36,45,45,34)}
    thumb,index,middle,ring,pinky=curls[gesture]
    vals={'親指':thumb,'人指':index,'中指':middle,'薬指':ring,'小指':pinky}
    for prefix,deg in vals.items():
        for j in ((0,1,2) if prefix=='親指' else (1,2,3)):
            n=prefix+str(j)+'.'+side
            if n not in a.pose.bones: continue
            b=a.pose.bones[n]; b.rotation_euler.x=math.radians(deg*(.62 if j==3 else 1)); b.keyframe_insert('rotation_euler',frame=F(t))

# Screen-accurate landmark timeline: hand to temple, turn, desk lean, hand on
# heart, lyric-section pointer, finger at lips, then clasped hands.
hand_marks=[
 # t, screen-right (L), screen-left (R), L fingers, R fingers
 (4.75,(.10,-.23,1.08),(-.08,-.23,1.08),'shy','shy'),
 (5.50,(.11,-.22,1.10),(-.13,-.22,1.13),'shy','soft'),
 (6.00,(.10,-.22,1.07),(-.12,-.22,1.11),'soft','soft'),
 (6.50,(.10,-.21,1.09),(-.28,-.17,1.17),'soft','open'),
 (7.00,(.12,-.21,1.09),(-.17,-.22,1.10),'soft','soft'),
 (7.50,(.12,-.22,1.08),(-.14,-.21,1.10),'soft','soft'),
 (8.00,(.10,-.23,1.09),(-.26,-.16,1.37),'soft','point'),
 (8.50,(.11,-.22,1.08),(-.24,-.17,1.43),'soft','point'),
 (9.00,(.10,-.23,1.08),(-.19,-.18,1.38),'soft','soft'),
 (9.50,(.11,-.22,1.10),(-.47,-.10,.98),'soft','soft'),
 (10.50,(.10,-.22,1.10),(-.47,-.10,.98),'soft','soft'),
 (11.50,(.08,-.21,1.13),(-.10,-.23,1.17),'shy','shy'),
 (12.00,(.10,-.22,1.17),(-.08,-.24,1.16),'shy','shy'),
 (12.43,(.16,-.18,.97),(-.02,-.54,.78),'soft','soft'),
 (13.00,(.16,-.18,.96),(-.02,-.54,.78),'soft','soft'),
 (14.00,(.17,-.18,.98),(-.02,-.54,.78),'soft','soft'),
 (15.00,(.17,-.18,.98),(-.02,-.54,.78),'soft','soft'),
 (16.00,(.16,-.18,.97),(-.02,-.54,.78),'soft','soft'),
 (16.40,(.50,-.08,.93),(-.50,-.08,.93),'soft','soft'),
 (17.00,(.50,-.08,.93),(-.50,-.08,.93),'soft','soft'),
 (18.00,(.10,-.22,1.11),(-.38,-.15,1.08),'shy','soft'),
 (19.00,(.10,-.23,1.11),(-.11,-.25,1.13),'shy','shy'),
 (19.85,(.10,-.22,1.08),(-.16,-.19,1.43),'soft','soft'),
 (20.50,(.11,-.22,1.10),(-.18,-.19,1.43),'soft','open'),
 (21.50,(.10,-.22,1.08),(-.20,-.18,1.43),'soft','point'),
 (21.95,(.10,-.22,1.08),(-.38,-.12,1.13),'soft','open'),
 (22.50,(.10,-.22,1.09),(-.28,-.17,1.30),'soft','open'),
 (23.00,(.27,-.17,1.44),(-.11,-.22,1.12),'soft','soft'),
 (23.70,(.24,-.17,1.41),(-.13,-.22,1.12),'soft','soft'),
 (23.85,(.12,-.22,1.11),(-.30,-.17,1.17),'soft','point'),
 (24.50,(.11,-.22,1.12),(-.30,-.17,1.17),'soft','point'),
 (25.50,(.12,-.22,1.10),(-.29,-.18,1.15),'soft','point'),
 (26.50,(.10,-.22,1.10),(-.12,-.22,1.10),'soft','soft'),
 (26.85,(.10,-.22,1.10),(-.14,-.23,1.12),'soft','soft'),
 (27.50,(.10,-.22,1.10),(-.11,-.23,1.12),'soft','soft'),
 (28.00,(.10,-.22,1.10),(-.02,-.28,1.40),'soft','point'),
 (28.50,(.10,-.22,1.10),(-.02,-.28,1.40),'soft','point'),
 (29.25,(.08,-.22,1.10),(-.04,-.27,1.39),'soft','point'),
 (30.00,(.07,-.23,1.09),(-.07,-.24,1.12),'shy','shy'),
 (31.00,(.06,-.23,1.10),(-.06,-.24,1.11),'shy','shy'),
 (32.00,(.07,-.23,1.10),(-.06,-.24,1.11),'shy','shy'),
 (33.00,(.11,-.22,1.10),(-.07,-.23,1.11),'soft','shy'),
 (33.80,(.22,-.20,1.16),(-.07,-.23,1.11),'open','soft'),
 (35.00,(.28,-.21,1.19),(-.10,-.23,1.11),'open','soft'),
 (36.50,(.27,-.20,1.18),(-.10,-.23,1.11),'open','soft'),
 (37.24,(.45,-.10,.93),(-.45,-.10,.93),'soft','soft')]
for t,L,R,Lg,Rg in hand_marks:
    wrist('L',t,L); wrist('R',t,R); fingers('L',t,Lg); fingers('R',t,Rg)

# Head axes were calibrated in Blender: X nod, Y turn, Z ear-to-shoulder tilt.
heads=[
 (4.75,12,-4,-3),(5.5,7,0,0),(6,0,0,0),(6.5,-2,0,1),(7.0,2,0,0),
 (7.5,7,-2,-2),(8,8,-2,-3),(8.5,7,0,-2),(9,9,14,1),(9.5,1,30,0),
 (10,14,20,-3),(10.5,9,18,-2),(11,3,12,-1),(11.5,-2,8,0),(12,0,0,1),
 (12.43,20,-8,-8),(13,16,-7,-6),(14,10,-5,-5),(15,6,0,-4),(16,18,-5,-8),
 (16.5,4,0,0),(17,0,0,0),(17.5,-3,-4,-1),(18,5,0,0),(18.5,6,0,-2),
 (19,5,0,-2),(19.5,0,0,0),(19.85,-1,-3,1),(20.5,-2,2,1),(21,10,-5,-3),
 (21.5,0,2,-1),(22,0,-4,-2),(22.5,-2,1,2),(23,7,0,-3),(23.5,0,1,0),
 (24,6,-5,-2),(24.5,2,0,-2),(25,5,0,-2),(25.5,0,0,0),(26,7,8,1),
 (26.5,0,0,0),(27,4,-4,-3),(27.5,-2,-2,1),(28,8,0,-5),(28.5,1,0,0),
 (29,0,0,0),(29.5,-3,0,1),(30,0,0,0),(30.5,0,0,0),(31,4,0,-1),
 (31.5,1,0,0),(32,0,0,0),(32.5,-2,0,0),(33,5,-3,-2),(33.5,1,0,0),
 (34,0,0,0),(34.5,0,0,0),(35,0,0,0),(35.5,1,0,0),(36,1,0,0),
 (36.5,0,0,0),(37.24,0,0,0)]
for t,x,y,z in heads:
    setrot('頭',t,(x,y,z)); setrot('上半身',t,(x*.15,0,z*.20))

# Observed eye state and smile accents.  Continuous mouth movement is added
# below with source-audio amplitude, while these points mark the expressions.
face=[
 (4.75,1,.25,0),(5.5,1,.35,0),(6,0,.15,0),(6.5,.35,.25,0),
 (7,0,.18,0),(7.5,.12,.03,0),(8,1,.08,0),(8.5,1,.08,0),
 (9,1,.05,0),(9.5,0,.02,0),(10,1,.10,0),(10.5,1,.10,0),
 (11,.5,.02,0),(11.5,0,.02,0),(12,1,.22,0),
 (12.43,.8,.08,0),(13,.15,.02,0),(14,.05,.02,0),(15,.05,.02,0),
 (16,.7,.02,0),(16.5,1,.04,0),(17,0,.04,0),(17.5,.55,.03,0),
 (18,0,.10,0),(18.5,0,.06,0),(19,.25,.08,0),(19.5,0,.10,0),
 (19.85,0,.25,0),(20.5,0,.25,0),(21,.25,.18,0),(21.5,0,.25,0),
 (22,.05,.18,.65),(22.5,.05,.25,.60),(23,.05,.35,.65),(23.5,1,.35,0),
 (24,1,.30,0),(24.5,1,.35,0),(25,1,.35,0),(25.5,.15,.28,0),
 (26,0,.25,0),(26.5,0,.30,0),(27,1,.32,0),(27.5,.05,.18,0),
 (28,.05,.18,0),(28.5,0,.25,0),(29,1,.35,0),(29.5,.05,.25,0),
 (30,0,.25,0),(30.5,0,.25,0),(31,1,.40,0),(31.5,1,.42,0),
 (32,1,.45,0),(32.5,1,.45,0),(33,0,.28,0),(33.5,0,.25,0),
 (34,0,.18,0),(34.5,0,.18,0),(35,0,.15,0),(35.5,0,.15,0),
 (36,0,.12,0),(36.5,0,.12,0),(37.24,0,.05,0)]
for t,blink,smile,wink in face:
    setshape('まばたき',t,blink); setshape('笑い',t,smile); setshape('ウィンク',t,wink)

raw=(P/'original_audio.f32').read_bytes(); samples=struct.unpack('<'+str(len(raw)//4)+'f',raw)
for f in range(F(4.75),END+1,2):
    t=(f-1)/FPS; center=int(t*8000); seg=samples[max(0,center-250):min(len(samples),center+250)]
    rms=(sum(v*v for v in seg)/max(1,len(seg)))**.5
    setshape('あ',t,min(.72,max(.02,(rms-.016)*5.3)))
    setshape('口角上げ',t,.12 if t>19.85 else .05)

# Source title rhythm and lyric cards. Text remains on the same side as in
# the source rather than following the moving character.
fonts={
 'latin':bpy.data.fonts.load('C:/Windows/Fonts/arial.ttf'),
 'korean':bpy.data.fonts.load('C:/Windows/Fonts/malgun.ttf'),
 'japanese':bpy.data.fonts.load('C:/Windows/Fonts/YuGothM.ttc'),
 'chinese':bpy.data.fonts.load('C:/Windows/Fonts/simsun.ttc')}
def text(name,body,x,z,size,color=(.04,.035,.04),font='latin'):
    cu=bpy.data.curves.new(name,'FONT'); cu.body=body; cu.size=size; cu.font=fonts[font]
    cu.align_x='LEFT'; cu.align_y='CENTER'
    o=bpy.data.objects.new(name,cu); s.collection.objects.link(o); o.location=(x,-.35,z); o.rotation_euler.x=math.pi/2
    cu.materials.append(flat_material(name+' ink',color)); return o
for word,lo,hi in [('Falling..',1.22,2.10),('Falling',2.11,2.88),('In',2.89,3.67),('Love',3.68,4.74)]:
    o=text('Opening '+word,word,-.115,1.30,.078,(.95,.95,.95))
    sethide(o,0,True); sethide(o,lo,False); sethide(o,hi,True)

lyrics=[
 (19.85,21.95,-.38,1.39,'Kasi mahal kita','(Because I love you)','latin'),
 (21.95,23.85,.32,1.40,'너 뿐 이야','(Only you)','korean'),
 (23.85,26.85,-.39,1.40,'あなたであるだけで','(Just being you\nmakes me happy)','japanese'),
 (26.85,29.25,.31,1.40,'你的微笑','(Your smile)','chinese'),
 (29.25,31.00,-.36,1.40,'La tua risata','(Your laugh)','latin')]
for idx,(lo,hi,x,z,original,translation,font) in enumerate(lyrics):
    native=text('Lyric original '+str(idx),original,x,z,.033,font=font)
    en=text('Lyric translation '+str(idx),translation,x,z-.055,.022 if idx==2 else .025)
    for o in (native,en): sethide(o,0,True); sethide(o,lo,False); sethide(o,hi,True)

source=P.parent/'source_media'/'Falling in Love 💙 - Monolithia (1080p).mp4'
if not source.exists():
    source=Path('C:/Users/reage/Downloads/Falling in Love 💙 - Monolithia (1080p).mp4')
try:
    if source.exists(): s.sequence_editor_create().strips.new_sound('Original soundtrack',str(source),channel=1,frame_start=1)
except Exception as exc: print('Audio strip unavailable:',exc)
# Linear keys prevent Bézier overshoot from moving the character downward
# before the desk cut, and preserve the source's abrupt camera edits.
for animated,paths in ((a,{'location'}),(cam,{'location'}),(cd,{'ortho_scale'})):
    if animated.animation_data and animated.animation_data.action:
        action=animated.animation_data.action
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for curve in bag.fcurves:
                        if curve.data_path in paths:
                            for point in curve.keyframe_points: point.interpolation='LINEAR'
s.frame_set(1)
s.render.filepath=str(P/'refined_frames'/'frame_')
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file:
        path=Path(bpy.path.abspath(im.filepath))
        if path.is_file(): im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(P/'Hu_Tao_Refined.blend'))
print('Saved refined scene',END,'frames')
