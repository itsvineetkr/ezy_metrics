from django.shortcuts import render
from django.http import HttpResponse
from etl.models import LeadData, CampaignData
import csv
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def reporting_home(request):
    return render(request, "reporting/reporting_home.html")


def download_lead_data_csv(request):
    """
    This function generates a CSV file containing Lead Data.
    """
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)

    writer.writerow(
        [
            "Lead_ID",
            "Lead_Name",
            "Email",
            "Phone_Number",
            "Lead_Source",
            "Lead_Stage",
            "Date_of_Inquiry",
            "Campaign_ID",
        ]
    )

    data = LeadData.objects.all()

    for i in data:
        writer.writerow(
            [
                i.lead_id,
                i.lead_name,
                i.lead_email,
                i.lead_phone,
                i.lead_source,
                i.lead_stage,
                i.date_of_inquiry,
                i.campaign_id,
            ]
        )

    return response


def download_campaign_data_csv(request):
    """
    This function generates a CSV file containing Campaign Data.
    """
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)

    writer.writerow(
        [
            "Campaign_ID",
            "Campaign_Name",
            "Start_Date",
            "End_Date",
            "Campaign_Budget",
            "Leads_Generated",
        ]
    )

    data = CampaignData.objects.all()
    for i in data:
        writer.writerow(
            [
                i.campaign_id,
                i.campaign_name,
                i.start_date,
                i.end_date,
                i.campaign_budget,
                i.leads_generated,
            ]
        )

    return response


def download_pdf(request):
    """
    This function generates a PDF file containing Lead and Campaign Data.
    """
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()
    styles["Title"].fontSize = 16
    styles["BodyText"].fontSize = 10
    styles["Heading2"].fontSize = 12

    title = Paragraph("Lead and Campaign Report", styles["Title"])

    description_text = """
    This report includes a summary of Lead Data and Campaign Data.<br/>
    <b>Lead Data Columns:</b> Lead Name, Email, Phone, Source, Stage, and Campaign Name.<br/>
    <b>Campaign Data Columns:</b> Campaign Name, Start Date, End Date, Budget, and Leads Generated.
    """
    description = Paragraph(description_text, styles["BodyText"])

    elements.append(title)
    elements.append(Spacer(1, 12))
    elements.append(description)
    elements.append(Spacer(1, 24))

    lead_heading = Paragraph("Lead Data", styles["Heading2"])
    elements.append(lead_heading)
    elements.append(Spacer(1, 12))

    lead_queryset = LeadData.objects.all()[:100]
    lead_data = [["Lead Name", "Email", "Phone", "Source", "Stage", "Campaign Name"]]

    for lead in lead_queryset:
        lead_data.append(
            [
                lead.lead_name,
                lead.lead_email,
                lead.lead_phone,
                lead.lead_source,
                lead.lead_stage,
                lead.campaign_id.campaign_name,
            ]
        )

    lead_table = Table(lead_data)
    elements.append(lead_table)
    elements.append(Spacer(1, 24))

    campaign_heading = Paragraph("Campaign Data", styles["Heading2"])
    elements.append(campaign_heading)
    elements.append(Spacer(1, 12))

    campaign_queryset = CampaignData.objects.all()[:100]
    campaign_data = [
        ["Campaign Name", "Start Date", "End Date", "Budget", "Leads Generated"]
    ]

    for campaign in campaign_queryset:
        campaign_data.append(
            [
                campaign.campaign_name,
                campaign.start_date.strftime("%Y-%m-%d"),
                campaign.end_date.strftime("%Y-%m-%d"),
                f"${campaign.campaign_budget}",
                campaign.leads_generated,
            ]
        )

    campaign_table = Table(campaign_data)
    elements.append(campaign_table)

    pdf.build(elements)

    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")
