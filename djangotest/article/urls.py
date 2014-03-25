from django.conf.urls import patterns, include, url

urlpatterns =patterns('',
	url(r'^all/$', 'article.views.articles'),
	#url(r'^get/(?P<article_id>\d+)/$', 'article.views.article'),
	# P  - passing a parameter
	#url(r'^get/(?P<article_title>)/$', 'article.views.article'),
	url(r'^(?P<article_title>[-\w\d]+)/$', 'article.views.article'),
)
