# views in MVC
from django.shortcuts import render_to_response, render
from django.template import RequestContext, Context, loader
from documentViewerApp.models import Category, Document
from django.http import HttpResponse
from django.core.files import File
import os
import KmeansClustering as clustering
import sys
sys.path.append('/ScannedThumbnailCode')
from scanned_image_processing.thumbnailConstruction import thumbnail_construction_for_files_in_directory as ScannedThumbnailMaker
from digital_image_processing.thumbnailConstruction import thumbnail_construction_for_files_in_directory as DigitalThumbnailMaker

MEDIA_PATH = '/media/'
DATA_PATH = MEDIA_PATH + 'Data/'
INITIAL_CATEGORY_NAME = 'Category0'

from django.utils import simplejson

def CategoriesAll(request):
	
	""" Reneders categories.html page.
	Retrives all the categorises sorted by their name from Category table.
	Retrives all the documents sorted by their name from Document table.
	Runs Kmeans clustering algorithm on the thubmail files against the user inputs.
	"""
	categories = Category.objects.all().order_by('name')
	documents = Document.objects.all().order_by('name')
	context = {'categories':categories, 'documents': documents, 'json_data': json_data}
	
	if(request.GET.get('kmeansbtn')):
		source_path = DATA_PATH
		kmean_result_path = MEDIA_PATH + 'ResultDirs/'
		feature_matrix_path = source_path + 'NormalizedFeaturesMatrix.csv'
		pdf_path = kmean_result_path + 'PDFResults/'
		png_path = kmean_result_path + 'PNGResults/'
		
		_run_kmeans(feature_matrix_path, source_path,kmean_result_path, request);
		_delete_MAC_hidden_files(pdf_path)
		_free_database()
		_save_data_in_database(pdf_path, png_path)

	return render_to_response('documentViewerApp/categories.html', context, 
		context_instance = RequestContext(request))	

def _run_kmeans(feature_matrix_path, source_path, kmean_result_path, request):
	clustering.KmeansAlgorithm(
	feature_matrix_path, source_path,kmean_result_path, 
	int(request.GET.get('clusternumber')),
	float(request.GET.get('region1Text')), float(request.GET.get('region1Line')), float(request.GET.get('region1Image')), 
	float(request.GET.get('region2Text')), float(request.GET.get('region2Line')), float(request.GET.get('region2Image')), 
	float(request.GET.get('region3Text')), float(request.GET.get('region3Line')), float(request.GET.get('region3Image')), 
	)

def _delete_MAC_hidden_files(directory):
	files = os.listdir(directory)
	if '.DS_Store' in files:
		files.remove('.DS_Store')

def _free_database():
	Category.objects.all().delete()
	Document.objects.all().delete()

def _save_data_in_database(pdf_path, png_path):
	category_folders = os.listdir(pdf_path)
	for foldername in category_folders:
		_create_database_category(foldername)
		_delete_MAC_hidden_files(pdf_path + foldername)		
		for pdffile in os.listdir(pdf_path + foldername):
			_create_database_document(pdffile, pdf_path + foldername , png_path + foldername, foldername)

def _create_database_document(pdffile, pdf_path , png_path, foldername):
	database_document = Document(
		name = os.path.splitext(pdffile)[0], 
		pdfFile = pdf_path + '/' + os.path.splitext(pdffile)[0] + '.pdf', 
		thumbnail = png_path + '/' + os.path.splitext(pdffile)[0] + '.png', 
		category = Category.objects.get(name = foldername)
		)
	print pdffile
	database_document.save()

def _create_database_category(foldername):
	database_category = Category(name = foldername, description = '')
	print foldername
	database_category.save()

def get_documents_by_category(request, category_name):
	""" Returns documents for a category. 
	Args:
		category_name: name spcified in database
	Returns:
		All the documents within the requested category. 
	"""
	documents = Document.objects.get(category = category_name)
	context = {'documents':documents}
	return render_to_response('documentViewerApp/singledocument.html', context, 
		context_instance = RequestContext(request))
	
def index(request):
	""" Reneders index.html page.
	"""
	return render_to_response('documentViewerApp/index.html')	
	
def detail(request, document_id):
	""" Pops up information about a specific document by their document id in database. 
	TODO: Should show original pdf document when the user clicks on a thubmail.
	"""
	return HttpResponse('you are looking at doc %s'%document_id)

def ThumbnailMaker(request):
	""" Cunstructs thubmails for all the pdf document in the source directory, and stores them in the target directory.
	If the pdf files are originaly digital, runs ThumbnailExtraction_DigitalPdf code.
	If the pdf files are scanned from papers, runs ThumbnailExtraction_ScannedPdf code.
	"""
	source_path = DATA_PATH + 'PdfCollection/'
	result_path = DATA_PATH + 'ThumbnailCollection/'
	if(request.GET.get('makethumb')):
		if(request.GET.get('scanned')):
			ScannedThumbnailMaker(sourcedirectory, resultdirectory)
		if(request.GET.get('digital')):
			DigitalThumbnailMaker(sourcedirectory, resultdirectory)
	return render_to_response('documentViewerApp/ThumbnailMaker.html')

def InputData(request):
	""" Renders InputData.html page and responds to user clicks. 
	Reads raw data from pdf path and thumbnail path and calls a method to creates
	related documents data and saves these data to database. 
	"""
	source_path = DATA_PATH
	pdf_path = source_path + 'PdfCollection/'
	thumbnail_path = source_path + 'ThumbnailCollection/'
			
	_create_initial_category()
	_delete_MAC_hidden_files(pdf_path)
	_delete_MAC_hidden_files(thumbnail_path)
	
	for pdffile in os.listdir(pdf_path):
		if pdffile.endswith('.pdf'):
			_create_database_document(pdffile, pdf_path , thumbnail_path, INITIAL_CATEGORY_NAME)

	return render_to_response('documentViewerApp/InputData.html')

def _create_initial_category():
	initial_category = Category(name = INITIAL_CATEGORY_NAME, description = 'My initial category')
	initial_category.save()

def TrainingSetBuild(request):
	""" The user could drag and drop the documents withing the categories. After they did their changes, the user can 
	select TrainingSetBuild button to save the changes and store this set of data to be used in the next phase 
	of classification algorithm as a training set.
	"""
	categories = Category.objects.all().order_by('name')
	documents = Document.objects.all()
	context = {'categories':categories,'documents': documents}		
	return render_to_response('documentViewerApp/TrainingSetBuild.html', context, 
		context_instance = RequestContext(request))	

def Classification(request):
	""" TODO: Result of the classification algorithm will be presented Classification.html page. 
	"""
	return render_to_response('documentViewerApp/Classification.html')

def Evaluation(request):
	""" TODO: Result of evalucation of classification algorithm will be presented in Evaluation.html page.
	"""
	return render_to_response('documentViewerApp/Evaluation.html')


def init_js_template(request):
    import json
    print '*************'
    data = open('navigation.json').read() #opens the json file and saves the raw contents
    json_data = json.dumps(data) #converts to a json structure
    print json_data
    return render_to_respons('documentViewerApp/categories.html', {'json_data':json_data})

