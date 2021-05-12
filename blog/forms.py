from django import forms
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.Form):
    title = forms.CharField(label='', required=False)
    content = forms.CharField(widget=CKEditorWidget(), label='')

    title.widget.attrs.update({'placeholder':'Post Title','class':'form-control','style':'height: 50px; font-size: 30px;','required':True})
    content.widget.attrs.update({'placeholder':'Type your blog content here','class':'form-control','style':'height: 8000px;'})