from django.contrib import admin
from django.urls import path
from django.urls import include
from dailydoodle import views

app_name = "dailydoodle"

urlpatterns = [
    path("",views.Index.as_view(),name="index"),
    path("collections/",views.Collections.as_view(),name="collections"),
    path("submissions/<username>/",views.Submissions.as_view(),name="submissions"),
    path("profile/",views.Profile.as_view(),name="profile"),
    path("leaderboard/",views.LeaderBoard.as_view(),name="leaderboard"),
    path("draw/",views.Draw.as_view(),name="draw"),
    path("drawing/<drawing_id>",views.DrawingView.as_view(),name="drawing"),
    #add view for handling deletion of account
]
