import numpy as np
from scipy.cluster.vq import whiten, vq, kmeans
import csv
import os
import shutil

import matplotlib.cm as cm 
import pylab
from pylab import *

def main():
    KmeansAlgorithm('./Data/NormalizedFeaturesMatrix.csv','./Data/','./ResultDirs/',8, 3,3,3,1,1,1,1,1,1)
    #ScatterPlot(X[2], centroids)


def ExtractInfoFromCSVFile(filepath):
    myfile = open(filepath,'rU')
    myfilereader = csv.reader(myfile)
    next(myfilereader)
    for line in myfilereader:
        new=[]
        line.pop(0)
        for element in line:
            new.append(float(element))
        X.append(new) 
    myfile.close()
       
  
def ExtractNamesFromCSVFile(filepath):
    myfile = open(filepath,'rU')
    myfilereader = csv.reader(myfile)
    next(myfilereader)
    for line in myfilereader:
        new=[]
        new.append((line[0]))
        new=''.join(new)
        Z.append(new) 
    myfile.close()


def  SaveFilesIntoResultsDirectory(sourcedir, resdir, codes,idx, savetype):
    sourcedirectory =  sourcedir
    resultdirectory =  resdir
    
    if(savetype == '.pdf'):
        resultdirectory += 'PDFResults/'
        sourcedirectory += 'pdfCollection/'
    else:
        if(savetype == '.png'):
            resultdirectory += 'PNGResults/'
            sourcedirectory += 'ThumbnailCollection/'
        
    if os.path.isdir(resultdirectory):
        shutil.rmtree(resultdirectory)    
    if not os.path.isdir(resultdirectory):
        os.makedirs(resultdirectory)
    
    ClusterId = np.arange(codes)
    
    for clusterid in ClusterId:
        categorydirname = resultdirectory + 'Category' + str(clusterid) + '/'
        if not os.path.isdir(categorydirname):
            os.makedirs(categorydirname)
        start=0
        for element in idx:  
            if (clusterid == element ):
                filename= Z[start]
                filename = os.path.splitext(filename)[0] + savetype
                filesourcepath = sourcedirectory +  filename 
                if os.path.exists(filesourcepath):
                    print clusterid, ' ' ,  filename
                    shutil.copyfile(filesourcepath ,  categorydirname + filename )
            start += 1
        print '...'
        
def FileNameChange():
    import re
    for f in os.listdir('./Data/ThumbnailCollection/'):
        if f.endswith('.png'):
            s = re.sub('\_page1', '', f)
            s='./Data/ThumbnailCollection/'+s
            shutil.move('./Data/ThumbnailCollection/'+f,s)
    
def FeatureEmphesize(featurenumber, multinumber):
    for row in X:
        row[featurenumber] *=multinumber


#TODO: output Presentation
def ScatterPlot(feature, groupnum):

    colors = cm.rainbow(np.linspace(0, 1, len(feature)))
    for y, c in zip(feature, colors):
        xx=np.arange(groupnum)
        for x1 , y1 in zip(xx, feature):
            pylab.scatter(x1, y1, color=c)
    pylab.savefig('./clustering.png')


def KmeansAlgorithm(csvfilepath, sourcedatapath, resultpath, num, a1,b1,c1,a2,b2,c2,a3,b3,c3):
    global X  # The data matrix
    X = []
    global Z  # The file names
    Z = []
    #FileNameChange()
    
    filepath = csvfilepath
    ExtractInfoFromCSVFile(filepath)
    ExtractNamesFromCSVFile(filepath)
    
    #X = whiten(X) # normalizing (although with did this manually)
    X = np.array(X)
    print X
    FeatureEmphesize(0,a1) #first feature multiplied by a1
    FeatureEmphesize(1,b1)
    FeatureEmphesize(2,c1)
    
    FeatureEmphesize(3,a2) #first feature multiplied by a1
    FeatureEmphesize(4,b2)
    FeatureEmphesize(5,c2)

    FeatureEmphesize(6,a3) #first feature multiplied by a1
    FeatureEmphesize(7,b3)
    FeatureEmphesize(8,c3)
    print X
    codes = num # number of categories
    centroids,_ =  kmeans(X,codes) 
    idx,_ = vq(X, centroids)
    print idx
    SaveFilesIntoResultsDirectory(sourcedatapath, resultpath, codes,idx,'.png')
    SaveFilesIntoResultsDirectory(sourcedatapath, resultpath, codes,idx,'.pdf')
    



if __name__ == '__main__':
    main()

