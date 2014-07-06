from django.shortcuts import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from article.models import Article
from article.models import comment_table
from django.http import HttpResponseRedirect
from django.utils.datastructures import SortedDict
import re
from django.core.context_processors import csrf

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
    c.update({'article': Article.objects.get(title=recipetitle.replace("-"," ")),
		 'latest_recipes_ten' : Article.objects.all().order_by('-pub_date')[:10],
		 'popular_recipes_ten' : Article.objects.all().order_by('-likes')[:10],
		 'ingredient'	     :ingredient_dictionary,
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
        return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))


def like_article(request, recipetype="",recipetitle=""):
    if recipetype and recipetitle:
        a = Article.objects.get(title=recipetitle.replace("-"," "))
        count = a.likes
	count += 1
	a.likes = count
	a.save()
    return HttpResponseRedirect('/recipes/%s/%s/'% (recipetype,recipetitle))
