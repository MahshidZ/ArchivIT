from pylab import imread, imsave
from image_processing.util_archiveIT import preprocessing, remove_object_from_image
from algorithms.thinning import zhangSuen_vec
from image_processing.lineProcessing import get_image_line
from image_processing.logoProcessing import get_image_logo
from image_processing.textProcessing import get_image_text
from pylab import imread, mean, imsave
from os import listdir
from os.path import isfile, join
import sys
import numpy
import scipy

def thumbnail_construction_for_files_in_directory(target_foldername, destination_foldername):
	scanned_image_file_name = [ f for f in listdir(target_foldername) if isfile(join(target_foldername,f)) ]

	for file_name in scanned_image_file_name:
		if(file_name[-4:] == '.png'):
			original_image = imread(target_foldername + file_name)
			thumbnail = construct_thumbnail(original_image)
			print thumbnail
			print destination_foldername+file_name[0:-4]+'.png'
			scipy.misc.imsave(destination_foldername+file_name[0:-4]+'.png', thumbnail)


def construct_thumbnail(original_image):
	# parameters
	resize_x = 1000
	thinning_iteration = 3
	line_segment_size = 15
	line_variation = 2
	line_margin = 5
	line_minlength = 60
	line_line_connected = 4
	removing_margin = 5
	logo_min_density = 0.1
	logo_min_size_x = 60
	logo_min_size_y = 60
	text_word_distance = 100
	text_min_size_x = 10
	text_min_size_y = 50
	thumbnail_size_x = 100
	debug = 1
		
	image_thresholded = preprocessing(original_image, resize_x)
	image_thinned = zhangSuen_vec(image_thresholded.astype(int), thinning_iteration) > 0
	image_thinned = image_thinned.astype(int)

	lines = get_image_line(image_thinned, line_segment_size, line_variation, 
		line_margin ,line_minlength, line_line_connected )
	image_line_removed = remove_object_from_image(image_thresholded.copy(), 
		lines, removing_margin, 0)

	logos = get_image_logo(image_line_removed, logo_min_density, 
		logo_min_size_x, logo_min_size_y)
	image_logo_removed = remove_object_from_image(image_line_removed.copy(), logos, removing_margin, 0)

	text = get_image_text(image_logo_removed, text_word_distance, text_min_size_x, text_min_size_y) 
	
	thumbnail_size_y = int(thumbnail_size_x / float(len(image_thresholded)) * len(image_thresholded[0]))
	thumbnail = _construct_thumbnail_image([len(image_thresholded), 
		len(image_thresholded[0])], lines, logos, text, 
		[thumbnail_size_x, thumbnail_size_y])

	if debug == 1:
		imsave("resultSteps/thresholded.png", image_thresholded)
		imsave("resultSteps/thinnedImage.png", image_thinned)
		imsave("resultSteps/linesRemoved.png", image_line_removed)
		imsave("resultSteps/logoRemoved.png", image_logo_removed)

	return thumbnail

def _construct_thumbnail_image(image_size, line, logo, text, thumbnail_size):
	thumbnail_image = numpy.zeros((thumbnail_size[0], thumbnail_size[1],3))
	
	ratio_x = float(thumbnail_size[0]) / float(image_size[0])
	ratio_y = float(thumbnail_size[1]) / float(image_size[1])
	
	for l in text:
		text_position = ((round(float(l[0]) * ratio_x), round(float(l[1]) * ratio_y), 
			round(float(l[2]) * ratio_x), round(float(l[3]) * ratio_y)))
		thumbnail_image[text_position[0]:text_position[2]+1, 
			text_position[1]:text_position[3]+1,0] = 1

	for l in logo:
		logo_position = ((round(float(l[0]) * ratio_x), round(float(l[1]) * ratio_y), 
			round(float(l[2]) * ratio_x), round(float(l[3]) * ratio_y)))
		thumbnail_image[logo_position[0]:logo_position[2]+1, 
			logo_position[1]:logo_position[3]+1,1] = 1

	for l in line:
		line_position = ((round(float(l[0]) * ratio_x), round(float(l[1]) * ratio_y), 
			round(float(l[2]) * ratio_x), round(float(l[3]) * ratio_y)))
		thumbnail_image[line_position[0]:line_position[2]+1, 
			line_position[1]:line_position[3]+1,2] = 1

		
	return thumbnail_image
