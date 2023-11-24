from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import CustomUser, Post, Rating
from .forms import CustomUserRegistrationForm, CustomUserLoginForm, PostForm, RatingForm, EditPostForm, SearchForm
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from .forms import EditProfileForm
from django.http import JsonResponse
from django.template.loader import render_to_string


class CustomLogoutView(LogoutView):
    template_name = 'myapp/landing.html'  # Optionally, create a custom template for logout

    def dispatch(self, request, *args, **kwargs):
        # Customize the logout behavior if needed
        # For example, you can add a confirmation message
        messages.info(request, "You have been successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

@login_required(login_url='/')
def home(request):
    posts = Post.objects.all().order_by('-created_at')  # Retrieve all posts from the database
    return render(request, 'myapp/home.html', {'posts': posts})

@login_required(login_url='/')
def ratings_list(request):
    ratings = Rating.objects.all().order_by('-date_time')
    return render(request, 'myapp/ratings.html', {'ratings': ratings})

def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_authenticated and getattr(user, 'is_admin', False):
                    return redirect('myapp:admin_panel')  # Redirect admin users to the admin panel
                else:
                    return redirect('myapp:home')  # Redirect to the home page after successful login
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomUserLoginForm()

    return render(request, 'myapp/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            return redirect('myapp:login')  # Redirect to the home page after registration
        else:
            messages.error(request, "Passwords don't match.")

    else:
        form = CustomUserRegistrationForm()
    return render(request, 'myapp/registers.html', {'form': form})

@login_required(login_url='/')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.userID = request.user
            post.save()
            return redirect('myapp:home')  # Redirect back to the home page
    else:
        form = PostForm()
    return render(request, 'myapp/create_post.html', {'form': form})

@login_required(login_url='/')
def user_profile(request):
    user = request.user  # Get the currently logged-in user
    user_posts = user.post_set.all().order_by('-created_at')  # Assuming there's a related name 'post_set' in your Post model

    context = {
        'user': user,
        'user_posts': user_posts,
    }

    return render(request, 'myapp/user_profile.html', context)

@login_required(login_url='/')
def edit_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('myapp:edit_profile', pk=pk)  # Redirect to the 'edit_profile' URL with the appropriate primary key
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'myapp/edit_user.html', {'form': form})

@login_required(login_url='/')
def add_ratings(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.userID = request.user
            rating.save()
            return redirect('myapp:ratings_list')  # Replace 'success_page' with the URL where you want to redirect after a successful submission
    else:
        form = RatingForm()
    
    return render(request, 'myapp/add_ratings.html', {'form': form})

@login_required(login_url='/')
def about_us(request):
    return render(request, 'myapp/about_us.html')

def edit_post(request, pk=None):
    if pk:
        post = get_object_or_404(Post, pk=pk)
    else:
        post = None

    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('myapp:user_profile')  # Replace 'post_detail' with your detail view name
    else:
        form = EditPostForm(instance=post)

    return render(request, 'myapp/edit_post.html', {'form': form, 'post': post})

from django.shortcuts import get_object_or_404, redirect
from .models import Post

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        # Additional logic if needed
        return redirect('myapp:user_profile')  # Replace 'myapp:list' with the actual URL name or path for redirecting after deletion

def landing(request):
    return render(request, 'myapp/landing.html')

@login_required(login_url='/')
def admin_panel(request):

    posts = Post.objects.all().order_by('-created_at')  
    return render(request, 'myapp/admin.html', {'posts': posts})

@login_required(login_url='/')
def admin_delete_post(request, pk):
    # Check if the user is an admin
    if not request.user.is_admin:
        return redirect('myapp:home')  # Redirect non-admins to home or another page

    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        # Additional logic if needed
        return redirect('myapp:admin_panel')  # Redirect to the admin panel after deletion

@login_required(login_url='/')
def analytics(request):
    # Check if the user is an admin
    if not request.user.is_authenticated or not request.user.is_admin:
        return redirect('myapp:home')  # Redirect non-authenticated or non-admin users to home or another page

    total_users = CustomUser.objects.count()
    total_posts = Post.objects.count()
    total_ratings = Rating.objects.count()

    context = {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_ratings': total_ratings,
    }

    return render(request, 'myapp/analytics.html', context)

def search(request):
    posts = Post.objects.all().order_by('-created_at')  # Retrieve all posts

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            if request.is_ajax():
                results = posts.filter(
                     Q(description__icontains=search_query)
                    | Q(full_name__icontains=search_query)
                    | Q(item_name__icontains=search_query)
                    | Q(time_place__icontains=search_query)
                    | Q(status__icontains=search_query)
                )
                html = render_to_string('myapp/search_results_partial.html', {'results': results})
                return JsonResponse({'html': html})

    else:
        form = SearchForm()

    return render(request, 'myapp/search.html', {'form': form, 'posts': posts})

def users_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user_posts = user.post_set.all().order_by('-created_at')

    context = {
        'profile_user': user,
        'user_posts': user_posts,
    }

    return render(request, 'myapp/users_view.html', context)