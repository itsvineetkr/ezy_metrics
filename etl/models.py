from django.db import models

class CampaignData(models.Model):
    campaign_id = models.CharField(max_length=36, unique=True, null=False)
    campaign_name = models.CharField(max_length=100, null=False)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    campaign_budget = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    leads_generated = models.IntegerField(null=False)
    
    def __str__(self):
        return self.campaign_name


class LeadData(models.Model):
    lead_id = models.CharField(max_length=36, unique=True, null=False)
    lead_name = models.CharField(max_length=100, null=False)
    lead_email = models.EmailField(max_length=100, null=False)
    lead_phone = models.CharField(max_length=20, null=False)
    lead_source = models.CharField(max_length=100, null=False)
    lead_stage = models.CharField(max_length=100, null=False)
    date_of_inquiry = models.DateTimeField(null=False)
    campaign_id = models.ForeignKey(CampaignData, on_delete=models.CASCADE)

    def __str__(self):
        return self.lead_name