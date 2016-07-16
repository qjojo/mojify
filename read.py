from PIL import Image
import csv
from ast import literal_eval as make_tuple
from math import sqrt


def load_img(image):
    im = Image.open(image).convert('RGBA')
    return im

if __name__ == '__main__':
    emoji_list = []
    with open('proc.csv') as raw_list:
        emoji_list = []
        reader = csv.reader(raw_list)
        raw_list = list(reader)
    for entry in raw_list:
            emoji_list.append([entry[0],
                               make_tuple(entry[1]),
                               make_tuple(entry[2])])
    poke = load_img('147.png')
    size = poke.size
    avg_color = 0
    pix = poke.load()
    emoji_grid = []
    # XXX: this currently gives a reversed emoji grid (xy swapped)
    for x in range(0, size[0]):
        emoji_grid.append([])
        for y in range(0, size[1]):
            pixel = pix[x, y]
            best_delta = float('Inf')
            for entry in emoji_list:
                emoji_color = entry[1]
                if pixel[3] == 0:
                    best = None
                else:
                    # this is a color comparison algorithm i shamelessly stole
                    # from http://www.compuphase.com/cmetric.htm
                    # i had the idea to use vector distance but i googled it
                    # and someone else had already done it ¯\_(ツ)_/¯
                    red_mean = (emoji_color[0] + pixel[0]) / 2
                    red = emoji_color[0] - pixel[0]
                    green = emoji_color[1] - pixel[1]
                    blue = emoji_color[2] - pixel[2]
                    delta = (2 + (red_mean / 256)) * (red ** 2)
                    delta += (4 * (green ** 2))
                    delta += (2 + ((255 - red_mean) / 256)) * (blue ** 2)
                    delta = sqrt(delta)
                    if delta < best_delta:
                        best = entry[0]
                        best_delta = delta
            emoji_grid[-1].append(best)
    with open('out.txt', '+w', encoding='utf-8') as out:
        for line in emoji_grid:
            line_out = ''
            for char in line:
                if char is None:
                    line_out += '⬜'
                else:
                    if '-' in char:
                        char = char[:char.index('-')]
                    char_code = '0x' + char
                    char_code = int(char_code, base=16)
                    line_out += chr(char_code)
            out.writelines(line_out + '\n')
