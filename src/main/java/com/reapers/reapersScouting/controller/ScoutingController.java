package com.reapers.reapersScouting.controller;

import com.reapers.reapersScouting.model.ScoutingReport;
import com.reapers.reapersScouting.repository.ReportRepository;
import com.reapers.reapersScouting.service.FtcApiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class ScoutingController {

    @Autowired
    private FtcApiService ftcApiService;

    @Autowired
    private ReportRepository reportRepository;

    @GetMapping("/test-api")
    public List<Map<String, Object>> testApi() {
        return ftcApiService.getRecentEvents();
    }

    @GetMapping("/matches/{eventCode}")
    public Object getMatches(@PathVariable String eventCode) {
        return ftcApiService.getMatchesByEvent(eventCode);
    }

    @PostMapping("/reports")
    public ScoutingReport saveReport(@RequestBody ScoutingReport report) {
        report.setCreatedAt(LocalDateTime.now(ZoneId.of("America/New_York")));
        return reportRepository.save(report);
    }

    @GetMapping("/reports/{teamNumber}")
    public List<ScoutingReport> getReports(@PathVariable String teamNumber) {
        return reportRepository.findByTeamNumberOrderByCreatedAtDesc(teamNumber);
    }
}