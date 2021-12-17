from django.forms import ModelForm
from django import forms
from blogs.models import Blog
from blogs.models import Review


class BlogForm(ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'short_intro', 'featured_image', 'description', 'demo_link',
                  'source_link', ]

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input input--text'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your vote (put /" up /" if you found this helpful)',
            'body': 'Write something worth reading'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input input--text'})
