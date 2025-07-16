import os
import argparse
import subprocess
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from .tools import vulnerability_reader_tool, example_detector_reader_tool, read_vulnerability_file, create_plugin_template
from .util import extract_java_from_markdown


load_dotenv()

    

class PluginImplementation(BaseModel):
    """
    Template for the Structured Output of the model
    """
    vulnerability_type: str
    plugin_name: str
    description: str
    recommendation: str
    endpoints: list[str]
    payloads: list[str]
    imports: list[str] 
    java_code: str



def parse_raw_json_response(output: str, vulnerability_type: str) -> PluginImplementation:
    """
    Robustly parse the raw JSON response from the LLM, handling escaped characters and malformed JSON
    """
    import json
    import re
    
    print(f"Parsing raw response of length: {len(output)}")
    
    # Method 1: Try to find and parse complete JSON
    json_patterns = [
        r'```json\s*(\{.*?\})\s*```',  # JSON in markdown blocks
        r'(\{[^{}]*"vulnerability_type"[^{}]*\})',  # Simple JSON object
        r'(\{.*?"java_code".*?\})',  # JSON containing java_code
    ]
    
    for pattern in json_patterns:
        json_match = re.search(pattern, output, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            try:
                plugin_data = json.loads(json_str)
                print("Successfully parsed JSON")
                return PluginImplementation(
                    vulnerability_type=plugin_data.get('vulnerability_type', vulnerability_type),
                    plugin_name=plugin_data.get('plugin_name', vulnerability_type + '_detector'),
                    java_code=plugin_data.get('java_code', ''),
                    description=plugin_data.get('description', f"Detects {vulnerability_type} vulnerabilities"),
                    recommendation=plugin_data.get('recommendation', f"Implement proper security measures to prevent {vulnerability_type} attacks"),
                    endpoints=plugin_data.get('endpoints', []),
                    payloads=plugin_data.get('payloads', []),
                    imports=plugin_data.get('imports', [])
                )
            except json.JSONDecodeError as e:
                print(f"JSON parsing failed: {e}")
                continue
    
    # Method 2: Extract individual fields using regex
    print("JSON parsing failed, trying field extraction...")
    
    # Extract vulnerability type
    vuln_type_match = re.search(r'"vulnerability_type":\s*"([^"]*)"', output)
    vuln_type = vuln_type_match.group(1) if vuln_type_match else vulnerability_type
    
    # Extract plugin name
    plugin_name_match = re.search(r'"plugin_name":\s*"([^"]*)"', output)
    plugin_name = plugin_name_match.group(1) if plugin_name_match else vulnerability_type + '_detector'
    
    # Extract description
    description_match = re.search(r'"description":\s*"([^"]*)"', output)
    description = description_match.group(1) if description_match else f"Detects {vulnerability_type} vulnerabilities"
    
    # Extract recommendation
    recommendation_match = re.search(r'"recommendation":\s*"([^"]*)"', output)
    recommendation = recommendation_match.group(1) if recommendation_match else f"Implement proper security measures to prevent {vulnerability_type} attacks"
    
    # Extract Java code (most complex part)
    java_code = extract_java_code_from_raw_response(output)
    
    # Extract imports
    imports_match = re.search(r'"imports":\s*\[([^\]]*)\]', output)
    imports = []
    if imports_match:
        imports_str = imports_match.group(1)
        # Extract individual imports from the array
        import_matches = re.findall(r'"([^"]*)"', imports_str)
        imports = import_matches
    
    print(f"Extracted fields: vuln_type={vuln_type}, plugin_name={plugin_name}, java_code_length={len(java_code)}, imports={imports}")
    
    return PluginImplementation(
        vulnerability_type=vuln_type,
        plugin_name=plugin_name,
        java_code=java_code,
        description=description,
        recommendation=recommendation,
        endpoints=[],
        payloads=[],
        imports=imports
    )


def extract_java_code_from_raw_response(output: str) -> str:
    """
    Extract Java code from raw response using multiple strategies
    """
    import re
    
    # Strategy 1: Extract from "java_code" field with proper escape handling
    # This is the most robust approach for handling the complex escaping
    
    # Find the start of the java_code field
    java_start = output.find('"java_code":')
    if java_start == -1:
        print("No java_code field found")
        return '// TODO: Implement vulnerability detection logic\nreturn false;'
    
    # Find the opening quote after "java_code":
    quote_start = output.find('"', java_start + len('"java_code":'))
    if quote_start == -1:
        print("No opening quote found for java_code")
        return '// TODO: Implement vulnerability detection logic\nreturn false;'
    
    # Extract everything until we find the next JSON field or end of JSON
    # Look for the next field (like "description", "recommendation", etc.)
    next_field_patterns = [
        r'"description"\s*:',
        r'"recommendation"\s*:',
        r'"endpoints"\s*:',
        r'"payloads"\s*:',
        r'}\s*$',  # End of JSON
        r'}\s*,',  # End of this JSON object
    ]
    
    # Start from after the opening quote
    search_start = quote_start + 1
    java_end = len(output)  # Default to end of string
    
    for pattern in next_field_patterns:
        match = re.search(pattern, output[search_start:])
        if match:
            # Found a field, now we need to find the closing quote before it
            field_start = search_start + match.start()
            
            # Look backwards from the field start to find the closing quote
            for i in range(field_start - 1, search_start, -1):
                if output[i] == '"' and output[i - 1] != '\\':
                    java_end = i
                    break
            break
    
    # Extract the Java code between the quotes
    if java_end > search_start:
        java_code = output[search_start:java_end]
        
        # Clean up the escaped characters
        java_code = java_code.replace('\\n', '\n')
        java_code = java_code.replace('\\"', '"')
        java_code = java_code.replace('\\\\', '\\')
        java_code = java_code.replace('\\t', '\t')
        
        # Remove any trailing garbage (like incomplete JSON)
        java_code = java_code.rstrip('", \n\t')
        
        if len(java_code) > 100:  # Reasonable threshold
            print(f"Extracted Java code with improved parsing: {len(java_code)} characters")
            return java_code
    
    # Strategy 2: Try regex patterns as fallback
    java_code_patterns = [
        r'"java_code":\s*"((?:[^"\\]|\\.)*)"',  # Handle escaped quotes
        r'"java_code":\s*"([^"]*(?:\\.[^"]*)*)"',  # Alternative pattern
    ]
    
    for pattern in java_code_patterns:
        java_match = re.search(pattern, output, re.DOTALL)
        if java_match:
            java_code = java_match.group(1)
            # Unescape the Java code
            java_code = java_code.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
            if len(java_code) > 100:  # Reasonable threshold
                print(f"Extracted Java code from regex pattern: {len(java_code)} characters")
                return java_code
    
    # Strategy 3: Look for Java method directly in the response
    method_patterns = [
        r'(private boolean isServiceVulnerable\s*\([^)]*\)\s*\{.*?(?=private\s+|public\s+|protected\s+|\}[^}]*$))',  # Method until next method
        r'(private boolean isServiceVulnerable.*?^\s*\})',  # Complete method
        r'(private boolean isServiceVulnerable.*?return false;)',  # Method ending with return false
        r'(private boolean isServiceVulnerable.*?return true;)',   # Method ending with return true
    ]
    
    for pattern in method_patterns:
        method_match = re.search(pattern, output, re.DOTALL | re.MULTILINE)
        if method_match:
            java_code = method_match.group(1)
            print(f"Extracted Java method directly: {len(java_code)} characters")
            return java_code
    
    print("No Java code found, using fallback")
    return '// TODO: Implement vulnerability detection logic\nreturn false;'



def create_plugin_workflow(args, vulnerability_type: str):
    """Main workflow for creating a Tsunami plugin from vulnerability description."""
    model_provider = args.model_provider
    model = args.model

    if args.model_provider == "openai":
        llm = ChatOpenAI(model=model, temperature=0.0, max_tokens=7000) # type: ignore
    else:
        llm = ChatAnthropic(
            model_name=model,
            temperature=0,
            timeout=None,
            max_retries=2,
            stop=["\n\nHuman:"],
            max_tokens_to_sample=7000,  # Increase token limit for Anthropic
        )

    print(f"Creating plugin for {vulnerability_type} vulnerability using {model} from {model_provider}")
    
    # Step 1: Analyze vulnerability
    parser = PydanticOutputParser(pydantic_object=PluginImplementation)
    
    analysis_prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are an expert security researcher who creates Tsunami Security Scanner plugins.
        Your task is to analyze vulnerability information and create a complete Java implementation 
        for the isServiceVulnerable method in a Tsunami plugin.
        
        WORKFLOW:
        1. First, read the example SQL injection detector to understand the correct API patterns
        2. Analyze the vulnerability information from the vulnerability_reader_tool. It provides solutions.
        3. Generate Java code following the patterns from the example
        4. List any additional imports needed that aren't in the standard template
        
        Based on the vulnerability information provided, you need to:
        1. Extract relevant endpoints, parameters, and payloads for detection
        2. Generate Java code for the COMPLETE isServiceVulnerable method that can detect this vulnerability and make sure to implement all possible attack scenarios from the vulnerability_reader_tool. 
        3. The code must test the Application on all written attacks, record the result of each of them and after executing the last attack, return #succesful attacks > 0
        3. Provide a clear description and recommendation
        4. List any additional imports needed beyond the standard template
        
        CRITICAL REQUIREMENTS:
        - Study the example detector FIRST to understand the correct API patterns
        - Follow the exact same patterns for HTTP requests, URL building, and method signatures
        - Output ONLY a JSON object with the required fields
        - Do NOT include markdown code blocks (```json) around the JSON
        - Escape all quotes and newlines properly in the java_code field
        - The java_code should be a COMPLETE implementation with ALL methods and not contain anything else except the code
        - ALL helper methods MUST follow the same patterns as the example
        - Include any additional imports needed in the "imports" array
        - Do NOT truncate your response
        - Do not add any explanations after creating the Structured Output as it will mess up the agent.
        - Make sure to not write any syntax errors that cause problems. Common mistakes from your previous iterations are: 
            - error: cannot find symbol .setBody(loginPayload) 
            - you wrote: `.setRequestBody(payload)` but required was: .setRequestBody(ByteString.copyFromUtf8(payload)) 
        
        
        Example format:
        {{
          "vulnerability_type": "SQL Injection",
          "plugin_name": "SqlInjection",
          "description": "Detects SQL injection vulnerabilities",
          "recommendation": "Use parameterized queries and input validation",
          "endpoints": ["/login", "/search"]
          "payloads": ["' OR '1'='1", "'; DROP TABLE users; --"],
          "imports": ["com.google.protobuf.ByteString", "java.net.URLEncoder"],
          "java_code": "private boolean isServiceVulnerable(NetworkService networkService) {{\\n    // Complete implementation following example patterns\\n    return false;\\n}}",
        }}
        
        Output format: {format_instructions}
        """),
        ("human", """
        Analyze this vulnerability information and create a Tsunami plugin implementation:
        
        Vulnerability Type: {vulnerability_type}
        
        Vulnerability Details available with the vulnerability_reader_tool
        
        Output ONLY the JSON object without markdown formatting.
        """),
        ("placeholder", "{agent_scratchpad}")
    ]).partial(format_instructions=parser.get_format_instructions())
    
    tools = [vulnerability_reader_tool, example_detector_reader_tool]
    
    agent = create_tool_calling_agent(
        llm=llm,
        prompt=analysis_prompt,
        tools=tools,
    )
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )
    
    # Read vulnerability content

    vulnerability_content = read_vulnerability_file(vulnerability_type)
    
    # Generate plugin implementation
    response = agent_executor.invoke({
        "vulnerability_type": vulnerability_type,
        "vulnerability_content": vulnerability_content
    })
    
    print(f"Response type: {type(response)}")
    print(f"Response keys: {response.keys() if isinstance(response, dict) else 'Not a dict'}")
    
    output = response.get("output", "")
    print(f"Raw output length: {len(output)}")
    print(f"Raw output type: {type(output)}")
    
    
    try:
        # Extract the output from the response
        output = response.get("output", "")
        
        # If output is a list, take the first element
        if isinstance(output, list) and len(output) > 0:
            if isinstance(output[0], dict) and 'text' in output[0]:
                output = output[0]['text']
            else:
                output = str(output[0])
        
        # Ensure output is a string
        if not isinstance(output, str):
            output = str(output)
        
        # Try to parse the JSON from the output using robust parsing
        plugin_implementation = parse_raw_json_response(output, vulnerability_type)
        
        print("\nGenerated plugin implementation:")
        print(f"Plugin Name: {plugin_implementation.plugin_name}")
        print(f"Description: {plugin_implementation.description}")
        print(f"Recommendation: {plugin_implementation.recommendation}")
        print(f"Java Code Length: {len(plugin_implementation.java_code) if plugin_implementation.java_code else 0} characters")
        print(f"Additional Imports: {plugin_implementation.imports if plugin_implementation.imports else 'None'}")
        
        # Step 2: Create plugin template with the generated Java code and imports
        plugin_dir = create_plugin_template(
            plugin_name=plugin_implementation.plugin_name, 
            recommendation=plugin_implementation.recommendation,
            java_code=plugin_implementation.java_code,
            imports=plugin_implementation.imports
        )
        print(f"\nTemplate creation result: {plugin_dir}")

        # Step 3: Verify and correct the generated plugin
        max_retries = 3
        for i in range(max_retries):
            print(f"\n--- Verification Attempt {i+1}/{max_retries} ---")
            
            try:
                process = subprocess.run(
                    ["build-plugin", plugin_dir],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=120
                )
                verification_result = process.stdout + "\n" + process.stderr
                
                if process.returncode == 0:
                    print("Java plugin built successfully!")
                    break
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                verification_result = f"Build command failed: {e}"

            print(f"Build failed. Attempting to fix...")
            print(f"Error: {verification_result}")

            # If build fails, ask the LLM to fix the code
            fix_prompt = ChatPromptTemplate.from_messages([
                ("system", """
                You are a Java debugging expert. The provided Java code for a Tsunami plugin has a build error.
                Your task is to analyze the error message and the code, then provide a corrected version of the code.

                CRITICAL REQUIREMENTS:
                - ONLY output the corrected, complete Java code for the `isServiceVulnerable` method.
                - Do NOT output any explanations, markdown, or JSON.
                - Ensure the corrected code is a single block of text.
                - Pay close attention to the error message to identify the exact problem (e.g., missing imports, syntax errors, incorrect method calls).
                """),
                ("human", """
                The following Java code failed to build. Please fix it.

                Build Error:
                {build_error}

                Faulty Java Code:
                {java_code}

                Provide the corrected and complete `isServiceVulnerable` method implementation:
                """)
            ])
            
            # Create a new chain for fixing the code
            fix_chain = fix_prompt | llm
            
            # Invoke the LLM with the error and the faulty code
            fix_response = fix_chain.invoke({
                "build_error": verification_result,
                "java_code": plugin_implementation.java_code
            })
            
            # The response content should be the corrected Java code
            raw_corrected_code = fix_response.content
            
            print(f"LLM proposed a fix of length: {len(raw_corrected_code)}")

            # Use the new function to extract only the pure Java code
            corrected_java_code = extract_java_from_markdown(raw_corrected_code)
            
            # Update the plugin implementation with the new code
            plugin_implementation.java_code = corrected_java_code
            
            # Re-create the plugin with the corrected code
            plugin_dir = create_plugin_template(
                plugin_name=plugin_implementation.plugin_name,
                recommendation=plugin_implementation.recommendation,
                java_code=plugin_implementation.java_code,
                imports=plugin_implementation.imports
            )
            print(f"Re-created plugin with corrected code in: {plugin_dir}")

        else: # This block executes if the loop completes without a break
            print("\nError: Max retries reached. Could not fix the plugin build.")
            return None

        # Verify the Java code was injected correctly
        if plugin_implementation.java_code and len(plugin_implementation.java_code) > 50:
            print("Java code successfully generated and injected into template")
        else:
            print("Warning: Java code may not have been properly generated")
        
        return plugin_implementation
        
    except Exception as e:
        print(f"Error parsing plugin implementation: {e}")
        print(f"Raw response: {response}")
        return None

def main(args):
    if hasattr(args, 'vulnerability_type') and args.vulnerability_type:
        # Plugin creation workflow
        return create_plugin_workflow(args, args.vulnerability_type)
    else:
        raise ValueError("No Vulnerability Type Provided!")
    



if __name__ == "__main__":
    # get arguments from command line
    parser = argparse.ArgumentParser(description="Tsunami Agent")
    parser.add_argument(
        "--model-provider",
        type=str,
        choices=["openai", "anthropic"],
        default="anthropic",
        help="Model provider to use for the agent",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["gpt-4", "claude-sonnet-4-20250514"],
        default="claude-sonnet-4-20250514",
        help="Model to use for the agent. Default is 'claude-sonnet-4-20250514' for Anthropic or 'gpt-4' for OpenAI.",
    )
    parser.add_argument(
        "--vulnerability-type",
        type=str,
        help="Type of vulnerability to create a plugin for (e.g., 'sql_injection', 'xss', 'broken_access_control')",
    )
    parser.add_argument(
        "--list-vulnerabilities",
        action="store_true",
        help="List all available vulnerability types",
    )
    
    args = parser.parse_args()
    
    # List vulnerabilities if requested
    if args.list_vulnerabilities:
        from .tools import list_available_vulnerabilities
        print(list_available_vulnerabilities())
    else:
        main(args)
