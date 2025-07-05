#!/usr/bin/env python3
"""
Command-line interface for the Tsunami Agent
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tsunami_agent.main import create_plugin_workflow
from tsunami_agent.tools import list_available_vulnerabilities

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description='Tsunami Security Scanner Plugin Generator')
    parser.add_argument('--vulnerability-type', '-v', 
                       help='Type of vulnerability to create plugin for')
    parser.add_argument('--model-provider', '-p', 
                       choices=['openai', 'anthropic'],
                       default='anthropic',
                       help='LLM provider to use')
    parser.add_argument('--model', '-m',
                       default='claude-3-5-sonnet-20241022',
                       help='Model to use for generation')
    parser.add_argument('--list-vulnerabilities', '-l',
                       action='store_true',
                       help='List available vulnerability types')
    
    args = parser.parse_args()
    
    # List vulnerabilities if requested
    if args.list_vulnerabilities:
        print("Available vulnerability types:")
        vulnerabilities = list_available_vulnerabilities()
        print(vulnerabilities)
        return
    
    # Check if API keys are set
    if args.model_provider == 'anthropic' and not os.getenv('ANTHROPIC_API_KEY'):
        print("Error: ANTHROPIC_API_KEY not found in environment variables")
        print("Please set it in your .env file")
        return
    
    if args.model_provider == 'openai' and not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set it in your .env file")
        return
    
    # Create the plugin
    try:
        print(f"Creating plugin for {args.vulnerability_type} vulnerability...")
        print(f"Using {args.model} from {args.model_provider}")
        
        result = create_plugin_workflow(args, args.vulnerability_type)
        
        print(f"Plugin creation completed: {result}")
        
        # Show the created plugin directory
        plugin_dir = f"tsunami-agent-plugins/{args.vulnerability_type}_vulnerability"
        if os.path.exists(plugin_dir):
            print(f"\nPlugin created in: {plugin_dir}")
            print("Files created:")
            for root, dirs, files in os.walk(plugin_dir):
                level = root.replace(plugin_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    print(f"{subindent}{file}")
        
    except Exception as e:
        print(f"Error creating plugin: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
