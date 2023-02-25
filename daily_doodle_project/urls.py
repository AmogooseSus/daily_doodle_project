from django.contrib import admin
from django.urls import path
from django.urls import include
from dailydoodle import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.Index.as_view()),
    path("dailydoodle/",include("dailydoodle.urls")),
    path('admin/', admin.site.urls),
    path("accounts/",include("registration.backends.simple.urls")),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
