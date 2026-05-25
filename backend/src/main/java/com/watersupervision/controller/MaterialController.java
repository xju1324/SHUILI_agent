package com.watersupervision.controller;

import com.watersupervision.entity.Material;
import com.watersupervision.entity.ReviewRecord;
import com.watersupervision.entity.User;
import com.watersupervision.repository.ReviewRecordRepository;
import com.watersupervision.repository.UserRepository;
import com.watersupervision.service.MaterialService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.*;

@RestController
@RequestMapping("/api/materials")
public class MaterialController {

    private final MaterialService materialService;
    private final ReviewRecordRepository reviewRecordRepository;
    private final UserRepository userRepository;

    public MaterialController(MaterialService materialService,
                              ReviewRecordRepository reviewRecordRepository,
                              UserRepository userRepository) {
        this.materialService = materialService;
        this.reviewRecordRepository = reviewRecordRepository;
        this.userRepository = userRepository;
    }

    /** 材料列表 */
    @GetMapping
    public ResponseEntity<List<Material>> list() {
        return ResponseEntity.ok(materialService.listAll());
    }

    /** 我的材料 */
    @GetMapping("/my")
    public ResponseEntity<List<Material>> myMaterials(HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ResponseEntity.ok(materialService.listByApplicant(userId));
    }

    /** 材料详情（含审核记录） */
    @GetMapping("/{id}")
    public ResponseEntity<Map<String, Object>> detail(@PathVariable Long id) {
        return materialService.getById(id)
                .map(material -> {
                    Map<String, Object> result = new LinkedHashMap<>();
                    result.put("material", material);
                    List<ReviewRecord> records = reviewRecordRepository
                            .findByMaterialIdOrderByReviewedAtDesc(id);
                    result.put("reviewRecords", records);
                    return ResponseEntity.ok(result);
                })
                .orElse(ResponseEntity.notFound().build());
    }

    /** 获取某材料的审核记录 */
    @GetMapping("/{id}/reviews")
    public ResponseEntity<List<ReviewRecord>> reviews(@PathVariable Long id) {
        return ResponseEntity.ok(
                reviewRecordRepository.findByMaterialIdOrderByReviewedAtDesc(id));
    }

    /** 创建材料 */
    @PostMapping
    public ResponseEntity<Material> create(@RequestBody Material material, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        if (userId != null) {
            User user = userRepository.findById(userId).orElse(null);
            material.setApplicant(user);
        }
        return ResponseEntity.ok(materialService.create(material));
    }

    /** 更新材料 */
    @PutMapping("/{id}")
    public ResponseEntity<Material> update(@PathVariable Long id, @RequestBody Material material) {
        return ResponseEntity.ok(materialService.update(id, material));
    }

    /** 删除材料 */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        materialService.delete(id);
        return ResponseEntity.noContent().build();
    }

    /** 提交材料进行审查 */
    @PostMapping("/{id}/submit")
    public ResponseEntity<Material> submit(@PathVariable Long id) {
        return ResponseEntity.ok(materialService.submit(id));
    }

    /** 文件上传 */
    @PostMapping("/upload")
    public ResponseEntity<Map<String, String>> upload(@RequestParam("file") MultipartFile file) {
        String filename = materialService.uploadFile(file);
        Map<String, String> result = new HashMap<>();
        result.put("filename", filename);
        result.put("message", "上传成功");
        return ResponseEntity.ok(result);
    }
}