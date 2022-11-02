from django.db import models
from users.models import User

# Create your models here.
class Music(models.Model):
    title = models.CharField(max_length=50)
    image = models.TextField()
    artist = models.CharField(max_length=20)
    album = models.CharField(max_length = 50)
    track_id = models.CharField(max_length = 50)

    def __str__(self):
        return str(self.title)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grade = models.IntegerField()

    def __str__(self):
        return str(self.content)

