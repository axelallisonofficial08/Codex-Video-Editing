"""Make a compact frame strip around the three fastest shot transitions."""
from pathlib import Path
from PIL import Image, ImageDraw

p = Path(__file__).resolve().parent
fps = 24
times = [12.25,12.33,12.42,12.50,12.58,12.67,
         16.00,16.08,16.17,16.25,16.33,16.42,
         23.50,23.58,23.67,23.75,23.83,23.92]
w,h = 320,180
out = Image.new('RGB',(6*w,3*(h+24)),(16,16,16))
d = ImageDraw.Draw(out)
for j,t in enumerate(times):
    f = round(t*fps)+1
    source = p/'polished_frames'/f'frame_{f:04d}.png'
    image = Image.open(source).convert('RGB').resize((w,h))
    x,y=(j%6)*w,(j//6)*(h+24)
    out.paste(image,(x,y+24))
    d.text((x+8,y+5),f'{t:.2f}s  frame {f}',fill='white')
out.save(p/'polished_motion_review.jpg',quality=88)
print('Saved',p/'polished_motion_review.jpg')
