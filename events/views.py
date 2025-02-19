from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from events.models import Event, Category
from events.forms import Eventform, CategoryForm
from django.contrib import messages
from django.db.models import Count, Q
from django.utils.timezone import now
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from events.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RSVPForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()

def is_organizer_or_participant(user):
    return is_organizer(user) or is_participant(user)

@login_required
@user_passes_test(is_organizer_or_participant)
def event_list(request):
    events = Event.objects.select_related('category').annotate(participant_count=Count('participants'))
    categories = Category.objects.all()
    
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))
    if category_id:
        events = events.filter(category_id=category_id)
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])
    
    return render(request, 'events/event_list.html', {'events': events, 'categories': categories, 'search_query': search_query})

@login_required
@user_passes_test(is_organizer)
def event_create(request):
    if request.method == 'POST':
        form = Eventform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully!!!")
            return redirect('event_list')
    else:
        form = Eventform()
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    participants = event.participants.all()
    return render(request, 'events/event_detail.html', {'event': event, 'participants': participants})

@login_required
@user_passes_test(is_organizer)
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = Eventform(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully!!!")
            return redirect('event_list')
    else:
        form = Eventform(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

@login_required
@user_passes_test(is_organizer)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')

@login_required
def dashboard(request):
    total_events = Event.objects.count()
    total_participants = User.objects.filter(rsvp_events__isnull=False).distinct().count()
    upcoming_events = Event.objects.filter(date__gte=now()).count()
    past_events = Event.objects.filter(date__lt=now()).count()
    todays_events = Event.objects.filter(date=now().date())
    
    filter_type = request.GET.get('filter', '')
    filtered_events = None
    filtered_participants = None
    
    if filter_type == "total_participants":
        filtered_participants = User.objects.filter(rsvp_events__isnull=False).distinct()
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
        "filtered_participants": filtered_participants,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "todays_events": todays_events,
        "filtered_events": filtered_events,
        "filter_type": filter_type,
    }
    
    return render(request, "events/dashboard.html", context)

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = RSVPForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        
        send_mail(
        "Event RSVP Confirmation",
        f"You have successfully RSVP'd for {event.name}.",
        "noreply@eventmanagement.com",
        [request.user.email],
        fail_silently=False,
        )
        return redirect('event_detail', pk=event_id)  # Redirect to event details after RSVP
    else:
            form = RSVPForm(initial={'event_id': event.id})

    return render(request, 'events/rsvp_event.html', {'event': event, 'form': form})

@login_required
def cancel_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.participants.all():
        event.participants.remove(request.user)  # Remove user from participants list

    return redirect('event_detail', pk=event_id)
        
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()

            
            participant_group, created = Group.objects.get_or_create(name="Participant")
            user.groups.add(participant_group)

           
            token = default_token_generator.make_token(user)
            activation_url = f"{settings.FRONTEND_URL}/activate/{user.id}/{token}/"

            
            subject = 'Activate Your Account'
            message = f"Hi {user.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank you!"
            recipient_list = [user.email]

            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
                messages.success(request, 'A confirmation email has been sent. Please check your inbox.')
            except Exception as e:
                print(f"Failed to send activation email: {str(e)}")

            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'events/signup.html', {'form': form})

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated! You can now log in.")
            return redirect('login')
        else:
            return HttpResponse('Invalid activation link or expired token.')
    except User.DoesNotExist:
        return HttpResponse('User not found.')




@login_required
def admin_dashboard(request):
    return render(request, "events/admin_dashboard.html")

@login_required
def organizer_dashboard(request):
    return render(request, "events/organizer_dashboard.html")

@login_required
def participant_dashboard(request):
    return render(request, "events/participant_dashboard.html")



def login_view(request):
    if request.method =='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            
            if user.groups.filter(name="Admin").exists():
                return redirect("admin_dashboard")
            elif user.groups.filter(name="Organizer").exists():
                return redirect("organizer_dashboard")
            else:
                return redirect("participant_dashboard")
    else:
        form = AuthenticationForm()
    return render(request,'events/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('event_list')

@login_required
def change_role_view(request):
    if not request.user.is_superuser:
        return redirect('event_list')  # Restrict access

    users = User.objects.all()
    roles = Group.objects.all()

    if request.method == "POST":
        for user in users:
            selected_role = request.POST.get(f'role_{user.id}')
            if selected_role:
                user.groups.clear()
                group = Group.objects.get(name=selected_role)
                user.groups.add(group)
                messages.success(request, f"Updated {user.username}'s role to {selected_role}")

        return redirect('admin_dashboard') #admin dashboard

    return render(request, "events/change_role.html", {"users": users, "roles": roles})

