from django import forms
from .models import Comment


# Custom form to handle user sharing post via email
class EmailPostForm(forms.Form):
    name = forms.CharField(label = 'user name', max_length = 25)
    email = forms.EmailField(label = 'sender email')
    to = forms.EmailField(label = 'reciever email')
    comments = forms.CharField(label = 'comment area', required=False,widget = forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body',)