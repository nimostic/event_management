from django.shortcuts import render,redirect,get_object_or_404
from events.models import Event,Participant,Category
from events.forms import Eventform,ParticipantForm,CategoryForm
from django.contrib import messages
from django.db.models import Count,Sum,Q
import datetime
from django.utils.timezone import now

def event_list(request):
    events = Event.objects.select_related('category').annotate(participant_count=Count('participant'))
    categories = Category.objects.all()

    # get search parameters
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # apply search filters
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )
    if category_id:
        events = events.filter(category_id=category_id)
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,
        'search_query': search_query
    })


def event_create(request):
    if request.method == 'POST':
        form = Eventform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Event Created Successfully!!!")
            return redirect('event_list')
    else:
        form = Eventform()
    return render(request,'events/event_form.html',{'form':form})

def event_detail(request, pk):
    event = Event.objects.prefetch_related('participant_set').get(pk=pk)
    participants = event.participant_set.all()
    return render(request, 'events/event_detail.html', {'event': event, 'participants': participants})



def event_update(request,pk):
    event = get_object_or_404(Event,pk=pk)
    if request.method == 'POST':
        form = Eventform(request.POST,instance=event)
        if form.is_valid():
            form.save()
            messages.success(request,"Event Updated Successfully!!!")
            return redirect('event_list')
    else:
        form = Eventform(instance=event)
    return render(request,'events/event_form.html',{'form':form})

def event_delete(request,pk):
    event = get_object_or_404(Event,pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    



def dashboard(request):
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    print(total_participants)
    upcoming_events = Event.objects.filter(date__gte=now()).count()
    past_events = Event.objects.filter(date__lt=now()).count()
    todays_events = Event.objects.filter(date=now().date())

    # Handle Filtering
    filter_type = request.GET.get('filter', '')
    filtered_events = None
    filtered_participants = None
    if filter_type == "total_participants":
        filtered_participants = Participant.objects.all()
        filtered_events = None
    elif filter_type == "total_events":
        filtered_events = Event.objects.all()
    elif filter_type == "upcoming_events":
        filtered_events = Event.objects.filter(date__gte=now())
    elif filter_type == "past_events":
        filtered_events = Event.objects.filter(date__lt=now())
    else:
        filtered_events = todays_events  

    context = {
        "total_events": total_events,
        "total_participants": total_participants,
        "filtered_participants": filtered_participants , 
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "todays_events": todays_events,
        "filtered_events": filtered_events,
        "filter_type": filter_type,
    }
    print(context)
    return render(request, "events/dashboard.html", context)

