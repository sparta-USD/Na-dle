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
    
    def avg_grade(self):
        reviews = self.reviews.all() # Review 역참조
        sum_grade = 0
        if reviews:
            for review in reviews:
                sum_grade += review.grade
            avg_grade = sum_grade / len(reviews)
            avg_grade = round(avg_grade, 1)
            return avg_grade
        else: # 리뷰가 없다면
            return 0

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_reviews")
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grade = models.IntegerField()

    def __str__(self):
        return str(self.content)

