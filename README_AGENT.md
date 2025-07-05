# Tsunami Security Scanner Plugin Agent

An AI-powered agent that automatically creates Tsunami Security Scanner plugins for various vulnerabilities found in OWASP Juice Shop.

## Features

- **Vulnerability Analysis**: Reads and analyzes vulnerability descriptions from markdown files
- **Plugin Generation**: Creates complete Tsunami plugin templates with Java code
- **Detection Logic**: Generates `isServiceVulnerable` method implementations
- **Multiple Vulnerabilities**: Supports SQL injection, XSS, broken access control, and more

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
# or with poetry
poetry install
```

3. Set up environment variables:
```bash
export ANTHROPIC_API_KEY="your-api-key"
# or
export OPENAI_API_KEY="your-api-key"
```

## Usage

### List Available Vulnerabilities

```bash
python -m src.tsunami_agent.main --list-vulnerabilities
```

### Create a Plugin for a Specific Vulnerability

```bash
python -m src.tsunami_agent.main --vulnerability-type sql_injection
```

### Use Different Models

```bash
# Use OpenAI GPT-4
python -m src.tsunami_agent.main --model-provider openai --model gpt-4 --vulnerability-type xss

# Use Anthropic Claude (default)
python -m src.tsunami_agent.main --model-provider anthropic --model claude-sonnet-4-20250514 --vulnerability-type broken_access_control
```

## Available Vulnerability Types

- `sql_injection`
- `xss`
- `broken_access_control`
- `broken_authentication`
- `directory_traversal`
- `file_upload`
- `improper_input_validation`
- `insecure_deserialization`
- `sensitive_data_exposure`
- `server_side_request_forgery`
- `unvalidated_redirects`
- `vulnerable_components`
- `weak_password`
- `xml_external_entity_xxe_injection`

## How It Works

1. **Vulnerability Reading**: The agent reads vulnerability descriptions from markdown files in the `vulnerabilities/` directory
2. **Analysis**: It analyzes the vulnerability information to extract:
   - Vulnerable endpoints
   - Attack parameters
   - Payload patterns
   - Detection methods
3. **Code Generation**: Creates Java code for the `isServiceVulnerable` method that can detect the vulnerability
4. **Template Creation**: Uses the templater to create a complete plugin structure
5. **Code Injection**: Injects the generated detection logic into the template

## Example Workflow

```bash
# Create a SQL injection plugin
python -m src.tsunami_agent.main --vulnerability-type sql_injection
```

This will:
1. Read `vulnerabilities/sql_injection_vulnerabilities.md`
2. Analyze the vulnerability patterns
3. Generate Java detection code
4. Create a plugin template in `tsunami-agent-plugins/sql_injection_vulnerability/`
5. Inject the detection logic into the template

## Generated Plugin Structure

```
tsunami-agent-plugins/
└── sql_injection_vulnerability/
    ├── build.gradle
    ├── settings.gradle
    ├── gradlew
    ├── gradle/
    │   └── wrapper/
    └── src/
        └── main/
            └── java/
                └── com/
                    └── google/
                        └── tsunami/
                            └── plugins/
                                └── raid/
                                    ├── SqlInjectionDetector.java
                                    └── SqlInjectionDetectorBootstrapModule.java
```

## Testing

Run the test script to verify functionality:

```bash
python test_agent.py
```

## Architecture

- **main.py**: Main application entry point and workflow orchestration
- **tools.py**: LangChain tools for file reading, analysis, and template generation
- **templater.py**: Plugin template generator
- **vulnerabilities/**: Vulnerability descriptions and solutions

## Contributing

1. Add new vulnerability descriptions to the `vulnerabilities/` directory
2. Follow the existing markdown format
3. Test the agent with your new vulnerability type
4. Submit a pull request

## License

Licensed under the Apache License, Version 2.0
