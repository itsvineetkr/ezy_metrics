from django.urls import path
from reporting import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("reporting-home/", views.reporting_home, name="reporting_home"),
    path("download-pdf/", views.download_pdf, name="download_pdf"),
    path("download-campaign-data-csv/", views.download_campaign_data_csv, name="download_campaign_data_csv"),
    path("download-lead-data-csv/", views.download_lead_data_csv, name="download_lead_data_csv"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
