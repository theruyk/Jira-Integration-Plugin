from django.urls import path
from .views import ConfigListView

urlpatterns = [
    path('config/', ConfigListView.as_view(), name='config-list'),
]