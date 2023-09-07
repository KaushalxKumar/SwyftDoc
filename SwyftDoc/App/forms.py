from django.contrib.auth.forms import UserCreationForm
from App.models import Person

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Person
        fields = ['username', 'email', 'password1', 'password2']
