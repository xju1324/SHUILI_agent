package com.waterpermit.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

/**
 * 调用 Python AI 服务的 HTTP 客户端
 */
@Service
public class AIServiceClient {

    private final RestTemplate restTemplate;

    @Value("${ai-service.base-url}")
    private String aiBaseUrl;

    public AIServiceClient() {
        this.restTemplate = new RestTemplate();
    }

    /**
     * 提交材料给AI进行审查
     */
    public Map<String, Object> submitForReview(Long materialId, Map<String, Object> materialData) {
        String url = aiBaseUrl + "/api/review";
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        materialData.put("material_id", materialId);
        HttpEntity<Map<String, Object>> request = new HttpEntity<>(materialData, headers);
        return restTemplate.postForObject(url, request, Map.class);
    }

    /**
     * 检查AI服务健康状态
     */
    public boolean isAIServiceAvailable() {
        try {
            String url = aiBaseUrl + "/health";
            Map<String, Object> response = restTemplate.getForObject(url, Map.class);
            return response != null && "ok".equals(response.get("status"));
        } catch (Exception e) {
            return false;
        }
    }
}
