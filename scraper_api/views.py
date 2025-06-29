from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import scrape_topic

class ScrapeTopicView(APIView):
    def get(self, request):
        topic = request.query_params.get('topic')
        limit = request.query_params.get('limit', 5)
        if not topic:
            return Response({"error": "Missing 'topic' query param"}, status=400)

        articles = scrape_topic(topic, limit)
        return Response(articles, status=status.HTTP_200_OK)
