import requests
from testy.plugins.hooks import TestyPluginConfig, hookimpl

class JiraIntegrationConfig(TestyPluginConfig):
    package_name = 'testy_jira_integration'
    verbose_name = 'Jira Integration'
    description = 'Sync TestY test cases with Jira issues'
    version = '1.0.0'
    plugin_base_url = 'jira-integration'
    author = 'Your Name'
    index_reverse_name = 'config-list'
    urls_module = 'testy_jira_integration.urls'

@hookimpl
def config():
    return JiraIntegrationConfig

class JiraAPI:
    # URL вашей Jira, например, 'https://your-jira-instance.atlassian.net'
    JIRA_BASE_URL = 'https://your-jira-instance.atlassian.net'
    
    # Укажите ваш email и API-токен Jira
    JIRA_USERNAME = 'your-email'
    JIRA_API_TOKEN = 'your-api-token'
    
    # Укажите ID кастомного поля Jira для статусов тестов
    JIRA_CUSTOM_FIELD_ID = 'customfield_12345'  # Укажите ID кастомного поля Jira для статусов тестов
    
    def __init__(self):
        self.base_url = self.JIRA_BASE_URL  
        self.auth = (self.JIRA_USERNAME, self.JIRA_API_TOKEN)
        self.headers = {'Content-Type': 'application/json'}

    def link_test_case_to_issue(self, test_case_id, issue_key):
        url = f"{self.base_url}/rest/api/2/issueLink"
        payload = {
            "type": { "name": "Relates" },
            "inwardIssue": { "key": issue_key },
            "outwardIssue": { "key": f"TC-{test_case_id}" }
        }
        try:
            response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при связывании тест-кейса с задачей Jira: {e}")
            return False
        return response.status_code == 201

    def update_test_status_in_jira(self, issue_key, test_cases):
        test_status = ", ".join([f"TC-{tc['id']}: {tc['status']}" for tc in test_cases])
        url = f"{self.base_url}/rest/api/2/issue/{issue_key}"
        payload = {"fields": {self.JIRA_CUSTOM_FIELD_ID: test_status}}
        try:
            response = requests.put(url, json=payload, auth=self.auth, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обновлении статуса тест-кейса в Jira: {e}")
            return False
        return response.status_code == 204
