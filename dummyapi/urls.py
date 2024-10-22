from django.urls import path
from dummyapi import views


urlpatterns = [
    path('fetch_lead_data', views.fetch_lead_data, name="fetch_lead_data"),
    path('fetch_campaign_data', views.fetch_campaign_data, name="fetch_campaign_data"),
]
