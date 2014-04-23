from django.db import models

class Document(models.Model):
	name=models.CharField(max_length=200)
	pdfFile=models.FileField(upload_to='original pdf file')
	thumbnail=models.ImageField(upload_to='thumbnail image')
	def admin_thumbnail(self):
		return u'<img src="%s" />' % (self.thumbnail.url)
	admin_thumbnail.short_description = 'AdThumbnail'
	admin_thumbnail.allow_tags=True
	category=models.ForeignKey('Category')
	def __unicode__(self):
		return self.name

class Category(models.Model):
	name=models.CharField(max_length=200)
	description=models.TextField(blank=True)
	def __unicode__(self):
		return self.name



