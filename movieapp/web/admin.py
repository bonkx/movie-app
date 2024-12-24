from django.contrib import admin
from web.models import Genre, Language, Movie, MpaaRating

# Register your models here.


@admin.register(Movie, site=admin.site)
class MovieAdmin(admin.ModelAdmin):
    model = Movie
    search_fields = ("name", "description",)
    list_display = ('id', 'name', 'description', 'img_path', 'duration', 'user_rating', 'language', 'get_genre', 'mpaa_rating')

    def get_genre(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    get_genre.short_description = 'Genre'


@admin.register(Genre, site=admin.site)
class GenreAdmin(admin.ModelAdmin):
    model = Genre
    search_fields = ("name", )
    list_display = [f.name for f in model._meta.fields]


@admin.register(Language, site=admin.site)
class LanguageAdmin(admin.ModelAdmin):
    model = Language
    search_fields = ("name", )
    list_display = [f.name for f in model._meta.fields]


@admin.register(MpaaRating, site=admin.site)
class MpaaRatingAdmin(admin.ModelAdmin):
    model = MpaaRating
    search_fields = ("type", "label",)
    list_display = [f.name for f in model._meta.fields]
