from django import template
from dailydoodle.models import UserProfile
from daily_doodle_project.settings import MEDIA_URL

register = template.Library()

@register.inclusion_tag("dailydoodle/nav.html")
def get_nav(current_link=None,user=None):
    # links of format { name: link}
    user_profile_picture = None
    if(user.username):
        user_profile_picture = UserProfile.objects.filter(user=user)[0].profile_picture
    all_links = {"Homepage": "dailydoodle:index"}
    non_locked_links = {"Register":"registration_register","Login":"auth_login"}
    locked_links = {"Collections":"dailydoodle:collections","Profile":"dailydoodle:profile","Leaderboard":"dailydoodle:leaderboard","Logout":"auth_logout"}
    return {"all_links": all_links,"non_locked_links": non_locked_links,"locked_links": locked_links,"current_link": current_link,"user":user,"user_profile_picture":user_profile_picture,"MEDIA_URL": MEDIA_URL}