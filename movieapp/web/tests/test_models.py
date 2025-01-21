from django.test import TestCase
from web.models import Genre, Language, Movie, MpaaRating

# Create your tests here.


class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Genre.objects.create(name='Comedy')

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name

        self.assertEqual(field_label, 'name')
        self.assertEqual(genre.name, 'Comedy')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length

        self.assertEqual(max_length, 50)


class LanguageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Language.objects.create(name='English')

    def test_name_label(self):
        lang = Language.objects.get(id=1)
        field_label = lang._meta.get_field('name').verbose_name

        self.assertEqual(field_label, 'name')
        self.assertEqual(lang.name, 'English')

    def test_name_max_length(self):
        lang = Language.objects.get(id=1)
        max_length = lang._meta.get_field('name').max_length

        self.assertEqual(max_length, 50)


class MpaaRatingModelTest(TestCase):

    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.mpa = MpaaRating.objects.create(type='PG', label='Some Violence')
        self.mpa_empty_label = MpaaRating.objects.create(type='PG')

    def test_type_label(self):
        field_label = self.mpa._meta.get_field('type').verbose_name
        max_length = self.mpa._meta.get_field('type').max_length

        self.assertEqual(field_label, 'type')
        self.assertEqual(self.mpa.type, 'PG')
        self.assertEqual(max_length, 50)

    def test_label(self):
        field_label = self.mpa._meta.get_field('label').verbose_name
        max_length = self.mpa._meta.get_field('label').max_length

        self.assertEqual(field_label, 'label')
        self.assertEqual(self.mpa.label, 'Some Violence')
        self.assertEqual(max_length, 100)

    def test_label_when_empty(self):
        self.assertEqual(str(self.mpa_empty_label.label), "")


class MovieModelTest(TestCase):

    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.genre1 = Genre.objects.create(name='Action')
        self.genre2 = Genre.objects.create(name='Adventure')
        self.lang = Language.objects.create(name='English')
        self.mpa = MpaaRating.objects.create(type='PG', label='Some Violence')
        self.movie = Movie.objects.create(
            name="Marvel's Captain America: Civil War",
            description="Marvel’s Captain America: Civil War picks up where - Avengers: Age of Ultron - left off, as Steve Rogers leads the new team of Avengers in their continued efforts to safeguard humanity. After another international incident involving the Avengers results in collateral damage, political pressure mounts to install a system of accountability and a governing body to determine when to enlist the services of the team. The new status quo fractures the Avengers while they try to protect the world from a new and nefarious villain.",
            img_path="assets/images/civilwar.jpg",
            duration=148,
            user_rating="5",
            language=self.lang,
            mpaa_rating=self.mpa,
        )
        # handle ManyToMany fields while testing
        self.movie.genre.set([self.genre1, self.genre2])

    def test_name_label(self):
        field_label = self.movie._meta.get_field('name').verbose_name

        self.assertEqual(field_label, 'name')
        self.assertEqual(self.movie.name, "Marvel's Captain America: Civil War")

    def test_genre_length(self):
        genre = self.movie.genre.all()

        self.assertEqual(len(genre), 2)
