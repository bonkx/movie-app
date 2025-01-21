from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Genres"
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message="Genre already exists (case insensitive match)"
            ),
        ]


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Languages"
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message="Language already exists (case insensitive match)"
            ),
        ]


class MpaaRating(models.Model):
    type = models.CharField(max_length=50)
    label = models.CharField(max_length=100, default="", blank=True, null=True)

    def __str__(self):
        if self.label is None:
            self.label = ""
        return "{}-{}".format(self.type, self.label)

    class Meta:
        ordering = ("type",)
        verbose_name_plural = "Mpaa Ratings"


class Movie(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    img_path = models.CharField(max_length=255)
    duration = models.IntegerField()
    user_rating = models.CharField(max_length=1)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    mpaa_rating = models.ForeignKey(MpaaRating, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('movie_details', args=[str(self.id)])

    class Meta:
        ordering = ("id",)
        verbose_name_plural = "Movies"
