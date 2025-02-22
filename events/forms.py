from django import forms
from events.models import Event,Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Event


class RSVPForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput())
    def save(self, user):
        event = Event.objects.get(id=self.cleaned_data['event_id'])
        if user not in event.participants.all():
            event.participants.add(user)
        return event
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']

class Eventform(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full'}),
            'description': forms.Textarea(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full'}),
            'date': forms.DateInput(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full'}),
            'category': forms.Select(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full'}),
            
        }


class SignupForm(UserCreationForm):
    email = forms.EmailField(required = True)
    role = forms.ChoiceField(choices=[('Organizer', 'Organizer'), ('Participant', 'Participant')], required=True)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2', 'role']
