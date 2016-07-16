from PIL import Image
import csv
from ast import literal_eval as make_tuple
from math import sqrt


def load_img(image):
    im = Image.open(image).convert('RGBA')
    return im


def color_distance(c_tuple1, c_tuple2):
    red_mean = (c_tuple1[0] + c_tuple2[0]) / 2
    red = c_tuple1[0] - c_tuple2[0]
    green = c_tuple1[1] - c_tuple2[1]
    blue = c_tuple1[2] - c_tuple2[2]
    delta = (2 + (red_mean / 256)) * (red ** 2)
    delta += (4 * (green ** 2))
    delta += (2 + ((255 - red_mean) / 256)) * (blue ** 2)
    delta = sqrt(delta)
    return delta


def write_out(text_matrix):
    with open('out.txt', '+w', encoding='utf-8') as out:
        for line in text_matrix:
            line_out = ''
            for char in line:
                # TODO: ZWJ support
                if char is None:
                    line_out += '\u2001\u2006'
                else:
                    char_code = '0x' + char
                    char_code = int(char_code, base=16)
                    line_out += chr(char_code)
            out.writelines(line_out + '\n')

if __name__ == '__main__':
    emoji_list = []
    with open('proc.csv') as raw_list:
        emoji_list = []
        reader = csv.reader(raw_list)
        raw_list = list(reader)
    for entry in raw_list:
            emoji_list.append([entry[0],
                               make_tuple(entry[1]),
                               make_tuple(entry[2]),
                               make_tuple(entry[3])])
    poke = load_img('snight_med.png')
    size = poke.size
    avg_color = 0
    pix = poke.load()
    emoji_grid = []
    for y in range(0, size[1]):
        emoji_grid.append([])
        for x in range(0, size[0]):
            pixel = pix[x, y]
            best_delta = float('Inf')
            for entry in emoji_list:
                emoji_color = entry[1]
                if pixel[3] == 0:
                    best = None
                else:
                    delta = color_distance(emoji_color, pixel)
                    if delta < best_delta:
                        best = entry[0]
                        best_delta = delta
            emoji_grid[-1].append(best)
    write_out(emoji_grid)
