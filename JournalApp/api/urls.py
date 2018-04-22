from django.urls import path, include

from .views import JournalRudView, JournalAPIView

app_name = 'api'
urlpatterns = [
    # These are API URLs
    path('', JournalAPIView.as_view(), name='api-view'),
    path('journal/<int:id>', JournalRudView.as_view(), name='journalCrud'),
]


