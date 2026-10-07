"""Paint soft stage backplates using colors and framing sampled from the reference."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math, random
p=Path(__file__).resolve().parent
w,h=1280,720
random.seed(12)
im=Image.new('RGB',(w,h))
px=im.load()
for y in range(h):
    for x in range(w):
        # The first shot is a blurred reddish wooden room with a warm rail.
        v=math.sin(x*.011)*3+math.sin(x*.028)*2+random.uniform(-1.2,1.2)
        vignette=1-.18*((x-w/2)/(w/2))**2
        px[x,y]=(int((112+v)*vignette),int((65+v*.55)*vignette),int((62+v*.5)*vignette))
d=ImageDraw.Draw(im,'RGBA')
for x in (80,305,945,1170):
    d.rectangle((x-14,0,x+14,h),fill=(43,20,22,35))
    d.rectangle((x-3,0,x+3,h),fill=(230,150,94,35))
for y in (270,282,595):
    d.rectangle((0,y,w,y+10),fill=(249,179,101,100 if y<300 else 50))
im=im.filter(ImageFilter.GaussianBlur(17))
im.save(p/'wood_backplate.png')

white=Image.new('RGB',(w,h),(248,250,249))
d=ImageDraw.Draw(white)
cyan=(215,241,245)
for x in (320,960): d.rectangle((x-14,0,x+14,h),fill=cyan)
for y in (52,668): d.rectangle((0,y,w,y+12),fill=cyan)
white=white.filter(ImageFilter.GaussianBlur(2))
white.save(p/'white_backplate.png')
