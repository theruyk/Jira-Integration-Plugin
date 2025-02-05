import logging
import requests
from testy.plugins.hooks import TestyPluginConfig, hookimpl

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JiraAPIError(Exception):
    """Кастомное исключение для ошибок взаимодействия с Jira."""
    pass

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
    # URL вашей Jira
    JIRA_BASE_URL = 'https://your-jira-instance.atlassian.net'
    
    # Данные авторизации
    JIRA_USERNAME = 'your-email'
    JIRA_API_TOKEN = 'your-api-token'
    
    # ID кастомного поля Jira для статусов тестов
    JIRA_CUSTOM_FIELD_ID = 'customfield_12345'

    def __init__(self):
        self.base_url = self.JIRA_BASE_URL  
        self.auth = (self.JIRA_USERNAME, self.JIRA_API_TOKEN)
        self.headers = {'Content-Type': 'application/json'}

    def link_test_case_to_issue(self, test_case_id, issue_key):
        url = f"{self.base_url}/rest/api/2/issueLink"
        payload = {
            "type": {"name": "Relates"},
            "inwardIssue": {"key": issue_key},
            "outwardIssue": {"key": f"TC-{test_case_id}"}
        }
        try:
            response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Тест-кейс TC-{test_case_id} успешно связан с задачей {issue_key} в Jira.")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при связывании тест-кейса с задачей Jira: {e}")
            raise JiraAPIError(f"Не удалось связать тест-кейс {test_case_id} с задачей {issue_key}.")

    def update_test_status_in_jira(self, issue_key, test_cases):
        test_status = ", ".join([f"TC-{tc['id']}: {tc['status']}" for tc in test_cases])
        url = f"{self.base_url}/rest/api/2/issue/{issue_key}"
        payload = {"fields": {self.JIRA_CUSTOM_FIELD_ID: test_status}}
        try:
            response = requests.put(url, json=payload, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Статус тестов обновлен в задаче {issue_key}: {test_status}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при обновлении статуса тест-кейса в Jira: {e}")
            raise JiraAPIError(f"Не удалось обновить статусы тест-кейсов в задаче {issue_key}.")
