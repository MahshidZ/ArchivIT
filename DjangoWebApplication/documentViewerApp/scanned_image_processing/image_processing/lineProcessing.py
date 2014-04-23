from util_archiveIT import bresenham
import pymorph 
import numpy
import scipy.signal as signal
from pylab import imread, mean, imsave
import math
from random import randint

def _get_line_filter(segment_size, variation):
	"""Computes the filters that can be used to enhance vertical lines in 
	an Image.

	Args:
		segment_size: Size of the segment
		variatoin: Variation in horizontal axes if user wants not exact
		vertical lines.
	Returns:
		filters saved in 3D matrices, each 3rd dimension includes a filter
	"""

	smalldisk = pymorph.sedisk(1);
	bigdisk = pymorph.sedisk(2);
	
	horizontal_filter = numpy.zeros((variation*2+1, variation*2+1, segment_size))
	horizontal_surrounding = numpy.zeros((variation*2+1, variation*2+1, segment_size))

	index = -1

	# Generates the filters for each direction of lines
	for variation_index in range(-variation, variation + 1):
		index = index + 1;
		points = bresenham(variation + variation_index,0, variation - variation_index, segment_size - 1)
		tmp = numpy.zeros((variation*2+1)*segment_size).reshape((variation*2+1, segment_size))
		for point_ind in range(0, len(points)):
			tup_point = points[point_ind]
			tmp[tup_point[0], tup_point[1]] = 1
		tmp_filter = pymorph.dilate(pymorph.binary(tmp), smalldisk)
		tmp_surrounding = pymorph.subm(pymorph.dilate(pymorph.binary(tmp), bigdisk) , \
			pymorph.dilate(pymorph.binary(tmp), smalldisk))
		horizontal_filter[index,:,:] = tmp_filter
		horizontal_surrounding[index,:,:] = tmp_surrounding
	
	return horizontal_filter, horizontal_surrounding
	
	
def _get_horizontal_lines(image, segment_size, variation, margin, line_connected):
	"""Filter the image with horizontal filters 
	Args:
		image: the input image
		segment_size: size of the segments that are search to find a line within
		variation: variation allowed to lines to be angled
		margin: margin of the image for searching for lines
		line_connected: a maximum accepted distance between two segment line 
						to attach them together
	Returns:
		The list of horizontal lines in the image
	"""
	# Get the filters 
	horizontal_filter, horizontal_surrounding = _get_line_filter(segment_size, variation)

	# Amount of points that should appear "on" the line
	online_thr = 0.75 * segment_size;
	# Amount of points that shouldn't be "around" the line
	surround_thr = 0.02 * segment_size;

	# Filter the image with the the first filter
	image_line_filter = signal.convolve(image, horizontal_filter[0,:,:], mode='same') > online_thr
	image_line_surrounding = signal.convolve(image, horizontal_surrounding[0,:,:], mode='same') < surround_thr
	image_line = (image_line_surrounding * image_line_filter).astype(int)
	
	# Go over all other filters and apply them to the image
	for i in range(1,len(horizontal_filter)):
		image_line_filter = signal.convolve(image,horizontal_filter[i,:,:], mode='same') > online_thr
		image_line_surrounding = signal.convolve(image,horizontal_surrounding[i,:,:], mode='same') < surround_thr
		image_line = image_line + (image_line_surrounding * image_line_filter).astype(int)

	# Sum up the result of all filters and threshold it by zero
	image_line = image_line > 0;

	# Go over all points in the filtered image and connect segments to each 
	# other.
	lines = []
	for j in range(segment_size/2+1,len(image_line[0])-segment_size/2-1):
		for i in range(margin,len(image_line) - margin):
			if(image_line[i, j]):
				if not lines:
					lines.append((i, j-segment_size/2, i, j+segment_size/2))
				else:
					hasfound = 0
					index = -1
					# Check the found line with those in the list and connect 
					# them if they are close and remove the one in the list 
					# and add the connected lines. 
					for eachline in lines:	
						index = index + 1					
						if (abs(eachline[0]-i) < variation and j-eachline[-1] < line_connected):
							newline = ((i+eachline[0])/2, eachline[1], (i+eachline[0])/2, j+segment_size/2)
							del lines[index]
							lines.append(newline)
							hasfound = 1
							break
					if hasfound == 0:
						lines.append((i, j-segment_size/2, i, j+segment_size/2))
				image_line[i-margin:i+margin,j-segment_size/2:j+segment_size/2] = 0
	
	return lines
	
def get_image_line(image, segment_size, variation, margin, minlength, line_connected):
	"""finds horizontal and vertical lines in an image
	Args:
		image: the input image
		segment_size: size of the segments that are search to find a line within
		variation: variation allowed to lines to be angled
		margin: margin of the image for searching for lines
		minlength: minimum accepted length of lines
		line_connected: a maximum accepted distance between two segment line 
						to attach them together
	Returns:
		The list of lines in the image
	"""

	# find horizontal lines
	horizontal_line = _get_horizontal_lines(image.copy(), segment_size, variation, margin, line_connected)
	# transpose the image and find horizontal lines which is actuall vertical lines
	image = image.transpose()
	vertical_line = _get_horizontal_lines(image.copy(), segment_size, variation, margin, line_connected)
	for lines in vertical_line:
		newline = (lines[1], lines[0], lines[3], lines[2])
		horizontal_line.append(newline)
		
	# Check all lines if they fulfill the minlength criteria
	all_lines = []
	for lines in horizontal_line:
		if(math.sqrt((lines[0]-lines[2])*(lines[0]-lines[2])+(lines[1]-lines[3])*(lines[1]-lines[3])) > minlength):
			all_lines.append(lines)
	
	return all_lines