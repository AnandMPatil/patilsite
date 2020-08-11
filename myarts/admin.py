from django.contrib import admin
from myarts.models import Article ,Comment,Fav

# Register your models here.
# Define the PicAdmin class
class PicAdmin(admin.ModelAdmin):
    exclude = ('picture', 'content_type')

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Fav)
