from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json  # To parse JSON data
from django.contrib.auth.decorators import login_required  # Ensure only logged-in users can access the edit function
from django.views.decorators.csrf import csrf_exempt  # To bypass CSRF protection (use with caution)
from django.views.decorators.http import require_http_methods  # To restrict the allowed HTTP methods
from django.shortcuts import get_object_or_404




from .models import User, Post, Follow
from django.http import JsonResponse  # To return a JSON response


def index(request):
    all_posts = Post.objects.all().order_by('date_time').reverse()

    paginator = Paginator(all_posts, 10) # Show 10 per page

    # get page number via get request on url
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # on first load, page_number is none
    # page_obj.number is automatically 1 if page_number is none
    
    # print(page_number)
    # print(page_obj.number)

    return render(request, "network/index.html", {
        'page_obj': page_obj
    })


@login_required  # Ensure the user is authenticated
def followings(request):
    # get all users the current_user is following
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    # print(following_users)
    # <QuerySet [1]>

    # Get the posts made by those users
    follower_posts = Post.objects.filter(author__in=following_users).order_by('-date_time')
    # print(follower_posts)
    # <QuerySet [<Post: sk 2024-09-27 02:41:55.787038+00:00>, <Post: sk 2024-09-20 03:09:52.454979+00:00>]>

    paginator = Paginator(follower_posts, 10) # Show 10 per page

    # get page number via get request on url
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/followings.html", {
        'page_obj': page_obj
    })

# @require_http_methods(["PUT"])  # Only allow PUT method for this view
@login_required  # Ensure the user is authenticated
@csrf_exempt  # Disable CSRF for simplicity in this example (use with caution in production)
def like(request, id):
    if request.method == "POST":
        try:
            single_post = get_object_or_404(Post, pk=id)
        
            # check if user has already liked the post
            if(request.user in single_post.likes.all()):
                # remove like entry
                single_post.likes.remove(request.user)
                liked = False

            # like the post
            else:
                # add like entry
                single_post.likes.add(request.user)
                liked = True

            single_post.save()
            print(single_post.likes.count())

            # return count_likes, boolean is_like
            return JsonResponse({"success": True,
                                  "count_likes": single_post.likes.count(),
                                   "liked": liked })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    



@require_http_methods(["PUT"])  # Only allow PUT method for this view
@login_required  # Ensure the user is authenticated
@csrf_exempt  # Disable CSRF for simplicity in this example (use with caution in production)
def edit(request, id):
    if request.method == "PUT":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            new_content = data.get("content")
            
            # Get post by id
            try:
                single_post = Post.objects.get(pk=id)
            except Post.DoesNotExist:
                single_post = None

            if request.user != single_post.author:
                return JsonResponse({"error": "You are not allowed to edit this post."}, status=403)
            
            # Update the post content
            single_post.content = new_content
            single_post.save()
            # Respond with success
            return JsonResponse({"success": True, "message": "Post updated successfully."})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


def user_profile(request, id):
    try:
        # profile of user selected
        selected_user_data = User.objects.get(id=id)
        selected_user_all_post = Post.objects.filter(author=selected_user_data).order_by('date_time').reverse()
        
        # add pagination
        paginator = Paginator(selected_user_all_post, 10) # Show 10 per page

        # get page number via get request on url
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except User.DoesNotExist:
        selected_user_data = None
    
    # check if logged in user is following the person of the profile page
    try:
        # check if following and follower combination exist
        single_row = Follow.objects.get(follower=request.user, following=selected_user_data)
        is_following = True
    except Follow.DoesNotExist:
        single_row = None
        is_following = False

    # display number of followings
    try:
        all_followers = Follow.objects.filter(following=selected_user_data)
        count_follows = len(all_followers)
    except Follow.DoesNotExist:
        count_follows = 0

    # display number of followers
    try:
        all_following = Follow.objects.filter(follower=selected_user_data)
        count_followings = len(all_following)
    except Follow.DoesNotExist:
        count_followings = 0

    return render(request, "network/profile.html", {
        'page_obj': page_obj,
        'is_following': is_following,
        'selected_user_data' : selected_user_data,
        'count_follows': count_follows,
        'count_followings': count_followings,
    })


def unfollow(request, id):
    selected_user_data = User.objects.get(id=id)
    row_to_delete = Follow.objects.get(follower=request.user, following=selected_user_data)
    row_to_delete.delete()
    
    return HttpResponseRedirect(reverse("user_profile", args=(id, )))


def follow(request, id):
    selected_user_data = User.objects.get(id=id)
    new_row = Follow(follower=request.user, following=selected_user_data)
    new_row.save()
    
    return HttpResponseRedirect(reverse("user_profile", args=(id, )))


def create(request):
    if request.method != "GET":
        new_post = request.POST['new_post']
        
        new_row = Post(author=request.user, content=new_post)
        new_row.save()
    
    return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
