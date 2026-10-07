from pathlib import Path
from PIL import Image, ImageDraw
p=Path(__file__).resolve().parent
times=(0,2,4,5,6,8,10,12,13,15,16,18,20,22,24,27,29,31,34,37)
canvas=Image.new('RGB',(5*424,4*262),'#101010'); d=ImageDraw.Draw(canvas)
for j,t in enumerate(times):
    f=min(907,round(t*24)+1)
    path=p/'refined_frames'/f'frame_{f:04d}.png'
    im=Image.open(path).convert('RGB'); im.thumbnail((424,239))
    x=(j%5)*424; y=(j//5)*262
    canvas.paste(im,(x,y+23)); d.text((x+6,y+3),f'{t}s',fill='white')
canvas.save(p/'refined_review.jpg',quality=90)
