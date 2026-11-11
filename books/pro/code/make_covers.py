# -*- coding: utf-8 -*-
"""从 logo 图生成封面与封底背景（A4 比例，压缩 JPEG）。"""
from pathlib import Path

from PIL import Image, ImageEnhance

SRC = Path(r"E:/Study/0-logo")
OUT = Path(__file__).resolve().parent.parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

A4 = (1240, 1754)  # 150 dpi


def crop_to(im: Image.Image, ratio: float) -> Image.Image:
    w, h = im.size
    target = w / ratio
    if target <= h:
        top = (h - target) / 2
        im = im.crop((0, top, w, top + target))
    else:
        target_w = h * ratio
        left = (w - target_w) / 2
        im = im.crop((left, 0, left + target_w, h))
    return im


def make(src: str, dst: str, ratio: float = A4[1] / A4[0]) -> None:
    im = Image.open(SRC / src).convert("RGB")
    im = crop_to(im, ratio)
    im = im.resize(A4, Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.05)
    im.save(OUT / dst, "JPEG", quality=84, optimize=True, progressive=True)
    print(dst, (OUT / dst).stat().st_size // 1024, "KB")


if __name__ == "__main__":
    make("logo1.png", "cover.jpg")
    make("logo13.png", "backcover.jpg")
