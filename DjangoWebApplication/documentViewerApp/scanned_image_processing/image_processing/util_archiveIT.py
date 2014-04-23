import scipy.signal as signal
import scipy
import numpy as np
import matplotlib.pyplot as plt
from pylab import imread, mean, imsave
from PIL import Image
import scipy.misc as misc
import math
#import mahotas

def gauss2D(shape=(3,3),sigma=0.5):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

def preprocessing(original_image, resize_x):

    if(original_image.ndim == 3):
        original_image = mean(original_image,2)

    smoothing_sigma = len(original_image)*0.0005;
    gaussian_filter = gauss2D((18,18), smoothing_sigma);
    smoothed_image = signal.convolve(original_image, gaussian_filter, mode = 'same');

    resize_y = int(resize_x/float(len(smoothed_image))*len(smoothed_image[0]))
    resized_image = misc.imresize(smoothed_image, (resize_x, resize_y), 'bilinear')
    thresholded_image = resized_image < resized_image.max()*0.4
    margin_removed_image = _remove_image_margin(thresholded_image)

    return margin_removed_image

def _remove_image_margin(image):
    image[0:5,] = 0
    image[-5:0,] = 0
    image[:,0:5] = 0
    image[:,-5:0] = 0
    return image
	
def bresenham(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points

def remove_object_from_image(image, object, margin, removing_value):
	for l in object:
		image[l[0] - margin:l[2] + margin,l[1] - margin:l[3] + margin] = removing_value
	return image
	
