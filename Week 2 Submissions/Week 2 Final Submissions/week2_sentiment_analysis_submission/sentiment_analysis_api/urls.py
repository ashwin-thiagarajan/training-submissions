from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("sentiment.urls")),
    path("", include("sentiment.health_urls")),
]

