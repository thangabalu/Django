from django.db import models
import os
import time

# Receive the post_delete signal and delete the file associated with the model instance.
from django.db.models.signals import post_delete
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


# Create your models here.


def get_upload_file_name(instance, filename):
	return "uploaded_files/%s.jpg" % instance.title.replace(" ", "-")
	#Todo - now adding jpg to all file name. Find the extension of the file and add it in the future

class time_functions:
    def get_time(self):
        return time.strftime("%c")

# I am making the title field unique, because I will use this in the part of the url
# If changing the spelling of the fields or adding new fields, please change in pre_save_signal function
class Article(models.Model):

    Recipe_Choices = (
      ('baking', 'baking'),
      ('breakfast', 'breakfast'),
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
    recipe_type     = models.CharField(max_length=100,choices=Recipe_Choices)
    recipe_type_1   = models.CharField(max_length=100, choices=Recipe_Choices,blank=True)
    recipe_type_2   = models.CharField(max_length=100, choices=Recipe_Choices,blank=True)
    also_known_as   = models.TextField(blank = True)
    prep_time       = models.CharField(max_length=20,blank = True)
    cooking_time    = models.CharField(max_length=20,blank = True)
    serves          = models.CharField(max_length=20,blank = True)
    pub_date        = models.DateTimeField()
    photo           = models.FileField(upload_to= get_upload_file_name,blank=True)
    ingredients     = models.TextField()
    directions      = models.TextField()
    did_you_know    = models.TextField(blank = True)
    meta_description    = models.TextField(blank = True, null = True,max_length=500)
    note            = models.TextField(blank = True)
    tips            = models.TextField(blank = True)
    meta_keyword    = models.TextField(blank = True, null = True,max_length=50)
    likes           = models.IntegerField(max_length=100,default=0)
    page_views      = models.IntegerField(max_length=100,default=0)

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
    time_object = time_functions()
    
    ip_address 	       = models.IPAddressField()
    date 	       = models.DateTimeField(auto_now=True)
    no_of_times        = models.IntegerField(max_length=100,default=1)
    country            = models.CharField(max_length=100)
    city               = models.CharField(max_length=100)

    def __unicode__(self):
        #date_time = self.date[:19]
        return u'"%s"-->"%s" -->"%s times" -->"%s" --> "%s"' % (self.ip_address, self.date, self.no_of_times, self.country, self.city)

@receiver(post_delete, sender=Article)
def delete_uploaded_file(sender, instance, **kwargs):
    # Pass false so photo doesn't save the model.
    instance.photo.delete(False)

#from article.views import Email
#@receiver(pre_save, sender=Article)
#def pre_save_signal(sender, instance, **kwargs):
#    """
#    Usage of getattr
#    m = "world"
#    hello = helloworld()
#    getattr(hello, m)()
#    Hello World!  
#    """
#    try:
#        fetch_item = Article.objects.get(pk=instance.pk)
#    except Article.DoesNotExist:
#        pass # Object is new, so field hasn't technically changed, but you may want to do something else here.
#    else:
#        # Field value has changed
#        title_split = fetch_item.title.split()
#        title_join = "-".join(title_split)
#        url = "surekha-cookhouse.rhcloud.com/recipes/%s/%s" %(fetch_item.recipe_type, title_join)
#        message = "Title - %s\n Url - %s\n" %(fetch_item.title, url)

#        for field in Article._meta.fields: #This fetches the field name
#            if field.name == "likes":
#                if not getattr(fetch_item, field.name) == getattr(instance, field.name):
#                    subject = "Some one has liked the recipe"
#            elif field.name == "page_views":
#                if not getattr(fetch_item, field.name) == getattr(instance, field.name):
#                    subject = "Some one has seen the recipe"
#            else:
#                subject = "Existing recipe updated"
#                if not getattr(fetch_item, field.name) == getattr(instance, field.name):
#                    message += "*****************************\n"
#                    message += "Updated field - %s \n" %field.name
#                    message += "*****************************\n"
#                    message += "\nOld value:\n%s\n" %getattr(fetch_item, field.name)
#                    message += "\nNew value:\n%s\n\n" %getattr(instance,field.name)

#        Email_object = Email()
#        Email_object.send_email(subject, message)

#@receiver(post_save, sender=Article)
#def post_save_signal(sender, instance, created, **kwargs):
#    Email_object = Email()
#    title_split = instance.title.split()
#    title_join = "-".join(title_split)
#    url = "surekha-cookhouse.rhcloud.com/recipes/%s/%s" %(instance.recipe_type, title_join)
#    message = "Title of the recipe - %s\n url of the recipe - %s" %(instance.title, url)
#    if created:
#        subject = "New recipe posted"
#        Email_object.send_email(subject, message)
