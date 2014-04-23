
from django.contrib import admin
from documentViewerApp.models import Category,Document
class CategoryAdmin(admin.ModelAdmin):
	list_display=('name','description')
	search_fields=['name']

class DocumentAdmin(admin.ModelAdmin):
	list_display=('name','pdfFile','admin_thumbnail','category','thumbnail')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Document,DocumentAdmin)
