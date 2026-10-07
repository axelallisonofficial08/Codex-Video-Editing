import bpy
arm=next(o for o in bpy.data.objects if o.type=='ARMATURE')
mesh=next(o for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)>1000)
print('ARMATURE LOCATION',tuple(arm.location),'MESH BOUNDS',[(tuple(v)) for v in mesh.bound_box])
for b in arm.data.bones:
    n=b.name
    if any(t in n for t in ('頭','首','肩','腕','ひじ','手首','親指','人差','中指','目','上半身','腰')):
        print('BONE',n,'HEAD',tuple(round(v,3) for v in b.head_local),'TAIL',tuple(round(v,3) for v in b.tail_local))
