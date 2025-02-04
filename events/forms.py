from django import forms
from events.models import Event,Participant,Category

class Eventform(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time','location','category']
        
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name','email','events']
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full'}),
            'description': forms.Textarea(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full'}),
            'date': forms.DateInput(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full'}),
            'category': forms.Select(attrs={'class': 'bg-[#474747] text-black border border-yellow-500 rounded p-2 w-full'}),
        }
