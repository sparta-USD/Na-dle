from django.db import models

# Create your models here.
class Music(models.Model):
    title = models.CharField(max_length=50)
    image = models.TextField()
    artist = models.CharField(max_length=20)
    album = models.CharField(max_length = 50)
    track_id = models.CharField(max_length = 50)

    def __str__(self):
        return str(self.title)