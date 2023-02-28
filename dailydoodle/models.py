from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# UserProfile model to store profile picture of every user
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_images",blank=True)

    def __str__(self):
        return self.user.username

# Prompt model
class Prompt(models.Model):
    prompt = models.CharField(max_length=30,unique=True)
    prompt_date = models.DateField()

    def __str__(self):
        return self.prompt


# Drawing model
class Drawing(models.Model):
    drawing = models.ImageField(upload_to="drawings",blank=False)
    drawing_id = models.CharField(max_length=61,unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    prompt = models.OneToOneField(Prompt,on_delete=models.CASCADE)

# Comment model
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField()
    comment = models.CharField(max_length=200,unique=False)
    drawing = models.ForeignKey(Drawing,on_delete=models.CASCADE)

# Rating model
class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    drawing = models.ForeignKey(Drawing,on_delete=models.CASCADE)
    