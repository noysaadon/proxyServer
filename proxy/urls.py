from django.urls import path
from .views import StreamView #, StatsView

urlpatterns = [
    path('stream/', StreamView.as_view(), name='stream'),
   # path('stats/', StatsView.as_view(), name='stats'),
]