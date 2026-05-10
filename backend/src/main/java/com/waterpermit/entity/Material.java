package com.waterpermit.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "materials")
public class Material {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "applicant_id")
    private User applicant;

    @Column(nullable = false, length = 200)
    private String title;

    @Enumerated(EnumType.STRING)
    private MaterialStatus status = MaterialStatus.DRAFT;

    @Column(length = 200)
    private String projectName;

    @Column(length = 200)
    private String waterIntakeLocation;

    @Column(length = 100)
    private String waterIntakePurpose;

    @Column(precision = 15, scale = 2)
    private BigDecimal annualWaterVolume;

    @Column(length = 200)
    private String applicantCompany;

    @Column(length = 50)
    private String applicantLegalPerson;

    @Column(length = 50)
    private String businessLicenseNo;

    @Column(length = 20)
    private String contactPhone;

    @Column(length = 500)
    private String applicationFormPath;

    @Column(length = 500)
    private String businessLicensePath;

    @Column(length = 500)
    private String idCardPath;

    @Column(length = 500)
    private String waterCertificatePath;

    @Column(columnDefinition = "TEXT")
    private String otherFilesPath;

    private LocalDateTime submitTime;
    private LocalDateTime reviewTime;

    @Column(updatable = false)
    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    public enum MaterialStatus {
        DRAFT, SUBMITTED, REVIEWING, APPROVED, REJECTED
    }
}
