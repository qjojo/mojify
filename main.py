from PIL import Image
import csv
from ast import literal_eval as make_tuple
from math import sqrt
import argparse
import os.path


def load_img(image):
    # load an image as a PIL object
    im = Image.open(image).convert('RGBA')
    return im


def color_distance(c_tuple1, c_tuple2):
    # calculate the color distance between two rgb tuples
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
    # write out emoji grid to txt file
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


def gen_matrix(pix_data):
    # generate unicode data from colors
    pix = pix_data.load()
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
    return emoji_grid


def handle_arguments():
    parser = argparse.ArgumentParser(
        description='Represent an image using emoji'
    )
    parser.add_argument('image', help='image to be processed')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = handle_arguments()
    path = args.image
    emoji_list = []
    with open('proc.csv') as raw_list:
        emoji_list = []
        reader = csv.reader(raw_list)
        raw_list = list(reader)
    for entry in raw_list:
            emoji_list.append([entry[0], make_tuple(entry[1])])
    image = load_img(path)
    size = image.size
    emoji_grid = gen_matrix(image)
    write_out(emoji_grid)
    print('Output in out.txt')
