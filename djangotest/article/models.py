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
    recipe_type     = models.CharField(max_length=100,choices=Recipe_Choices)
    likes           = models.IntegerField(max_length=100)
    did_you_know    = models.CharField(max_length=1000, default="Nothing for this")
    meta_keyword    = models.TextField(blank = True, null = True,max_length=50)
    meta_description    = models.TextField(blank = True, null = True,max_length=100)


    def __unicode__(self):
    	return self.title

class comment_table(models.Model):

    comment         = models.CharField(max_length=200)
    name            = models.CharField(max_length=200)
    date            = models.DateTimeField(auto_now_add=True)
    recipeid        = models.ForeignKey(Article)
    def __unicode__(self):
    	return self.comment
