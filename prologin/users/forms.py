from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from .widgets import PreviewFileInput


class UserSimpleForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'country', 'phone', 'birthday', 'newsletter', 'avatar', 'picture')
        widgets = {
            'avatar': PreviewFileInput(),
            'picture': PreviewFileInput(),
        }


class RegisterForm(forms.ModelForm):
    captcha = CaptchaField(help_text=_("Type the four letters to prove you are not an automated bot."))
    newsletter = forms.BooleanField(required=False, label=_("Subscribe to the newsletter"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'newsletter', 'captcha')
        widgets = {
            'password': forms.PasswordInput(),
        }
