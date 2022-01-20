from django.forms import ModelForm
from .models import Discussion
from Accounts.models import User

class DiscussionForm(ModelForm):
    class Meta:
        model = Discussion
        fields = '__all__'
        exclude = ['host', 'participants']




class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username', 'email', 'institution', 'bio']