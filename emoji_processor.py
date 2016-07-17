from read import load_img, color_distance
from random import randint
import os
import sys
import csv
import argparse


# color comprehension algorithm

class Emoji:
    def __init__(self, number, alg):
        # is handling args here bad practice? i don't know!!
        path = os.path.normpath(args.path + '\\' + number + '.png')
        self.image = load_img(path)
        self.ordinal = number
        self.dom = (0, 0, 0)
        if alg == 'average':
            self.get_avg()
        elif alg == 'mode':
            self.get_mode()
        else:
            self.get_kmeans()

    def get_avg(self):
        # get the average color of the emoji
        # average tends to work best
        def alpha_handling(px_tuple):
            px = list(px_tuple)
            for band in px[:3]:
                band += (255 - px[3])
                if band < 255:
                    band = 255
            return tuple(px)
        size = self.image.size
        pix = self.image.load()
        for x in range(0, size[0]):
            for y in range(0, size[1]):
                pixel = pix[x, y]
                pixel = alpha_handling(pixel)
                self.dom = [sum(a) for a in zip(self.dom[:3], pixel)]
        n_pixels = size[0] * size[1]
        self.dom = tuple(map(lambda band: band // n_pixels, self.dom))
        self.dom = tuple(map(int, self.dom))

    def get_mode(self):
        # as in the statistical mode, not image mode
        # TODO: add fuzziness options so that colors that aren't very different
        # are counted as the same
        size = self.image.size
        pix = self.image.load()
        colors = {}
        for x in range(0, size[0]):
            for y in range(0, size[1]):
                pixel = pix[x, y]
                if pixel[3] != 0:
                    if pixel not in colors.keys():
                        colors[pixel] = 1
                    else:
                        colors[pixel] += 1
                        if pixel[3] != 255:
                            colors[pixel] -= pixel[3] / 255
        mode_count = 0
        for key in colors.keys():
            if colors[key] > mode_count:
                self.dom = key[:3]
                mode_count = colors[key]
        self.dom = tuple(map(int, self.dom))

    def get_kmeans(self):
        # XXX: Its broken, only picks null
        # heavily commented because this is my first time doing this
        size = self.image.size
        pix = self.image.load()
        # Most emoji dont use more than 3 colors, if that many
        pixel_list = []
        sensitivity = 20
        k = 3
        for x in range(0, size[0]):
            for y in range(0, size[1]):
                pixel_list.append(pix[x, y])
        # pick starting centroids
        centroids = [tuple([randint(0, 255)] * 3)] * k
        # begin iterations
        converged = False
        while not converged:
            # assign to centroids
            centroid_bins = [[0] * 3] * k
            centroid_bins_count = [float('Inf')] * k
            converged = True
            for pixel in pixel_list:
                if pixel[3] == 0:
                    for band in pixel[:3]:
                        band += 255 - pixel[3]
                nearest_distance = float('Inf')
                for i in range(0, k):
                    dist = color_distance(pixel[:3], centroids[i])
                    if dist < nearest_distance:
                        nearest_distance = dist
                        nearest = i
                centroid_bins[nearest] = [sum(a) for a in
                                          zip(centroid_bins[nearest],
                                              pixel[:3])]
                centroid_bins_count[nearest] += 1
            # recalculate centroids
            old_centroids = centroids[:]
            for i in range(0, k):
                scratch = centroid_bins[i]
                scratch = map(lambda x: x // centroid_bins_count[i], scratch)
                neg_scratch = map(lambda x: x * -1, scratch)
                centroids[i] = tuple(scratch)
                delta_c = [sum(a) for a in zip(old_centroids[i], neg_scratch)]
                if sum(map(abs, delta_c)) > sensitivity:
                    converged = False
        mode_centroid = centroid_bins_count.index(
            max(centroid_bins_count))
        self.dom = mode_centroid


def color_magnitude(c_tuple):
    return color_distance(c_tuple, tuple([0] * len(c_tuple)))


def get_all():
    return [f for f in os.listdir(path) if f[-3:] == 'png']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute color information')
    parser.add_argument('path', help='path to emoji pngs')
    parser.add_argument('-a', '--algorithm', metavar='algorithm',
                        help='color analysis algorithm (default: average)',
                        choices=['average', 'mode', 'kmeans'],
                        default='average',
                        required=False)
    args = parser.parse_args()
    path = os.path.normpath(args.path + '\\')
    file_list = get_all()
    with open('proc.csv', '+w', newline='') as out:
        writer = csv.writer(out)
        for moji_name in file_list:
            if '-' not in moji_name:
                moji = Emoji(moji_name[:-4], args.algorithm)
                writer.writerow([moji.ordinal, str(moji.dom)])
