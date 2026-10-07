"""Keep the singing audio available in the editable Blender timeline."""
import bpy
from pathlib import Path

source = Path(__file__).resolve().parent.parent / 'source_media' / 'Falling in Love 💙 - Monolithia (1080p).mp4'
if not source.exists():
    source = Path('C:/Users/reage/Downloads/Falling in Love 💙 - Monolithia (1080p).mp4')
s = bpy.context.scene
s.sequence_editor_create()
for strip in list(s.sequence_editor.strips):
    s.sequence_editor.strips.remove(strip)
song = s.sequence_editor.strips.new_sound('Reference song, singing section only',
                                          str(source), channel=1, frame_start=round(4.2*18)+1)
song.frame_offset_start = round(4.8*18)
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print('SOUND ADDED', song.frame_final_start, song.frame_final_end)
