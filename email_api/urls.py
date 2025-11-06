from django.urls import path
from .views import send_email_api

urlpatterns = [
    path('api/send-email/', send_email_api, name='send_email_api'),
]
