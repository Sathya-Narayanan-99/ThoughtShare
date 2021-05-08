from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view,name='home'),
    path('blog/', views.blog_view, name='blog'),
    path('post/', views.post_view, name='post'),
]