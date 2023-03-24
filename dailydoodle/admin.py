from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from dailydoodle.models import *
from dailydoodle.apis import get_random_profile_picture
import os
from daily_doodle_project import settings

# Register your models here.
class UserOverideAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin,self).__init__(*args, **kwargs)

    # Create a user profile when creating users in admin
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        UserProfile.objects.create(user=obj,profile_picture=get_random_profile_picture(obj.username))


class DrawingAdmin(admin.ModelAdmin):

    # delete the stored media image 
    def delete_model(self, request,obj):
        dir = f"{settings.MEDIA_ROOT}/submissions/{obj.drawing_id}.jpeg"
        dir.replace("\\","/")
        os.remove(dir)
        super().delete_model(request, obj)

# Register all models to the admin interface
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Prompt)
admin.site.register(Rating)
admin.site.register(Drawing,DrawingAdmin)
admin.site.unregister(User)
admin.site.register(User, UserOverideAdmin)

