from django.urls import path
from .views import ScrapeTopicView

urlpatterns = [
    path('scrape/', ScrapeTopicView.as_view(), name='scrape-topic'),
]
