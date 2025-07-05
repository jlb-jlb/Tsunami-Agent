#!/usr/bin/env python3
"""
Test the actual LLM agent to generate a plugin
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_agent_plugin_creation():
    """Test the actual agent plugin creation with LLM"""
    print("Testing LLM Agent Plugin Creation...")
    
    try:
        from tsunami_agent.main import create_plugin_workflow
        
        # Create a mock args object
        class MockArgs:
            def __init__(self):
                self.model_provider = "anthropic"  # or "openai"
                self.model = "claude-sonnet-4-20250514"  # Using the correct model name from main.py
                self.vulnerability_type = "xss"
        
        args = MockArgs()
        
        print(f"Creating plugin for {args.vulnerability_type} vulnerability...")
        print(f"Using model: {args.model} from {args.model_provider}")
        
        # Run the actual workflow
        result = create_plugin_workflow(args, args.vulnerability_type)
        
        print(f"Plugin creation result: {result}")
        
        # Check if the plugin was created
        if result is None:
            print("✗ Plugin creation failed - no result returned")
            return False
            
        plugin_dir = f"tsunami-agent-plugins/{result.plugin_name}_vulnerability"
        if os.path.exists(plugin_dir):
            print(f"✓ Plugin directory created: {plugin_dir}")
            
            # Check if Java files were created and modified
            java_detector_path = os.path.join(plugin_dir, "src/main/java/com/google/tsunami/plugins/raid")
            if os.path.exists(java_detector_path):
                java_files = [f for f in os.listdir(java_detector_path) if f.endswith('.java')]
                
                print(f"Java files created: {java_files}")
                
                # Check the detector file content
                detector_file = next((f for f in java_files if 'Detector.java' in f), None)
                if detector_file:
                    detector_path = os.path.join(java_detector_path, detector_file)
                    with open(detector_path, 'r') as f:
                        content = f.read()
                        if 'isServiceVulnerable' in content:
                            print("✓ isServiceVulnerable method found in detector")
                        else:
                            print("✗ isServiceVulnerable method not found in detector")
                            
                        print(f"Detector file preview:\n{content[:500]}...")
                else:
                    print("✗ No detector Java file found")
            else:
                print(f"✗ Java detector path not found: {java_detector_path}")
            
            return True
        else:
            print(f"✗ Plugin directory not created: {plugin_dir}")
            return False
            
    except Exception as e:
        print(f"✗ Agent plugin creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("Running LLM Agent Test...")
    
    # Check if environment variables are set
    if not os.getenv('ANTHROPIC_API_KEY') and not os.getenv('OPENAI_API_KEY'):
        print("Warning: No API keys found in environment variables")
        print("Please set ANTHROPIC_API_KEY or OPENAI_API_KEY in your .env file")
        return
    
    # Test the agent
    if test_agent_plugin_creation():
        print("✓ LLM Agent test passed")
    else:
        print("✗ LLM Agent test failed")
    
    print("\nLLM Agent test completed!")

if __name__ == "__main__":
    load_dotenv()
    main()
