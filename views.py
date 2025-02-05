from django.shortcuts import render
from django.views import View
from .jira_api import JiraAPI

class ConfigListView(View):
    def get(self, request):
        # Логика для отображения списка конфигураций
        return render(request, 'testy_jira_integration/config_list.html')

    def post(self, request):
        # Логика для обработки формы конфигурации
        jira_url = request.POST.get('jira_url')
        jira_username = request.POST.get('jira_username')
        jira_api_token = request.POST.get('jira_api_token')
        jira_custom_field_id = request.POST.get('jira_custom_field_id')

        # Сохранение конфигурации (например, в базу данных или файл)
        # ...

        return render(request, 'testy_jira_integration/config_list.html', {'success': True})