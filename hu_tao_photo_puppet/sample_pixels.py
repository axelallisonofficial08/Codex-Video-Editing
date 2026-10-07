import bpy
import numpy as np
from pathlib import Path
src = Path(__file__).resolve().parent.parent / 'source_media' / 'WhatsApp Image 2026-10-06 at 20.37.59.jpeg'
if not src.exists():
    src = Path(r'C:\Users\reage\Downloads\WhatsApp Image 2026-10-06 at 20.37.59.jpeg')
im = bpy.data.images.load(str(src))
w,h = im.size
a=np.empty(w*h*4,dtype=np.float32)
im.pixels.foreach_get(a)
a=a.reshape(h,w,4)[::-1]
for x,y in [(100,100),(100,600),(640,300),(630,165),(620,150),(600,650),(620,650),(650,650),(690,650),(750,650),(560,350),(520,430),(610,500),(715,560)]:
    print(x,y,np.round(a[y,x,:3],3))
