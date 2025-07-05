#!/usr/bin/env python3
"""
Test the complete workflow with a manual example
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tsunami_agent.main import PluginImplementation
from tsunami_agent.tools import create_plugin_template

def test_complete_workflow():
    """Test the complete workflow with predefined data"""
    print("Testing complete workflow with manual Java code...")
    
    # Create a complete Java method implementation
    java_code = """private boolean isServiceVulnerable(NetworkService networkService) {
    String baseUri = NetworkServiceUtils.buildWebApplicationRootUrl(networkService);
    
    try {
        // Test for broken access control - admin registration
        String registerEndpoint = baseUri + "/api/Users";
        String payload = "{\\"email\\":\\"test@test.com\\",\\"password\\":\\"test123\\",\\"role\\":\\"admin\\"}";
        
        HttpHeaders headers = HttpHeaders.builder()
            .addHeader("Content-Type", "application/json")
            .build();
            
        HttpRequest request = HttpRequest.post(registerEndpoint)
            .setHeaders(headers)
            .setRequestBody(HttpRequestBody.create(payload.getBytes(StandardCharsets.UTF_8)))
            .build();
            
        HttpResponse response = httpClient.send(request, networkService);
        
        // If registration succeeds with admin role, it's vulnerable
        if (response.status().isSuccess() && 
            response.bodyString().isPresent() && 
            response.bodyString().get().contains("admin")) {
            return true;
        }
        
        // Test admin page access without authentication
        String adminUrl = baseUri + "/#/administration";
        HttpRequest adminRequest = HttpRequest.get(adminUrl).withEmptyHeaders().build();
        HttpResponse adminResponse = httpClient.send(adminRequest, networkService);
        
        // If we get 200 instead of 403, it might be vulnerable
        return adminResponse.status().isSuccess();
        
    } catch (IOException e) {
        logger.atWarning().log("Broken access control test failed on '%s': %s", networkService, e.getMessage());
        return false;
    }
  }"""
    
    # Create a PluginImplementation object
    plugin_implementation = PluginImplementation(
        vulnerability_type="broken_access_control",
        plugin_name="broken_access_control_detector",
        java_code=java_code,
        description="Detects broken access control vulnerabilities by testing admin registration and page access",
        recommendation="Implement proper role-based access control, validate permissions server-side, and use secure session management",
        endpoints=["/api/Users", "/#/administration"],
        payloads=['{"email":"test@test.com","password":"test123","role":"admin"}']
    )
    
    print(f"Plugin Name: {plugin_implementation.plugin_name}")
    print(f"Description: {plugin_implementation.description}")
    
    # Create plugin template with the Java code
    template_result = create_plugin_template(
        plugin_implementation.plugin_name,
        plugin_implementation.recommendation,
        plugin_implementation.java_code
    )
    
    print(f"Template creation result: {template_result}")
    
    # Check if the plugin was created correctly
    plugin_dir = f"tsunami-agent-plugins/{plugin_implementation.plugin_name}_vulnerability"
    java_file = f"{plugin_dir}/src/main/java/com/google/tsunami/plugins/raid/BrokenAccessControlDetectorDetector.java"
    
    if os.path.exists(java_file):
        print(f"✓ Plugin file created: {java_file}")
        
        with open(java_file, 'r') as f:
            content = f.read()
            if "admin registration" in content and "test@test.com" in content:
                print("✓ Java code successfully injected into template!")
                print("✓ Complete workflow test passed!")
                
                # Show a snippet of the generated code
                print("\\nGenerated code snippet:")
                lines = content.split('\\n')
                for i, line in enumerate(lines):
                    if "isServiceVulnerable" in line:
                        print("\\n".join(lines[i:i+10]))
                        break
                        
                return True
            else:
                print("✗ Java code not properly injected")
                return False
    else:
        print(f"✗ Plugin file not created: {java_file}")
        return False

if __name__ == "__main__":
    test_complete_workflow()
