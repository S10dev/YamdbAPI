from django.contrib import admin
from .models import Title, Category, Genre, Review, Comment, User
# Register your models here.

class titleadmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category',) 
    search_fields = ("name",) 
    list_filter = ("year",) 
    empty_value_display = "-пусто-"


class Reviewadmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'score', 'title', 'pub_date') 
    search_fields = ("author",) 
    list_filter = ("author",) 
    empty_value_display = "-пусто-"


class Commentadmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'review', 'pub_date') 
    search_fields = ("author",) 
    list_filter = ("author",) 
    empty_value_display = "-пусто-"

admin.site.register(User,)
admin.site.register(Title, titleadmin)
admin.site.register(Category,)
admin.site.register(Genre,)
admin.site.register(Review, Reviewadmin)
admin.site.register(Comment, Commentadmin)