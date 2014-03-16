from django.shortcuts import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from article.models import Article

# Create your views here.

def hello(request):
    name = "Prabhu"
    html = "<html> <body> Hi %s, this is working. Thank god </body></html>" %name
    return HttpResponse(html)

def hello_template(request):
    name = "Balu"
    t = get_template('hello.html')
    html = t.render(Context({'name' : name}))
    return HttpResponse(html)

def hello_template_simple(request):
    name = "Surekha"
    return render_to_response('hello.html', {'name': name})

def articles(request):
    return render_to_response('articles.html',
				{'articles': Article.objects.all()})

#If the url doesn't have the article id, default is 1
def article (request, article_id=1):
    return render_to_response('article.html',
				{'article': Article.objects.get(id=article_id) })
