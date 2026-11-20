#!/usr/bin/env python3
"""Normaliza o genera imágenes de producto para Odoo (image_1920).

Modos:
  python3 img_producto.py url  <URL_o_ruta> <salida.jpg>
      Descarga/abre, recorta bordes blancos, centra en lienzo 1200x1200 blanco,
      JPEG calidad 85 (<~350 KB). Imprime ruta y tamaño.
  python3 img_producto.py card "<MARCA>" "<MODELO>" "<CODIGO>" <salida.jpg>
      Genera tarjeta provisional 1200x1200 (marca, modelo, código) cuando no hay foto.
  python3 img_producto.py b64 <archivo.jpg>
      Imprime el base64 listo para image_1920.
"""
import base64
import io
import sys
import urllib.request

from PIL import Image, ImageChops, ImageDraw, ImageFont

SIZE = 1200
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}


def _open(src):
    if src.startswith("http"):
        data = urllib.request.urlopen(urllib.request.Request(src, headers=UA), timeout=30).read()
        return Image.open(io.BytesIO(data))
    return Image.open(src)


def _trim(im):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.add(ImageChops.difference(im, bg), ImageChops.difference(im, bg), 2.0, -20)
    box = diff.getbbox()
    return im.crop(box) if box else im


def normalizar(src, out):
    im = _open(src)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        fondo = Image.new("RGBA", im.size, (255, 255, 255, 255))
        fondo.alpha_composite(im)
        im = fondo
    im = _trim(im.convert("RGB"))
    m = int(SIZE * 0.9)
    im.thumbnail((m, m), Image.LANCZOS)
    lienzo = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    lienzo.paste(im, ((SIZE - im.width) // 2, (SIZE - im.height) // 2))
    q = 88
    while True:
        buf = io.BytesIO()
        lienzo.save(buf, "JPEG", quality=q, optimize=True)
        if buf.tell() < 350_000 or q <= 60:
            break
        q -= 6
    open(out, "wb").write(buf.getvalue())
    print(out, buf.tell(), "bytes", f"origen {im.size}")


def _font(sz, bold=False):
    for p in [
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]:
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def _wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def card(marca, modelo, codigo, out):
    im = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([40, 40, SIZE - 40, SIZE - 40], outline=(220, 220, 220), width=4)
    fm, fmod, fc = _font(110, True), _font(64), _font(48)
    y = 380
    d.text((SIZE / 2, y), marca.upper(), font=fm, fill=(20, 20, 20), anchor="mm")
    y += 140
    for ln in _wrap(d, modelo.upper(), fmod, SIZE - 200):
        d.text((SIZE / 2, y), ln, font=fmod, fill=(60, 60, 60), anchor="mm")
        y += 80
    d.text((SIZE / 2, SIZE - 150), codigo, font=fc, fill=(120, 120, 120), anchor="mm")
    d.text((SIZE / 2, SIZE - 90), "IMAGEN PROVISIONAL", font=_font(32), fill=(170, 170, 170), anchor="mm")
    im.save(out, "JPEG", quality=85, optimize=True)
    print(out)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "url":
        normalizar(sys.argv[2], sys.argv[3])
    elif mode == "card":
        card(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif mode == "b64":
        print(base64.b64encode(open(sys.argv[2], "rb").read()).decode())
