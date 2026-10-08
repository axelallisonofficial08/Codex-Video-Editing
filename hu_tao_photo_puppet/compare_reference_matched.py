"""Create side-by-side QA sheets from the final 30 fps render."""
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
groups = [(5,5.5,6,6.5),(8,8.5,9,9.5),(12.5,13,13.5,14),
          (15,15.5,16,16.5),(20,20.5,21,21.5),(22,22.5,23,23.5),
          (24,24.5,25,25.5),(27,27.5,28,28.5),(29,29.5,30,30.5),
          (31,31.5,32,32.5),(34,34.5,35,35.5)]
for group_number, times in enumerate(groups, 1):
    sheet = Image.new('RGB', (1000, 1520), (17,17,17))
    draw = ImageDraw.Draw(sheet)
    for row, time in enumerate(times):
        reference = Image.open(root/'reference_halfsec'/f'ref_{round(time*2)+1:03d}.jpg').convert('RGB')
        rendered = Image.open(root/'natural_frames'/f'frame_{round(time*30)+1:04d}.png').convert('RGB')
        rendered = rendered.resize((500,355), Image.Resampling.LANCZOS)
        y = row*380
        sheet.paste(reference, (0,y+25))
        sheet.paste(rendered, (500,y+25))
        draw.text((8,y+5), f'{time:04.1f}s  REFERENCE', fill='white')
        draw.text((508,y+5), f'{time:04.1f}s  HU TAO', fill='white')
    sheet.save(root/f'reference_matched_comparison_{group_number:02d}.jpg', quality=90)
print(f'Made {len(groups)} reference-matched comparison sheets')
