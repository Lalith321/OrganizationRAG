from django.urls import path
from .views import HotelRag

urlpatterns = [
    # path('process/', get_string, name='string-process'),
    path('process/test/', HotelRag.as_view(), name='insert-string-process'),
]