from django.test import TestCase
from django.urls import reverse
from web.models import Genre, Language, Movie, MpaaRating


class MovieListViewsTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')

        # check the response status code is 200
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))

        # check the response status code is 200
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))

        # check the response status code is 200
        self.assertEqual(response.status_code, 200)

        # check the template used
        self.assertTemplateUsed(response, 'web/home.html')

    def test_movie_list_ajax_exception_method(self):
        response = self.client.post(reverse('movie_list'))

        # check the response status code is 400
        self.assertEqual(response.status_code, 400)
        # check the message is correct
        self.assertEqual(response.json()['status'], "Invalid request")
