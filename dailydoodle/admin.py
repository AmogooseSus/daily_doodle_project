from django.contrib import admin
from  dailydoodle.models import *

# Register your models here.

# Register all models to the admin interface
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Drawing)
admin.site.register(Prompt)
admin.site.register(Rating)

