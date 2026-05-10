package com.waterpermit.controller;

import com.waterpermit.entity.Material;
import com.waterpermit.service.MaterialService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/materials")
public class MaterialController {

    private final MaterialService materialService;

    public MaterialController(MaterialService materialService) {
        this.materialService = materialService;
    }

    /** 材料列表 */
    @GetMapping
    public ResponseEntity<List<Material>> list() {
        return ResponseEntity.ok(materialService.listAll());
    }

    /** 材料详情 */
    @GetMapping("/{id}")
    public ResponseEntity<Material> detail(@PathVariable Long id) {
        return materialService.getById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /** 创建材料 */
    @PostMapping
    public ResponseEntity<Material> create(@RequestBody Material material) {
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
