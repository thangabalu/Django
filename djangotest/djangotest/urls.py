from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangotest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^home/$', 'article.views.home'),
    url(r'^$', 'article.views.home'),
    url(r'^recipes/', include('article.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
