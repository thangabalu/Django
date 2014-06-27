from django.db import models
import os
import time
# Create your models here.

def get_upload_file_name(instance, filename):
	return "uploaded_files/%s_%s" % (str(time.time()).replace('.','_'), filename)

# I am making the title field unique, because I will use this in the part of the url
class Article(models.Model):

    Recipe_Choices = (
      ('cakes', 'cakes'),
      ('quick-food', 'quick food'),
      ('pastries', 'pastries'),
      ('variety-rice', 'variety rice'),
      ('one-pot-cooking', 'one pot cooking')
    )
    title           = models.CharField(max_length=200, unique = True)
    ingredients     = models.TextField()
    pub_date        = models.DateTimeField()
    directions      = models.TextField()
    note            = models.TextField(blank = True)
    tips            = models.TextField(blank = True)
    photo           = models.FileField(upload_to= get_upload_file_name)
    recipe_type     = models.CharField(max_length=10,choices=Recipe_Choices)
    likes           = models.IntegerField(max_length=10)
    meta_keyword    = models.TextField(blank = True, null = True,max_length=50)
    meta_description    = models.TextField(blank = True, null = True,max_length=100)


    def __unicode__(self):
    	return self.title
