import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from web.models import Genre, Language, Movie, MpaaRating


def clear_genre():
    print('----- clear_genre')
    Genre.objects.all().delete()


def clear_language():
    print('----- clear_language')
    Language.objects.all().delete()


def clear_mpaarating():
    print('----- clear_mpaarating')
    MpaaRating.objects.all().delete()


class Command(BaseCommand):
    help = 'Create movie data from json file'

    def handle(self, *args, **options):
        # remove Genre
        clear_genre()
        # remove Language
        clear_language()
        # remove MpaaRating
        clear_mpaarating()

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
                for g in genre_list:
                    movie.genre.add(g)
                print(f'Movie :', movie)

        self.stdout.write(self.style.SUCCESS('Successfully created movies'))
