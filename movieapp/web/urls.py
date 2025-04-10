from django.urls import include, path
from web import views

urlpatterns = [

    path("", views.index, name="home"),
    # path("ajax/movie-list/", views.movie_list, name="movie_list"),
    path("movies/<int:pk>/", views.details, name="movie_details"),

]
