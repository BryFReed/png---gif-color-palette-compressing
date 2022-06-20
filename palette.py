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

def clumping(arry, closeness):
    # do the pixels in teh array devided by 255 as the max clump, then clump together the things in the sorted array that are super simalr, but not a biger clump then the previous decided size.
    max_clump = len(arry)//255
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
        if len(aux) == 255:
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


def palatte(file):
    r = png.Reader(filename=file)
    reader = r.read()
    img_info = []
    for row in reader[2]:
        for pix in row:
            img_info.append(pix)
    histog = histo(img_info)
    clumps = clumping(histog, 12)
    fin = []
    for item in clumps:
        fin.append(thinning(item))
    return fin


def main():
    print(palatte(r"C:\Users\bryan\OneDrive\Desktop\57-570732_transparent-black-faded-circle-png-gradient-red-ombre.png"))


if __name__ == '__main__':
    main()

