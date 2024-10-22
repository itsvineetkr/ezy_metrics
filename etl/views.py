from django.shortcuts import render, redirect
from etl.utils import *
from creds import reciever_mail


def index(request):
    return render(request, "etl/index.html")

def clear_db(request):
    if CampaignData.objects.exists():
        CampaignData.objects.all().delete()
    if LeadData.objects.exists():
        LeadData.objects.all().delete()

    return redirect("/etl")


def etl(request):
    campaign_data = []
    lead_data = []
    if request.method == "POST":
        if "extract_data" in request.POST:
            campaign_data = fetch_campaign_data()
            lead_data = fetch_lead_data()

        if "transform_data" in request.POST:
            campaign_data = fetch_campaign_data()
            lead_data = fetch_lead_data()
            if campaign_data:
                add_campaign_data(campaign_data)
            if lead_data:
                add_lead_data(lead_data)
            send_mail(reciever_mail)

    db_data = {
        "campaign_data": CampaignData.objects.all(),
        "lead_data": LeadData.objects.all(),
    }

    fetch_data = {
        "len_campaign_data": len(campaign_data) if len(campaign_data)!= 0 else None,
        "len_lead_data": len(lead_data) if len(lead_data)!= 0 else None,
    }

    return render(
        request,
        "etl/extract.html",
        {
            "db_data": db_data,
            "fetch_data": fetch_data,
        },
    )
