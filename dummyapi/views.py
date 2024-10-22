from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.staticfiles import finders
import pandas as pd


@api_view(["GET"])
def fetch_lead_data(request):
    file_path = finders.find("dummy_data/lead_data.csv")
    if file_path:
        lead_data = pd.read_csv(file_path).to_dict(orient="records")
    else:
        lead_data = None

    if lead_data:
        return Response({"status": 200, "data": lead_data})

    else:
        return Response({"status": 404, "data": "No lead data found"})


@api_view(["GET"])
def fetch_campaign_data(request):
    file_path = finders.find("dummy_data/campaign_data.csv")
    if file_path:
        campaign_data = pd.read_csv(file_path).to_dict(orient="records")
    else:
        campaign_data = None

    if campaign_data:
        return Response({"status": 200, "data": campaign_data})

    else:
        return Response({"status": 404, "data": "No campaign data found"})
