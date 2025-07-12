from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import scrape_topic, fetch_person_info
from django.http import JsonResponse

def cors_debug(request):
    return JsonResponse({
        "origin": request.META.get("HTTP_ORIGIN"),
        "headers": dict(request.headers),
    })

class ScrapeTopicView(APIView):
    def get(self, request):
        topic = request.query_params.get('topic')
        limit = request.query_params.get('limit', 5)
        if not topic:
            return Response({"error": "Missing 'topic' query param"}, status=400)

        articles = scrape_topic(topic, limit)
        return Response(articles, status=status.HTTP_200_OK)

class FetchPersonInfoView(APIView):
    def get(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({"error": "Missing 'name' query param"}, status=400)

        try:
            full_report = fetch_person_info(name)

            # Generate a preview (e.g., first 3 non-empty lines from the report)
            preview_lines = full_report.strip().split('\n')
            preview = []
            for line in preview_lines:
                if line.strip() != "" and len(preview) < 3:
                    preview.append(line.strip())

            return Response({
                "name": name,
                "preview": " ".join(preview),
                "info": full_report  # Still include full report for full detail access
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

