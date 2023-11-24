from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    userID = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='images/profile_pics/', null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    def matches_search_query(self, search_query):
        return (
            self.full_name.lower().find(search_query.lower()) != -1
        )

    def __str__(self):
        return self.username


class Post(models.Model):
    postID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey to User model
    description = models.TextField()
    image = models.ImageField(upload_to='images/post_images/', blank=True, null=True)
    item_name = models.CharField(max_length=255)
    fo_name = models.CharField(max_length=255)
    time_place = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    contact = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)  # This field will automatically store the creation time



    def __str__(self):
        return f"Post by {self.userID.username}"\

    def matches_search_query(self, search_query):
        return (
            self.description.lower().find(search_query.lower()) != -1 or
            self.item_name.lower().find(search_query.lower()) != -1 or
            self.time_place.lower().find(search_query.lower()) != -1 or
            self.status.lower().find(search_query.lower()) != -1
        )

class Rating(models.Model):
    ratingID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey to User model
    ratings = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating by {self.userID.username}"