from PIL import Image, ImageDraw
from random import randint, choice

w, h = 1024, 4096
colorS = [
    (255, 255, 255), (200, 150, 255), (255, 255, 150), (255, 100, 100), (150, 255, 150)
]


def main():
    for _ in range(1, len(colorS) + 1):
        new_image = Image.new("RGB", (w, h), (0, 0, 30))
        draw = ImageDraw.Draw(new_image)
        for i in range(1000):
            x, y = randint(0, w - 10), randint(0, h - 10)
            draw.ellipse((x, y, x + 10, y + 10), outline='black', fill=colorS[_ - 1])

        new_image.save(f'data/bg{_}.png', "PNG")


def dop():
    new_image = Image.new("RGB", (w, h), (0, 0, 30))
    draw = ImageDraw.Draw(new_image)
    for i in range(1000):
        x, y = randint(0, w), randint(0, h)
        draw.ellipse((x, y, x + 10, y + 10), outline='black', fill=choice(colorS))

    new_image.save(f'data/bg6.png', "PNG")


main()
dop()
