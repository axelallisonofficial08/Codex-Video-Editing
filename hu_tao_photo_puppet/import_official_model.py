"""Import the official Hu Tao PMX into a separate editable Blender project."""
from pathlib import Path
import sys
import bpy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'addons'))
sys.path.insert(0, str(HERE / 'addons' / 'opencc-wheel'))
import mmd_tools
mmd_tools.register()

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
pmx = HERE / 'official_model' / '胡桃.pmx'
result = bpy.ops.mmd_tools.import_model(
    filepath=str(pmx),
    scale=0.08,
    types={'MESH', 'ARMATURE', 'MORPHS'},
    clean_model=True,
)
print('IMPORT RESULT', result)
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE':
        print('ARMATURE', obj.name, 'BONES', len(obj.data.bones))
        print('BONE NAMES', [b.name for b in obj.data.bones])
    elif obj.type == 'MESH':
        print('MESH', obj.name, 'VERTICES', len(obj.data.vertices), 'SHAPES', [k.name for k in (obj.data.shape_keys.key_blocks if obj.data.shape_keys else [])][:100])

bpy.ops.wm.save_as_mainfile(filepath=str(HERE / 'official_hutao_rig.blend'))
