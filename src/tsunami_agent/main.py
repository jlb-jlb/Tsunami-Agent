import os
import argparse
import re
import subprocess
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from .tools import vulnerability_reader_tool, example_detector_reader_tool, create_plugin_template
from .util import extract_java_from_markdown

load_dotenv()


def parse_llm_output(output: str, vulnerability_type: str) -> tuple[str, str, list[str]]:
    """Parses the LLM output to extract java code and imports."""
    java_code = extract_java_from_markdown(output)

    imports_match = re.search(r"IMPORTS:(.*)", output, re.DOTALL)
    imports = []
    if imports_match:
        imports_str = imports_match.group(1).strip()
        imports = [line.strip() for line in imports_str.split('\n') if line.strip().startswith('import')]

    plugin_name = "".join(word.capitalize() for word in vulnerability_type.split('_')) + "Detector"
    
    return plugin_name, java_code, imports

def create_plugin_workflow(args, vulnerability_type: str):
    """Main workflow for creating a Tsunami plugin from vulnerability description."""
    model_provider = args.model_provider
    model = args.model

    if args.model_provider == "openai":
        llm = ChatOpenAI(model=model, temperature=0.0, max_tokens=7000)
    else:
        llm = ChatAnthropic(
            model_name=model,
            temperature=0,
            timeout=None,
            max_retries=2,
            stop=["\n\nHuman:"],
            max_tokens_to_sample=7000,
        )

    print(f"Creating plugin for {vulnerability_type} vulnerability using {model} from {model_provider}")

    analysis_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert security researcher creating Tsunami Security Scanner plugins.
Your task is to analyze vulnerability information and generate a complete Java implementation for the `isServiceVulnerable` method.

WORKFLOW:
1. First, read the example SQL injection detector to understand the correct API patterns.
2. Analyze the vulnerability information from the `vulnerability_reader_tool`.
3. Generate the complete Java code for the `isServiceVulnerable` method, including all necessary helper methods, following the patterns from the example.
4. List any additional Java imports required by your code.

CRITICAL REQUIREMENTS:
- Your FINAL output must be only the Java code and the imports.
- Start with the list of imports, prefixed with "IMPORTS:".
- After the imports, provide the complete Java code for the `isServiceVulnerable` method, wrapped in a ```java ... ``` markdown block.
- Do NOT include any other text, explanations, or formatting.
- In previous iterations you tried to import com.google.common.net.HttpHeaders;. This causes errors. Don't import it.
- The code must test the Application on all generated attacks, record the result of each of them and after executing the last attack, return #succesful attacks > 0
                  
EXAMPLE OUTPUT:
IMPORTS:
import com.google.protobuf.ByteString;
import java.net.URLEncoder;

```java
private boolean isServiceVulnerable(NetworkService networkService) {{
    // Complete implementation following example patterns
    return false;
}}
```
"""),
        ("human", """Analyze the vulnerability details for `{vulnerability_type}` and generate the Java code and imports."""),
        ("placeholder", "{agent_scratchpad}")
    ])

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
    
    response = agent_executor.invoke({
        "vulnerability_type": vulnerability_type,
    })
    
    output = response.get("output", "")

    # Ensure output is a string, handling list-based outputs from some models
    if isinstance(output, list):
        if len(output) > 0 and isinstance(output[0], dict) and 'text' in output[0]:
            output = output[0]['text']
        else:
            output = str(output) # Fallback for unexpected list formats
    
    if not isinstance(output, str):
        output = str(output) # Final fallback to ensure it's a string
    
    plugin_name, java_code, imports = parse_llm_output(output, vulnerability_type)
    recommendation = f"Implement proper security measures to prevent {vulnerability_type.replace('_', ' ')} attacks."

    print("\nGenerated plugin implementation:")
    print(f"Plugin Name: {plugin_name}")
    print(f"Java Code Length: {len(java_code)} characters")
    print(f"Additional Imports: {imports}")

    plugin_dir = create_plugin_template(
        plugin_name=plugin_name, 
        recommendation=recommendation,
        java_code=java_code,
        imports=imports
    )
    print(f"\nTemplate creation result: {plugin_dir}")

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

        fix_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Java debugging expert. The provided Java code for a Tsunami plugin has a build error.
Your task is to analyze the error message and the code, then provide a corrected version of the code.

CRITICAL REQUIREMENTS:
- ONLY output the corrected, complete Java code for the `isServiceVulnerable` method.
- Do NOT output any explanations, markdown, or JSON.
- Ensure the corrected code is a single block of text.
- Pay close attention to the error message to identify the exact problem (e.g., missing imports, syntax errors, incorrect method calls).
"""),
            ("human", """The following Java code failed to build. Please fix it.

Build Error:
{build_error}

Faulty Java Code:
{java_code}

Provide the corrected and complete `isServiceVulnerable` method implementation:
""")
        ])
        
        fix_chain = fix_prompt | llm
        
        fix_response = fix_chain.invoke({
            "build_error": verification_result,
            "java_code": java_code
        })
        
        raw_corrected_code = fix_response.content
        
        print(f"LLM proposed a fix of length: {len(raw_corrected_code)}")

        corrected_java_code = extract_java_from_markdown(raw_corrected_code)
        
        java_code = corrected_java_code
        
        plugin_dir = create_plugin_template(
            plugin_name=plugin_name,
            recommendation=recommendation,
            java_code=java_code,
            imports=imports
        )
        print(f"Re-created plugin with corrected code in: {plugin_dir}")

    else: 
        print("\nError: Max retries reached. Could not fix the plugin build.")
        return None

    if java_code and len(java_code) > 50:
        print("Java code successfully generated and injected into template")
    else:
        print("Warning: Java code may not have been properly generated")
    
    return {
        "plugin_name": plugin_name,
        "description": recommendation,
        "imports": imports
    }

def main(args):
    if hasattr(args, 'vulnerability_type') and args.vulnerability_type:
        create_plugin_workflow(args, args.vulnerability_type)
    else:
        raise ValueError("No Vulnerability Type Provided!")

if __name__ == "__main__":
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
    
    if args.list_vulnerabilities:
        from .tools import list_available_vulnerabilities
        print(list_available_vulnerabilities())
    else:
        main(args)