from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/create-user/', views.User.as_view(), name='api_create_user'),
    path('api/api-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/', views.Login.as_view(), name='login_user'),
    path('api/events/', views.event_list.as_view(), name='event_list'),
    path('api/events/list/', views.events_list, name='events_list'),
    path('api/events/create/', views.create_event_f, name='create_event'),
    path('api/events/delete/<str:event_id>/', views.delete_event, name='delete_event'),
    path('api/events/update/<str:event_id>/', views.update_event, name='update_event'),
    path('api/events/<str:event_id>/', views.event_detail.as_view(), name='events_details'),
    path('logout', views.logout),
]