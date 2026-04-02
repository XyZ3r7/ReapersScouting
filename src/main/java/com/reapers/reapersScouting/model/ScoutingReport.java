package com.reapers.reapersScouting.model;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Data
public class ScoutingReport {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String teamNumber;
    private String matchNumber;

    // Auton
    private String shootingRange;
    private Integer artifactsCount;

    // Teleop
    private Integer maxScoreNoPattern;
    private Integer maxScoreWithPattern;
    private String needsHumanPlayer;

    // Endgame
    private String hasLifting;

    @Column(columnDefinition = "TEXT")
    private String notes;

    private LocalDateTime createdAt;
}