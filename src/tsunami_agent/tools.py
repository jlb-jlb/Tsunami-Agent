from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import os
import re


search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information using DuckDuckGo",
)

wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100) # type: ignore
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)


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


def create_plugin_template(plugin_name: str, recommendation: str | None = None, java_code: str | None = None) -> str:
    """Create a plugin template using the templater script."""
    try:
        # Import the templater module
        from .templater import create_plugin_template
        
        # Create a mock args object
        class Args:
            def __init__(self, plugin_name, recommendation, java_code):
                self.plugin_name = plugin_name
                self.recommendation = recommendation or f"Implement proper security measures to prevent {plugin_name.replace('_', ' ')} vulnerabilities."
                self.java_code = java_code
        
        args = Args(plugin_name, recommendation, java_code)
        create_plugin_template(args)
        
        return f"Successfully created plugin template for '{plugin_name}'"
    except Exception as e:
        return f"Error creating plugin template: {str(e)}"


def analyze_vulnerability_for_detection(vulnerability_content: str) -> str:
    """Analyze vulnerability content to extract detection patterns."""
    patterns = {
        'endpoints': [],
        'parameters': [],
        'payloads': [],
        'responses': [],
        'methods': []
    }
    
    lines = vulnerability_content.split('\n')
    for line in lines:
        line = line.strip()
        
        # Extract endpoints
        if '/rest/' in line or '/api/' in line:
            endpoint_match = re.search(r'`([^`]*(?:/rest/|/api/)[^`]*)`', line)
            if endpoint_match:
                patterns['endpoints'].append(endpoint_match.group(1))
        
        # Extract parameters
        param_match = re.search(r'`([a-zA-Z_][a-zA-Z0-9_]*)`.*parameter', line)
        if param_match:
            patterns['parameters'].append(param_match.group(1))
        
        # Extract payloads
        payload_matches = re.findall(r'`([^`]*(?:UNION|SELECT|INSERT|UPDATE|DELETE|<script|<iframe|javascript:)[^`]*)`', line)
        patterns['payloads'].extend(payload_matches)
        
        # Extract HTTP methods
        if 'POST request' in line or 'GET request' in line or 'PUT request' in line:
            method_match = re.search(r'(POST|GET|PUT|DELETE) request', line)
            if method_match:
                patterns['methods'].append(method_match.group(1))
    
    # Convert to string representation for LLM
    result = []
    for key, values in patterns.items():
        unique_values = list(set(values))
        if unique_values:
            result.append(f"{key}: {', '.join(unique_values)}")
    
    return "Detection patterns found:\n" + "\n".join(result) if result else "No specific detection patterns found"


def inject_java_code_into_template(plugin_name: str, java_code: str) -> str:
    """Inject generated Java code into the plugin template."""
    try:
        # Find the generated plugin directory
        plugin_dir = f"tsunami-agent-plugins/{plugin_name}_vulnerability"
        java_file_path = f"{plugin_dir}/src/main/java/com/google/tsunami/plugins/raid/{plugin_name.replace('_', '').title()}Detector.java"
        
        if not os.path.exists(java_file_path):
            return f"Error: Plugin file not found at {java_file_path}"
        
        # Read the existing template
        with open(java_file_path, 'r') as f:
            template_content = f.read()
        
        # Find the isServiceVulnerable method and replace it
        # Look for the method signature and replace everything until the closing brace
        import re
        
        # Pattern to match the entire isServiceVulnerable method
        pattern = r'(private boolean isServiceVulnerable\(NetworkService networkService\) \{[\s\S]*?\n  \})'
        
        if re.search(pattern, template_content):
            # Replace the method with the generated code
            updated_content = re.sub(pattern, java_code, template_content)
            
            # Write back to file
            with open(java_file_path, 'w') as f:
                f.write(updated_content)
            
            return f"Successfully injected Java code into {java_file_path}"
        else:
            return "Error: Could not find isServiceVulnerable method in template"
            
    except Exception as e:
        return f"Error injecting Java code: {str(e)}"


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

vulnerability_analyzer_tool = Tool(
    name="analyze_vulnerability",
    func=analyze_vulnerability_for_detection,
    description="Analyze vulnerability content to extract detection patterns like endpoints, parameters, and payloads. Input should be the vulnerability content as a string.",
)

java_injection_tool = Tool(
    name="inject_java_code",
    func=lambda args: inject_java_code_into_template(args.split("|")[0], args.split("|")[1]),
    description="Inject generated Java code into plugin template. Input format: 'plugin_name|java_code'",
)






