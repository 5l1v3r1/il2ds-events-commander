# -*- coding: utf-8 -*-
"""
Forms for authentication-related views.
"""
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (UserChangeForm as BaseUserChangeForm,
    UserCreationForm as BaseUserCreationForm, )
from django.utils.translation import ugettext_lazy as _

from auth_custom import signup_confirmation
from auth_custom.models import User


class SignInForm(forms.Form):
    """
    Form class for authenticating users.
    """
    email_username = forms.CharField(
        label=_("Username or email"),
        help_text=_("Data to identify account"),
        max_length=254,
        required=True)
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput)
    remember_me = forms.BooleanField(
        label=_('Remember me'),
        initial=False,
        required=False)

    error_messages = {
        'invalid_data': _("Wrong authentication data."),
        'inactive': _("Account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The form data comes in via the standard 'data' kwarg.
        """
        self.user_cache = None
        super(SignInForm, self).__init__(*args, **kwargs)

    def clean(self):
        email_username = self.cleaned_data.get('email_username')
        password = self.cleaned_data.get('password')

        if email_username and password:
            self.user_cache = authenticate(username=email_username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_data'],
                    code='invalid_data',
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class UserCreationForm(BaseUserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username,
    email and password. Used in admin.
    """
    username = forms.RegexField(
        label=_("Username"),
        help_text=_("Name which is used in game"),
        max_length=30,
        regex=r'^[\w.@+-=()\[\]{}]+$',
        required=True,
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/=/_/(/)/[/]/{/} characters.")
        })
    email = forms.EmailField(
        label=_("Email"),
        required=True)

    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)
        self.error_messages.update({
            'duplicate_email': _("A user with that email already exists."),
        })

    class Meta:
        model = User
        fields = ('username', 'email', )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User._default_manager.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User._default_manager.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['duplicate_email'],
                code='duplicate_email')
        return email


class UserChangeForm(BaseUserChangeForm):
    """
    A form for updating users. Includes all the fields on the user, but
    replaces the password field with admin's password hash display field.
    Used in admin.
    """
    username = forms.RegexField(
        label=_("Username"),
        help_text=_("Name which is used in game"),
        max_length=30,
        regex=r'^[\w.@+-=()\[\]{}]+$',
        required=True,
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/=/_/(/)/[/]/{/} characters.")
        })

    class Meta:
        model = User
        fields = '__all__'


class SignUpRequestForm(forms.Form):
    """
    Form for getting data to create a request for sign up.
    """
    email = forms.EmailField(
        label=_("Email"),
        help_text=_("Email to send your sign up instructions to"),
        required=True)


class SignUpForm(forms.Form):
    """
    A form that creates a user with no privileges from the given first name,
    last name, username, password, language. Sign up request data (email and
    confirmation_key) must be provided.
    """
    FATAL_ERROR_CODE = 1

    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'duplicate_username': _("A user with that username already exists."),
    }

    email = forms.EmailField(
        required=True,
        widget=forms.HiddenInput)
    confirmation_key = forms.CharField(
        required=True,
        validators=[signup_confirmation.validate_key, ],
        widget=forms.HiddenInput)

    first_name = forms.CharField(
        label=_("First name"),
        help_text=_("Your first name"),
        max_length=30,
        required=True)
    last_name = forms.CharField(
        label=_("Last name"),
        help_text=_("Your last name (optional)"),
        max_length=30,
        required=False)
    username = forms.RegexField(
        label=_("Username"),
        help_text=_("Your in-game name"),
        max_length=30,
        regex=r'^[\w.@+-=()\[\]{}]+$',
        required=True,
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/=/_/(/)/[/]/{/} characters.")
        })
    password = forms.CharField(
        label=_("Password"),
        help_text=_("Password for website"),
        max_length=128,
        required=True,
        widget=forms.PasswordInput)
    language = forms.ChoiceField(
        label=_("Language"),
        help_text=_("Language to use on website and in game chat"),
        choices=settings.LANGUAGES,
        required=True,
        widget=forms.Select)
    remember_me = forms.BooleanField(
        label=_("Remember me"),
        required=False,
        help_text=_("Stay signed in on website"))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User._default_manager.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User._default_manager.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['duplicate_email'],
                code='duplicate_email')
        return email


class RemindMeForm(forms.Form):
    """
    Form for getting data to create a request for reminding username and
    resetting password.
    """
    email_username = forms.CharField(
        label=_("Username or email"),
        help_text=_("Data to identify account"),
        max_length=254,
        required=True)
