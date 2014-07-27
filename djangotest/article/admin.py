from django.contrib import admin
from article.models import Article
from article.models import comment_table
from article.models import ipaddress_table
from article.models import comment_reply_table

# Register your models here.

# The following line registers the "Article" model to the admin

admin.site.register(Article)
admin.site.register(comment_table)
admin.site.register(ipaddress_table)
admin.site.register(comment_reply_table)