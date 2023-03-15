from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.views import View
from dailydoodle.models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views 
from django.urls import reverse
from registration.backends.simple.views import RegistrationView
from django.utils.decorators import method_decorator
from dailydoodle.apis import *
from dailydoodle.view_helpers import *
from datetime import date,datetime
from daily_doodle_project.settings import MEDIA_URL,MEDIA_ROOT
import base64
from django.db.models import Avg, Max, Min


# Create your views here.

# NOTE any class views that don't benifit from using class based syntax will
# be reverted to a function

# TODO replace all filter where we want only element with .objects.get()

# Class view for homepage 
class Index(View):

    def get(self,request):
        # get todays prompt 
        prompt = Prompt.objects.get(prompt_date=date.today())
        context_dict = {"current_link": "Homepage"}
        # get top 5 drawings (use helper function) and add them to context dict
        top_drawings = Drawing.objects.filter(prompt=prompt).order_by("-total_upvotes")[:5].values()
        for x in top_drawings:
            x["user_profile_picture"] = UserProfile.objects.get(user_id=x["user_id"]).profile_picture
            x["username"] = User.objects.get(id=x["user_id"]).username
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
        context_dict["top_drawings"] = {"amount": len(top_drawings), "top": top_drawings}
        return render(request,"dailydoodle/index.html",context=context_dict)
    

# Class view for collections
class Collections(View):

    @method_decorator(login_required)
    def get(self,request):
        if not request.user.is_authenticated:
            # Redirect to home
            return HttpResponseRedirect(reverse('dailydoodle:index'))

        context_dict = {"current_link": "Collections"}

        drawings = Drawing.objects.filter(drawing__icontains='')
        print(len(drawings))
        context_dict['drawings'] = drawings

        return render(request, "dailydoodle/collections.html", context=context_dict)
        # get intial n prompts using helper function and add to context dict
        # get intial n drawings using helper function and add to context dictionary
        # Also add method for handling searching of prompts, getting more prompts and getting more drawings


# Class view for any users submissions
class Submissions(View):

    def get(self,request,username):
        if not request.user.is_authenticated:
            # Redirect to login page or handle anonymous user
            return HttpResponseRedirect(reverse('dailydoodle:index'))

        if(username == request.user.username):
            context_dict = {"current_link": "My Submissions"}
        else:
            context_dict = {}

        drawings = Drawing.objects.filter(user=request.user)
        print(len(drawings))

        context_dict['drawings'] = drawings

        return render(request, "dailydoodle/submissions.html", context=context_dict)
        # get user 
        # get intial n drawings user has participated in
        # get intial n prompts user has participated in
        # Also add method for handling searching of prompts and getting more prompts



# Class view for leadboards
class LeaderBoard(View):

    @method_decorator(login_required)
    def get(self,request):
        context_dict = {"current_link": "Leaderboard"}
        # retrieve the top 10 users
        users = UserProfile.objects.filter(upvotes_recieved__gt=1).order_by("-upvotes_recieved")[:5]
        # retrieve their top most liked drawing 
        most_liked_drawings = []
        for user in users:
            most_liked_drawings.append(Drawing.objects.filter(user=user.user).order_by("-total_upvotes")[0])
        data = zip(users,most_liked_drawings)
        context_dict["data"] = data
        context_dict["amount"] = len(users)
        return render(request,"dailydoodle/leaderboard.html",context=context_dict)
    
    # Also add method for handling searching of users via post request
    

# Class view for profile
class Profile(View):

    def get(self,request):
        context_dict = {"current_link": "Profile"}
        # simply return users username,email and profile picture
        currUser:User = request.user
        context_dict = {}
        userName = User.get_username(currUser)
        email = currUser.email
        context_dict["username"] = userName
        context_dict["email"] = email
        user_profile_picture = UserProfile.objects.filter(user=currUser)[0].profile_picture
        context_dict["user_profile_picture"] = user_profile_picture
        return render(request,"dailydoodle/profile.html",context=context_dict) 
    
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
        name = request.POST.get("name")
        if(name == "submit"):
            return self.handle_submission(request)
        elif(name == "search"):
            return self.handle_reference_request(request)
      
    def handle_submission(self,request):
        prompt = Prompt.objects.filter(prompt_date=date.today())[0]
        user_drawing = Drawing.objects.filter(user=request.user,prompt=prompt)
        if(len(user_drawing) != 0):
            print("drawing already exists")
            return HttpResponse("REDIRECT")
        image = request.POST.get("imageBase64").replace("data:image/jpeg;base64,","")
        image = base64.b64decode(image)
        with open(f"{MEDIA_ROOT}/submissions/{request.user}-{prompt.prompt}.jpeg","wb") as sub:
            sub.write(image)
        Drawing.objects.create(user=request.user,prompt=prompt,drawing=f"/submissions/{request.user}-{prompt}.jpeg",drawing_id=f"{request.user.username}-{prompt}")
        return HttpResponse("REDIRECT")
    
    def handle_reference_request(self,request):
        data = get_references(request.POST.get("query"))
        print(data)
        return JsonResponse({"data": json.dumps(data)})

    
# Class view for viewing a Drawing
class DrawingView(View):

    @method_decorator(login_required)
    def get(self,request,drawing_id):
        context_dict = {}
        prompt = Prompt.objects.filter(prompt_date=date.today())[0].prompt
        user_drawing = Drawing.objects.get(drawing_id=drawing_id)
        comments = Comment.objects.filter(drawing=drawing_id)
        print(prompt, user_drawing, comments)
        context_dict["prompt"] = prompt
        context_dict["user_drawing"] = user_drawing
        context_dict["comments"] = comments
        return render(request,"dailydoodle/drawing.html",context=context_dict)

    # Also add methods for handling post requests e.g comments ,upvotes etc
    @method_decorator(login_required)
    def post(self,request,drawing_id):
        print(request.POST)
        name = request.POST.get("name")
        if(name == "comment"):
            return self.handle_comment(request,drawing_id)
        elif(name == "upvote"):
            return self.handle_upvote(request,drawing_id)

    def handle_comment(self,request,drawing_id):
        Comment.objects.create(user=request.user,comment=request.POST.get("comment_text"),date=datetime.now(),drawing=Drawing.objects.get(drawing_id=drawing_id))
        return HttpResponse("OK")
    
    def handle_upvote(self,request,drawing_id):
        rating = Rating.objects.filter(user=request.user,drawing=Drawing.objects.get(drawing_id=drawing_id))
        if(len(rating) == 0):
            Rating.objects.create(user=request.user,drawing=Drawing.objects.get(drawing_id=drawing_id))
            return JsonResponse({"upvotes":  Drawing.objects.get(drawing_id=drawing_id).total_upvotes})
        else:
            Rating.objects.get(user=request.user,drawing=Drawing.objects.get(drawing_id=drawing_id)).delete()
            return JsonResponse({"upvotes":  Drawing.objects.get(drawing_id=drawing_id).total_upvotes})


# Class view that extends the register functionality
# This allows use to redirect to making a user profile
class RegistrationView(RegistrationView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_link"] = "Register"
        return context

    def get_success_url(self,user):
        #for each user we associate a profile picture of format username.jpg
        #intially we get a random profile picture using an api
        media_url = get_random_profile_picture(user.username)
        profile = UserProfile.objects.create(user=user,profile_picture=media_url)
        return reverse("dailydoodle:index")


# Class view that extends the login functionality mainly to add the current link for nav
class LoginView(auth_views.LoginView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_link"] = "Login"
        return context

