from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/<int:pk>/update/', views.event_update, name='event_update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('organizer-dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('participant-dashboard/', views.participant_dashboard, name='participant_dashboard'),
    
    path('rsvp/<int:event_id>/', views.rsvp_event, name='rsvp_event'),
    path('rsvp/<int:event_id>/cancel/', views.cancel_rsvp, name='cancel_rsvp'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-role/', views.change_role_view, name='change_role'),
    path("activate/<int:user_id>/<str:token>/", views.activate_user, name="activate_user"),
]
