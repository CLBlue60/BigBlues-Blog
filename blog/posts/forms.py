from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['status', 'is_archived', 'author']:
            if field_name in self.fields:
                del self.fields[field_name]


        self.fields['content'].widget = forms.Textarea(attrs={'rows': 4})
