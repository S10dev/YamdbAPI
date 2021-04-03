from django.contrib import admin
from .models import Title, Category, Genre
# Register your models here.

class titleadmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category', 'genre') 
    search_fields = ("name",) 
    list_filter = ("year",) 
    empty_value_display = "-пусто-"

admin.site.register(Title, titleadmin)
admin.site.register(Category,)
admin.site.register(Genre,)