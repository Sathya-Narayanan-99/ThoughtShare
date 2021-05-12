from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import post_category

class PostForm(forms.Form):
    title = forms.CharField(label='')
    post_pic = forms.ImageField()
    category= forms.ChoiceField(choices=post_category)
    content = forms.CharField(widget=CKEditorWidget(), label='')

    title.widget.attrs.update({'placeholder':'Post Title','class':'form-control','style':'height: 50px; font-size: 30px;'})
    content.widget.attrs.update({'placeholder':'Type your blog content here','class':'form-control','style':'height: 8000px;'})