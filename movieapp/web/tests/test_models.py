import pytest
from django.contrib.auth.models import User
from web.models import Genre, Language, Movie, MpaaRating


@pytest.mark.django_db
class TestGenreModel:
    @pytest.fixture(autouse=True)
    def init(self,  payload_genre):
        self.payload_genre = payload_genre

    def test_create_genre(self):
        obj = Genre.objects.create(name=self.payload_genre['name'])
        assert Genre.objects.count() == 1
        assert obj.name == self.payload_genre['name']
        assert obj.__str__() == self.payload_genre['name']


@pytest.mark.django_db
class TestLanguageModel:
    @pytest.fixture(autouse=True)
    def init(self,  payload_language):
        self.payload_language = payload_language

    def test_create_language(self):
        obj = Language.objects.create(name=self.payload_language['name'])
        assert Language.objects.count() == 1
        assert obj.name == self.payload_language['name']
        assert obj.__str__() == self.payload_language['name']


@pytest.mark.django_db
class TestMpaaRatingModel:
    @pytest.fixture(autouse=True)
    def init(self,  payload_mpaarating):
        self.payload_mpaarating = payload_mpaarating

    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.mpa = MpaaRating.objects.create(type=self.payload_mpaarating['type'], label=self.payload_mpaarating['label'])
        self.mpa_empty_label = MpaaRating.objects.create(type='PG', label=None)

    def test_type_label(self):
        assert self.mpa.__str__() == f"{self.payload_mpaarating['type']}-{self.payload_mpaarating['label']}"

    def test_label_when_empty(self):
        assert self.mpa_empty_label.label == None
        assert self.mpa_empty_label.__str__() == "PG-"


@pytest.mark.django_db
class TestMovieModel:
    @pytest.fixture(autouse=True)
    def init(self,  payload_movie):
        self.payload_movie = payload_movie

    @pytest.fixture(autouse=True)
    def setup_data(self):
        genre_list = list()
        # create Genre
        for genre in self.payload_movie['genre']:
            gen = Genre.objects.create(name=genre)
            genre_list.append(gen)
        # create Language
        self.lang = Language.objects.create(name=self.payload_movie['language'])
        # create MpaaRating
        self.mpaarating = MpaaRating.objects.create(type=self.payload_movie['mpaaRating']['type'], label=self.payload_movie['mpaaRating']['label'])

        self.movie = Movie.objects.create(
            name=self.payload_movie['name'],
            description=self.payload_movie['description'],
            img_path=self.payload_movie['imgPath'],
            duration=self.payload_movie['duration'],
            user_rating=self.payload_movie['userRating'],
            language=self.lang,
            mpaa_rating=self.mpaarating,
        )

        # handle ManyToMany fields
        self.movie.genre.set(genre_list)

    def test_name_label(self):
        assert self.movie.__str__() == self.payload_movie['name']

    def test_genre_length(self):
        genre = self.movie.genre.all()

        assert len(genre) == len(self.payload_movie['genre'])

    def test_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        assert self.movie.get_absolute_url() == '/movies/1/'


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('john_doe', 'john_doe@example.com', 'john_doe_password')
    assert User.objects.count() == 1
