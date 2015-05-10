import re
import urllib
import json


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
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from article.models import Article
from article.models import comment_table
from article.models import ipaddress_table
from article.models import comment_reply_table
from article.models import time_functions

import logging
logger = logging.getLogger(__name__)

def generate_ipaddress(ipaddressrange):
    logger.info("Generating ip address range - %s " %ipaddressrange)

    ipaddress_split = ipaddressrange.split("-")
    first_set = ipaddress_split[0]
    dot_separated = first_set.split(".")

    first_digit, second_digit, third_digit, last_digit = dot_separated
    first_three_digits = first_digit+"."+second_digit+"."+third_digit

    ipaddress_list = []

    top_range = int(ipaddress_split[1])
    current_ip = int(last_digit)

    while (current_ip <= top_range):
        ipaddress_list.append(str(first_three_digits)+'.'+str(current_ip))
        current_ip += 1

    logger.info("Completed generating ip address range. Returning list")
    return ipaddress_list


block_ip_addresses = ["46.161.41.199", "176.10.104.227", "176.10.104.234"]

ipaddress_range    = generate_ipaddress("188.143.232.1-100")
block_ip_addresses = block_ip_addresses + ipaddress_range


class ipaddress_class:
   def get_ipaddress(self, request):
      ip_address = request.META.get("HTTP_X_FORWARDED_FOR", None)
      if ip_address:
         # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
         ip_address = ip_address.split(",")[0]
      else:
         ip_address = request.META.get("REMOTE_ADDR", "")

      logger.debug("Got the ip address - %s" %ip_address)
      return ip_address
      
   def save_ipaddress(self, ip_address):
      #Check if ipaddress is already present. If not, add it. If present, increase the count
      fetch_ip = ipaddress_table.objects.filter(ip_address = ip_address)

      if fetch_ip:
         #If it returns multiple ip records, it fetches the first one.
         fetch_ip_address_row = fetch_ip[0]
         fetch_ip_address_row.no_of_times = fetch_ip_address_row.no_of_times + 1
         fetch_ip_address_row.save()
         logger.debug("Ip address already present in the table. Adding +1 to the existing count")
      else:
         #Insert new row
         self.api_ip_address(ip_address)

      if ip_address in block_ip_addresses:
         logger.error("Ip address in blocking list. Redirecting to 404 page")
         raise Http404

   def api_ip_address(self, ip_address):
      #response = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s&position=true'%ip_address).read()
      #country = re.findall(r'Country:\s+(.*)',response)
      #city    = re.findall(r'City:\s+(.*)\n',response)
      #row = ipaddress_table()
      #row.ip_address = ip_address
      #row.country = country[0]
      #row.city    = city[0] #Date field will add current time automatically ?
      #row.no_of_times = 1
      row = ipaddress_table()
      row.ip_address = ip_address
      row.country = "no data"
      row.city    = "no data" #Date field will add current time automatically ?
      row.no_of_times = 1
      row.save()
      logger.debug("New IP address. Inserted a new record into table")
         
#Order.objects.order_by('-date')[0]
def home(request):
   logger.info("Entering the home view")
   ip_address_object = ipaddress_class()
   ip_address        = ip_address_object.get_ipaddress(request)
   ip_address_object.save_ipaddress(ip_address)

   logger.info("Redirecting to home page")

   #Total page views
   #total_page_views = ipaddress_table.objects.aggregate(Sum('no_of_times'))

   return render_to_response('home.html', 
				{#'total_page_views'   : total_page_views["no_of_times__sum"],
                                 'latest_recipes_one' : Article.objects.all().order_by('-pub_date')[:1],
                              	 'popular_recipes_one' : Article.objects.all().order_by('-likes')[0:1]})

def recipes_all(request):
    logger.info("Entering the recipes_all view")
    ip_address_object = ipaddress_class()
    ip_address        = ip_address_object.get_ipaddress(request)
    ip_address_object.save_ipaddress(ip_address)

    logger.info("Redirecting to recipes_all page")
    return render_to_response('recipes_all.html')


def recipetype (request, recipetype):
    logger.info("Entering the recipetype view")
    ip_address_object = ipaddress_class()
    ip_address        = ip_address_object.get_ipaddress(request)
    ip_address_object.save_ipaddress(ip_address)
    logger.debug("Successfully stored the ip address in the table")

    all_recipes = Article.objects.all()
    choices = Article.Recipe_list
    filtered_recipes = []
    if recipetype in choices:
        for recipe in all_recipes:
            if recipe.recipe_type==recipetype:
                filtered_recipes.append(recipe)
            elif recipe.recipe_type_1==recipetype:
                filtered_recipes.append(recipe)
            elif recipe.recipe_type_2==recipetype:
                filtered_recipes.append(recipe)
        logger.info("Successfully found the recipe type in the table. Now redirecting to recipe_type_new page")
        return render_to_response('recipe_type_new.html',
				{'recipes': filtered_recipes,
                                 'type' : recipetype})
    else:
        logger.error("Failed to find the recipe type in the table. Now redirecting to 404 page")
        raise Http404

def showrecipe (request, recipetitle=""):
   logger.info("Entering the showtype view. Recipe title - %s" %recipetitle)
   ip_address_object = ipaddress_class()
   ip_address        = ip_address_object.get_ipaddress(request)
   ip_address_object.save_ipaddress(ip_address)

   c={}
   c.update(csrf(request))
   try:
      recipe = Article.objects.get(title=recipetitle.replace("-"," "))
   except ObjectDoesNotExist:
      logger.error("Failed to find the recipe in the table. Now redirecting to 404 page")
      raise Http404

   logger.debug("Building ingredient dictionary")
   recipe_id = recipe.id
   ingredients = recipe.ingredients
   ingredients_split = ingredients.split('\n')    
   ingredient_dictionary= SortedDict()
   for ingredient in ingredients_split:
      if '<h>' in ingredient:
         match = re.search('\s*<h>\s*(.*)',ingredient)
         if match:
            ingredient_dictionary[match.group(1)] =[]
            key=match.group(1)
      elif ';' in ingredient:
         match = re.search('\s*(.*);\s*(.*)',ingredient)
         if match:
            ingredient_dictionary[key].append([match.group(1),match.group(2)])

   logger.debug("Building directions list")   
   directions = recipe.directions
   directions_split = directions.split('\n')

   logger.info("Adding 1 to the recipe page views: %s" %recipe.page_views)
   recipe.page_views = recipe.page_views + 1
   recipe.save()

   logger.debug("Getting comments and comment reply")
   comment_rows = comment_table.objects.filter(recipeid=recipe_id).order_by('date')
   if comment_rows:
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
      logger.debug("Add the number of comments and comment replies")
      comment_number =len(comment_table.objects.filter(recipeid=recipe_id))
      total_comments = comment_number +  comment_reply_number
   else:
      comment_rows = []
      comment_reply_dictionary = []
      total_comments = 0
      logger.info("No comments for this recipe")

   #You might also like and ten latest recipes
   logger.debug("Get the 'you might also like' list and 'latest_recipes_ten' list")
   you_might_also_like = []
   latest_recipes_ten = Article.objects.all().order_by('-pub_date')[:10]
   count = 0
   for fetch_you_might in latest_recipes_ten:
      if fetch_you_might.title != recipe.title and count < 3: #To ignore the current recipe
         you_might_also_like.append(fetch_you_might)
         count = count + 1

   #Popular recipes
   logger.debug("Get ten popular recipes list")
   popular_recipes_ten = Article.objects.all().order_by('-likes')[:10]

   #send mail - Ignore internal address, 10.35.63.79
#   if ip_address != "10.35.63.79":
#      subject='Ipaddress-%s, seen your recipe' %ip_address
#      message=' Recipe title -> %s \n Recipe url -> surekha-cookhouse.rhcloud.com/recipes/%s/%s/ \n'%(recipe.title, recipe.recipe_type, recipetitle)
#      Email_object = Email()
#      Email_object.send_email(subject, message)

   c.update({    'article'                  : recipe,
		 'latest_recipes_ten'       : latest_recipes_ten,
		 'popular_recipes_ten'      : popular_recipes_ten,
		 'ingredient'	            : ingredient_dictionary,
                 'direction'                : directions_split,
		 'recipe_title_url_format'  : recipetitle,
                 'comments'                 : comment_rows,
                 'comment_reply_dictionary' : comment_reply_dictionary,
                 'total_comments'           : total_comments,
                 'you_might_also_like'      : you_might_also_like
		})

   logger.info("Redirecting to show_recipe page")	    
   return render_to_response('show_recipe.html',c)

def popular_recipes(request):
    logger.info("Entering the popular_recipes view")
    ip_address_object = ipaddress_class()
    ip_address        = ip_address_object.get_ipaddress(request)
    ip_address_object.save_ipaddress(ip_address)

    logger.info("Redirecting to popular_or_latest_recipes page")
    return render_to_response('popular_or_latest_recipes.html',
				{'popular_or_latest_recipes_all': Article.objects.all().order_by('-likes'),
                                 'popular_or_latest'  : 'Popular recipes'})

def latest_recipes(request):
    logger.info("Entering the latest_recipes view")
    ip_address_object = ipaddress_class()
    ip_address        = ip_address_object.get_ipaddress(request)
    ip_address_object.save_ipaddress(ip_address)

    logger.info("Redirecting to popular_or_latest_recipes page")
    return render_to_response('popular_or_latest_recipes.html',
				{'popular_or_latest_recipes_all' : Article.objects.all().order_by('-pub_date'),
                                 'popular_or_latest'  : 'Latest recipes'})      

class Email:

    def __init__(self):
        self.from_email = settings.EMAIL_HOST_USER
        self.to_list    = ['thangabalu@gmail.com', 'surekhascookhouse@gmail.com']

    def send_email(self,subject, message):
        send_mail(subject, message, self.from_email, self.to_list, fail_silently=True)
    

def recipes_comments(request):
    logger.info("Entering the recipes_comments view")
    comment = request.POST.get('comment','')    
    name = request.POST.get('name','')
    if name == "":
      name="Anonymous"    
    recipe_id = request.POST.get('recipe_id','')
    recipe_type  = request.POST.get('recipe_type','')
    recipe_title = request.POST.get('recipe_title','')

    if re.findall(r'.*(href).*',comment) or re.findall(r'.*(http).*',comment)or re.findall(r'.*(<a).*',comment) or re.findall(r'.*(www.).*',comment) :
        logger.info("Seems like spam comment. Redirecting without doing anything")
        return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))

    #If comment field is empty, just redirect without writing to database
    if comment=="":
        logger.info("Comment field is empty. Redirecting without doing anything")
        return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))

    else:
        ip_address_object = ipaddress_class()
        ip_address        = ip_address_object.get_ipaddress(request)
        ip_address_object.save_ipaddress(ip_address)

        row = comment_table(comment=comment, name=name, recipeid_id=recipe_id)
        row.save()
	#Send email
	subject='Comment from %s, Ipaddress -%s' %(name, str(ip_address))
	message=' %s has left a comment for the below recipe:\n\n Recipe title -> %s \n Recipe url -> surekha-cookhouse.rhcloud.com/recipes/%s/%s/ \n Comment -> %s \n\n This comment is stored in the table comment_table'%(name,recipe_title,recipe_type,recipe_title,comment)
        Email_object = Email()
        Email_object.send_email(subject, message)
        logger.info("Stored the comment in the database. Successfuly sent email and redirecting to show recipe page")
        logger.info("subject - %s, message - %s" %(subject, message))
        return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))

@csrf_exempt
def recipes_comments_reply(request):
   logger.info("Entering the recipes_comments_reply view")
   name = request.POST.get('name','')
   if name == "":
      name="Anonymous"   
   comment = request.POST.get('comment','')
   comment_id = request.POST.get('comment_id','')

   recipe_type = request.POST.get('recipe_type','')
   recipe_title = request.POST.get('recipe_title_url_format','')

   if comment=="":
      logger.info("Comment field is empty. Redirecting without doing anything")
      return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))
   else:        
      ip_address_object = ipaddress_class()
      ip_address        = ip_address_object.get_ipaddress(request)
      ip_address_object.save_ipaddress(ip_address)

      row = comment_reply_table(name=name, comment_reply_id_id=comment_id, comment=comment )
      row.save()
      #Send email
      subject='Comment from %s, Ipaddress -%s' %(name, str(ip_address))
      message=' %s has replied for an existing comment for the below recipe:\n\n Recipe title -> %s \n Recipe url -> surekha-cookhouse.rhcloud.com/recipes/%s/%s/ \n Comment -> %s \n\n This comment is stored in the table comment_reply_table'%(name,recipe_title,recipe_type,recipe_title,comment)
      Email_object = Email()
      Email_object.send_email(subject, message)
      logger.info("Stored the reply of the comment in the database. Successfuly sent email and redirecting to show recipe page")
      logger.info("subject - %s, message - %s" %(subject, message))
      return HttpResponseRedirect('/recipes/%s/%s/'%(recipe_type,recipe_title))

def like_article(request, recipetype="",recipetitle=""):
    logger.info("Entering the like_article view")
    if recipetype and recipetitle:
        ip_address_object = ipaddress_class()
        ip_address        = ip_address_object.get_ipaddress(request)
        ip_address_object.save_ipaddress(ip_address)

        try:
            a = Article.objects.get(title=recipetitle.replace("-"," "))
        except ObjectDoesNotExist:
            logger.error("Failed to find the recipe in the table. Now redirecting to 404 page")
            raise Http404

        count = a.likes
        logger.info("Previous likes number is %s" %count)
	count += 1
	a.likes = count
	a.save()
        logger.info("New likes number is %s" %count)

	subject='IpAddress-%s, liked %s'%(str(ip_address), a.title)
	message=' Recipe title -> %s \n Recipe url -> surekha-cookhouse.rhcloud.com/recipes/%s/%s/ \n'%(a.title, a.recipe_type, recipetitle)
        Email_object = Email()
        Email_object.send_email(subject, message)
        return HttpResponseRedirect('/recipes/%s/%s/'% (recipetype,recipetitle))
    else:
        logger.error("Failed to find the recipe type in the table. Now redirecting to 404 page")
        raise Http404

def search(request):
   logger.info("Entering the search view")
   ip_address_object = ipaddress_class()
   ip_address        = ip_address_object.get_ipaddress(request)
   ip_address_object.save_ipaddress(ip_address)

   c={}
   c.update(csrf(request))
   logger.info("Redirecting to search.html")   
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

def contact(request):
   logger.info("Entering the contact view")
   ip_address_object = ipaddress_class()
   ip_address        = ip_address_object.get_ipaddress(request)
   ip_address_object.save_ipaddress(ip_address)

   c={}
   c.update(csrf(request))
   logger.info("Redirecting to contact.html")   
   return render_to_response('contact.html',c)

def contact_submit(request):
   logger.info("Entering the contact_submit view")
   ip_address_object = ipaddress_class()
   ip_address        = ip_address_object.get_ipaddress(request)
   ip_address_object.save_ipaddress(ip_address)

   name = request.POST.get('name','')    
   email = request.POST.get('email','')    
   question_subject = request.POST.get('subject','')
   message = request.POST.get('message','')
    
   #Send email
   subject='Question from %s' %(name)
   message='Email id -%s\n Subject -%s\n Message-%s\n'%(email,question_subject,message)
   Email_object = Email()
   Email_object.send_email(subject, message)
   logger.info("Sent the email for contact page contents")
   logger.info("subject - %s, message - %s" %(subject, message))
   return HttpResponse(json.dumps("success"))
