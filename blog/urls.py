from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view,name='home'),
    path('blog/', views.blog_view, name='blog'),
    path('post/<int:pk>/', views.post_view, name='post'),
    path('draft/', views.draft_view, name='draft'),
    path('search/', views.search_view, name='search'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile_view, name='edit_profile'),

    path('new/', views.new_post_view, name='new_post'),
    path('edit/<int:pk>/', views.edit_post_view, name='edit'),
    path('preview/<int:pk>/', views.preview_post_view, name='preview'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/', views.user_registration, name='registration'),
    path('change_password/<str:username>/', views.change_password_view, name='change_password'),

    path('add_comment/', views.add_comment, name='add_comment'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('add_to_draft/', views.add_to_draft, name='add_to_draft'),
    path('publish_post/<int:pk>/', views.publish_post, name='publish_post'),
    path('edit_draft/<int:pk>/', views.add_edit_draft, name='edit_draft'),
]