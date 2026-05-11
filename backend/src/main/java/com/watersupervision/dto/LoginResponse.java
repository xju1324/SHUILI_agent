package com.watersupervision.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
public class LoginResponse {
    private String token;
    private Long userId;
    private String username;
    private String realName;
    private String role;
    private String email;
    private String phone;

    public LoginResponse(String token, Long userId, String username, String realName, String role, String email, String phone) {
        this.token = token;
        this.userId = userId;
        this.username = username;
        this.realName = realName;
        this.role = role;
        this.email = email;
        this.phone = phone;
    }
}
