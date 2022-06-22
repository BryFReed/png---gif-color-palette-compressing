import sys

import png
import math

class Linked():
    def __init__(self, data):
        self.prev = None
        self.next = None
        self.data = data

def histo(arry):
    pix = {}
    aux = []
    fin = []
    # create dictionary with rgb as key and occerences are the value
    i = 0
    while i < len(arry) - 2:
        rgb = (arry[i], arry[i+1], arry[i+2])
        if rgb not in pix:
            pix[rgb] = 1
            aux.append(rgb)
        else:
            pix[rgb] += 1
        i += 3

    # get all the unique keys somewhere else so they can be all called to sort the array of rgb based on number of occurences
    for i in range(len(pix)):
        fin.append((aux[i], (pix[aux[i]])))
    fin.sort(key=lambda y: y[1])
    return fin

def clumping(arry, closeness, pal_count):
    # do the pixels in teh array devided by 255 as the max clump, then clump together the things in the sorted array that are super simalr, but not a biger clump then the previous decided size.
    if pal_count > len(arry):
        pal_count = len(arry)
    max_clump = len(arry)//pal_count
    aux = []
    trailer = Linked(None)
    header = Linked(None)
    curr = header
    for i in range(1, len(arry) + 1):
        curr.next = Linked(arry[-i])
        curr.next.prev = curr
        curr = curr.next
    curr.next = trailer
    curr.prev = curr
    start = header.next
    aux = []
    while start.next:
        tracker = start.next
        sub_aux = [start.data]
        while tracker.next:
            if abs(tracker.data[0][0] - start.data[0][0]) + abs(tracker.data[0][1] - start.data[0][1]) + abs(tracker.data[0][2] - start.data[0][2]) < closeness:
                sub_aux.append(tracker.data)
                temp = tracker.next
                tracker.prev.next = tracker.next
                tracker.next.prev = tracker.prev
                tracker = temp
            else:
                tracker = tracker.next
            if len(sub_aux) == max_clump:
                break
        aux.append(sub_aux)
        if len(aux) == pal_count:
            break
        start = start.next
    return aux

def thinning(sub_arr):
    temp_rgb = [0,0,0]
    big_num = 0
    for item in sub_arr:
        mult = int(item[1] ** (4 / 7))
        temp_rgb[0] += (item[0][0] * mult)
        temp_rgb[1] += (item[0][1] * mult)
        temp_rgb[2] += (item[0][2] * mult)
        big_num += mult
    for i in range(3):
        temp_rgb[i] /= big_num
    return (int(temp_rgb[0]), int(temp_rgb[1]), int(temp_rgb[2]))


def palatte(file, size):
    r = png.Reader(filename=file)
    reader = r.read()
    img_info = []
    for row in reader[2]:
        for pix in row:
            img_info.append(pix)
    histog = histo(img_info)
    clumps = clumping(histog, 15, size)
    fin = []
    for item in clumps:
        fin.append(thinning(item))
    return fin


def best_color(arry, pixel):
    best = 1000
    pix = ()
    for item in arry:
        if abs(item[0] - pixel[0]) + abs(item[1] - pixel[1]) + abs(item[2] - pixel[2]) < best:
            pix = item
            best = abs(item[0] - pixel[0]) + abs(item[1] - pixel[1]) + abs(item[2] - pixel[2])
    return pix

def recolor(file, size):
    sary = palatte(file, size)
    r = png.Reader(filename=file)
    img = r.read()
    rows = img[0]
    cols = img[1]
    alpha = img[3]['alpha']
    img_info = []
    count = 0
    for row in img[2]:
        for pix in row:
            if count != 3:
                img_info.append(pix)
                if alpha == True:
                    count += 1
            else:
                count = 0
    sub = []
    fin = []
    i = 0
    rlen = 3 * rows

    while i < len(img_info) - 2:
        bc = best_color(sary, (img_info[i], img_info[i+1], img_info[i+2]))
        sub.append(bc[0])
        sub.append(bc[1])
        sub.append(bc[2])
        if len(sub)  == rlen:
            fin.append(tuple(sub))
            sub = []
        i += 3

    f = open('neww.png', 'wb')
    w = png.Writer(rows, cols, greyscale=False)
    w.write(f, fin)
    f.close()
def main():
    file = sys.argv[1]
    size = int(sys.argv[2])
    recolor(file, size)


if __name__ == '__main__':
    main()

