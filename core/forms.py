from wagtail.users.forms import UserEditForm, UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    password_required = False