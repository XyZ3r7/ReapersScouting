package com.reapers.reapersScouting.repository;

import com.reapers.reapersScouting.model.ScoutingReport;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ReportRepository extends JpaRepository<ScoutingReport, Long> {
    List<ScoutingReport> findByTeamNumberOrderByCreatedAtDesc(String teamNumber);
}