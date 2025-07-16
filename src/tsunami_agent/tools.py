from langchain.tools import Tool
import os
import re



def read_vulnerability_file(vulnerability_type: str) -> str:
    """Read vulnerability information from markdown files."""
    vulnerabilities_dir = "vulnerabilities"
    filename = f"{vulnerability_type}_vulnerabilities.md"
    filepath = os.path.join(vulnerabilities_dir, filename)
    
    if not os.path.exists(filepath):
        return f"Error: Vulnerability file '{filename}' not found. Available files: {', '.join(os.listdir(vulnerabilities_dir)) if os.path.exists(vulnerabilities_dir) else 'None'}"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


def list_available_vulnerabilities() -> str:
    """List all available vulnerability types."""
    vulnerabilities_dir = "vulnerabilities"
    if not os.path.exists(vulnerabilities_dir):
        return "Vulnerabilities directory not found"
    
    try:
        files = [f for f in os.listdir(vulnerabilities_dir) if f.endswith('_vulnerabilities.md')]
        vulnerability_types = [f.replace('_vulnerabilities.md', '') for f in files]
        return f"Available vulnerability types: {', '.join(vulnerability_types)}"
    except Exception as e:
        return f"Error listing vulnerabilities: {str(e)}"


def create_plugin_template(plugin_name: str, recommendation: str | None = None, java_code: str | None = None, imports: list[str] | None = None) -> str:
    """Create a plugin template using the templater script."""
    try:
        # Import the templater module
        from .templater import create_plugin_template
        
        # Create a mock args object
        class Args:
            def __init__(self, plugin_name, recommendation, java_code, imports):
                self.plugin_name = plugin_name
                self.recommendation = recommendation or f"Implement proper security measures to prevent {plugin_name.replace('_', ' ')} vulnerabilities."
                self.java_code = java_code
                self.imports = imports or []
        
        args = Args(plugin_name, recommendation, java_code, imports)
        create_plugin_template(args)
        
        return f"Successfully created plugin template for '{plugin_name}'"
    except Exception as e:
        return f"Error creating plugin template: {str(e)}"




def read_example_detector() -> str:
    """Read the example SQL injection detector to understand the correct API patterns."""
    example_path = "example_plugins/sql_injection_template/src/main/java/com/google/tsunami/plugins/raid/SqlInjectionDetector.java"
    
    if not os.path.exists(example_path):
        return "Error: Example detector file not found"
    
    try:
        with open(example_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading example detector: {str(e)}"


# Create tool instances
vulnerability_reader_tool = Tool(
    name="read_vulnerability_file",
    func=read_vulnerability_file,
    description="Read vulnerability information from markdown files. Input should be the vulnerability type (e.g., 'sql_injection', 'xss', 'broken_access_control')",
)

vulnerability_lister_tool = Tool(
    name="list_vulnerabilities",
    func=list_available_vulnerabilities,
    description="List all available vulnerability types that can be used to create plugins",
)

plugin_template_tool = Tool(
    name="create_plugin_template",
    func=create_plugin_template,
    description="Create a new plugin template. Input should be the plugin name in snake_case (e.g., 'sql_injection', 'xss_reflected')",
)

example_detector_tool = Tool(
    name="read_example_detector",
    func=read_example_detector,
    description="Read the example SQL injection detector to understand the correct API patterns.",
)

example_detector_reader_tool = Tool(
    name="read_example_detector", 
    func=lambda _: read_example_detector(),  # Ignore any arguments passed by the LLM
    description="Read the example SQL injection detector to understand the correct Tsunami API patterns, imports, and method structure. Use this to learn the proper way to implement vulnerability detection methods."
)






