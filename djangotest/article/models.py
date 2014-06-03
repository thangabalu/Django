from django.db import models
import os
import time
# Create your models here.

def get_upload_file_name(instance, filename):
	return "uploaded_files/%s_%s" % (str(time.time()).replace('.','_'), filename)

# I am making the title field unique, because I will use this in the part of the url
class Article(models.Model):

    Recipe_Choices = (
      ('cake', 'cakes'),
      ('quick', 'quick food'),
      ('past', 'pastries'),
      ('variety', 'variety rice'),
      ('one', 'one pot cooking')
    )
    title           = models.CharField(max_length=200, unique = True)
    ingredients     = models.TextField()
    pub_date        = models.DateTimeField(auto_now=True)
    directions      = models.TextField()
    note            = models.TextField(blank = True)
    tips            = models.TextField(blank = True)
    photo           = models.FileField(upload_to= get_upload_file_name)
    recipe_type     = models.CharField(max_length=10,choices=Recipe_Choices)

    def __unicode__(self):
    	return self.title
