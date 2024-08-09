from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    post = models.CharField(max_length=1000, null=True, blank=True)
    time_date = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Posted by {self.user} on {self.time_date}"
# Reminder for me:
# Profile page should have: number of followers, number of following
# Posts for that user but that's solved with Post model
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return f"{self.user} follows {self.follower}"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")

    def __str__(self):
        return f"{self.user} liked {self.post}"