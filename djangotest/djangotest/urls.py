from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangotest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^home/$', 'article.views.home'),
    url(r'^$', 'article.views.home'),
    url(r'^contact/$', 'article.views.contact'),
    url(r'^contact_submit/$', 'article.views.contact_submit'),
    url(r'^search/$', 'article.views.search'),
    url(r'^search_titles/$', 'article.views.search_titles'),
    url(r'^recipes/', include('article.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
