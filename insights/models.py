from django.db import models

class SearchResult(models.Model):
    SEARCH_TYPES = [
        ("pagespeed", "PageSpeed Insights"),
        ("custom_search", "Google Custom Search"),
        ("maps_search", "Google Maps Search"),
        ("business_search", "Google My Business Search"),
        ("website_status", "Website Availability Check"),
    ]

    search_type = models.CharField(max_length=20, choices=SEARCH_TYPES)
    query = models.TextField()
    response_data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.get_search_type_display()} - {self.query} ({self.timestamp})"
