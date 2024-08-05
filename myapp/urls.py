from django.urls import path
from .views import HotelRag

urlpatterns = [
    # path('process/', get_string, name='string-process'),
    path('Organization-rag/', HotelRag.as_view(), name='insert-string-process'),
]