from django.urls import path
from .views import *

urlpatterns = [
    path('popular', popular),
    path('charts', charts),
    path('personalised',personalised)
]
