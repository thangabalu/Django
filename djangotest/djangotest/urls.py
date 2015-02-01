from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangotest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^$', 'article.views.home'),
    url(r'^contact/$', 'article.views.contact'),
    url(r'^contact_submit/$', 'article.views.contact_submit'),
    url(r'^search/$', 'article.views.search'),
    url(r'^search_titles/$', 'article.views.search_titles'),
    url(r'^popular_recipes/$', 'article.views.popular_recipes'),
    url(r'^latest_recipes/$', 'article.views.latest_recipes'),
    url(r'^recipes/', include('article.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
