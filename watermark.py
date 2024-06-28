# Import necessary libraries
import os
import numba
import argparse
import numpy as np
from PIL import Image
from skimage import io
from pdf2image import convert_from_path

# Create an argument parser for command line arguments
parser = argparse.ArgumentParser(description='Remove Watermark')
# source file path
parser.add_argument('--source', default='source.pdf', type=str, help='source file')
# target directory
parser.add_argument('--target', default='out', type=str, help='target directory')

# numba's JIT decorator for speed
@numba.jit(nopython=True) 
def handle(img):
    shape = img.shape
    # Turn the image into a one-dimensional array and avoid loops that are too deep for nesting
    img = img.reshape(-1, 3)
    for i in range(img.shape[0]):
        # If the RGB values of the pixel are between 175 and 250, assume it's part of the watermark and set it to white
        if 175 < img[i][0] < 250 and 175 < img[i][1] < 250 and 175 < img[i][2] < 250:
            img[i] = [255, 255, 255]
    # Reshape the image back
    img = img.reshape(shape)
    return img

if __name__ == '__main__':
    # Parse command line arguments
    args = parser.parse_args()

    # Check if the target directory exists, and create it if it does not
    if not os.path.exists(args.target):
        os.mkdir(args.target)

    # Get the file extension of the source file
    fileext = os.path.splitext(os.path.basename(args.source))[1]
    # Handle different image formats based on the file extension
    if fileext == '.jpg':
        img = io.imread(args.source)
        io.imsave(os.path.join(args.target, 'result{}'.format(fileext)), handle(img))
    elif fileext == '.png':
        # Read the png and convert it to RGB mode
        img = np.array(Image.open(args.source).convert('RGB'))
        io.imsave(os.path.join(args.target, 'result{}'.format(fileext)), handle(img))
    elif fileext == '.pdf':
        # Convert the pdf file to a list of images
        imgs = np.array(convert_from_path(args.source))
        # Iterate over the list of images, process each one, and save it
        for i in range(len(imgs)):
            io.imsave(os.path.join(args.target, '{}.jpg').format(i + 1), handle(imgs[i]))
    else:
        # If the file format is not supported, print an error message
        print('Unsupported file format')