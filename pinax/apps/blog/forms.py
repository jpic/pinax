from datetime import datetime

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from pinax.apps.blog.models import Post



class BlogForm(forms.ModelForm):
    
    slug = forms.SlugField(
        max_length = 20,
        help_text = _("a short version of the title consisting only of letters, numbers, underscores and hyphens."),
    )
    publish = forms.DateField(('%d/%m/%Y',), required=True,
        widget=forms.DateTimeInput(format='%d/%m/%Y', attrs={
            'class':'input',
            'readonly':'readonly',
            'size':'15'
        })
    )

    class Media:
        js = (
            settings.STATIC_URL + 'pinax/js/jquery-ui-1.7.3.datepicker.min.js',
            settings.STATIC_URL + 'pinax/css/jquery-ui-1.7.3.cupertrino.css',
        )

    class Meta:
        model = Post
        exclude = [
            "author",
            "creator_ip",
            "created_at",
            "updated_at",
        ]
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(BlogForm, self).__init__(*args, **kwargs)
    
    def clean_slug(self):
        if not self.instance.pk:
            if Post.objects.filter(author=self.user, created_at__month=datetime.now().month, created_at__year=datetime.now().year, slug=self.cleaned_data["slug"]).exists():
                raise forms.ValidationError(u"This field must be unique for username, year, and month")
            return self.cleaned_data["slug"]
        try:
            post = Post.objects.get(
                author = self.user,
                created_at__month = self.instance.created_at.month,
                created_at__year = self.instance.created_at.year,
                slug = self.cleaned_data["slug"]
            )
            if post != self.instance:
                raise forms.ValidationError(u"This field must be unique for username, year, and month")
        except Post.DoesNotExist:
            pass
        return self.cleaned_data["slug"]
