from django.urls import path
from etl import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("etl/", views.etl, name="etl"),
    path("clear_db/", views.clear_db, name="clear_db"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
