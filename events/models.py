from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events_images',blank=True,null=True,default='events_images/default_event.jpg')
    participants = models.ManyToManyField(User, related_name="rsvp_events")

    def __str__(self):
        return self.name

# class Participant(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     events = models.ManyToManyField(Event)
    
#     def __str__(self):
#         return self.name
