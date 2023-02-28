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


# Create your views here.

# NOTE any class views that don't benifit from using class based syntax will
# be reverted to a function

# Class view for homepage 
class Index(View):

    def get(self,request):
        # get top 5 drawings (use helper function) and add them to context dict
        # get users submission if exists or add no submission to context dict
        # get todays prompt 
        return render(request,"dailydoodle/index.html")
    

# Class view for collections
class Collections(View):

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
        return render(request,"dailydoodle/leadboard.html")
    
    # Also add method for handling searching of users via post request
    

# Class view for profile
class Profile(View):

    def get(self,request):
        # simply return users username,email and profile picture
        return render(request,"dailydoodle/profile.html") 
    
    # Also add method for handling profile changes


# Class view for Draw mode
class Draw(View):

    def get(self,request):
        # get todays prompt
        return render(request,"dailydoodle/draw.html")
    
    # Also add method for handling submission of drawing
    
# Class view for viewing a Drawing
class Drawing(View):

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


