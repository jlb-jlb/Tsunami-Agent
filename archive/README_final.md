# Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd tsunami-agent
```

### 2. Install Dependencies
```bash
# first, make sure poetry is installed 
    # curl -sSL https://install.python-poetry.org | python3 -
    # export PATH="/home/{user}/.local/bin:$PATH"
poetry install
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys:
# ANTHROPIC_API_KEY=your_anthropic_key_here
# OPENAI_API_KEY=your_openai_key_here
```

### 4. Verify Installation
```bash
poetry run python cli.py --list-vulnerabilities
```

# Quick Start

### Generate a Plugin

```bash
# Generate SQL injection detection plugin
poetry run python cli.py -v sql_injection

# Generate XSS detection plugin with specific model
poetry run python cli.py -v xss -m gpt-4 -p openai
```
### Build & Run the Plugins

```bash
# builds the plugins
# runs tsunami
# fetches tokens
python solution.py
```

# Project Structure

```
tsunami-agent/
├── src/tsunami_agent/           # Core agent implementation
│   ├── main.py                  # Main workflow and LLM orchestration
│   ├── tools.py                 # LangChain tools and utilities
│   └── templater.py             # Plugin template generation
├── vulnerabilities/             # Vulnerability descriptions (14 types)
├── example_plugins/             # Reference implementations
├── tsunami-agent-plugins/       # Generated plugin output
├── cli.py                       # Command-line interface
└── tests/                       # Test suite
```

