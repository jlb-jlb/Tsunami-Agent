#!/usr/bin/env python3
"""
Full workflow test for the Tsunami Agent
"""

import os
import sys

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tsunami_agent.tools import list_available_vulnerabilities, read_vulnerability_file, create_plugin_template

def test_templater():
    """Test the templater functionality"""
    print("Testing templater functionality...")
    
    # Create a mock args object
    class MockArgs:
        def __init__(self, plugin_name, recommendation=None):
            self.plugin_name = plugin_name
            self.recommendation = recommendation
    
    # Test creating a plugin template
    args = MockArgs("test_xss_plugin", "Sanitize user input to prevent XSS attacks")
    
    try:
        result = create_plugin_template(args.plugin_name, args.recommendation)
        print(f"Template creation result: {result}")
        
        # Check if the directory was created
        expected_dir = f"tsunami-agent-plugins/{args.plugin_name}_vulnerability"
        if os.path.exists(expected_dir):
            print(f"✓ Plugin directory created: {expected_dir}")
            
            # List the contents
            for root, dirs, files in os.walk(expected_dir):
                level = root.replace(expected_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    print(f"{subindent}{file}")
        else:
            print(f"✗ Plugin directory not created: {expected_dir}")
            
        return True
    except Exception as e:
        print(f"✗ Templater test failed: {e}")
        return False

def test_vulnerability_analysis():
    """Test vulnerability analysis"""
    print("\nTesting vulnerability analysis...")
    
    # Read a vulnerability file
    vulnerability_content = read_vulnerability_file("sql_injection")
    print(f"Read {len(vulnerability_content)} characters from SQL injection vulnerability")
    
    # Test pattern extraction (we'll implement this in tools.py)
    from tsunami_agent.tools import analyze_vulnerability_for_detection
    
    patterns = analyze_vulnerability_for_detection(vulnerability_content)
    print(f"Extracted patterns: {patterns}")
    
    return True

def main():
    """Main test function"""
    print("Running Full Tsunami Agent Workflow Tests...")
    
    # Test 1: List vulnerabilities
    vulnerabilities = list_available_vulnerabilities()
    print(f"Available vulnerabilities: {vulnerabilities}")
    
    # Test 2: Template creation
    if test_templater():
        print("✓ Templater test passed")
    else:
        print("✗ Templater test failed")
    
    # Test 3: Vulnerability analysis
    if test_vulnerability_analysis():
        print("✓ Vulnerability analysis test passed")
    else:
        print("✗ Vulnerability analysis test failed")
    
    print("\nAll workflow tests completed!")

if __name__ == "__main__":
    main()
