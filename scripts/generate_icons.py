#!/usr/bin/env python3
"""Generate placeholder home-screen icons for the TSA PWA from a maroon lettermark.

Regenerate with: python3 scripts/generate_icons.py
Swap in a real logo later by replacing this script's output in icons/.
"""

import os

from PIL import Image, ImageDraw, ImageFont

MAROON = (124, 24, 62)  # #7C183E
WHITE = (255, 255, 255)

FONT_PATH = os.path.expanduser(
    "~/Library/Containers/com.amazon.Lassen/Data/Library/Application Support/"
    "com.amazon.Lassen/AppExpansionResources/quote_share_font_oswald_1/Oswald-Regular.ttf"
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "icons")


def make_icon(size, text, corner_radius_ratio, text_scale, out_name):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    radius = int(size * corner_radius_ratio)
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=MAROON)

    font_size = int(size * text_scale)
    font = ImageFont.truetype(FONT_PATH, font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pos = ((size - text_w) / 2 - bbox[0], (size - text_h) / 2 - bbox[1])
    draw.text(pos, text, font=font, fill=WHITE)

    img.save(os.path.join(OUT_DIR, out_name))
    print(f"wrote {out_name} ({size}x{size})")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    # Standard icons: mark fills most of the canvas.
    make_icon(192, "TSA", corner_radius_ratio=0.22, text_scale=0.34, out_name="icon-192.png")
    make_icon(512, "TSA", corner_radius_ratio=0.22, text_scale=0.34, out_name="icon-512.png")
    # Maskable: keep the mark inside the ~80% "safe zone" Android's adaptive mask uses.
    make_icon(512, "TSA", corner_radius_ratio=0.0, text_scale=0.26, out_name="icon-512-maskable.png")
    # iOS wants a fully opaque square, no transparency, no pre-rounded corners.
    apple = Image.new("RGB", (180, 180), MAROON)
    draw = ImageDraw.Draw(apple)
    font = ImageFont.truetype(FONT_PATH, 62)
    bbox = draw.textbbox((0, 0), "TSA", font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((180 - text_w) / 2 - bbox[0], (180 - text_h) / 2 - bbox[1]), "TSA", font=font, fill=WHITE)
    apple.save(os.path.join(OUT_DIR, "apple-touch-icon.png"))
    print("wrote apple-touch-icon.png (180x180)")

    favicon = apple.resize((32, 32), Image.LANCZOS)
    favicon.save(os.path.join(OUT_DIR, "favicon.png"))
    print("wrote favicon.png (32x32)")


if __name__ == "__main__":
    main()
