from django.urls import path
from events.views import event_list,event_create,event_detail,event_update,event_delete,dashboard

urlpatterns = [
    path('',event_list, name='event_list'), 
    path('event/create/',event_create, name='event_create'), 
    path('event/<int:pk>/',event_detail, name='event_detail'), 
    path('event/<int:pk>/update/',event_update, name='event_update'), 
    path('event/<int:pk>/delete/',event_delete, name='event_delete'),
    path('dashboard/', dashboard, name='dashboard'),
  
]
