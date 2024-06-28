import os
import numba
import argparse
import numpy as np
from skimage import io
from pdf2image import convert_from_path

parser = argparse.ArgumentParser(description='Remove Watermark')
parser.add_argument('--source', default='source.pdf', type=str,help='source file')
parser.add_argument('--target', default='out', type=str,help='target dir')

@numba.jit(nopython=True) 
def handle(img):
    shape = img.shape
    img = img.reshape(-1,3)
    for i in range(img.shape[0]):
        if 175 < img[i][0] < 250 and 175 < img[i][1] < 250 and 175 < img[i][2] < 250:
            img[i] = [255, 255, 255]
    img = img.reshape(shape)
    return img

if __name__ == '__main__':

    args = parser.parse_args()

    if not os.path.exists(args.target):
        os.mkdir(args.target)

    images = np.array(convert_from_path(args.source))

    for i in range(len(images)):      
        io.imsave(os.path.join(args.target,'{}.jpg').format(i+1), handle(images[i]))