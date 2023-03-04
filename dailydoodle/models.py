from django.db import models
from django.contrib.auth.models import User
import os
from daily_doodle_project import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.

# Add a signal for when user is deleted
@receiver(pre_delete,sender=User)
def handle_user_deletion(sender,instance,**kwargs):
    # delete the stored profile picture on delete 
    try:
        dir = f"{settings.MEDIA_ROOT}/profile_images/{instance.username}.jpg"
        dir.replace("\\","/")      
        os.remove(dir)
    except:
        print("user profile was default")

#Add a signal when a drawing is deleted (DOES NOT WORK AS EXPECTED)
@receiver(pre_delete,sender=User)
def handle_drawing_deletion(sender,instance,**kwargs):
    try: 
        dir = f"{settings.MEDIA_ROOT}/submissions/{instance.drawing_id}.jpeg"
        dir.replace("\\","/")
        print(dir)
        os.remove(dir)
    except:
            print("could not delete drawing file")

# UserProfile model to store profile picture of every user
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_images",blank=True)

    def __str__(self):
        return self.user.username
    
    # def save(self, *args, **kwargs):
    #     # resize the profile_picture to the desired resolution


# Prompt model
class Prompt(models.Model):
    prompt = models.CharField(max_length=30,unique=True)
    prompt_date = models.DateField()

    def __str__(self):
        return self.prompt


# Drawing model
class Drawing(models.Model):
    drawing = models.ImageField(upload_to="submissions",blank=False)
    drawing_id = models.CharField(max_length=61,unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt,on_delete=models.CASCADE)


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
    