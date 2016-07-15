from PIL import Image


def load_img(image):
    im = Image.open(image).convert('RGBA')
    return im

if __name__ == '__main__':
    poke = load_img('147.png')
    size = poke.size
    avg_color = 0
    pix = poke.load()
    for x in range(0, size[0]):
        for y in range(0, size[1]):
            pixel = pix[x, y]
            if pixel != (0, 0, 0, 0):
                print(pixel)
