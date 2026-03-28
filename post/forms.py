from django import forms
from .models import Post, Comment




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # 'author' is excluded — set server-side via form.instance.author in AddPostView.form_valid()
        fields = ('title', 'body', 'header_image', 'video', 'file')
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title required'}),
            'body':         forms.Textarea(attrs={'class': 'form-control'}),
            'header_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video':        forms.FileInput(attrs={
                                'class': 'form-control',
                                'accept': 'video/mp4,video/webm,video/ogg,video/quicktime,video/x-msvideo,video/x-matroska,.mp4,.webm,.ogg,.mov,.mkv,.avi,.m4v,.3gp',
                            }),
            'file':         forms.FileInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class':       'form-control',
                'placeholder': 'Écrire un commentaire…',
                'rows':        2,
                'maxlength':   1000,
            }),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'header_image', 'video', 'file')
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title required'}),
            'body':         forms.Textarea(attrs={'class': 'form-control'}),
            'header_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video':        forms.FileInput(attrs={
                                'class': 'form-control',
                                'accept': 'video/mp4,video/webm,video/ogg,video/quicktime,video/x-msvideo,video/x-matroska,.mp4,.webm,.ogg,.mov,.mkv,.avi,.m4v,.3gp',
                            }),
            'file':         forms.FileInput(attrs={'class': 'form-control'}),
        }