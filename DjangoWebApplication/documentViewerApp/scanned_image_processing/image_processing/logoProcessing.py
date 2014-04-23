import numpy
from scipy.ndimage.measurements import label
def get_image_logo(image, min_density, min_logo_size_x, min_logo_size_y):
	image_logo_component, lablenumber = label(image > 0)
	
	image_logo = []
	for i in range(1, lablenumber):
		component_size_x = max(numpy.where(image_logo_component == i)[0]) - \
							min(numpy.where(image_logo_component == i)[0])+1
		component_size_y = max(numpy.where(image_logo_component == i)[1]) - \
							min(numpy.where(image_logo_component == i)[1])+1
		component_density = float(sum(sum(image_logo_component == i))) / \
							float(component_size_x*component_size_x)
		if(component_density > min_density and 
			component_size_x > min_logo_size_x and 
			component_size_y > min_logo_size_y):
			text_position_x_left = min(numpy.where(image_logo_component == i)[0])
			text_position_x_right = max(numpy.where(image_logo_component == i)[0])
			text_position_y_top = min(numpy.where(image_text_component == i)[1]) 
			text_position_y_bottom = max(numpy.where(image_text_component == i)[1]) 
			image_logo.append((text_position_x_left, text_position_y_top, 
				text_position_x_right, text_position_y_bottom))
	
	return image_logo