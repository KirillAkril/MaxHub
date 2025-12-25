from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import PortfolioItem, SocialLink, Testimonial, User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "title", "bio", "avatar", "email", "max_username"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "max_username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите username аккаунта в MAX"}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = True


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ["platform", "label", "url", "icon", "order"]
        widgets = {
            "platform": forms.Select(attrs={"class": "form-select"}),
            "label": forms.TextInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
            "icon": forms.TextInput(attrs={"class": "form-control", "placeholder": "bi bi-telegram"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }


class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = ["title", "description", "image", "project_archive", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "project_archive": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 5, "class": "form-control", "placeholder": "Напишите ваш отзыв..."}),
        }


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["email"].required = True
        # Добавляем классы для полей пароля
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})

