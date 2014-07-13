import re

from django.shortcuts import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.datastructures import SortedDict
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings

from article.models import Article
from article.models import comment_table


# Create your views here.
#Order.objects.order_by('-date')[0]
def home(request):
   return render_to_response('home.html', 
				{'latest_recipes_one' : Article.objects.all().order_by('-pub_date')[:1],
                              	 'popular_recipes_one' : Article.objects.all().order_by('-likes')[0:1]})

def recipetype (request, recipetype):
    return render_to_response('recipe_type_new.html',
				{'type' : recipetype,
				 'recipes': Article.objects.all()})

def showrecipe (request, recipetitle=""):
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
	    match = re.search('(.*);(.*)',ingredient)
	    if match:
	        ingredient_dictionary[key].append([match.group(1),match.group(2)])

    directions = recipe.directions
    directions_split = directions.split('\n') 
    directions_dictionary= SortedDict()
    key=""
    for direction in directions_split:
      if '<h>' in direction:
         match = re.search('<h>(.*)',direction)
   	 if match:
	    directions_dictionary[match.group(1)] =""
	    key=match.group(1)
      else:
         if key:
 	    directions_dictionary[key]= directions_dictionary[key] + direction
    
    
    c.update({'article': Article.objects.get(title=recipetitle.replace("-"," ")),
		 'latest_recipes_nine'     : Article.objects.all().order_by('-pub_date')[:9],
		 'latest_recipe_tenth'     : Article.objects.all().order_by('-pub_date')[9:10],                 
		 'popular_recipes_nine'    : Article.objects.all().order_by('-likes')[:9],
		 'popular_recipe_tenth'    : Article.objects.all().order_by('-likes')[9:10],            
		 'ingredient'	           : ingredient_dictionary,
                 'direction'               : directions_dictionary,
		 'recipe_title_url_format' : recipetitle,
                  'comments': comment_table.objects.filter(recipeid=recipe_id)
		})
	    
    return render_to_response('show_recipe.html',c)

def recipes_all(request):
    return render_to_response('recipes_all.html',
				{'articles': Article.objects.all()})

def recipes_comments(request):
    comment = request.POST.get('comment','')    
    name = request.POST.get('name','anonymous')    
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
	#Need below to send non empty name in email
        if name == "":
		name="Anonymous"
	subject='Comment from %s' %(name)
	message=' %s has left a comment for the below recipe:\n\n Recipe title -> %s \n Recipe type -> %s \n Comment -> %s \n\n This comment is stored in the table comment_table'%(name,recipe_title,recipe_type,comment)
	from_email=settings.EMAIL_HOST_USER
	to_list=['thangabalu@gmail.com','surekhabe@gmail.com']
	
	send_mail(subject,message,from_email,to_list,fail_silently=True)
        return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))


def like_article(request, recipetype="",recipetitle=""):
    if recipetype and recipetitle:
        a = Article.objects.get(title=recipetitle.replace("-"," "))
        count = a.likes
	count += 1
	a.likes = count
	a.save()
    return HttpResponseRedirect('/recipes/%s/%s/'% (recipetype,recipetitle))
