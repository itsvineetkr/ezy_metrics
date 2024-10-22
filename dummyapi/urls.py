from django.urls import path
from dummyapi import views


urlpatterns = [
    path('api/fetch_lead_data', views.fetch_lead_data, name="fetch_lead_data"),
    path('api/fetch_campaign_data', views.fetch_campaign_data, name="fetch_campaign_data"),
]
