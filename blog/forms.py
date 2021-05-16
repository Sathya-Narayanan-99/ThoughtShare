from django import forms
from django.forms import fields

from .models import Post, post_category

class PostForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['title'].widget.attrs.update({'placeholder':'Post Title','class':'form-control','style':'height: 50px; font-size: 30px;','required':True})
        # self.fields['post_pic'].widget.attrs.update({'required':True})
        self.fields['description'].widget.attrs.update({'placeholder':'A small intro about the post','class':'form-control','style':'font-size: 20px;','required':True})
        self.fields['content'].widget.attrs.update({'placeholder':'Type your blog content here','class':'form-control','style':'height: 8000px;','required':True})
        self.fields['category'].widget.attrs.update({'class':'form-control','required':True})

    class Meta:
        model = Post
        fields = ["title","post_pic","description","category","content"]