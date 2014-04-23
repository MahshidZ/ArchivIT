from os import listdir
from os.path import isfile, join
import sys
from pylab import imread, imsave
from thumbnailCreator import createThumbnail



def thumbnailForFolder(targetFolderName, destFolderName):
	origFiles = [ f for f in listdir(targetFolderName) if isfile(join(targetFolderName,f)) ]

	for files in origFiles:
		if(files[-4:] == '.png'):
			print(files)
			originalImage = imread(targetFolderName + files)
			thumbnail = createThumbnail(originalImage)
			imsave(destFolderName+files[0:-4]+'.png', thumbnail)

		
