from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    SetPasswordForm,
    AuthenticationForm,
)
from django import forms
from .models import Profile


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "w-full ps-2 mb-2"
        self.fields["username"].widget.attrs["placeholder"] = "User Name"
        self.fields["password"].widget.attrs["class"] = "w-full ps-2"
        self.fields["password"].widget.attrs["placeholder"] = "Password"
        self.fields["username"].label = ""
        self.fields["password"].label = ""


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "w-full ps-2 my-2", "placeholder": "Email Address"}
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "w-full ps-2 my-2", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "w-full ps-2", "placeholder": "Last Name"}
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "w-full ps-2"
        self.fields["username"].widget.attrs["placeholder"] = "User Name"
        self.fields["username"].label = ""
        self.fields["username"].help_text = (
            '<span class="form-text text-muted text-white"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        )

        self.fields["password1"].widget.attrs["class"] = "w-full ps-2"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].label = ""
        self.fields["password1"].help_text = (
            '<ul class="form-text text-muted p-2 text-white"><small><li>Your password cant be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password cant be a commonly used password.</li><li>Your password cant be entirely numeric.</li></small></ul>'
        )

        self.fields["password2"].widget.attrs["class"] = "w-full ps-2"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].label = ""
        self.fields["password2"].help_text = (
            '<span class="form-text text-muted text-white"><small>Enter the same password as before, for verification.</small></span>'
        )


class UpdateUserForm(UserChangeForm):
    password = None
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={"class": "w-full ps-2", "placeholder": "Email Address"}
        ),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "w-full ps-2", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "w-full ps-2", "placeholder": "Last Name"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "w-full ps-2"
        self.fields["username"].widget.attrs["placeholder"] = "User Name"
        self.fields["username"].label = "User"
        self.fields["username"].help_text = (
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        )


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs["class"] = "w-full ps-2"
        self.fields["new_password1"].widget.attrs["placeholder"] = "Password"
        self.fields["new_password1"].label = "Password"
        self.fields["new_password1"].help_text = (
            "<ul class=\"form-text text-muted small\"><li>Your password can't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can't be a commonly used password.</li><li>Your password can't be entirely numeric.</li></ul>"
        )

        self.fields["new_password2"].widget.attrs["class"] = "w-full ps-2"
        self.fields["new_password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["new_password2"].label = "Confirm Password"
        self.fields["new_password2"].help_text = (
            '<span class="block">Enter the same password as before, for verification.</span>'
        )


class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(
        label="Phone",
        widget=forms.TextInput(attrs={"class": "w-full ps-2", "placeholder": "Phone"}),
        required=False,
    )
    address1 = forms.CharField(
        label="Address 1",
        widget=forms.TextInput(
            attrs={"class": "w-full ps-2", "placeholder": "Address 1"}
        ),
        required=False,
    )
    address2 = forms.CharField(
        label="Address 2",
        widget=forms.TextInput(
            attrs={"class": "w-full ps-2", "placeholder": "Address 2"}
        ),
        required=False,
    )
    city = forms.CharField(
        label="City",
        widget=forms.TextInput(attrs={"class": "w-full ps-2", "placeholder": "City"}),
        required=False,
    )
    state = forms.CharField(
        label="State",
        widget=forms.TextInput(attrs={"class": "w-full ps-2", "placeholder": "State"}),
        required=False,
    )
    zipcode = forms.CharField(
        label="Zipcode",
        widget=forms.TextInput(
            attrs={"class": "w-full ps-2", "placeholder": "Zipcode"}
        ),
        required=False,
    )
    country = forms.CharField(
        label="Country",
        widget=forms.TextInput(
            attrs={"class": "w-full ps-2", "placeholder": "Country"}
        ),
        required=False,
    )

    class Meta:
        model = Profile
        fields = (
            "phone",
            "address1",
            "address2",
            "city",
            "state",
            "zipcode",
            "country",
        )
