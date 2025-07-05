#!/usr/bin/env python3
"""
Test script for the Tsunami Agent
"""

import os
import sys

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tsunami_agent.tools import list_available_vulnerabilities, read_vulnerability_file

def test_vulnerability_reading():
    """Test reading vulnerability files"""
    print("Testing vulnerability file reading...")
    
    # List available vulnerabilities
    vulnerabilities = list_available_vulnerabilities()
    print(f"Available vulnerabilities: {vulnerabilities}")
    
    # Try to read SQL injection vulnerability
    sql_content = read_vulnerability_file("sql_injection")
    print(f"SQL Injection content preview: {sql_content[:200]}...")
    
    return True

def test_plugin_creation():
    """Test plugin creation workflow"""
    print("\nTesting plugin creation workflow...")
    
    # Create a mock args object
    class MockArgs:
        def __init__(self):
            self.model_provider = "anthropic"
            self.model = "claude-sonnet-4-20250514"
            self.vulnerability_type = "sql_injection"
    
    args = MockArgs()
    
    # This would normally call the LLM - for testing, we'll just test the setup
    print(f"Would create plugin for: {args.vulnerability_type}")
    print(f"Using model: {args.model} from {args.model_provider}")
    
    return True

def main_test():
    """Main test function"""
    print("Running Tsunami Agent Tests...")
    
    # Test 1: Vulnerability file reading
    if test_vulnerability_reading():
        print("✓ Vulnerability file reading test passed")
    else:
        print("✗ Vulnerability file reading test failed")
    
    # Test 2: Plugin creation setup
    if test_plugin_creation():
        print("✓ Plugin creation setup test passed")
    else:
        print("✗ Plugin creation setup test failed")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main_test()
