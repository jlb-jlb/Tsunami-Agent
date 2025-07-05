#!/usr/bin/env python3
"""
Test the improved templater with direct Java code injection
"""

import os
import sys

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tsunami_agent.tools import create_plugin_template

def test_templater_injection():
    """Test the templater with direct Java code injection"""
    print("Testing templater with Java code injection...")
    
    # Sample Java code to inject
    sample_java_code = """private boolean isServiceVulnerable(NetworkService networkService) {
    String targetUri = NetworkServiceUtils.buildWebApplicationRootUrl(networkService);
    try {
      // Test for XSS vulnerability
      String xssPayload = "<script>alert('xss')</script>";
      String encodedPayload = URLEncoder.encode(xssPayload, StandardCharsets.UTF_8);
      
      String testUrl = targetUri + "/search?q=" + encodedPayload;
      HttpRequest request = HttpRequest.get(testUrl).withEmptyHeaders().build();
      HttpResponse response = httpClient.send(request, networkService);
      
      if (response.status().isSuccess() && 
          response.bodyString().isPresent() && 
          response.bodyString().get().contains(xssPayload)) {
        return true;
      }
      
      return false;
    } catch (IOException e) {
      logger.atWarning().log("XSS test failed on '%s': %s", networkService, e.getMessage());
      return false;
    }
  }"""
    
    # Test creating template with injected code
    result = create_plugin_template(
        plugin_name="test_xss_injection",
        recommendation="Implement proper input validation and output encoding to prevent XSS attacks.",
        java_code=sample_java_code
    )
    
    print(f"Template creation result: {result}")
    
    # Check if the plugin was created with the injected code
    plugin_dir = "tsunami-agent-plugins/test_xss_injection_vulnerability"
    java_file = f"{plugin_dir}/src/main/java/com/google/tsunami/plugins/raid/TestXssInjectionDetector.java"
    
    if os.path.exists(java_file):
        print(f"✓ Plugin file created: {java_file}")
        
        with open(java_file, 'r') as f:
            content = f.read()
            if "alert('xss')" in content:
                print("✓ Java code successfully injected into template")
                print("✓ Test passed!")
                return True
            else:
                print("✗ Java code not found in template")
                return False
    else:
        print(f"✗ Plugin file not created: {java_file}")
        return False

if __name__ == "__main__":
    test_templater_injection()
