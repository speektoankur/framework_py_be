#!/usr/bin/env python3
"""
Test runner script for User Management API tests
Supports different environments and test execution modes
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Add test directory to Python path
test_dir = Path(__file__).parent
sys.path.insert(0, str(test_dir))

from allure_config import allure_config
from common.config_reader import config_reader

def run_tests(environment: str = "localhost", test_type: str = "all", generate_report: bool = True):
    """
    Run tests with specified parameters
    
    Args:
        environment: Environment to test against (localhost/release)
        test_type: Type of tests to run (all/smoke/regression)
        generate_report: Whether to generate Allure report
    """
    
    print(f"🚀 Starting test execution for environment: {environment}")
    print(f"📋 Test type: {test_type}")
    print(f"📊 Generate report: {generate_report}")
    
    # Setup Allure configuration
    try:
        config = config_reader.load_config(environment)
        base_url = config.get("base_url", "http://localhost:8000")
        
        allure_config.create_allure_properties(environment)
        allure_config.create_environment_file(environment, base_url)
        allure_config.create_categories_file()
        allure_config.create_executor_file(environment)
        
        print("✅ Allure configuration created successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not setup Allure config: {e}")
    
    # Build pytest command
    cmd = [
        "python3", "-m", "pytest",
        "test/testcases/",
        f"--env={environment}",
        "--alluredir=test/reports/allure-results",
        "--clean-alluredir",
        "-v"
    ]
    
    # Add test type specific options
    if test_type == "smoke":
        cmd.extend(["-m", "smoke"])
    elif test_type == "regression":
        cmd.extend(["-m", "regression"])
    elif test_type == "api":
        cmd.extend(["-m", "api"])
    
    # Add HTML report
    cmd.extend(["--html=test/reports/pytest_report.html", "--self-contained-html"])
    
    print(f"🔧 Running command: {' '.join(cmd)}")
    
    # Run tests
    try:
        result = subprocess.run(cmd, cwd=test_dir.parent, capture_output=False)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            
    except Exception as e:
        print(f"💥 Error running tests: {e}")
        return False
    
    # Generate Allure report
    if generate_report:
        try:
            print("📊 Generating Allure report...")
            allure_cmd = [
                "allure", "generate", 
                "test/reports/allure-results", 
                "-o", "test/reports/allure-report",
                "--clean"
            ]
            
            subprocess.run(allure_cmd, cwd=test_dir.parent, check=True)
            print("✅ Allure report generated successfully!")
            print(f"📁 Report location: {test_dir}/reports/allure-report/index.html")
            
            # Try to open report in browser (optional)
            try:
                allure_serve_cmd = ["allure", "open", "test/reports/allure-report"]
                print("🌐 Opening Allure report in browser...")
                subprocess.Popen(allure_serve_cmd, cwd=test_dir.parent)
            except Exception as e:
                print(f"⚠️  Could not open report in browser: {e}")
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error generating Allure report: {e}")
            print("💡 Make sure Allure is installed: brew install allure (macOS) or download from https://github.com/allure-framework/allure2/releases")
        except FileNotFoundError:
            print("❌ Allure command not found")
            print("💡 Install Allure: brew install allure (macOS) or download from https://github.com/allure-framework/allure2/releases")
            print("📊 Allure results are available in test/reports/allure-results/ for manual report generation")
        except Exception as e:
            print(f"❌ Unexpected error generating report: {e}")
    
    return result.returncode == 0

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description="Run User Management API tests")
    
    parser.add_argument(
        "--env", 
        choices=["localhost", "release"], 
        default="localhost",
        help="Environment to test against (default: localhost)"
    )
    
    parser.add_argument(
        "--type",
        choices=["all", "smoke", "regression", "api"],
        default="all",
        help="Type of tests to run (default: all)"
    )
    
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip Allure report generation"
    )
    
    parser.add_argument(
        "--list-envs",
        action="store_true",
        help="List available environments"
    )
    
    args = parser.parse_args()
    
    if args.list_envs:
        try:
            envs = config_reader.get_all_environments()
            print("Available environments:")
            for env in envs:
                print(f"  - {env}")
        except Exception as e:
            print(f"Error listing environments: {e}")
        return
    
    # Run tests
    success = run_tests(
        environment=args.env,
        test_type=args.type,
        generate_report=not args.no_report
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
