from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_author")
    content = models.CharField(max_length=128)
    date_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="posts_liked")

    def __str__(self):
        return f"{self.author} {self.date_time}"

class Follow(models.Model):
    # Person that wants to follow
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower")
    # Person that was followed
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")

    def __str__(self):
        return f"{self.follower} follows {self.following}"