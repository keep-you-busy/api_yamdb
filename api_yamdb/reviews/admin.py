from django.contrib import admin
from .models import Category, Genre, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'get_genre')
    empty_value_display = '-пусто-'

    def get_genre(self, title):
        return title.genre.all()


admin.site.register(Genre)
admin.site.register(Category)
