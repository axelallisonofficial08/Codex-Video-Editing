"""Extract the actual JPEG character pixels for the new 2D Blender puppet."""
from collections import deque
from pathlib import Path
import bpy
import numpy as np

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'original_reference.jpeg'
image = bpy.data.images.load(str(SOURCE))
w, h = image.size
pixels = np.empty(w * h * 4, dtype=np.float32)
image.pixels.foreach_get(pixels)
rgb = pixels.reshape(h, w, 4)[::-1, :, :3]

# This particular supplied JPEG has a neutral-gray background. Retain its
# actual foreground RGB pixels; only the background gains alpha.
x0, y0, x1, y1 = 482, 52, 755, 714
crop = rgb[y0:y1, x0:x1].copy()
height, width = crop.shape[:2]
chroma = crop.max(axis=2) - crop.min(axis=2)
brightness = crop.mean(axis=2)
foreground = (chroma > .035) | (brightness < .68)

# Restore only small enclosed neutral details, such as eye whites. Large
# neutral spaces between the legs and coat tails stay transparent.
seen = np.zeros((height, width), dtype=bool)
for sy in range(height):
    for sx in range(width):
        if seen[sy, sx] or foreground[sy, sx]:
            continue
        queue = deque([(sy, sx)])
        component = []
        touches_edge = False
        seen[sy, sx] = True
        while queue:
            y, x = queue.popleft()
            component.append((y, x))
            touches_edge |= y == 0 or x == 0 or y == height - 1 or x == width - 1
            for ny, nx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
                if 0 <= ny < height and 0 <= nx < width and not seen[ny,nx] and not foreground[ny,nx]:
                    seen[ny,nx] = True
                    queue.append((ny,nx))
        if False and not touches_edge and len(component) <= 90:
            for y,x in component:
                foreground[y,x] = True

# Discard isolated JPEG color flecks in the neutral stage.
seen_fg = np.zeros((height, width), dtype=bool)
clean = np.zeros((height, width), dtype=bool)
for sy in range(height):
    for sx in range(width):
        if seen_fg[sy,sx] or not foreground[sy,sx]:
            continue
        queue = deque([(sy,sx)])
        component = []
        seen_fg[sy,sx] = True
        while queue:
            y,x = queue.popleft()
            component.append((y,x))
            for ny,nx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
                if 0 <= ny < height and 0 <= nx < width and not seen_fg[ny,nx] and foreground[ny,nx]:
                    seen_fg[ny,nx] = True
                    queue.append((ny,nx))
        if len(component) >= 22:
            for y,x in component:
                clean[y,x] = True
alpha = clean.astype(np.float32)
# Exclude the cast floor shadow adjacent to the shoes; it belongs to the
# source stage, not the character puppet.
for y in range(height):
    if y > 530:
        left = 75 + int(max(0, y - 530) * .16)
        right = 243 - int(max(0, y - 530) * .14)
        alpha[y, :left] = 0
        alpha[y, right:] = 0
# JPEG antialiasing leaves a pale rim that becomes obvious over the warm
# background. Peel that light-only rim while retaining dark hair/ribbons.
for _ in range(3):
    pad = np.pad(alpha, 1, mode='constant')
    neighbors = sum(pad[dy:dy+height, dx:dx+width] for dy in range(3) for dx in range(3))
    alpha[(alpha > 0) & (neighbors < 9) & (brightness > .68)] = 0
# One-pixel edge softening conceals JPEG color noise without altering the
# interior image. The original RGB is left untouched.
padded = np.pad(alpha, 1, mode='constant')
edge = sum(padded[dy:dy+height, dx:dx+width] for dy in range(3) for dx in range(3)) / 9.0
alpha *= .6 + .4 * edge
rgba = np.concatenate((crop, alpha[..., None]), axis=2)

out = bpy.data.images.new('Hu Tao from supplied JPEG', width, height, alpha=True)
out.file_format = 'PNG'
out.filepath_raw = str(ROOT / 'character_cutout.png')
out.pixels.foreach_set(rgba[::-1].ravel())
out.save()
print('Saved', out.filepath_raw, 'foreground pixels', int(np.count_nonzero(alpha > .5)))
