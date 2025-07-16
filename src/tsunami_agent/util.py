import re

def extract_java_from_markdown(text: str) -> str:
    """
    Extracts Java code from a markdown block if present.
    If no markdown block is found, returns the original text, stripped of whitespace.
    """
    # Pattern to find a ```java ... ``` block and capture the content
    match = re.search(r'```java\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        # Return the captured group (the code inside the block)
        return match.group(1).strip()
    else:
        # If no markdown block is found, assume the text is the code itself
        return text.strip()
