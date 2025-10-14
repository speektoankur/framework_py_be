import json
import os
from typing import Dict, Any, Optional

class ConfigReader:
    """Configuration reader for test environments"""
    
    def __init__(self, config_dir: str = "test/config"):
        self.config_dir = config_dir
        self._config_cache: Dict[str, Any] = {}
    
    def load_config(self, environment: str) -> Dict[str, Any]:
        """
        Load configuration for specified environment
        
        Args:
            environment: Environment name (e.g., 'localhost', 'release')
            
        Returns:
            Configuration dictionary
        """
        if environment in self._config_cache:
            return self._config_cache[environment]
        
        config_file = os.path.join(self.config_dir, f"{environment}.json")
        
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                self._config_cache[environment] = config
                return config
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file {config_file}: {e}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {e}")
    
    def get_base_url(self, environment: str) -> str:
        """Get base URL for specified environment"""
        config = self.load_config(environment)
        return config.get("base_url", "")
    
    def get_timeout(self, environment: str) -> int:
        """Get request timeout for specified environment"""
        config = self.load_config(environment)
        return config.get("timeout", 30)
    
    def get_retry_count(self, environment: str) -> int:
        """Get retry count for specified environment"""
        config = self.load_config(environment)
        return config.get("retry_count", 3)
    
    def get_test_data_config(self, environment: str) -> Dict[str, Any]:
        """Get test data configuration for specified environment"""
        config = self.load_config(environment)
        return config.get("test_data", {})
    
    def get_all_environments(self) -> list:
        """Get list of available environments"""
        if not os.path.exists(self.config_dir):
            return []
        
        environments = []
        for file in os.listdir(self.config_dir):
            if file.endswith('.json'):
                environments.append(file[:-5])  # Remove .json extension
        
        return environments

# Global config reader instance
config_reader = ConfigReader()

