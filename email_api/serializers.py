from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    recipient = serializers.EmailField()
    header = serializers.CharField(required=False, allow_blank=True)
    action_url = serializers.URLField(required=False, allow_blank=True)
    action_text = serializers.CharField(required=False, allow_blank=True)
    system_name = serializers.CharField(required=False, allow_blank=True)
    support_email = serializers.EmailField(required=False, allow_blank=True)
