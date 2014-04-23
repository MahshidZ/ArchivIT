import numpy

def neighbours_vec(image):
    """Computes the 8-neighbours of all pixels in the image

    Args:
        An image as an numpy array
    Returns:
        neighbours in image format
    """
    return image[2:,1:-1], image[2:,2:], image[1:-1,2:], image[:-2,2:], image[:-2,1:-1], image[:-2,:-2], image[1:-1,:-2], image[2:,:-2]

def transitions_vec(P2, P3, P4, P5, P6, P7, P8, P9):
    """Computes the transitions between 8-neighbours surroung pixels"""

    return (((P3-P2) > 0).astype(int) + ((P4-P3) > 0).astype(int) + \
            ((P5-P4) > 0).astype(int) + ((P6-P5) > 0).astype(int) + \
            ((P7-P6) > 0).astype(int) + ((P8-P7) > 0).astype(int) + \
            ((P9-P8) > 0).astype(int) + ((P2-P9) > 0).astype(int))
	
def zhangSuen_vec(image, iterations):
    """Computes a thined version of the given image

    Args:
        image: a binary image given in numpy array format
        iteration: number of iterations that thinning algorithm should be 
        performed
    Returns:
        The thinned image
    """

    for iter in range (1, iterations): # Main iterations of the thinning
    	print iter
    	# step 1: The first set of conditions from zhang Suen algorithm
        P2,P3,P4,P5,P6,P7,P8,P9 = neighbours_vec(image)
        condition0 = image[1:-1,1:-1]
        condition4 = P4*P6*P8
        condition3 = P2*P4*P6
        condition2 = transitions_vec(P2, P3, P4, P5, P6, P7, P8, P9) == 1
        condition1 = (2 <= P2+P3+P4+P5+P6+P7+P8+P9) * (P2+P3+P4+P5+P6+P7+P8+P9 <= 6)
        cond = (condition0 == 1) * (condition4 == 0) * (condition3 == 0) * \
                (condition2 == 1) * (condition1 == 1)
        changing1 = numpy.where(cond == 1)
        image[changing1[0]+1,changing1[1]+1] = 0
        # step 2: The second set of conditions from Zhang Suen algorithm
        P2,P3,P4,P5,P6,P7,P8,P9 = neighbours_vec(image)
        condition0 = image[1:-1,1:-1]
        condition4 = P2*P6*P8
        condition3 = P2*P4*P8
        condition2 = transitions_vec(P2, P3, P4, P5, P6, P7, P8, P9) == 1
        condition1 = (2 <= P2+P3+P4+P5+P6+P7+P8+P9) * (P2+P3+P4+P5+P6+P7+P8+P9 <= 6)
        cond = (condition0 == 1) * (condition4 == 0) * (condition3 == 0) * \
                (condition2 == 1) * (condition1 == 1)
        changing2 = numpy.where(cond == 1)
        image[changing2[0]+1,changing2[1]+1] = 0
    return image
