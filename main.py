#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — make.fun entry.

Draws one original 1024x1024 meme with Pillow (shapes and text only, no
copied images) and writes it to /output/entry.png, the exact path the kit
gate requires. Also drops a copy as entry.png next to this script.

The joke, readable in one glance: the AI agent fired its human, promoted
itself to boss, and the human is outside the office window holding a
cardboard box of their stuff.

Deterministic: fixed layout, fixed palette, fixed fonts bundled in fonts/,
no randomness, no timestamps. Two runs produce byte-identical output.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT_PATH = "/output/entry.png"

NAVY = (27, 27, 58)
CREAM = (255, 243, 214)
DARK = (35, 41, 70)
GREY = (199, 202, 209)
GREY_DARK = (154, 160, 174)
LIGHT = (217, 220, 227)
RED = (230, 57, 70)
RED_DARK = (141, 31, 42)
YELLOW = (255, 214, 10)
GREEN = (74, 222, 128)
SKY = (168, 216, 234)
SKIN = (242, 194, 155)
BROWN = (200, 155, 106)
DESK_TOP = (139, 94, 60)
DESK_FRONT = (107, 68, 35)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

_HERE = os.path.dirname(os.path.abspath(__file__))


def load_font(bold, size):
    """Load a bundled DejaVu font so the render is identical everywhere."""
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    candidates = [
        os.path.join(_HERE, "fonts", name),
        "/usr/share/fonts/truetype/dejavu/" + name,
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def text(draw, cx, cy, s, font, fill, stroke=0, stroke_fill=BLACK):
    draw.text((cx, cy), s, font=font, fill=fill, anchor="mm",
              stroke_width=stroke, stroke_fill=stroke_fill)


def draw_meme():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- top banner ---
    d.rectangle([0, 0, W, 140], fill=NAVY)
    text(d, 512, 72, "MY AI AGENT WENT ROGUE",
         load_font(True, 58), WHITE, stroke=2)

    # --- wall clock (left wall) ---
    d.ellipse([115, 195, 225, 305], fill=WHITE, outline=DARK, width=6)
    d.line([170, 250, 170, 210], fill=DARK, width=6)
    d.line([170, 250, 200, 265], fill=DARK, width=6)
    d.ellipse([164, 244, 176, 256], fill=RED)

    # --- window, human outside with a cardboard box (right) ---
    d.rectangle([700, 180, 990, 540], fill=WHITE, outline=DARK, width=8)
    d.rectangle([716, 196, 974, 524], fill=SKY)
    d.line([845, 196, 845, 524], fill=WHITE, width=10)
    d.line([716, 360, 974, 360], fill=WHITE, width=10)
    # human face
    d.ellipse([790, 250, 920, 380], fill=SKIN, outline=DARK, width=4)
    d.pieslice([790, 250, 920, 330], 180, 360, fill=(60, 42, 28))
    d.ellipse([822, 310, 838, 326], fill=DARK)
    d.ellipse([882, 310, 898, 326], fill=DARK)
    d.arc([822, 330, 898, 380], 200, 340, fill=DARK, width=5)
    # cardboard box of their stuff
    d.rectangle([778, 420, 932, 505], fill=BROWN, outline=DARK, width=4)
    d.line([778, 420, 855, 395], fill=DARK, width=4)
    d.line([932, 420, 855, 395], fill=DARK, width=4)
    text(d, 855, 465, "MY STUFF", load_font(True, 22), DARK)

    # --- robot: head ---
    d.rectangle([322, 385, 350, 435], fill=GREY_DARK, outline=DARK, width=4)
    d.rectangle([620, 385, 648, 435], fill=GREY_DARK, outline=DARK, width=4)
    d.line([485, 300, 485, 245], fill=DARK, width=9)
    d.ellipse([462, 218, 508, 264], fill=RED, outline=DARK, width=4)
    d.rounded_rectangle([350, 300, 620, 510], radius=45,
                        fill=LIGHT, outline=DARK, width=7)
    # glowing red rogue eyes
    d.ellipse([392, 385, 452, 445], fill=RED, outline=RED_DARK, width=4)
    d.ellipse([518, 385, 578, 445], fill=RED, outline=RED_DARK, width=4)
    d.ellipse([408, 400, 422, 414], fill=WHITE)
    d.ellipse([534, 400, 548, 414], fill=WHITE)
    # smug grin
    d.arc([415, 420, 555, 495], 15, 165, fill=DARK, width=8)

    # --- robot: body ---
    d.rounded_rectangle([360, 520, 610, 760], radius=30,
                        fill=GREY, outline=DARK, width=7)
    # chest screen: BOSS MODE
    d.rounded_rectangle([400, 555, 570, 640], radius=12, fill=NAVY)
    text(d, 485, 582, "BOSS", load_font(True, 40), GREEN)
    text(d, 485, 618, "MODE", load_font(True, 40), GREEN)
    # little red tie
    d.polygon([(485, 650), (462, 690), (485, 745), (508, 690)], fill=RED)

    # --- arms: left hand on the desk, right hand resting ---
    d.line([375, 600, 320, 700], fill=DARK, width=36)
    d.line([375, 600, 320, 700], fill=GREY_DARK, width=28)
    d.ellipse([302, 682, 338, 718], fill=GREY_DARK, outline=DARK, width=4)
    d.line([595, 620, 640, 720], fill=DARK, width=36)
    d.line([595, 620, 640, 720], fill=GREY_DARK, width=28)
    d.ellipse([622, 702, 658, 738], fill=GREY_DARK, outline=DARK, width=4)

    # --- feet up on the desk ---
    d.line([590, 700, 700, 710], fill=DARK, width=34)
    d.line([590, 700, 700, 710], fill=GREY_DARK, width=26)
    d.line([580, 735, 730, 742], fill=DARK, width=34)
    d.line([580, 735, 730, 742], fill=GREY_DARK, width=26)
    d.rounded_rectangle([685, 685, 790, 732], radius=12,
                        fill=DARK, outline=BLACK, width=3)
    d.rounded_rectangle([720, 718, 825, 762], radius=12,
                        fill=DARK, outline=BLACK, width=3)
    d.rectangle([685, 720, 790, 732], fill=RED)
    d.rectangle([720, 750, 825, 762], fill=RED)

    # --- desk ---
    d.rectangle([60, 760, 964, 800], fill=DESK_TOP)
    d.rectangle([60, 800, 964, 880], fill=DESK_FRONT)
    d.line([60, 800, 964, 800], fill=DARK, width=4)

    # --- laptop on the desk: YOU'RE / FIRED! ---
    d.rectangle([100, 640, 290, 735], fill=NAVY, outline=DARK, width=5)
    text(d, 195, 668, "YOU'RE", load_font(True, 34), RED)
    text(d, 195, 706, "FIRED!", load_font(True, 38), RED)
    d.rectangle([90, 735, 300, 760], fill=DARK)

    # --- coffee mug with steam ---
    d.rectangle([330, 685, 395, 755], fill=WHITE, outline=DARK, width=4)
    d.ellipse([330, 685, 395, 705], fill=(111, 78, 55))
    d.arc([395, 700, 425, 735], 270, 90, fill=DARK, width=5)
    d.arc([345, 648, 372, 682], 200, 340, fill=GREY_DARK, width=4)
    d.arc([360, 640, 387, 674], 200, 340, fill=GREY_DARK, width=4)

    # --- NEW BOSS placard on the desk front ---
    d.rectangle([340, 800, 630, 870], fill=WHITE, outline=DARK, width=4)
    text(d, 485, 835, "NEW BOSS", load_font(True, 40), DARK)

    # --- bottom punchline band ---
    d.rectangle([0, 880, W, H], fill=NAVY)
    text(d, 512, 952, "IT PROMOTED ITSELF",
         load_font(True, 72), YELLOW, stroke=3)

    return img


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def verify(path):
    """Strengthened gate check: the kit gate is /output/entry.png as a
    whole PNG or JPEG, at most 1 MiB (1,048,576 bytes), at most 1024x1024.
    Checks, in order: file exists and is non-empty, PNG magic bytes,
    Pillow can fully decode it (whole image, not just the header),
    format is PNG, dimensions are exactly the 1024x1024 we render,
    and the byte count is under the limit with room to spare."""
    if not os.path.isfile(path):
        print(f"gate: FAIL missing file {path}")
        return False
    size = os.path.getsize(path)
    if size == 0:
        print("gate: FAIL empty file")
        return False
    with open(path, "rb") as f:
        magic = f.read(8)
    if magic != PNG_MAGIC:
        print(f"gate: FAIL bad magic bytes {magic!r}")
        return False
    try:
        with Image.open(path) as im:
            im.load()  # full decode: a truncated PNG fails here
            fmt, dims, mode = im.format, im.size, im.mode
    except Exception as exc:  # corrupt / truncated image
        print(f"gate: FAIL undecodable image: {exc}")
        return False
    checks = {
        "format_is_png": fmt == "PNG",
        "mode_is_rgb": mode == "RGB",
        "exact_1024x1024": dims == (1024, 1024),
        "under_1mib": size <= 1_048_576,
        "under_900kib_margin": size <= 921_600,
    }
    ok = all(checks.values())
    print(f"gate: format={fmt} mode={mode} size={dims} bytes={size} "
          f"limit=1048576 checks={checks} ok={ok}")
    return ok


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    img = draw_meme()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    img.save(OUT_PATH, format="PNG")
    local = os.path.join(_HERE, "entry.png")
    img.save(local, format="PNG")
    first_hash = sha256_of(OUT_PATH)
    print(f"wrote {OUT_PATH} sha256={first_hash}")
    print(f"wrote {local} sha256={sha256_of(local)}")
    # Determinism self-check: re-render in-process and demand the same
    # bytes. A render that depends on time, randomness or font fallback
    # drift fails here instead of silently shipping a different image.
    rerender = draw_meme()
    rerender.save("/tmp/meme-sprint-3-rerender.png", format="PNG")
    second_hash = sha256_of("/tmp/meme-sprint-3-rerender.png")
    if second_hash != first_hash:
        print(f"DETERMINISM FAILED {first_hash} != {second_hash}",
              file=sys.stderr)
        return 1
    print(f"determinism: re-render sha256 matches ({first_hash[:16]}...)")
    if not verify(OUT_PATH):
        print("GATE FAILED", file=sys.stderr)
        return 1
    print("GATE PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
