import numpy
import scipy.signal as signal
from pylab import imread, mean, imsave
from scipy.ndimage.measurements import label


def get_image_text(image, word_distance, min_text_size_x, min_text_size_y):
	text_enhance_filter  = numpy.ones((1,word_distance))
	
	image_text_enhanced = signal.convolve(image, text_enhance_filter, mode='same') > 0
	
	image_text = []
	image_text_component, lablenumber = label(image_text_enhanced)
	for i in range(1, lablenumber):
		component_size_x = max(numpy.where(image_text_component == i)[0]) - \
							min(numpy.where(image_text_component == i)[0])
		component_size_y = max(numpy.where(image_text_component == i)[1]) - \
							min(numpy.where(image_text_component == i)[1])
		if(component_size_x > min_text_size_x and component_size_y > min_text_size_y):
			text_position_x = (max(numpy.where(image_text_component == i)[0]) + \
				min(numpy.where(image_text_component == i)[0]))/2
			text_position_y_top = min(numpy.where(image_text_component == i)[1]) + word_distance
			text_position_y_bottom = max(numpy.where(image_text_component == i)[1]) - word_distance
			image_text.append((text_position_x, text_position_y_top, 
				text_position_x, text_position_y_bottom))
			
	return image_text