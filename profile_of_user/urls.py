# profile/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserLogin, name="Login"),
    path("forum/", views.forum, name="forum"),
    path("discussion/<int:myid>/", views.discussion, name="Discussions"),
    path("register/", views.UserRegister, name="Register"),
    path("logout/", views.UserLogout, name="Logout"),
    path("myprofile/", views.myprofile, name="Myprofile"),
    path("homepage/", views.homepage, name="homepage"),
    path("news/", views.news, name="news"),
]
