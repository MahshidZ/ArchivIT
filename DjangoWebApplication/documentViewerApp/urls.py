
from django.conf.urls import patterns, url
from documentViewerApp import views
from django.views.static import serve
from django.conf import settings

urlpatterns = patterns('',url(r'^$', views.index, name='index'),

	url(r'^(.*categoriesall/)(?P<document_id>\d+)/$', views.detail, name='detail'),
        url(r'^.*categoriesall.*$',views.CategoriesAll, name='categoriesall'),
        url(r'^(.*categoriesall/?P<cat_name>\d)()/$',views.get_documents_by_category, name='specificdocument'),
	url(r'^.*thumbnailmaker.*$',views.ThumbnailMaker, name='thumbnailmaker'),
        url(r'^.*InputData.*$',views.InputData, name='InputData'),
        url(r'^.*TrainingSetBuild.*$',views.TrainingSetBuild, name='TrainingSetBuild.html'),
        url(r'^.*Classification.*$',views.Classification, name='Classification.html'),
        url(r'^.*Evaluation.*$',views.Evaluation, name='Evaluation.html'),
	
)


