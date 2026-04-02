package com.reapers.reapersScouting.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;
import java.util.*;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.util.stream.Collectors;

@Service
public class FtcApiService {
    private final String AUTH_TOKEN = "";
    private final String USERNAME = "reapers";
    private final String BASE_URL = "https://ftc-api.firstinspires.org/v2.0/2025";

    private HttpHeaders getHeaders() {
        HttpHeaders headers = new HttpHeaders();
        String auth = USERNAME + ":" + AUTH_TOKEN;
        String encodedAuth = Base64.getEncoder().encodeToString(auth.getBytes(StandardCharsets.UTF_8));
        headers.set("Authorization", "Basic " + encodedAuth);
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
        headers.add("User-Agent", "Mozilla/5.0");
        return headers;
    }

    public List<Map<String, Object>> getRecentEvents() {
        RestTemplate restTemplate = new RestTemplate();
        try {
            String url = BASE_URL + "/events";
            ResponseEntity<Map> response = restTemplate.exchange(url, HttpMethod.GET, new HttpEntity<>(getHeaders()), Map.class);
            List<Map<String, Object>> events = (List<Map<String, Object>>) response.getBody().get("events");

            LocalDateTime now = LocalDateTime.now();
            LocalDateTime limit = now.plusHours(24);

            return events.stream()
                    .filter(e -> {
                        String dateStr = (String) e.get("dateStart");
                        LocalDateTime eventDate = LocalDateTime.parse(dateStr);
                        // Keep all past events, but hide those more than 24h in the future
                        return eventDate.isBefore(limit);
                    })
                    // Sort by date descending: Newest/Upcoming at the top, followed by past events
                    .sorted((e1, e2) -> ((String) e2.get("dateStart")).compareTo((String) e1.get("dateStart")))
                    .collect(Collectors.toList());
        } catch (Exception e) {
            System.err.println("API Error: " + e.getMessage());
            return new ArrayList<>();
        }
    }

    public Object getMatchesByEvent(String eventCode) {
        RestTemplate restTemplate = new RestTemplate();
        String url = BASE_URL + "/matches/" + eventCode;
        try {
            return restTemplate.exchange(url, HttpMethod.GET, new HttpEntity<>(getHeaders()), Object.class).getBody();
        } catch (Exception e) {
            return Collections.singletonMap("error", e.getMessage());
        }
    }
}