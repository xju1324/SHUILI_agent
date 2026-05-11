package com.watersupervision.service;

import com.watersupervision.entity.Material;
import com.watersupervision.repository.MaterialRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class MaterialService {

    private final MaterialRepository materialRepository;
    private final Path uploadDir = Paths.get("./uploads").toAbsolutePath().normalize();

    public MaterialService(MaterialRepository materialRepository) {
        this.materialRepository = materialRepository;
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
        existing.setProjectName(update.getProjectName());
        existing.setWaterIntakeLocation(update.getWaterIntakeLocation());
        existing.setWaterIntakePurpose(update.getWaterIntakePurpose());
        existing.setAnnualWaterVolume(update.getAnnualWaterVolume());
        existing.setApplicantCompany(update.getApplicantCompany());
        existing.setApplicantLegalPerson(update.getApplicantLegalPerson());
        existing.setBusinessLicenseNo(update.getBusinessLicenseNo());
        existing.setContactPhone(update.getContactPhone());
        return materialRepository.save(existing);
    }

    @Transactional
    public Material submit(Long id) {
        Material material = materialRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("材料不存在: " + id));
        material.setStatus(Material.MaterialStatus.SUBMITTED);
        material.setSubmitTime(LocalDateTime.now());
        return materialRepository.save(material);
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
