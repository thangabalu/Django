from django.contrib import admin

from article.models import Article
from article.models import comment_table
from article.models import ipaddress_table
from article.models import comment_reply_table

# Register your models here.

# The following line registers the "Article" model to the admin
class ipadress_table_admin(admin.ModelAdmin):  
    list_display = ('ip_address', 'date', 'no_of_times', 'country', 'city')
    ordering = ('-date',) # The negative sign indicate descendent order. Latest ones on top
    list_per_page = 300
    search_fields = ('ip_address', )

class Article_admin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'likes', 'page_views', 'visit_page')
    search_fields = ('title', )

    def visit_page(self, obj):
        title_split = obj.title.split()
        title_join = "-".join(title_split)
        url = "surekha-cookhouse.rhcloud.com/recipes/%s/%s" %(obj.recipe_type, title_join)
        #return '<a href="%s">%s</a>' % (url, url)
        return url
    #visit_page.allow_tags = True

class comment_table_admin(admin.ModelAdmin):
    list_display = ('name', 'date', 'comment')
    ordering = ('-date',)

class comment_reply_table_admin(admin.ModelAdmin):
    list_display = ('name', 'date', 'comment')
    ordering = ('-date',)

admin.site.register(Article, Article_admin)
admin.site.register(comment_table, comment_table_admin)
admin.site.register(ipaddress_table, ipadress_table_admin)
admin.site.register(comment_reply_table, comment_reply_table_admin)
