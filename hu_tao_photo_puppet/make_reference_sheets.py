from PIL import Image, ImageDraw
from pathlib import Path
p=Path(__file__).resolve().parent
images=sorted((p/'reference_halfsec').glob('ref_*.jpg'))
for start in range(0,len(images),8):
    canvas=Image.new('RGB',(2000,760),'#161616')
    draw=ImageDraw.Draw(canvas)
    for j,path in enumerate(images[start:start+8]):
        im=Image.open(path).convert('RGB')
        x=(j%4)*500; y=(j//4)*380
        canvas.paste(im,(x,y+22))
        seconds=(int(path.stem.split('_')[-1])-1)*.5
        draw.text((x+8,y+2),f'{seconds:04.1f}s',fill='white')
    canvas.save(p/f'reference_sheet_{start//8+1:02}.jpg',quality=90)
