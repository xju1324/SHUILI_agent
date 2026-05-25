package com.watersupervision.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.watersupervision.entity.Material;
import com.watersupervision.entity.ReviewRecord;
import com.watersupervision.repository.MaterialRepository;
import com.watersupervision.repository.ReviewRecordRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.*;

@Service
public class MaterialService {

    private static final Logger log = LoggerFactory.getLogger(MaterialService.class);

    private final MaterialRepository materialRepository;
    private final ReviewRecordRepository reviewRecordRepository;
    private final AIServiceClient aiServiceClient;
    private final ObjectMapper objectMapper;
    private final Path uploadDir = Paths.get("./uploads").toAbsolutePath().normalize();

    public MaterialService(MaterialRepository materialRepository,
                           ReviewRecordRepository reviewRecordRepository,
                           AIServiceClient aiServiceClient,
                           ObjectMapper objectMapper) {
        this.materialRepository = materialRepository;
        this.reviewRecordRepository = reviewRecordRepository;
        this.aiServiceClient = aiServiceClient;
        this.objectMapper = objectMapper;
        try {
            Files.createDirectories(uploadDir);
        } catch (IOException e) {
            throw new RuntimeException("无法创建上传目录", e);
        }
    }

    public List<Material> listAll() {
        return materialRepository.findAll();
    }

    public List<Material> listByApplicant(Long applicantId) {
        return materialRepository.findByApplicantIdOrderByCreatedAtDesc(applicantId);
    }

    public Optional<Material> getById(Long id) {
        return materialRepository.findById(id);
    }

    @Transactional
    public Material create(Material material) {
        material.setStatus(Material.MaterialStatus.DRAFT);
        return materialRepository.save(material);
    }

    @Transactional
    public Material update(Long id, Material update) {
        Material existing = materialRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("材料不存在: " + id));
        existing.setTitle(update.getTitle());
        existing.setCategory(update.getCategory());
        existing.setProjectName(update.getProjectName());
        existing.setWaterIntakeLocation(update.getWaterIntakeLocation());
        existing.setWaterIntakePurpose(update.getWaterIntakePurpose());
        existing.setAnnualWaterVolume(update.getAnnualWaterVolume());
        existing.setApplicantCompany(update.getApplicantCompany());
        existing.setApplicantLegalPerson(update.getApplicantLegalPerson());
        existing.setBusinessLicenseNo(update.getBusinessLicenseNo());
        existing.setContactPhone(update.getContactPhone());
        existing.setApplicationFormPath(update.getApplicationFormPath());
        existing.setBusinessLicensePath(update.getBusinessLicensePath());
        existing.setIdCardPath(update.getIdCardPath());
        existing.setWaterCertificatePath(update.getWaterCertificatePath());
        existing.setFormData(update.getFormData());
        return materialRepository.save(existing);
    }

    @Transactional
    public Material submit(Long id) {
        Material material = materialRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("材料不存在: " + id));

        // 1. 更新状态为审查中
        material.setStatus(Material.MaterialStatus.REVIEWING);
        material.setSubmitTime(LocalDateTime.now());
        material = materialRepository.save(material);

        // 2. 构建材料数据 Map 并调用 AI 服务
        Map<String, Object> materialData = buildMaterialDataMap(material);

        try {
            log.info("调用AI审核服务, materialId={}, category={}", id, material.getCategory());
            Map<String, Object> aiResponse = aiServiceClient.submitForReview(id, materialData);

            // 3. 解析AI审核结果，创建 ReviewRecord
            if (aiResponse != null) {
                parseAndSaveReviewResults(material, aiResponse);
            }

            // 4. 根据审核记录判断最终状态
            List<ReviewRecord> records = reviewRecordRepository.findByMaterialIdOrderByReviewedAtDesc(id);
            boolean hasErrors = records.stream()
                    .anyMatch(r -> r.getSeverity() == ReviewRecord.Severity.ERROR
                            && Boolean.FALSE.equals(r.getIsPass()));
            material.setReviewTime(LocalDateTime.now());
            if (hasErrors) {
                material.setStatus(Material.MaterialStatus.REJECTED);
            } else {
                material.setStatus(Material.MaterialStatus.APPROVED);
            }
            material = materialRepository.save(material);
            log.info("AI审核完成, materialId={}, status={}, records={}", id, material.getStatus(), records.size());

        } catch (Exception e) {
            log.error("AI审核失败, materialId={}, error={}", id, e.getMessage(), e);
            material.setStatus(Material.MaterialStatus.SUBMITTED);
            material.setReviewTime(null);
            material = materialRepository.save(material);
        }

        return material;
    }

    /**
     * 将 Material 实体转换为 AI 服务需要的 Map
     */
    private Map<String, Object> buildMaterialDataMap(Material m) {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("material_id", m.getId());
        data.put("category", m.getCategory() != null ? m.getCategory().name() : "WATER_INTAKE");
        data.put("title", m.getTitle());
        data.put("projectName", m.getProjectName());
        data.put("applicantCompany", m.getApplicantCompany());
        data.put("applicantLegalPerson", m.getApplicantLegalPerson());
        data.put("businessLicenseNo", m.getBusinessLicenseNo());
        data.put("contactPhone", m.getContactPhone());
        data.put("waterIntakeLocation", m.getWaterIntakeLocation());
        data.put("waterIntakePurpose", m.getWaterIntakePurpose());
        if (m.getAnnualWaterVolume() != null) {
            data.put("annualWaterVolume", m.getAnnualWaterVolume().doubleValue());
        }
        data.put("applicationFormPath", m.getApplicationFormPath());
        data.put("businessLicensePath", m.getBusinessLicensePath());
        data.put("idCardPath", m.getIdCardPath());
        data.put("waterCertificatePath", m.getWaterCertificatePath());

        if (m.getFormData() != null && !m.getFormData().isBlank()) {
            try {
                Map<String, Object> formFields = objectMapper.readValue(m.getFormData(),
                        new TypeReference<Map<String, Object>>() {});
                data.putAll(formFields);
            } catch (Exception e) {
                log.warn("解析 formData 失败: {}", e.getMessage());
            }
        }
        return data;
    }

    /**
     * 解析AI审核报告，创建审核记录
     */
    private void parseAndSaveReviewResults(Material material, Map<String, Object> aiResponse) {
        // Python API 返回字段为 review_result
        Object reviewTextObj = aiResponse.get("review_result");
        if (reviewTextObj == null) {
            reviewTextObj = aiResponse.get("review_report");
        }
        if (reviewTextObj == null) {
            reviewTextObj = aiResponse.get("output");
        }
        if (reviewTextObj == null) {
            try {
                reviewTextObj = objectMapper.writeValueAsString(aiResponse);
            } catch (Exception e) {
                reviewTextObj = "审核报告解析失败";
            }
        }
        String reviewText = String.valueOf(reviewTextObj);
        log.info("收到AI审核报告, length={}", reviewText.length());

        // 按照标记解析审核结果
        int parsed = 0;
        parsed += parseReviewLines(material, reviewText, "不合规项", "❌", false, ReviewRecord.ReviewType.COMPLIANCE);
        parsed += parseReviewLines(material, reviewText, "需关注项", "⚠", null, ReviewRecord.ReviewType.DATA_STANDARD);
        parsed += parseReviewLines(material, reviewText, "合规项", "✅", true, ReviewRecord.ReviewType.COMPLIANCE);
        // 解析完整性检查缺失项
        parsed += parseCompletenessRecords(material, reviewText);

        // 如果没有解析到任何记录，保存完整报告摘要
        if (parsed == 0) {
            ReviewRecord summary = new ReviewRecord();
            summary.setMaterial(material);
            summary.setReviewType(ReviewRecord.ReviewType.COMPLIANCE);
            int maxLen = Math.min(reviewText.length(), 4000);
            summary.setIssueDescription(reviewText.substring(0, maxLen)
                    + (reviewText.length() > 4000 ? "..." : ""));
            summary.setSeverity(ReviewRecord.Severity.INFO);
            summary.setIsPass(true);
            reviewRecordRepository.save(summary);
        }
    }

    private int parseReviewLines(Material material, String text, String issueCategory,
                                  String marker, Boolean isPass, ReviewRecord.ReviewType reviewType) {
        int count = 0;
        for (String line : text.split("\n")) {
            if (line.contains(marker)) {
                String cleaned = line.replaceAll("^[\\s\\-\\d.、•*·]+", "").trim();
                if (cleaned.length() > 8 && cleaned.length() < 500) {
                    ReviewRecord record = new ReviewRecord();
                    record.setMaterial(material);
                    record.setReviewType(reviewType);
                    record.setIsPass(isPass);
                    record.setIssueCategory(issueCategory);
                    record.setIssueDescription(cleaned);
                    if (isPass == Boolean.FALSE) {
                        record.setSeverity(ReviewRecord.Severity.ERROR);
                    } else if (isPass == null) {
                        record.setSeverity(ReviewRecord.Severity.WARNING);
                    } else {
                        record.setSeverity(ReviewRecord.Severity.INFO);
                    }
                    reviewRecordRepository.save(record);
                    count++;
                }
            }
        }
        return count;
    }

    private int parseCompletenessRecords(Material material, String text) {
        int count = 0;
        boolean inSection = false;
        for (String line : text.split("\n")) {
            if (line.contains("完整性检查") || line.contains("完整性")) {
                inSection = true;
                continue;
            }
            if (line.contains("法规检索") || line.contains("合规性评估") || line.contains("审查结论")) {
                inSection = false;
                continue;
            }
            if (inSection && (line.contains("缺失") || line.contains("缺少"))) {
                String cleaned = line.replaceAll("^[\\s\\-\\d.、•*·]+", "").trim();
                if (cleaned.length() > 5 && cleaned.length() < 300) {
                    ReviewRecord record = new ReviewRecord();
                    record.setMaterial(material);
                    record.setReviewType(ReviewRecord.ReviewType.FORMAT);
                    record.setIsPass(false);
                    record.setIssueCategory("完整性检查");
                    record.setIssueDescription(cleaned);
                    record.setSeverity(ReviewRecord.Severity.WARNING);
                    reviewRecordRepository.save(record);
                    count++;
                }
            }
        }
        return count;
    }

    public String uploadFile(MultipartFile file) {
        String originalName = file.getOriginalFilename();
        String storedName = UUID.randomUUID() + "_" + (originalName != null ? originalName : "file");
        try {
            Files.createDirectories(uploadDir);
            Path target = uploadDir.resolve(storedName);
            file.transferTo(target.toFile());
            return storedName;
        } catch (IOException e) {
            throw new RuntimeException("文件上传失败", e);
        }
    }

    @Transactional
    public void delete(Long id) {
        materialRepository.deleteById(id);
    }
}