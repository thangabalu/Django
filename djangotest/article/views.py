import re
import urllib

from django.shortcuts import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.datastructures import SortedDict
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

from article.models import Article
from article.models import comment_table
from article.models import ipaddress_table
from article.models import comment_reply_table
from article.models import time_functions

class ipaddress_class:
   def save_ipaddress(self,request):
      ip_address = request.META.get("HTTP_X_FORWARDED_FOR", None)
      if ip_address:
         # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
         ip_address = ip_address.split(",")[0]
      else:
         ip_address = request.META.get("REMOTE_ADDR", "")
      
      #Check if ipaddress is already present. If not, add it. If present, increase the count with latest time
      fetch_ip = ipaddress_table.objects.filter(ip_address = ip_address).count()
      if fetch_ip == 0:
         response = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s&position=true'%ip_address).read()
         country = re.findall(r'Country:\s+(.*)',response)
         city    = re.findall(r'City:\s+(.*)\n',response)
         row = ipaddress_table()
         row.ip_address = ip_address
         row.country = country[0]
         row.city    = city[0]
         row.save()
      else:
         #Get time
         time_object = time_functions()
         #Api call to get country and city
         response = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s&position=true'%ip_address).read()
         country = re.findall(r'Country:\s+(.*)',response)
         city    = re.findall(r'City:\s+(.*)\n',response)
         
         fetch_ip = ipaddress_table.objects.get(ip_address = ip_address)
         fetch_ip.no_of_times += 1
         fetch_ip.date = time_object.get_time()
         fetch_ip.country = country[0]
         fetch_ip.city    = city[0]
         fetch_ip.save()
   

# Create your views here.
#Order.objects.order_by('-date')[0]
def home(request):
   ip_address_object = ipaddress_class()
   ip_address_object.save_ipaddress(request)

   #Total page views
   total_page_views = ipaddress_table.objects.aggregate(Sum('no_of_times'))

   return render_to_response('home.html', 
				{'total_page_views'   : total_page_views["no_of_times__sum"],
                                 'latest_recipes_one' : Article.objects.all().order_by('-pub_date')[:1],
                              	 'popular_recipes_one' : Article.objects.all().order_by('-likes')[0:1]})

def recipetype (request, recipetype):
    ip_address_object = ipaddress_class()
    ip_address_object.save_ipaddress(request)

    return render_to_response('recipe_type_new.html',
				{'type' : recipetype,
				 'recipes': Article.objects.all()})

def showrecipe (request, recipetitle=""):
   ip_address_object = ipaddress_class()
   ip_address_object.save_ipaddress(request)

   c={}
   c.update(csrf(request))
   recipe = Article.objects.get(title=recipetitle.replace("-"," "))
   recipe_id = recipe.id
   ingredients = recipe.ingredients
   ingredients_split = ingredients.split('\n')    
   ingredient_dictionary= SortedDict()
   for ingredient in ingredients_split:
      if '<h>' in ingredient:
         match = re.search('<h>(.*)',ingredient)
         if match:
            ingredient_dictionary[match.group(1)] =[]
            key=match.group(1)
      elif ';' in ingredient:
         match = re.search('(.*);\s*(.*)',ingredient)
         if match:
            ingredient_dictionary[key].append([match.group(1),match.group(2)])
   
   directions = recipe.directions
   directions_split = directions.split('\n')
    
   # Starting from here for reply comments.
   comment_rows = comment_table.objects.filter(recipeid=recipe_id).order_by('date')
   comment_reply_number = 0 # This variable is used for counter total number of reply comments
   comment_reply_dictionary = SortedDict()
   for comment in comment_rows:
      result = comment_reply_table.objects.filter(comment_reply_id= comment.id).order_by('date')
      comment_reply_number += len(result)
      if result:
         comment_reply_dictionary[comment.id] = []
         for row in result:
            row_date = row.date
            row_comment  = row.comment
            row_id = row.comment_reply_id_id
            row_unique_id = row.id
            row_name = row.name
            comment_reply_dictionary[comment.id].append([row_id,row_date,row_comment,row_unique_id,row_name])
   #sum the number of comments and reply comments
   comment_number =len(comment_table.objects.filter(recipeid=recipe_id))
   total_comments = comment_number +  comment_reply_number

   #Add page views count
   count = recipe.page_views
   count += 1
   recipe.page_views = count
   recipe.save()
   
   c.update({'article': Article.objects.get(title=recipetitle.replace("-"," ")),
		 'latest_recipes_nine'     : Article.objects.all().order_by('-pub_date')[:9],
		 'latest_recipe_tenth'     : Article.objects.all().order_by('-pub_date')[9:10],                 
		 'popular_recipes_nine'    : Article.objects.all().order_by('-likes')[:9],
		 'popular_recipe_tenth'    : Article.objects.all().order_by('-likes')[9:10],            
		 'ingredient'	           : ingredient_dictionary,
                 'direction'               : directions_split,
		 'recipe_title_url_format' : recipetitle,
                 'comments': comment_table.objects.filter(recipeid=recipe_id),
                 'comment_reply_dictionary' : comment_reply_dictionary,
                 'total_comments'           : total_comments,
                 'you_might_also_like'      : Article.objects.all().order_by('?')[:3]
		})
	    
   return render_to_response('show_recipe.html',c)

def recipes_all(request):
    ip_address_object = ipaddress_class()
    ip_address_object.save_ipaddress(request)

    return render_to_response('recipes_all.html',
				{'articles': Article.objects.all()})

def recipes_comments(request):
    comment = request.POST.get('comment','')    
    name = request.POST.get('name','')
    if name == "":
      name="Anonymous"    
    recipe_id = request.POST.get('recipe_id','')
    recipe_type  = request.POST.get('recipe_type','')
    recipe_title = request.POST.get('recipe_title','')
    #If comment field is empty, just redirect without writing to database
    if comment=="":
        return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))
    else:        
        row = comment_table(comment=comment, name=name, recipeid_id=recipe_id)
        row.save()
	#Send email
        #Change the recipe url in the email content after buying a domain        
	subject='Comment from %s' %(name)
	message=' %s has left a comment for the below recipe:\n\n Recipe title -> %s \n Recipe url -> surekha-cookhouse.rhcloud.com/recipes/%s/%s/ \n Comment -> %s \n\n This comment is stored in the table comment_table'%(name,recipe_title,recipe_type,recipe_title,comment)
	from_email=settings.EMAIL_HOST_USER
	to_list=['thangabalu@gmail.com','surekhabe@gmail.com']
	#to_list=['thangabalu@gmail.com']	
	send_mail(subject,message,from_email,to_list,fail_silently=True)
        return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))

@csrf_exempt
def recipes_comments_reply(request):
   name = request.POST.get('name','')
   if name == "":
      name="Anonymous"   
   comment = request.POST.get('comment','')
   comment_id = request.POST.get('comment_id','')

   recipe_type = request.POST.get('recipe_type','')
   recipe_title = request.POST.get('recipe_title_url_format','')

   #Add email

   if comment=="":
      return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))
   else:        
      row = comment_reply_table(name=name, comment_reply_id_id=comment_id, comment=comment )
      row.save()
      #Send email
      #Change the recipe url in the email content after buying a domain        
      subject='Comment from %s' %(name)
      message=' %s has replied for an existing comment for the below recipe:\n\n Recipe title -> %s \n Recipe url -> surekha-cookhouse.rhcloud.com/recipes/%s/%s/ \n Comment -> %s \n\n This comment is stored in the table comment_reply_table'%(name,recipe_title,recipe_type,recipe_title,comment)
      from_email=settings.EMAIL_HOST_USER
      to_list=['thangabalu@gmail.com','surekhabe@gmail.com']
      #to_list=['thangabalu@gmail.com']	
      send_mail(subject,message,from_email,to_list,fail_silently=True)
      return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))

   return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))

def like_article(request, recipetype="",recipetitle=""):
    if recipetype and recipetitle:
        a = Article.objects.get(title=recipetitle.replace("-"," "))
        count = a.likes
	count += 1
	a.likes = count
	a.save()
    return HttpResponseRedirect('/recipes/%s/%s/'% (recipetype,recipetitle))

def search(request):
   c={}
   c.update(csrf(request))   
   return render_to_response('search.html',c)

def search_titles(request):
   if request.method == "POST":
      search_text = request.POST['search_text']
   else:
      search_text = ''
   #hotcoded value, because '' fetching all values from database   
   if search_text =='':
      search_text ='nothinggggggggggggggggggggggggggggggggggggg'

   #Can I pass the value directly from here instead of doing from another html
   recipes= Article.objects.filter(title__contains=search_text)
   return render_to_response('ajax_search.html',{'recipes':recipes})
