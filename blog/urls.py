from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view,name='home'),
    path('blog/', views.blog_view, name='blog'),
    path('post/<int:pk>/', views.post_view, name='post'),
    path('draft/', views.draft_view, name='draft'),

    path('new/', views.new_post_view, name='new_post'),
    path('edit/<int:pk>/', views.edit_post_view, name='edit'),
    path('preview/<int:pk>/', views.preview_post_view, name='preview'),


    path('add_comment/', views.add_comment, name='add_comment'),
    path('add_to_draft/', views.add_to_draft, name='add_to_draft'),
    path('publish_post/<int:pk>/', views.publish_post, name='publish_post'),
    path('edit_draft/<int:pk>/', views.add_edit_draft, name='edit_draft'),
]