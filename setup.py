from setuptools import setup, find_packages

setup(
    name='testy_jira_integration',
    version='1.0.0',
    description='Sync TestY test cases with Jira issues',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=3.2',
        'djangorestframework>=3.12.4',
        'requests>=2.25.1',
    ],
    entry_points={
        'testy': [
            'testy_jira_integration = testy_jira_integration',
        ],
    },
)