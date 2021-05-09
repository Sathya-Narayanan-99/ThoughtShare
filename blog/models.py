from django.db import models
from django.contrib.auth.models import User

post_category = {
    ("Growth", "Growth"),
    ("Bussiness", "Bussiness")
}

# Create your models here.
class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    post_pic = models.ImageField(blank=True, null=True )
    category = models.CharField(max_length=200 ,choices=post_category)
    author = models.ForeignKey(Blogger, on_delete=models.SET_NULL, null=True)
    date_published = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0,null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.post_pic.url
        except:
            url = ''
        return url

    @property
    def comment_count(self):
        try:
            commentCount = len(self.comment_set.all())
        except:
            commentCount = 0

        return commentCount

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    date_published = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return str(self.post) + ' comment ' + str(self.id)