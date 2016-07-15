from read import load_img
import os
import sys
import csv


# color picking algorithm

class Emoji:
    def __init__(self, number):
        # is handling args here bad practice? i don't know!!
        path = os.path.normpath(sys.argv[1] + '\\' + number + '.png')
        self.image = load_img(path)
        self.ordinal = number
        self.avg = (0, 0, 0)
        self.get_avg()
        self.mode = (0, 0, 0)
        self.get_mode()

    def get_avg(self):
        # get the average color of the emoji
        # mode generally works better, median might be even better but i'm lazy
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
        mode_count = 0
        for key in colors.keys():
            if colors[key] > mode_count:
                self.mode = key[:3]
                mode_count = colors[key]


def get_all():
    return [f for f in os.listdir(path) if f[-3:] == 'png']

if __name__ == '__main__':
    path = os.path.normpath(sys.argv[1] + '\\')
    file_list = get_all()
    with open('proc.csv', '+w', newline='') as out:
        writer = csv.writer(out)
        for moji_name in file_list:
            moji = Emoji(moji_name[:-4])
            writer.writerow([moji.ordinal, str(moji.avg), str(moji.mode)])
