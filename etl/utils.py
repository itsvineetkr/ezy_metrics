from django.db.models import Count
from etl.models import CampaignData, LeadData
import requests

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def fetch_campaign_data():
    """
    This function fetches campaign data from the API.
    Args: None
    Return: campaign_data (list): List of dictionaries containing campaign data.
    """

    campaign_data_response = requests.get("http://127.0.0.1:8000/fetch_campaign_data")

    if campaign_data_response.status_code == 200:
        campaign_data = campaign_data_response.json()["data"]
        return campaign_data

    else:
        return None


def add_campaign_data(campaign_data):
    """
    This function adds campaign data to the database. Also clears the existing data for demonstration purpose.
    Args: campaign_data (list): List of dictionaries containing campaign data.
    Return: None
    """

    # Deleting the existing data just for demonstration purpose, otherwise it will give unique constraint error
    if CampaignData.objects.exists():
        CampaignData.objects.all().delete()

    for data in campaign_data:
        CampaignData.objects.create(
            campaign_id=data["Campaign_ID"],
            campaign_name=data["Campaign_Name"],
            start_date=data["Start_Date"],
            end_date=data["End_Date"],
            campaign_budget=data["Campaign_Budget"],
            leads_generated=data["Leads_Generated"],
        )


def fetch_lead_data():
    """
    This function fetches lead data from the API.
    Args: None
    Return: lead_data (list): List of dictionaries containing lead data.
    """
    lead_data_response = requests.get("http://127.0.0.1:8000/fetch_lead_data")

    if lead_data_response.status_code == 200:
        lead_data = lead_data_response.json()["data"]
        return lead_data

    else:
        return None


def add_lead_data(lead_data):
    """
    This function adds lead data to the database. Also clears the existing data for demonstration purpose.
    Args: lead_data (list): List of dictionaries containing lead data.
    Return: None
    """
    
    # Deleting the existing data just for demonstration purpose, otherwise it will give unique constraint error
    if LeadData.objects.exists():
        LeadData.objects.all().delete()

    for data in lead_data:
        campaign = CampaignData.objects.get(campaign_id=data["Campaign_ID"])
        LeadData.objects.create(
            lead_id=data["Lead_ID"],
            lead_name=data["Lead_Name"],
            lead_email=data["Email"],
            lead_phone=data["Phone_Number"],
            lead_source=data["Lead_Source"],
            lead_stage=data["Lead_Stage"],
            date_of_inquiry=data["Date_of_Inquiry"],
            campaign_id=campaign,
        )


def send_mail(email):
    """
    This function sends an email to the recipient.
    Args: email (str): Email address of the recipient.
    Return: None
    """

    data = list(LeadData.objects.values('lead_stage').annotate(count=Count('lead_stage')))
    html_content = render_to_string(
        "etl/mail.html", {"data": data}
    )
    subject = "New CRM Data Fetched: Lead Count Summary"
    text_content = strip_tags(html_content)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()