from django.shortcuts import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from article.models import Article
from django.http import HttpResponseRedirect
from django.utils.datastructures import SortedDict
import re

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
    recipe = Article.objects.get(title=recipetitle.replace("-"," "))
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
	    
    return render_to_response('show_recipe.html',
		{'article': Article.objects.get(title=recipetitle.replace("-"," ")),
		 'latest_recipes_ten' : Article.objects.all().order_by('-pub_date')[:10],
		 'popular_recipes_ten' : Article.objects.all().order_by('-likes')[:10],
		 'ingredient'	     :ingredient_dictionary
		})

def recipes_all(request):
    return render_to_response('recipes_all.html',
				{'articles': Article.objects.all()})

def like_article(request, recipetype="",recipetitle=""):
    if recipetype and recipetitle:
        a = Article.objects.get(title=recipetitle.replace("-"," "))
        count = a.likes
	count += 1
	a.likes = count
	a.save()
    return HttpResponseRedirect('/recipes/%s/%s/'% (recipetype,recipetitle))
