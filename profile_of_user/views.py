# profile/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post, Replie, Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
import requests

def product_list_view(request):
    response = requests.get('http://localhost:8000/api/products/')
    products = response.json()
    return render(request, 'profile/product_list.html', {'products': products})

@login_required(login_url='/login')
def forum(request):
    print("User is authenticated:", request.user.is_authenticated)
    if request.method == "POST":
        user = request.user
        image = request.user.profile.image
        content = request.POST.get('content', '')
        print("Content:", content)
        post = Post(user1=user, post_content=content, image=image)
        post.save()
        alert = True
        return render(request, "forum.html", {'alert': alert})
    posts = Post.objects.filter().order_by('-timestamp')
    return render(request, "forum.html", {'posts': posts})

@login_required(login_url='/login')
def discussion(request, myid):
    post = Post.objects.filter(id=myid).first()
    replies = Replie.objects.filter(post=post)
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            image = request.user.profile.image
            desc = request.POST.get('desc', '')
            post_id = request.POST.get('post_id', '')
            reply = Replie(user=user, reply_content=desc, post=post, image=image)
            reply.save()
            alert = True
            return render(request, "discussion.html", {'alert': alert})
        else:
            messages.error(request, "You need to be logged in to reply.")
            return redirect('Login')
    return render(request, "discussion.html", {'post': post, 'replies': replies})

def UserRegister(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters.")
            return redirect('/register')
        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers.")
            return redirect('/register')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')
    return render(request, "register.html")

def UserLogin(request):
    if request.method == "POST":
        print("POST data:", request.POST)  # Debug statement to print POST data

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('Login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect('Login')

    return render(request, 'login.html')

def homepage(request):
    return render(request, "index.html")

def news(request):
    return render(request, "news.html")

def UserLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')

@login_required(login_url='/login')
def myprofile(request):
    if request.method == "POST":
        user = request.user    
        profile = Profile(user=user)
        profile.save()
        form = ProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, "profile.html", {'obj': obj})
    else:
        form = ProfileForm()
    return render(request, "profile.html", {'form': form})
