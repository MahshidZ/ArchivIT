
#The Image Module:
#http://www.pythonware.com/library/pil/handbook/image.htm
# Useful reply: https://github.com/SmileyChris/easy-thumbnails/issues/95
# Basic Python: http://www.astro.ufl.edu/~warner/prog/python.htmls

#This seems like a doc for pdfminer:
#http://pdfminer.sourcearchive.com/documentation/20100829plus-pdfsg-1/classpdfminer_1_1layout_1_1LTPage.html

from numpy import *         #For matrix 
from PIL import Image          #For image
import pdfminer                 #pdf extract information

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator

import os # directory's file names

INPUT_DIR_NAME = './PdfCollection/'
OUTPUT_DIR_NAME = '' + 'ThumbnailCollection/' + ''

THUMBNAIL_WIDTH = 128
THUMBNAIL_HEIGHT = 128

PAGE_COUNT=1

TEXT_LINE_WIDTH_RATIO = 0
LINE_LINE_WIDTH_RATIO = 2
RECT_LINE_WIDTH_RATIO = 3

BACKGROUND_COLOR = [int(255),int(255),int(255)]
TEXT_COLOR = [int(0),int(0),int(0)]
LINE_COLOR = [int(0),int(0),int(0)]
RECT_COLOR = [int(0),int(0),int(0)]
IMG_COLOR = [int(100),int(100),int(100)]
FIG_COLOR = [int(100),int(100),int(100)]

debug = 0

def thumbnail_construction_for_files_in_directory(source_foldername, destination_foldername):
    for file in os.listdir(source_foldername):
        if file.endswith('.pdf'):
            if(debug == 1):
                print file
            _construct_thumbnail(source_foldername + file, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT, destination_foldername)

def _construct_thumbnail(filename, thumbnail_Width, thumbnail_Height, destination_foldername):
    splitted_filename = filename.split('/')
    directoryname = l[1]
    pure_filename = l[2]
    
    # Open a PDF file.
    fp = open(filename, 'rb')
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams = laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pageNomber = 1
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        # pagesCounts: receive the LTPage object for the pagesCounts nth page.
        if pageNomber > PAGE_COUNT: 
            break
        interpreter.process_page(page)
        layout = device.get_result()
        originalPage_Width = layout.width
        originalPage_Height = layout.height
        Matrix = ones((originalPage_Width,originalPage_Height,3),int)
        Matrix = multiply(Matrix,BACKGROUND_COLOR)
        size = (int(originalPage_Width),int(originalPage_Height)) 

        for hbox in layout:         
         #hbox can be: LTTextBox, LTFigure, LTLine, LTRect, LTImage 
            if isinstance(hbox, pdfminer.layout.LTTextBoxHorizontal):
                _text_processing(hbox, Matrix)

            if isinstance(hbox, pdfminer.layout.LTRect):
                _rect_processing(hbox, Matrix)
                
            if isinstance(hbox, pdfminer.layout.LTLine):
                _line_processing(hbox, Matrix)

            if isinstance(hbox, pdfminer.layout.LTImage):
                _logo_processing(hbox, Matrix)
                        
            if isinstance(hbox, pdfminer.layout.LTFigure):
                _figure_processing(hbox, Matrix)
        
        _construct_thumbnail_image(size, Matrix, thumbnail_Width, thumbnail_Height, destination_foldername)

        pageNomber+=1


def _text_processing(hbox, Matrix):
    for things in hbox:
        if isinstance(things, pdfminer.layout.LTTextLineHorizontal):
            if(debug == 1):
                print ('LTTextLineHorizontal')
            line_Width = TEXT_LINE_WIDTH_RATIO
            (x0, y0, x1, y1) = things.bbox
            text_firstX = int(x0)  #Top left Corner x
            text_secondX = int(x1) #Bottom Right Corner x
            text_firstY = size[1] - int(y0)  #Top left Corner y
            text_secondY = size[1] - int(y1) #Bottom Right Corner y
        
            for i in range(text_firstX,text_secondX):
                for j in range(text_secondY,text_secondY+2):
                    Matrix[i,j] = TEXT_COLOR


def _rect_processing(hbox, Matrix):
    if(debug == 1):
        print ('Rect')
    (x0, y0, x1, y1) = hbox.bbox
    rect_firstX = int(x0)  #Top left Corner x
    rect_secondX = int(x1) #Bottom Right Corner x
    rect_firstY = size[1]-int(y0)  #Top left Corner y
    rect_secondY = size[1]-int(y1) #Bottom Right Corner y
    
    line_Ratio = RECT_LINE_WIDTH_RATIO
    line_Width = int((hbox.linewidth)+1)*line_Ratio

    for i in range(rect_firstX,rect_secondX):
        for j in range(rect_firstY -  line_Width+1, rect_firstY ): #  , rect_firstY ( +  -) line_Width  ?   --- (top)
            Matrix[i,j] = RECT_COLOR
            
    for i in range(rect_firstX,rect_firstX+line_Width-1): #       for i in range(rect_firstX,rect_firstX+line_Width):  
        for j in range(rect_secondY,rect_firstY):
            Matrix[i,j] = RECT_COLOR

    for i in range(rect_secondX-line_Width+1,rect_secondX):
        for j in range(rect_secondY,rect_firstY):
            Matrix[i,j]=RECT_COLOR

    for i in range(rect_firstX,rect_secondX):
        for j in range(rect_secondY, rect_secondY-line_Width,):  # -- (buttom)
            Matrix[i,j]=RECT_COLOR
            

def _line_processing(hbox, Matrix):
    if(debug == 1):
        print ('Line')
    (x0, y0, x1, y1)=hbox.bbox
    line_firstX=int(x0)  #Top left Corner x
    line_secondX=int(x1) #Bottom Right Corner x
    line_firstY=size[1]-int(y1)  #Top left Corner y
    line_secondY=size[1]-int(y0) #Bottom Right Corner y
    
    vertical=False
    horizontal=False

    line_Ratio=LINE_LINE_WIDTH_RATIO
    line_Width=int((hbox.linewidth)+1)*line_Ratio

    if(line_firstX==line_secondX):
        vertical=True
    if(line_firstY==line_secondY):
        horizontal=True
        
    if(vertical==True):
        for i in range(line_firstX-line_Width,line_secondX+line_Width):
            for j in range(line_secondY,line_firstY):
                Matrix[i,j]=LINE_COLOR
                
    if(horizontal==True):
        for i in range(line_firstX,line_secondX):
            for j in range(line_secondY+line_Width,line_firstY-line_Width):
                Matrix[i,j]=LINE_COLOR

def _logo_processing(hbox, Matrix):
    if(debug == 1):
        print ('Image')
    (x0, y0, x1, y1)=hbox.bbox
    image_firstX=int(x0)  #Top left Corner x
    image_secondX=int(x1) #Bottom Right Corner x
    image_firstY=size[1]-int(y0)  #Top left Corner y
    image_secondY=size[1]-int(y1) #Bottom Right Corner y
    

    if ((math.fabs(x1-x0)<=originalPage_Width+1 and math.fabs(x1-x0)>=originalPage_Width-1 )and
       ( math.fabs(y0-y1)<=originalPage_Height+1 and
        math.fabs(y0-y1)>=originalPage_Height-1 )
        ):
        print('Scanned Pdf page (Image)')
    else:
        for i in range(image_firstX,image_secondX):
            for j in range(image_secondY,image_firstY):
                    Matrix[i,j]=IMG_COLOR


def _figure_processing(hbox, Matrix):
    if(debug == 1):
        print ('Figure')
    (x0, y0, x1, y1)=hbox.bbox
    figure_firstX=int(x0)  #Top left Corner x
    figure_secondX=int(x1) #Bottom Right Corner x
    figure_firstY=size[1]-int(y1)  #Top left Corner y  #size[1]-int(y0) 
    figure_secondY=size[1]-int(y0) #Bottom Right Corner y   #size[1]-int(y0)
    if(debug == 1):
        print(figure_secondY)
    
    if ((math.fabs(x1-x0)<=originalPage_Width+1 and math.fabs(x1-x0)>=originalPage_Width-1 )and
       ( math.fabs(y1-y0)<=originalPage_Height+1 and
        math.fabs(y0-y1)>=originalPage_Height-1 )
        ):
        if(debug == 1):
            print('Scanned Pdf page')
                         
    else:
        for i in range(figure_firstX,figure_secondX):
            for j in range(figure_firstY,figure_secondY-10):  # for j in range(figure_secondY,figure_firstY) ?
                Matrix[i,j]=FIG_COLOR

def _construct_thumbnail_image(image_size, Matrix, thumbnail_Width, thumbnail_Height, destination_foldername):      
    thumbnail_image = Image.new('RGB',size)
    pix = thumbnail_image.load()
    for i in range(size[0]):
        for j in range(size[1]):
            pix[i,j] = tuple((Matrix[i,j]))
    imThumbnailSize = thumbnail_image
    size = thumbnail_Width, thumbnail_Height
    imThumbnailSize.thumbnail(size, Image.ANTIALIAS)
    imThumbnailSize = imThumbnailSize.rotate(360)
    if imThumbnailSize.mode != "RGB":
        imThumbnailSize = imThumbnailSize.convert("RGB")
    if not os.path.exists(destination_foldername):
        os.makedirs(destination_foldername)
    
    imThumbnailSize.save(destination_foldername + pure_filename.split('.')[0] + '.png')
    if(debug == 1):
        print('Thumbnail is created successfully ...')

