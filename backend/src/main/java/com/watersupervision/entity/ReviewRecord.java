package com.watersupervision.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "review_records")
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
public class ReviewRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "material_id", nullable = false)
    private Material material;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ReviewType reviewType;

    private Boolean isPass;

    @Column(length = 100)
    private String issueCategory;

    @Column(columnDefinition = "TEXT")
    private String issueDescription;

    @Column(columnDefinition = "TEXT")
    private String suggestion;

    @Column(length = 100)
    private String relatedField;

    @Enumerated(EnumType.STRING)
    private Severity severity = Severity.WARNING;

    @Column(precision = 3, scale = 2)
    private BigDecimal aiConfidence;

    private LocalDateTime reviewedAt;

    @PrePersist
    protected void onCreate() {
        reviewedAt = LocalDateTime.now();
    }

    public enum ReviewType {
        FORMAT, DATA_STANDARD, COMPLIANCE
    }

    public enum Severity {
        INFO, WARNING, ERROR
    }
}