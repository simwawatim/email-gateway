from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email_api.serializers import EmailSerializer


def send_generic_email(subject, message, recipient, **kwargs):
    html_content = render_to_string('emails/base_email.html', {
        'subject': subject,
        'message': message,
        'header': kwargs.get('header', 'Notification'),
        'action_url': kwargs.get('action_url', None),
        'action_text': kwargs.get('action_text', None),
        'system_name': kwargs.get('system_name', 'Email API'),
        'support_email': kwargs.get('support_email', 'support@example.com'),
    })

    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


@api_view(['POST'])
def send_email_api(request):
    serializer = EmailSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            "status": "fail",
            "status_code": 400,
            "message": "Invalid input data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data

    required_fields = ["subject", "message", "recipient"]
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return Response({
            "status": "fail",
            "status_code": 400,
            "message": f"Missing required fields: {', '.join(missing)}"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        send_generic_email(
            subject=data["subject"],
            message=data["message"],
            recipient=data["recipient"],
            header=data.get("header"),
            action_url=data.get("action_url"),
            action_text=data.get("action_text"),
            system_name=data.get("system_name"),
            support_email=data.get("support_email"),
        )

        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Email sent successfully!"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": "error",
            "status_code": 500,
            "message": f"Failed to send email: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
