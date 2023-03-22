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
        context_dict = {"current_link": "Collections"}
        prompts = Prompt.objects.all().order_by("-prompt_date")
        drawings = self.get_latest_drawings(prompts)
        context_dict["prompts"] = prompts
        context_dict["prompt_drawings"]  = drawings
        print(drawings)
        return render(request, "dailydoodle/collections.html", context=context_dict) 
    
    def get_latest_drawings(self,prompts):
        drawings = {}
        for prompt in prompts:
            prompt_drawings = Drawing.objects.filter(prompt=prompt).values()
            drawings[prompt.prompt] = prompt_drawings
        return drawings
    


# Class view for any users submissions
class Submissions(View):

    @method_decorator(login_required)
    def get(self,request,username):
        if(username == request.user.username):
            context_dict = {"current_link": "My Submissions"}
        else:
            context_dict = {}

        required_user = User.objects.get(username=username)
        drawings = Drawing.objects.filter(user=required_user).order_by('-prompt__prompt_date')
        all_prompts = []
        for drawing in drawings:
            all_prompts.append(Prompt.objects.get(prompt=drawing.prompt.prompt))
        user_profile = UserProfile.objects.get(user=required_user)
        name = user_profile.user.username
        user_pic = user_profile.profile_picture
        upvotes_received = user_profile.upvotes_recieved
        
        context_dict['user_pic'] = user_pic
        context_dict['upvotes'] = upvotes_received
        context_dict['username'] = name
        context_dict['drawings'] = drawings
        context_dict['MEDIA_URL'] = MEDIA_URL
        context_dict["all_prompts"] = all_prompts

        return render(request, "dailydoodle/submissions.html", context=context_dict)



# Class view for leadboards
class LeaderBoard(View):

    @method_decorator(login_required)
    def get(self,request):
        context_dict = {"current_link": "Leaderboard"}
        # retrieve the top 10 users
        users = UserProfile.objects.filter(upvotes_recieved__gte=1).order_by("-upvotes_recieved")[:10]
        # retrieve their top most liked drawing 
        most_liked_drawings = []
        for user in users:
            most_liked_drawings.append(Drawing.objects.filter(user=user.user).order_by("-total_upvotes")[0])
        data = zip(users,most_liked_drawings)
        context_dict["data"] = data
        context_dict["amount"] = len(users)
        return render(request,"dailydoodle/leaderboard.html",context=context_dict)
    
    # Also add method for handling searching of users via post request
    @method_decorator(login_required)
    def post(self,request):
        name = request.POST.get("name")
        if(name == "search"):
            return self.handle_search(request)
    
    def handle_search(self,request):
        query = request.POST.get("query")
        all_users = UserProfile.objects.filter(upvotes_recieved__gt=0).order_by("-upvotes_recieved").values()
        users = User.objects.filter(username__icontains=query).values()
        user_profiles = {}
        for x in users:
            profile = UserProfile.objects.get(user=x["id"])
            position = 1
            # determine position by adding to position from ordered set of profiles
            for user in all_users:
                if(user["user_id"] == x["id"]):
                    break 
                position += 1
            user_profiles[x["username"]] = {"position": position,"username": x["username"],"profile_picture": profile.profile_picture.url,"upvotes_recieved": profile.upvotes_recieved}
            user_drawings = Drawing.objects.filter(user=x["id"])
            if(len(user_drawings) != 0):
                user_profiles[x["username"]]["most_liked_drawing"] =  user_drawings[0].prompt.prompt
            else:
                user_profiles[x["username"]]["most_liked_drawing"] = None
        data = {"user_data": user_profiles}
        return JsonResponse(data)
    

# Class view for profile
class Profile(View):
    @method_decorator(login_required)
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

