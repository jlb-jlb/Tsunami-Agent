from pydantic import BaseModel

class PluginImplementation(BaseModel):
    """
    Structured data model for a Tsunami plugin's components.
    This is used by the tool-calling agent to structure its output.
    """
    vulnerability_type: str
    plugin_name: str
    description: str
    recommendation: str
    endpoints: list[str]
    payloads: list[str]
    imports: list[str] 
    java_code: str
