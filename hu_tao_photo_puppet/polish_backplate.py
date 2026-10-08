"""Paint a warm, softly focused room backdrop for the reference-matched shot."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

P = Path(__file__).resolve().parent
W, H = 1280, 720
y, x = np.mgrid[0:H, 0:W]
horizontal = 0.5 + 0.5 * np.cos((x-W/2) / (W/2) * np.pi)
warm = 0.5 + 0.5 * np.exp(-((y-225)/170)**2)
grain = np.random.default_rng(19).normal(0, 1.1, (H, W))
rgb = np.stack([
    91 + 24*horizontal + 16*warm + grain,
    48 + 11*horizontal + 8*warm + grain*.65,
    50 + 7*horizontal + 4*warm + grain*.55,
], axis=2).clip(0, 255).astype('uint8')
im = Image.fromarray(rgb, 'RGB')
glow = Image.new('RGBA', (W, H)); g = ImageDraw.Draw(glow, 'RGBA')
for col in (135, 408, 876, 1143):
    g.rectangle((col-44, -20, col+44, 800), fill=(245, 146, 71, 26))
    g.rectangle((col-18, -20, col+18, 800), fill=(255, 188, 116, 75))
glow = glow.filter(ImageFilter.GaussianBlur(34))
im = Image.alpha_composite(im.convert('RGBA'), glow)
details = Image.new('RGBA', (W,H)); d = ImageDraw.Draw(details, 'RGBA')
for col in (135,408,876,1143):
    d.rectangle((col-31,0,col-22,H), fill=(41,21,27,98))
    d.rectangle((col+22,0,col+31,H), fill=(35,18,25,95))
    d.rectangle((col-4,0,col+4,H), fill=(251,175,100,65))
for row in (236, 257, 544):
    d.rectangle((0,row,W,row+15), fill=(252,164,88,65))
    d.rectangle((0,row+19,W,row+26), fill=(40,17,22,55))
details = details.filter(ImageFilter.GaussianBlur(13))
im = Image.alpha_composite(im, details).convert('RGB')
im.save(P/'wood_backplate_polished.png')
print('Saved', P/'wood_backplate_polished.png')
