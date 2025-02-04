import os
import django
import random
from datetime import timedelta, date, time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Event, Participant, Category

def populate():
    print("📌 Populating database...")

    # Clear existing data (optional)
    Event.objects.all().delete()
    Participant.objects.all().delete()
    Category.objects.all().delete()

    # Create categories
    categories = ["Conference", "Workshop", "Meetup", "Webinar", "Hackathon", "Seminar","Weeding","Birthday"]

    category_objs = [Category.objects.create(name=cat) for cat in categories]

    # Create events
    events = []
    for i in range(15):  # Create 5 events
        event = Event.objects.create(
            name=f"Event {i+1}",
            description=f"Description for Event {i+1}",
            date=date.today() + timedelta(days=random.randint(-5, 5)),  # Past & upcoming events
            time=time(random.randint(10, 18), 0),  # Random time between 10 AM - 6 PM
            location=f"Location {i+1}",
            category=random.choice(category_objs)  # Assign random category
        )
        events.append(event)

    # Create participants
    for i, event in enumerate(events):
        for j in range(5):  # 3 participants per event
            participant = Participant.objects.create(
                name=f"Participant {j+1} for {event.name}",
                email=f"participant{j+1}_event{i+1}@example.com"
            )
            participant.events.set([event])  # ManyToManyField requires set()

    print("✅ Database populated successfully!")

if __name__ == "__main__":
    populate()
