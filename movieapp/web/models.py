from django.db import models

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Genres"


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Languages"


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

    class Meta:
        ordering = ("id",)
        verbose_name_plural = "Movies"
