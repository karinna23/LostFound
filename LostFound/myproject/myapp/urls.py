from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [    
    path('', views.landing, name='landing'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('create-post/', views.create_post, name='create'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('edit-profile/<int:pk>/', views.edit_profile, name='edit_profile'),
    path('add-ratings/', views.add_ratings, name='add_ratings'),
    path('ratings/', views.ratings_list, name='ratings_list'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('about_us/', views.about_us, name='about_us'),
    path('<int:pk>/edit/', views.edit_post, name='edit'),
    path('<int:pk>/delete/', views.delete_post, name='delete'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('admin_delete/<int:pk>/', views.admin_delete_post, name='admin_delete'),
    path('analytics/', views.analytics, name='analytics'),
    path('search/', views.search, name='search'),
    path('user/<str:username>/', views.users_view, name='users_view'),


]