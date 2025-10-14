"""
Allure configuration for test reporting
"""
import os
import json
from datetime import datetime

class AllureConfig:
    """Configuration class for Allure reporting"""
    
    def __init__(self):
        self.results_dir = "test/reports/allure-results"
        self.report_dir = "test/reports/allure-report"
        self.config_dir = "test/reports/allure-config"
        
        # Create directories if they don't exist
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)
    
    def create_allure_properties(self, environment: str = "localhost"):
        """Create allure.properties file"""
        properties_content = f"""allure.results.directory={self.results_dir}
allure.link.issue.pattern=https://example.com/issues/{{}}
allure.link.tms.pattern=https://example.com/tms/{{}}
allure.link.custom.pattern=https://example.com/custom/{{}}
allure.link.custom.name=Custom Link
allure.link.issue.name=Issue
allure.link.tms.name=TMS
allure.link.mylink.pattern=https://example.com/mylink/{{}}
allure.link.mylink.name=My Link
allure.link.mylink.type=custom
allure.link.mylink.url=https://example.com/mylink/{{}}
allure.link.mylink.title=My Link Title
allure.link.mylink.description=My Link Description
allure.link.mylink.icon=https://example.com/icon.png
allure.link.mylink.color=#FF0000
allure.link.mylink.size=16
allure.link.mylink.position=top
allure.link.mylink.target=_blank
allure.link.mylink.rel=noopener
allure.link.mylink.hreflang=en
allure.link.mylink.type=custom
allure.link.mylink.url=https://example.com/mylink/{{}}
allure.link.mylink.title=My Link Title
allure.link.mylink.description=My Link Description
allure.link.mylink.icon=https://example.com/icon.png
allure.link.mylink.color=#FF0000
allure.link.mylink.size=16
allure.link.mylink.position=top
allure.link.mylink.target=_blank
allure.link.mylink.rel=noopener
allure.link.mylink.hreflang=en
environment={environment}
test_framework=pytest
test_runner=pytest
allure_version=2.13.0
"""
        
        properties_file = os.path.join(self.results_dir, "allure.properties")
        with open(properties_file, 'w') as f:
            f.write(properties_content)
    
    def create_environment_file(self, environment: str = "localhost", base_url: str = "http://localhost:8000"):
        """Create environment.json file for Allure report"""
        env_data = {
            "environment": environment,
            "base_url": base_url,
            "test_execution_time": datetime.now().isoformat(),
            "test_framework": "pytest",
            "allure_version": "2.13.0",
            "python_version": "3.8+",
            "pytest_version": "7.0+"
        }
        
        env_file = os.path.join(self.results_dir, "environment.json")
        with open(env_file, 'w') as f:
            json.dump(env_data, f, indent=2)
    
    def create_categories_file(self):
        """Create categories.json file for test categorization"""
        categories = [
            {
                "name": "Product defects",
                "matchedStatuses": ["failed"],
                "messageRegex": ".*AssertionError.*"
            },
            {
                "name": "Test defects",
                "matchedStatuses": ["broken"],
                "messageRegex": ".*Exception.*"
            },
            {
                "name": "Skipped tests",
                "matchedStatuses": ["skipped"],
                "messageRegex": ".*Skipped.*"
            }
        ]
        
        categories_file = os.path.join(self.results_dir, "categories.json")
        with open(categories_file, 'w') as f:
            json.dump(categories, f, indent=2)
    
    def create_executor_file(self, environment: str = "localhost"):
        """Create executor.json file for build information"""
        executor_data = {
            "name": "User Management API Tests",
            "type": "pytest",
            "buildName": f"build-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "buildUrl": "https://example.com/build/",
            "reportUrl": "https://example.com/report/",
            "reportName": f"User Management API Test Report - {environment}",
            "executor": {
                "name": "pytest",
                "version": "7.0+",
                "type": "pytest"
            },
            "environment": environment
        }
        
        executor_file = os.path.join(self.results_dir, "executor.json")
        with open(executor_file, 'w') as f:
            json.dump(executor_data, f, indent=2)

# Global Allure config instance
allure_config = AllureConfig()

