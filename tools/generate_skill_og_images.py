"""Generate the four distinct Open Graph JPEGs for the Skill Hub."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1200, 630
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "images"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(size, bold=False, mono=False):
    return ImageFont.truetype(MONO if mono else BOLD if bold else FONT, size)


def gradient(top, bottom):
    image = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        draw.line((0, y, WIDTH, y), fill=color)
    return image


def text(draw, xy, value, size, color, *, bold=False, mono=False, anchor="la", spacing=8):
    draw.multiline_text(xy, value, font=font(size, bold, mono), fill=color, anchor=anchor, spacing=spacing)


def pill(draw, xy, value, fill, color, *, width=None):
    x, y = xy
    f = font(18, bold=True, mono=True)
    length = int(draw.textlength(value, font=f))
    box_width = width or length + 40
    draw.rounded_rectangle((x, y, x + box_width, y + 40), radius=20, fill=fill)
    draw.text((x + 20, y + 20), value, font=f, fill=color, anchor="lm")


def save(image, name):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT / name, format="JPEG", quality=94, optimize=True, progressive=True)


def book_summary():
    image = gradient((16, 36, 35), (32, 82, 72))
    draw = ImageDraw.Draw(image)
    # restrained paper grain
    for i in range(115):
        x = (i * 97) % WIDTH
        y = (i * 53) % HEIGHT
        draw.ellipse((x, y, x + 2, y + 2), fill=(75, 129, 114))
    pill(draw, (72, 56), "OPEN SOURCE SKILL", (225, 234, 222), (23, 63, 54))
    text(draw, (72, 147), "Book Summary\nSkill", 68, (246, 240, 219), bold=True, spacing=-2)
    text(draw, (77, 335), "книга → проверяемое саммари\nтекст · PDF · FB2 · один MP3", 25, (186, 221, 204), spacing=12)
    # Open book.
    draw.rounded_rectangle((676, 116, 1120, 494), radius=26, fill=(235, 223, 189))
    draw.polygon(((695, 144), (884, 178), (884, 458), (695, 428)), fill=(252, 247, 230))
    draw.polygon(((1110, 144), (901, 178), (901, 458), (1110, 428)), fill=(245, 238, 216))
    draw.line((893, 170, 893, 463), fill=(149, 126, 83), width=4)
    for y in range(212, 390, 35):
        draw.line((728, y, 846, y + 19), fill=(103, 151, 132), width=5)
        draw.line((936, y + 19, 1073, y), fill=(103, 151, 132), width=5)
    # Sound waveform leaves the book.
    for x in range(705, 1080, 14):
        amp = 16 + ((x * 13) % 45)
        if 844 < x < 949:
            amp += 35
        draw.line((x, 512 - amp, x, 512 + amp), fill=(232, 158, 86), width=6)
    text(draw, (72, 565), "PAVEL NASUTA  /  SKILL HUB", 15, (139, 197, 178), mono=True)
    save(image, "og-skill-book-summary.jpg")


def adaptive_support():
    image = gradient((18, 21, 56), (57, 42, 92))
    draw = ImageDraw.Draw(image)
    for radius, alpha in ((220, (47, 119, 147)), (150, (71, 152, 177)), (86, (129, 205, 192))):
        draw.ellipse((840 - radius, 305 - radius, 840 + radius, 305 + radius), outline=alpha, width=2)
    pill(draw, (72, 56), "OPEN SOURCE SKILL", (215, 229, 245), (33, 46, 103))
    text(draw, (72, 147), "Adaptive Support\nDialogue", 55, (241, 241, 252), bold=True, spacing=-1)
    text(draw, (77, 335), "прямой диалог с границами\nACT · КПТ · согласие на контекст", 25, (185, 203, 237), spacing=12)
    # Two layered dialogue shapes and an open route.
    draw.rounded_rectangle((690, 151, 1068, 307), radius=34, fill=(135, 207, 205))
    draw.polygon(((760, 306), (790, 306), (778, 342)), fill=(135, 207, 205))
    draw.rounded_rectangle((780, 306, 1132, 474), radius=34, fill=(238, 184, 206))
    draw.polygon(((1060, 472), (1092, 472), (1082, 506)), fill=(238, 184, 206))
    for x, y, width in ((727, 193, 183), (727, 239, 259), (817, 350, 227), (817, 397, 172)):
        draw.rounded_rectangle((x, y, x + width, y + 11), radius=5, fill=(38, 69, 105))
    # A deliberately incomplete line: dialogue does not force an answer.
    draw.line((652, 507, 718, 507, 754, 535, 830, 535), fill=(219, 232, 248), width=4)
    draw.ellipse((822, 527, 842, 547), fill=(219, 232, 248))
    text(draw, (72, 565), "PAVEL NASUTA  /  SKILL HUB", 15, (154, 179, 226), mono=True)
    save(image, "og-skill-adaptive-support.jpg")


def management_assistant():
    image = gradient((244, 237, 222), (224, 215, 195))
    draw = ImageDraw.Draw(image)
    for x in range(0, WIDTH, 56):
        draw.line((x, 0, x, HEIGHT), fill=(215, 204, 184), width=1)
    for y in range(0, HEIGHT, 56):
        draw.line((0, y, WIDTH, y), fill=(215, 204, 184), width=1)
    pill(draw, (72, 56), "PRIVATE PILOT", (34, 37, 44), (246, 235, 206))
    text(draw, (72, 147), "Ассистент\nруководителя", 70, (30, 35, 42), bold=True, spacing=-3)
    text(draw, (77, 335), "факт → решение → владелец → проверка", 25, (80, 78, 71))
    # Decision route with three precise stations.
    stations = [
        (670, 192, 248, "ФАКТ", (239, 200, 101)),
        (803, 317, 248, "РЕШЕНИЕ", (222, 101, 69)),
        (935, 192, 206, "ДЕЙСТВИЕ", (50, 57, 68)),
    ]
    draw.line((758, 288, 866, 386), fill=(59, 60, 58), width=7)
    draw.line((931, 386, 1024, 287), fill=(59, 60, 58), width=7)
    draw.polygon(((1021, 287), (998, 293), (1014, 313)), fill=(59, 60, 58))
    for x, y, w, label, color in stations:
        draw.rounded_rectangle((x, y, x + w, y + 96), radius=18, fill=color)
        text(draw, (x + 24, y + 28), label, 24, (246, 239, 222), bold=True)
        draw.line((x + 24, y + 68, x + w - 24, y + 68), fill=(246, 239, 222), width=3)
    text(draw, (72, 565), "PAVEL NASUTA  /  SKILL HUB", 15, (99, 93, 80), mono=True)
    save(image, "og-skill-management-assistant.jpg")


def anytype_agent():
    image = gradient((20, 35, 52), (38, 77, 92))
    draw = ImageDraw.Draw(image)
    for x in range(0, WIDTH, 48):
        draw.line((x, 0, x, HEIGHT), fill=(40, 92, 105), width=1)
    for y in range(0, HEIGHT, 48):
        draw.line((0, y, WIDTH, y), fill=(40, 92, 105), width=1)
    pill(draw, (72, 56), "PUBLIC REPOSITORY", (207, 235, 225), (22, 61, 67))
    text(draw, (72, 147), "Anytype Agent\nSkill", 68, (243, 247, 241), bold=True, spacing=-2)
    text(draw, (77, 335), "структура → поиск → проверяемая правка\nкарточки · схема · read-back", 25, (181, 220, 211), spacing=12)
    # A navigable object graph: connected cards and an inspected target.
    nodes = [(748, 195, 178, 92, (110, 205, 185), "SPACE"), (951, 151, 172, 92, (235, 186, 101), "MODEL"), (892, 365, 192, 96, (218, 130, 113), "VERIFY")]
    draw.line((835, 240, 951, 198), fill=(225, 240, 235), width=5)
    draw.line((1030, 243, 987, 365), fill=(225, 240, 235), width=5)
    draw.line((838, 287, 938, 365), fill=(225, 240, 235), width=5)
    for x, y, width, height, color, label in nodes:
        draw.rounded_rectangle((x, y, x + width, y + height), radius=18, fill=color)
        draw.rounded_rectangle((x + 18, y + 19, x + 59, y + 60), radius=11, fill=(22, 51, 60))
        text(draw, (x + 76, y + 25), label, 19, (22, 51, 60), bold=True)
        draw.line((x + 76, y + 65, x + width - 20, y + 65), fill=(22, 51, 60), width=3)
    # The small check mark is the difference between a plausible and verified change.
    draw.line((1058, 481, 1082, 505, 1131, 449), fill=(235, 241, 234), width=8)
    text(draw, (72, 565), "PAVEL NASUTA  /  SKILL HUB", 15, (145, 207, 196), mono=True)
    save(image, "og-skill-anytype-agent.jpg")


def art_directing_visuals():
    image = gradient((28, 55, 86), (17, 37, 61))
    draw = ImageDraw.Draw(image)
    pill(draw, (72, 56), "OPEN SOURCE SKILL", (245, 238, 212), (36, 58, 84))
    text(draw, (72, 147), "Art-directing\nvisuals", 68, (246, 242, 231), bold=True, spacing=-2)
    text(draw, (77, 335), "одна идея → читаемый визуал\nфакты · композиция · права", 25, (190, 215, 224), spacing=12)
    draw.polygon(((706, 130), (924, 173), (839, 347), (627, 299)), fill=(240, 200, 88))
    draw.rectangle((920, 161, 1108, 397), fill=(216, 96, 99))
    draw.ellipse((775, 331, 997, 553), fill=(230, 106, 58))
    draw.polygon(((1054, 414), (1140, 480), (1072, 558), (986, 492)), fill=(244, 241, 226))
    draw.rectangle((672, 116, 1127, 537), outline=(244, 241, 226), width=5)
    draw.line((694, 472, 1081, 196), fill=(25, 53, 80), width=7)
    draw.ellipse((1010, 257, 1032, 279), fill=(25, 53, 80))
    text(draw, (72, 565), "PAVEL NASUTA  /  SKILL HUB", 15, (147, 196, 213), mono=True)
    save(image, "og-skill-art-directing-visuals.jpg")


def skill_hub():
    image = gradient((22, 29, 63), (22, 59, 83))
    draw = ImageDraw.Draw(image)
    for x, y, r, color in ((1025, 92, 136, (72, 99, 188)), (1085, 164, 66, (93, 193, 198)), (895, 514, 182, (42, 114, 154))):
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
    pill(draw, (72, 56), "PRACTICAL AGENT SKILLS", (223, 239, 242), (24, 65, 85))
    text(draw, (72, 147), "Skills для\nAI-агентов", 76, (244, 247, 242), bold=True, spacing=-2)
    text(draw, (77, 335), "практика → переносимые навыки\nсценарии · онбординг · границы", 25, (183, 221, 225), spacing=12)
    # Modular catalogue cards, connected as a small system.
    cards = [
        (696, 196, 194, 116, (236, 189, 99), "BOOKS"),
        (918, 160, 194, 116, (126, 212, 203), "SUPPORT"),
        (848, 352, 194, 116, (205, 140, 186), "OPS"),
    ]
    draw.line((794, 254, 917, 218), fill=(235, 247, 246), width=4)
    draw.line((1015, 276, 946, 351), fill=(235, 247, 246), width=4)
    draw.line((844, 310, 912, 352), fill=(235, 247, 246), width=4)
    for x, y, w, h, color, label in cards:
        draw.rounded_rectangle((x, y, x + w, y + h), radius=20, fill=color)
        draw.rounded_rectangle((x + 18, y + 21, x + 65, y + 68), radius=12, fill=(26, 40, 67))
        text(draw, (x + 83, y + 30), label, 20, (24, 40, 67), bold=True)
        draw.line((x + 83, y + 70, x + w - 24, y + 70), fill=(24, 40, 67), width=3)
    text(draw, (72, 565), "PAVEL NASUTA  /  SKILL HUB", 15, (144, 205, 212), mono=True)
    save(image, "og-skills-hub.jpg")


if __name__ == "__main__":
    book_summary()
    adaptive_support()
    management_assistant()
    anytype_agent()
    art_directing_visuals()
    skill_hub()
    print("Generated 6 Skill Hub Open Graph images.")
