from django.conf.urls import patterns, include, url

urlpatterns =patterns('',
	#url(r'^all/$', 'article.views.articles'),
	url(r'^all/$', 'article.views.recipes_all'),
	# P  - passing a parameter
	url(r'^(?P<recipetype>[-\w\d\s]+)/$', 'article.views.recipetype'),
	url(r'^[\w]+/(?P<recipetitle>[-\w\d\s()]+)/$', 'article.views.showrecipe'),
	url(r'^(?P<recipetype>[-\w\d\s]+)/(?P<recipetitle>[-\w\d\s()]+)/like/$', 'article.views.like_article'),
)
