import json
import os

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode
from web.models import Genre, Language, Movie, MpaaRating

# def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
#     '''Custom reverse to handle query strings.
#     Usage:
#         reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
#     '''
#     base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
#     if query_kwargs:
#         return '{}?{}'.format(base_url, urlencode(query_kwargs))
#     return base_url


@pytest.mark.django_db
class TestMovieListViews:
    @pytest.fixture(autouse=True)
    def init(self,  client):
        self.client = client

    @pytest.fixture(autouse=True)
    def setup_data(self):
        # populate movies data
        # insert movies data
        jfile = os.path.join(settings.BASE_DIR, 'movies.json')
        # encode json file
        with open(jfile, encoding='utf-8') as json_data:
            dt = json.load(json_data)
            for data in dt:
                # print(data['name'])
                # print(data['description'])

                # NORMALIZE GENRE
                # print(data['genre'])
                data_genre_dumps = json.dumps(data['genre'])
                data_genre_replace = data_genre_dumps.replace("'", '"')
                # print(data_genre_replace)
                data_genre_dict = json.loads(data_genre_replace)
                # print(data_genre_dict)

                genre_list = list()
                # create Genre
                for genre in data_genre_dict:
                    gen, _ = Genre.objects.get_or_create(name=genre)
                    genre_list.append(gen)
                print(f'Genre :', genre_list)
                # create Language
                lang, _ = Language.objects.get_or_create(name=data['language'])
                print(f'Language :', lang)
                # create MpaaRating
                mpaarating, _ = MpaaRating.objects.get_or_create(type=data['mpaaRating']['type'], label=data['mpaaRating']['label'])
                print(f'MpaaRating :', mpaarating)

                movie, _ = Movie.objects.get_or_create(
                    name=data['name'],
                    description=data['description'],
                    img_path=data['imgPath'],
                    duration=data['duration'],
                    user_rating=data['userRating'],
                    language=lang,
                    mpaa_rating=mpaarating,
                )
                # add genres to movie
                movie.genre.set(genre_list)
                print(f'Movie :', movie)

        movies = Movie.objects.all()
        assert movies.count() == 15  # all movies
        assert len(movies[0].genre.all()) == 2  # Marvel's Captain America: Civil War movie

        self.movies = movies

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')

        # check the response status code is 200
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        url = reverse('home')
        response = self.client.get(url)

        # check the response status code is 200
        assert response.status_code == 200

    def test_view_uses_correct_template(self):
        url = reverse('home')
        response = self.client.get(url)
        
        assert response.status_code == 200
        # check the template used
        assert 'web/home.html' in (t.name for t in response.templates)

    def test_view_url_invalid_request(self):
        url = reverse('home')
        response = self.client.post(url)
        data = response.json()
        print(data)

        assert "status" in data
        assert data["status"] == "Invalid request"

    def test_view_with_search_param(self):
        # kwargs={'pk': 123}, query_kwargs={'search': 'Bob'}

        query_kwargs = {"q": "marvel"}
        url = '{}?{}'.format(reverse('home'), urlencode(query_kwargs))
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'Marvel' in str(response.content)

    def test_view_paginator_except(self):
        query_kwargs = {"page": "not integer"}
        url = '{}?{}'.format(reverse('home'), urlencode(query_kwargs))
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'Marvel' in str(response.content)

    def test_view_paginator_empty_page_back_to_last_page(self):
        query_kwargs = {"page": 10}
        url = '{}?{}'.format(reverse('home'), urlencode(query_kwargs))
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'Zootopia' in str(response.content)

    def test_movie_details_page(self):
        url = '{}'.format(reverse('movie_details', args=[1]))
        response = self.client.get(url)

        assert response.status_code == 200

    def test_movie_details_page_correct_template(self):
        url = '{}'.format(reverse('movie_details', args=[1]))
        response = self.client.get(url)

        assert response.status_code == 200
        # check the template used
        assert 'web/details.html' in (t.name for t in response.templates)

    def test_movie_details_page_not_found(self):
        url = '{}'.format(reverse('movie_details', args=[123]))
        response = self.client.get(url)

        assert response.status_code == 404
