import os
import shutil
import sys
import argparse

def to_pascal_case(snake_case_string):
    """Converts a snake_case string to PascalCase."""
    return "".join(word.capitalize() for word in snake_case_string.split('_'))

def create_plugin_template(args):
    """
    Creates a Tsunami security scanner plugin template.
    """
    plugin_name = args.plugin_name
    recommendation = args.recommendation
    java_code = getattr(args, 'java_code', None)  # Get java_code if provided
    imports = getattr(args, 'imports', [])  # Get additional imports if provided


    pascal_case_name = to_pascal_case(plugin_name)
    folder_name = f"{plugin_name}_vulnerability"
    base_path = f"tsunami-agent-plugins/{folder_name}"
    java_path = os.path.join(base_path, "src/main/java/com/google/tsunami/plugins/raid")
    gradle_wrapper_path = os.path.join(base_path, "gradle/wrapper")


    # Create directories
    os.makedirs(java_path, exist_ok=True)
    os.makedirs(gradle_wrapper_path, exist_ok=True)

    # --- File Contents ---

    build_gradle_content = f"""plugins {{
    id 'java-library'
}}

description = '{plugin_name} plugin.'
group = 'com.google.tsunami'
version = '0.0.1-SNAPSHOT'

repositories {{
    maven {{ // The google mirror is less flaky than mavenCentral()
        url 'https://maven-central.storage-download.googleapis.com/repos/central/data/'
    }}
    maven {{ // Google's Maven repository
        url 'https://maven.google.com'
    }}
    mavenCentral()
    mavenLocal()
}}

java {{
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11

    jar.manifest {{
        attributes('Implementation-Title': name,
                'Implementation-Version': version,
                'Built-By': System.getProperty('user.name'),
                'Built-JDK': System.getProperty('java.version'),
                'Source-Compatibility': sourceCompatibility,
                'Target-Compatibility': targetCompatibility)
    }}

    javadoc.options {{
        encoding = 'UTF-8'
        use = true
        links 'https://docs.oracle.com/javase/8/docs/api/'
    }}

    // Log stacktrace to console when test fails.
    test {{
        testLogging {{
            exceptionFormat = 'full'
            showExceptions true
            showCauses true
            showStackTraces true
        }}
        maxHeapSize = '1500m'
    }}
}}

ext {{
    tsunamiVersion = '0.0.29'
    junitVersion = '4.13'
    mockitoVersion = '5.12.0'
    truthVersion = '1.4.0'
    okhttpVersion = '3.12.0'
    guavaVersion = '28.2-jre'
    protobufVersion = '3.25.2'
    floggerVersion = '0.5.1'
}}

dependencies {{
    implementation "com.google.tsunami:tsunami-common:${{tsunamiVersion}}"
    implementation "com.google.tsunami:tsunami-plugin:${{tsunamiVersion}}"
    implementation "com.google.tsunami:tsunami-proto:${{tsunamiVersion}}"
    implementation "com.google.guava:guava:${{guavaVersion}}"
    implementation "com.google.protobuf:protobuf-java:${{protobufVersion}}"
    implementation "com.google.flogger:flogger:${{floggerVersion}}"
    implementation "com.google.flogger:flogger-system-backend:${{floggerVersion}}"

    testImplementation "com.google.tsunami:tsunami-plugin-testing:${{tsunamiVersion}}"
    testImplementation "junit:junit:${{junitVersion}}"
    testImplementation "org.mockito:mockito-core:${{mockitoVersion}}"
    testImplementation "com.google.truth:truth:${{truthVersion}}"
    testImplementation "com.google.truth.extensions:truth-java8-extension:${{truthVersion}}"
    testImplementation "com.google.truth.extensions:truth-proto-extension:${{truthVersion}}"
    testImplementation "com.squareup.okhttp3:mockwebserver:${{okhttpVersion}}"
}}
"""

    settings_gradle_content = f"rootProject.name = '{plugin_name}'"

    # Generate additional imports if provided
    additional_imports = ""
    if imports:
        # Filter out duplicates and standard imports that are already included
        standard_imports = {
            "com.google.common.base.Preconditions",
            "com.google.common.collect.ImmutableList",
            "com.google.common.flogger.GoogleLogger",
            "com.google.inject.Inject",
            "com.google.protobuf.util.Timestamps",
            "com.google.protobuf.ByteString",
            "com.google.tsunami.common.net.http.HttpClient",
            "com.google.tsunami.common.net.http.HttpResponse",
            "com.google.tsunami.common.net.http.HttpRequest",
            "com.google.tsunami.common.data.NetworkServiceUtils",
            "com.google.tsunami.common.time.UtcClock",
            "com.google.tsunami.plugin.annotations.PluginInfo",
            "com.google.tsunami.plugin.PluginType",
            "com.google.tsunami.plugin.VulnDetector",
            "com.google.tsunami.proto.DetectionReport",
            "com.google.tsunami.proto.DetectionReportList",
            "com.google.tsunami.proto.DetectionStatus",
            "com.google.tsunami.proto.NetworkService",
            "com.google.tsunami.proto.Severity",
            "com.google.tsunami.proto.TargetInfo",
            "com.google.tsunami.proto.Vulnerability",
            "com.google.tsunami.proto.VulnerabilityId",
            "com.google.tsunami.common.net.http.HttpHeaders",
            "java.io.IOException",
            "java.net.URLEncoder",
            "java.nio.charset.StandardCharsets",
            "java.time.Instant",
            "java.time.Clock",
            "java.util.regex.Pattern",
            "java.util.regex.Matcher"
        }
        
        unique_imports = []
        for imp in imports:
            if imp not in standard_imports and imp not in unique_imports:
                unique_imports.append(imp)
        
        if unique_imports:
            additional_imports = "\n" + "\n".join(f"import {imp};" for imp in unique_imports)

    # Generate the isServiceVulnerable method
    if java_code:
        # Use the provided Java code
        is_service_vulnerable_method = java_code
    else:
        # Use default template
        is_service_vulnerable_method = """private boolean isServiceVulnerable(NetworkService networkService) {
    // TODO: Implement vulnerability detection logic here.
    return false;
  }"""

    detector_java_content = f"""/*
 * Copyright 2024 Lukas Pirch
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.google.tsunami.plugins.raid;

import static com.google.common.base.Preconditions.checkNotNull;
import static com.google.common.collect.ImmutableList.toImmutableList;
import static java.lang.String.format;

import com.google.common.collect.ImmutableList;
import com.google.common.flogger.GoogleLogger;
import com.google.inject.Inject;
import com.google.protobuf.util.Timestamps;
import com.google.protobuf.ByteString;
import com.google.tsunami.common.net.http.HttpClient;
import com.google.tsunami.common.net.http.HttpResponse;
import com.google.tsunami.common.net.http.HttpRequest;
import com.google.tsunami.common.data.NetworkServiceUtils;
import com.google.tsunami.common.time.UtcClock;
import com.google.tsunami.plugin.annotations.PluginInfo;
import com.google.tsunami.plugin.PluginType;
import com.google.tsunami.plugin.VulnDetector;
import com.google.tsunami.proto.DetectionReport;
import com.google.tsunami.proto.DetectionReportList;
import com.google.tsunami.proto.DetectionStatus;
import com.google.tsunami.proto.NetworkService;
import com.google.tsunami.proto.Severity;
import com.google.tsunami.proto.TargetInfo;
import com.google.tsunami.proto.Vulnerability;
import com.google.tsunami.proto.VulnerabilityId;
import com.google.tsunami.common.net.http.HttpHeaders;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.time.Clock;
import java.util.regex.Pattern;
import java.util.regex.Matcher;{additional_imports}

@PluginInfo(
    type = PluginType.VULN_DETECTION,
    name = "{pascal_case_name}Detector",
    version = "0.1",
    description = "Detects {plugin_name} vulnerability.",
    author = "Joscha, Elena the Debug Dingos",
    bootstrapModule = {pascal_case_name}DetectorBootstrapModule.class)
public final class {pascal_case_name}Detector implements VulnDetector {{
  private static final GoogleLogger logger = GoogleLogger.forEnclosingClass();
  private final HttpClient httpClient;
  private final Clock utcClock;
  private String token = "";

  @Inject
  public {pascal_case_name}Detector(HttpClient httpClient, @UtcClock Clock utcClock) {{
    this.httpClient = httpClient;
    this.utcClock = checkNotNull(utcClock);
  }}

  @Override
  public DetectionReportList detect(
      TargetInfo targetInfo, ImmutableList<NetworkService> matchedServices) {{
    logger.atInfo().log("Starting detection for {pascal_case_name} Detector");
    return DetectionReportList.newBuilder()
        .addAllDetectionReports(
            matchedServices.stream()
                .filter(this::isServiceVulnerable)
                .map(networkService -> buildDetectionReport(targetInfo, networkService))
                .collect(toImmutableList()))
        .build();
  }}

  {is_service_vulnerable_method}

  private DetectionReport buildDetectionReport(
      TargetInfo targetInfo, NetworkService vulnerableNetworkService) {{
    return DetectionReport.newBuilder()
        .setTargetInfo(targetInfo)
        .setNetworkService(vulnerableNetworkService)
        .setDetectionTimestamp(
            Timestamps.fromMillis(Instant.now(utcClock).toEpochMilli()))
        .setDetectionStatus(DetectionStatus.VULNERABILITY_VERIFIED)
        .setVulnerability(
            Vulnerability.newBuilder()
                .setMainId(
                    VulnerabilityId.newBuilder()
                        .setPublisher("TSUNAMI_COMMUNITY")
                        .setValue("{plugin_name.upper()}_VULNERABILITY"))
                .setSeverity(Severity.CRITICAL)
                .setTitle("{plugin_name.replace("_", " ")} Vulnerability Exposed")
                .setDescription("The application is vulnerable to {plugin_name} attacks.")
                .setRecommendation(
                    "{recommendation}"))
        .build();
  }}
  
  public ImmutableList<Vulnerability> getAdvisories() {{
    return ImmutableList.of(
        Vulnerability.newBuilder()
            .setMainId(
                VulnerabilityId.newBuilder()
                    .setPublisher("TSUNAMI_COMMUNITY")
                    .setValue("{plugin_name.upper()}_VULNERABILITY"))
            .setSeverity(Severity.CRITICAL)
            .setTitle("{plugin_name.replace("_", " ")} Vulnerability Exposed")
            .setDescription(
                "The application is vulnerable to {plugin_name} attacks.")
            .setRecommendation(
                "{recommendation}")
        .build());
  }}
}}
"""

    bootstrap_module_content = f"""/*
 * Copyright 2024 Lukas Pirch
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.google.tsunami.plugins.raid;

import com.google.tsunami.plugin.PluginBootstrapModule;

/** A {{@link PluginBootstrapModule}} for the {pascal_case_name} Plugin. */
public final class {pascal_case_name}DetectorBootstrapModule extends PluginBootstrapModule {{
  @Override
  protected void configurePlugin() {{
    registerPlugin({pascal_case_name}Detector.class);
  }}
}}
"""

    

    gradle_wrapper_properties_content = r"""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.14-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""

    # --- Write/Copy Files ---

    # build.gradle
    with open(os.path.join(base_path, "build.gradle"), "w") as f:
        f.write(build_gradle_content.strip())

    # settings.gradle
    with open(os.path.join(base_path, "settings.gradle"), "w") as f:
        f.write(settings_gradle_content)

    # Detector.java
    with open(os.path.join(java_path, f"{pascal_case_name}Detector.java"), "w") as f:
        f.write(detector_java_content.strip())

    # BootstrapModule.java
    with open(os.path.join(java_path, f"{pascal_case_name}DetectorBootstrapModule.java"), "w") as f:
        f.write(bootstrap_module_content.strip())

    # gradlew
    shutil.copy("example_plugins/sql_injection_template/gradlew", base_path)
    os.chmod(os.path.join(base_path, "gradlew"), 0o755)


    # gradle-wrapper.properties
    with open(os.path.join(gradle_wrapper_path, "gradle-wrapper.properties"), "w") as f:
        f.write(gradle_wrapper_properties_content)

    # gradle-wrapper.jar
    shutil.copy("example_plugins/sql_injection_template/gradle/wrapper/gradle-wrapper.jar", gradle_wrapper_path)


    print(f"Successfully created plugin template '{plugin_name}' in '{base_path}'")
    return base_path


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: python templater.py <plugin_name>")
    #     sys.exit(1)
    parser = argparse.ArgumentParser(description="Tsunami Agent Templater")
    # plugin_name_arg = sys.argv[1]
    parser.add_argument(
        "--plugin-name",
        type=str,
        default="example_injection",
        help="Vulnerability Name. Must use _ e.g. 'sql_injection'"
    )
    parser.add_argument(
        "--recommendation",
        type=str,
        default="This is an example recommendation: Implement this for real and don't only implement the boilerplate.",
        help="Insightful recommendation on how to avoid the detected vulnerability effectively"
    )

    create_plugin_template(parser.parse_args())
