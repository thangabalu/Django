from django.db import models
import os
import time
# Create your models here.

def get_upload_file_name(instance, filename):
	return "uploaded_files/%s" % filename.replace(" ", "-")

def get_time():
	return time.strftime("%c")

# I am making the title field unique, because I will use this in the part of the url
class Article(models.Model):

    Recipe_Choices = (
      ('baking', 'baking'),
      ('quick-food', 'quick food'),
      ('pastries', 'pastries'),
      ('variety-rice', 'variety rice'),
      ('one-pot-cooking', 'one pot cooking'),      
      ('chutney', 'chutney'),
      ('sides', 'sides'),
      ('gravy', 'gravy'),
      ('others', 'others')
    )
    title           = models.CharField(max_length=200, unique = True)
    also_known_as   = models.TextField(blank = True)
    prep_time       = models.CharField(max_length=20,blank = True)
    cooking_time    = models.CharField(max_length=20,blank = True)
    serves          = models.CharField(max_length=20,blank = True)
    ingredients     = models.TextField()
    pub_date        = models.DateTimeField()
    directions      = models.TextField()
    note            = models.TextField(blank = True)
    tips            = models.TextField(blank = True)
    photo           = models.FileField(upload_to= get_upload_file_name,blank=True)
    recipe_type     = models.CharField(max_length=100,choices=Recipe_Choices)
    recipe_type_1   = models.CharField(max_length=100, choices=Recipe_Choices,blank=True)
    recipe_type_2   = models.CharField(max_length=100, choices=Recipe_Choices,blank=True)
    likes           = models.IntegerField(max_length=100,default=0)
    did_you_know    = models.TextField(blank = True)
    meta_keyword    = models.TextField(blank = True, null = True,max_length=50)
    meta_description    = models.TextField(blank = True, null = True,max_length=500)


    def __unicode__(self):
    	return self.title

class comment_table(models.Model):

    name            = models.CharField(max_length=200)
    date            = models.DateTimeField(auto_now_add=True)
    comment         = models.CharField(max_length=200)    
    recipeid        = models.ForeignKey(Article)
    def __unicode__(self):
    	return self.comment

class comment_reply_table(models.Model):

    comment_reply_id   = models.ForeignKey(comment_table)
    name            = models.CharField(max_length=200)
    comment            = models.CharField(max_length=200)
    date               = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
    	return self.comment

class ipaddress_table(models.Model):
    #LAter change the "date"s type to Date time field. Temporarily have charfield to see the date in admin
    #Because setting auto_now_add is true hides the value in the admin page
    ip_address = models.IPAddressField()
    date       = models.CharField(default=get_time,max_length=100)

    def __unicode__(self):
    	return self.ip_address