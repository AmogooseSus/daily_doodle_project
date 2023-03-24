import os
import environ


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_doodle_project.settings')

env = environ.Env()
environ.Env.read_env()

os.environ["SECRET_KEY"] = env("SECRET_KEY")

import django
django.setup()
from daily_doodle_project.settings import BASE_DIR

from django.contrib.auth.models import User
from dailydoodle.models import UserProfile, Prompt, Drawing, Comment, Rating
from datetime import date,datetime,timedelta
import shutil
import random
from dailydoodle.apis import get_random_profile_picture

password= "0I&NAjqFRZ"
users = ["Harry","Ferdinand","Chisha","Scot","Nathan","Robert","John", "Michael","David","Olivia","Emma", "Evelyn","Luna", "Eleanor"]
prompts = [
    "scream",
    "dog",
    "cat",
    "horse",
    "car",
    "train",
    "insects",
]


def create_users():
    print("Creating users......(this may take a while due to user profile created along side)")
    print("Ignore any internal server errors the website still works :)")
    for user in users:
        try:
            new_user = User(username=user,email=f"{user}@{user}.com")
            new_user.set_password(password)
            new_user.save()
            UserProfile.objects.create(user=new_user,profile_picture=get_random_profile_picture(new_user.username))
        except:
            pass
    print("Created all users successfully")


def create_prompts():
    print("Creating prompts......")
    dates = []
    for x in range(1,len(prompts)+1):
        dates.append(date.today() - timedelta(days=x))
    for prompt,date_stamp in zip(prompts,dates):
        Prompt.objects.get_or_create(prompt=prompt,prompt_date=date_stamp)
    print("Created all prompts successfully")


def create_drawings():
    print("Creating drawings......")
    sample_drawings = []
    for x in range(1,11):
        sample_drawings.append(os.path.join(BASE_DIR,"media/submissions/",f"Sample{x}.jpeg"))
    for user in users:
        for prompt in list(Prompt.objects.all().values()):
            random_sample = random.choice(sample_drawings)
            user_drawing = os.path.join(BASE_DIR,"media/submissions/",f"{user}-{prompt['prompt']}.jpeg")
            shutil.copyfile(random_sample,user_drawing)
            Drawing.objects.get_or_create(drawing_id=f"{prompt['prompt']}-{user}",user=User.objects.get(username=user),drawing=f"submissions/{user}-{prompt['prompt']}.jpeg",prompt=Prompt.objects.get(prompt=prompt["prompt"]))
    print("Finished creating drawings")

def create_ratings():
    print("Creating ratings........(This may take bit longer due random data being generated here)")
    all_drawings = list(Drawing.objects.all().values())
    all_users = list(User.objects.all().values())
    for x in range(500):
        random_drawing = random.choice(all_drawings)
        random_user  = random.choice(all_users)
        while(User.objects.get(username=random_user["username"]) != User.objects.get(id=random_drawing["user_id"]) and len(Rating.objects.filter(user=User.objects.get(username=random_user["username"]),drawing=Drawing.objects.get(drawing_id=random_drawing["drawing_id"]))) != 0):
            random_user = random.choice(all_users)
        Rating.objects.get_or_create(user=User.objects.get(username=random_user["username"]),drawing=Drawing.objects.get(drawing_id=random_drawing["drawing_id"]))
    print("Done creating ratings")

def create_comments():
    print("Creating comments.........")
    comments = ["cool","amazing","nice","I hate this never draw it again","Wow!","This is good but mines better","lol","What is that even supposed to be"," Even I can do better than that",
                 "Hmmmm","Not good","emmmm.....","This could have been better","nah......","crazy"
                ]
    all_drawings = list(Drawing.objects.all().values())
    all_users = list(User.objects.all().values())
    for x in range(100):
        random_drawing = random.choice(all_drawings)
        random_user  = random.choice(all_users)
        random_comment = random.choice(comments)
        Comment.objects.get_or_create(user=User.objects.get(username=random_user["username"]),drawing=Drawing.objects.get(drawing_id=random_drawing["drawing_id"]),date=datetime.today(),comment=random_comment)
    print("Done creating comments")

def populate():
    create_users()
    create_prompts()
    create_drawings()
    create_ratings()
    create_comments()

if __name__ == '__main__':
    print("Starting population script...")
    populate()
    