from django.forms import ModelForm
from .models import create_event
from django.contrib.auth.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class EventForm(ModelForm):
    class Meta:
        model = create_event
        fields = ('event_name', 'event_category', 'event_place', 'event_address', 'event_initial_date', 'event_final_date', 'event_type', 'thumbnail')