import json
import requests
import googlemaps
from googleapiclient.discovery import build
from django.http import JsonResponse
from django.utils.timezone import now
from rest_framework.decorators import api_view
from .models import SearchResult

GOOGLE_API_KEY = "AIzaSyBhfX5UMG1c1zEQ18-IeRChfZDjW3s4By0"
GOOGLE_CSE_ID = "01426446988ec4c8e"
GOOGLE_MAPS_API_KEY = "AIzaSyAu5P7u4qE72xFK05Woww4bO7jOXh1Zy_g"

gmaps_client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
search_service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)

@api_view(['GET'])
def fetch_pagespeed_results(request):
    url = request.GET.get("url")
    if not url:
        return JsonResponse({"error": "URL parameter is required"}, status=400)

    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={GOOGLE_API_KEY}"

    try:
        response = requests.get(api_url)
        data = response.json()
        lighthouse = data.get("lighthouseResult", {})
        audits = lighthouse.get("audits", {})

        important_data = {
            "url": url,
            "timestamp": data.get("analysisUTCTimestamp", "N/A"),
            "performance_score": lighthouse.get("categories", {}).get("performance", {}).get("score", "N/A"),
            "first_contentful_paint": audits.get("first-contentful-paint", {}).get("displayValue", "N/A"),
            "speed_index": audits.get("speed-index", {}).get("displayValue", "N/A"),
            "time_to_interactive": audits.get("interactive", {}).get("displayValue", "N/A"),
            "total_blocking_time": audits.get("total-blocking-time", {}).get("displayValue", "N/A"),
            "cumulative_layout_shift": audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A"),
            "largest_contentful_paint": audits.get("largest-contentful-paint", {}).get("displayValue", "N/A"),
            "first_meaningful_paint": audits.get("first-meaningful-paint", {}).get("displayValue", "N/A"),
            "server_response_time": audits.get("server-response-time", {}).get("displayValue", "N/A"),
            "dom_size": audits.get("dom-size", {}).get("displayValue", "N/A"),
            "estimated_input_latency": audits.get("estimated-input-latency", {}).get("displayValue", "N/A"),
            "max_potential_fid": audits.get("max-potential-fid", {}).get("displayValue", "N/A"),
        }

        SearchResult.objects.create(
            search_type="pagespeed",
            query=url,
            response_data=json.dumps(important_data)
        )

        return JsonResponse({"message": "Result saved!", "data": important_data})

    except requests.RequestException as e:
        return JsonResponse({"error": "Failed to fetch API data", "details": str(e)}, status=500)
    

@api_view(['GET'])
def google_custom_search(request):
    query = request.GET.get("query")
    if not query:
        return JsonResponse({"error": "Query parameter is required"}, status=400)

    try:
        search_results = search_service.cse().list(q=query, cx=GOOGLE_CSE_ID, num=10).execute()
        SearchResult.objects.create(
            search_type="custom_search",
            query=query,
            response_data=json.dumps(search_results)  
        )

        return JsonResponse({"results": search_results.get("items", [])})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def google_maps_search(request):
    query = request.GET.get("query")
    if not query:
        return JsonResponse({"error": "Query parameter is required"}, status=400)

    try:
        places = gmaps_client.places(query=query)
        SearchResult.objects.create(
            search_type="maps_search",
            query=query,
            response_data=json.dumps(places)  
        )

        return JsonResponse(places)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def google_my_business_search(request):
    query = request.GET.get("query")
    if not query:
        return JsonResponse({"error": "Query parameter is required"}, status=400)

    try:
        places = gmaps_client.places(query=query, type="establishment")
        SearchResult.objects.create(
            search_type="business_search",
            query=query,
            response_data=json.dumps(places)  
        )

        return JsonResponse({"business_results": places.get("results", [])})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def website_status(request):
    url = request.GET.get("url")
    if not url:
        return JsonResponse({"error": "URL parameter is required"}, status=400)

    try:
        response = requests.head(url, timeout=5)
        status = response.status_code == 200
        result = {"url": url, "available": status}
        SearchResult.objects.create(
            search_type="website_status",
            query=url,
            response_data=json.dumps(result)  
        )

        return JsonResponse(result)

    except requests.RequestException:
        return JsonResponse({"url": url, "available": False})

@api_view(['GET'])
def get_past_searches(request):
    searches = SearchResult.objects.all().order_by('-timestamp')
    
    results = [
        {
            "search_type": search.get_search_type_display(),
            "query": search.query,
            "timestamp": search.timestamp,
            "data": json.loads(search.response_data) if search.response_data else {}
        }
        for search in searches
    ]

    return JsonResponse({"past_searches": results})
