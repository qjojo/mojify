from read import load_img
import os
import sys
import csv


# color picking algorithm

class Emoji:
    def __init__(self, number):
        # the 0x is silent
        path = os.path.normpath(sys.argv[1] + '\\' + hex(number)[2:] + '.png')
        print(path)
        self.image = load_img(path)
        self.ordinal = number
        self.avg = (0, 0, 0)
        self.get_avg()
        self.mode = (0, 0, 0)
        self.get_mode()

    def get_avg(self):
        # get the average color of the emoji
        size = self.image.size
        pix = self.image.load()
        for x in range(0, size[0]):
            for y in range(0, size[1]):
                pixel = pix[x, y]
                if pixel[3] != 0:
                    self.avg = [sum(a) for a in zip(self.avg[:3], pixel)]
        n_pixels = size[0] * size[1]
        self.avg = tuple(map(lambda band: band // n_pixels, self.avg))

    def get_mode(self):
        # as in the statistical mode, if for some reason you want it instead
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
        mode_count = 0
        for key in colors.keys():
            if colors[key] > mode_count:
                self.mode = key[:3]
                mode_count = colors[key]


if __name__ == '__main__':
    with open('proc.csv', '+w', newline='') as out:
        writer = csv.writer(out)
        moji = Emoji(0x1f346)
        writer.writerow([hex(moji.ordinal), str(moji.avg), str(moji.mode)])
