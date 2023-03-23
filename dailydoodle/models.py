from django.db import models
from django.contrib.auth.models import User
import os
from daily_doodle_project import settings
from django.db.models.signals import pre_delete,pre_save
from django.dispatch import receiver

# Create your models here.

# Add a signal for when user is deleted
@receiver(pre_delete,sender=User)
def handle_user_deletion(sender,instance,**kwargs):
    # delete the stored profile picture on delete 
    try:
        profile = UserProfile.objects.get(user=instance)
        profile.profile_picture.delete()
    except:
        print("user profile was default")

def rename_path(instance,filename):
    file_type = filename[filename.rfind("."):]
    return f"profile_images/{instance.user.username}{file_type}"

# UserProfile model to store profile picture of every user
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=rename_path,blank=True)
    # we add this to query top users easily, however Rating table must be used to get relation between user and drawing upvote
    upvotes_recieved = models.IntegerField(default=0)


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
    drawing = models.ImageField(upload_to="submissions",blank=False)
    drawing_id = models.CharField(max_length=61,unique=True,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt,on_delete=models.CASCADE)
    # we add this to make querying top drawings easier, however Rating table must be used to get relation between user and drawing upvote
    total_upvotes = models.IntegerField(default=0)


#Add a signal when a drawing is deleted
@receiver(pre_delete,sender=Drawing)
def handle_drawing_deletion(sender,instance,**kwargs):
    try: 
        instance.drawing.delete()
    except:
            print("could not delete drawing file")


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


# Add a signal before a Rating is created so we can update user upvotes and drawing upvotes
@receiver(pre_save,sender=Rating)
def handle_rating_creation(sender,instance,**kwargs):
    user_profile = UserProfile.objects.filter(user=instance.drawing.user)[0]
    user_profile.upvotes_recieved += 1
    user_profile.save()
    instance.drawing.total_upvotes += 1
    instance.drawing.save()

# Add a signal before a Rating is created so we can update user upvotes and drawing upvotes
@receiver(pre_delete,sender=Rating)
def handle_rating_deletion(sender,instance,**kwargs):
    user_profile = UserProfile.objects.filter(user=instance.drawing.user)[0]
    user_profile.upvotes_recieved -= 1
    user_profile.save()
    instance.drawing.total_upvotes -= 1
    instance.drawing.save()
    

    