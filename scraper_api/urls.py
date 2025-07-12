from django.urls import path
from .views import ScrapeTopicView, FetchPersonInfoView
from .views import cors_debug

urlpatterns = [
    path('scrape/', ScrapeTopicView.as_view(), name='scrape-topic'),
    path('person/', FetchPersonInfoView.as_view(), name='fetch-person-info'),
    path("test-cors/", cors_debug),
]
