from django import forms
from dailydoodle.models import *

# UserProfile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("username","password")


