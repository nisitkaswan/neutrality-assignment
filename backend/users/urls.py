from django.urls import path
from .views import RandomUserList

urlpatterns = [
    path('users/', RandomUserList.as_view(), name='random-users'),
]