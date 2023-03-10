from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from dailydoodle.models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from registration.backends.simple.views import RegistrationView
from django.utils.decorators import method_decorator
from dailydoodle.apis import *
from dailydoodle.view_helpers import *
from datetime import date
from daily_doodle_project.settings import MEDIA_URL,MEDIA_ROOT
import base64


# Create your views here.

# NOTE any class views that don't benifit from using class based syntax will
# be reverted to a function

# Class view for homepage 
class Index(View):

    def get(self,request):
        context_dict = {}
        # get top 5 drawings (use helper function) and add them to context dict
        # get todays prompt 
        prompt = Prompt.objects.filter(prompt_date=date.today())[0]
        if(request.user.username):
            # get users submission if exists or add none to context dict
            user_drawing = Drawing.objects.filter(user=request.user,prompt=prompt)
            if len(user_drawing) != 0:
                user_drawing = user_drawing[0]
                context_dict["user_drawing"] = user_drawing.drawing
            else:
                context_dict["user_drawing"]  = None
        context_dict["prompt"] = prompt.prompt 
        context_dict["MEDIA_URL"] = MEDIA_URL
        return render(request,"dailydoodle/index.html",context=context_dict)
    

# Class view for collections
class Collections(View):

    @method_decorator(login_required)
    def get(self,request):
        # get intial n prompts using helper function and add to context dict
        # get intial n drawings using helper function and add to context dictionary
        return render(request,"dailydoodle/collections.html")
    
    # Also add method for handling searching of prompts, getting more prompts and getting more drawings


# Class view for any users submissions
class Submissions(View):

    def get(self,request):
        # get user 
        # get intial n drawings user has participated in
        # get intial n prompts user has participated in
        return render(request,"dailydoodle/submissions.html")
    
    # Also add method for handling searching of prompts and getting more prompts



# Class view for leadboards
class LeaderBoard(View):

    def get(self,request):
        # logic here needs more thinking 
        return render(request,"dailydoodle/leaderboard.html")
    
    # Also add method for handling searching of users via post request
    

# Class view for profile
class Profile(View):

    def get(self,request):
        # simply return users username,email and profile picture
        return render(request,"dailydoodle/profile.html") 
    
    # Also add method for handling profile changes


# Class view for Draw mode
class Draw(View):

    @method_decorator(login_required)
    def get(self,request):
        prompt = Prompt.objects.filter(prompt_date=date.today())[0]
        user_drawing = Drawing.objects.filter(user=request.user,prompt=prompt)
        if(len(user_drawing) != 0):
           return redirect(reverse("dailydoodle:index"))
        context_dict = {}
        # get todays prompt
        prompt = Prompt.objects.filter(prompt_date=date.today())[0]
        context_dict["prompt"] = prompt.prompt
        return render(request,"dailydoodle/draw.html",context=context_dict)
    
    # handle submissions of drawings
    @method_decorator(login_required)
    def post(self,request):
        prompt = Prompt.objects.filter(prompt_date=date.today())[0]
        user_drawing = Drawing.objects.filter(user=request.user,prompt=prompt)
        if(len(user_drawing) != 0):
            print("drawing alreayd exists")
            return HttpResponse("REDIRECT")
        image = request.POST.get("imageBase64").replace("data:image/jpeg;base64,","")
        image = base64.b64decode(image)
        with open(f"{MEDIA_ROOT}/submissions/{request.user}-{prompt.prompt}.jpeg","wb") as sub:
            sub.write(image)
        Drawing.objects.create(user=request.user,prompt=prompt,drawing=f"/submissions/{request.user}-{prompt}.jpeg",drawing_id=f"{request.user.username}-{prompt}")
        return HttpResponse("REDIRECT")

    
# Class view for viewing a Drawing
class DrawingView(View):

    def get(self,request):
        # use parameters to get drawing and other useful details
        return render(request,"dailydoodle/drawing.html")
    
    # Also add methods for handling post requests e.g comments ,upvotes etc


# Class view that extends the register functionality
# This allows use to redirect to making a user profile
class RegistrationView(RegistrationView):

    def get_success_url(self,user):
        #for each user we associate a profile picture of format username.jpg
        #intially we get a random profile picture using an api
        media_url = get_random_profile_picture(user.username)
        profile = UserProfile.objects.create(user=user,profile_picture=media_url)
        return reverse("dailydoodle:index")



# Class view that extends the logout functionality so we instantly redirect user back to homescreen

