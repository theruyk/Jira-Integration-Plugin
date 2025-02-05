from rest_framework import serializers

class JiraConfigSerializer(serializers.Serializer):
    jira_url = serializers.URLField()
    jira_username = serializers.CharField(max_length=100)
    jira_api_token = serializers.CharField(max_length=100)
    jira_custom_field_id = serializers.CharField(max_length=100)