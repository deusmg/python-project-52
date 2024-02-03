from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )


class UserUpdateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )

    def clean_username(self):
        return self.cleaned_data.get("username")
