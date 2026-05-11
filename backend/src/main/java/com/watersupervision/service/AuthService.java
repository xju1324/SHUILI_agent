package com.watersupervision.service;

import com.watersupervision.dto.LoginRequest;
import com.watersupervision.dto.LoginResponse;
import com.watersupervision.dto.RegisterRequest;
import com.watersupervision.entity.User;
import com.watersupervision.repository.UserRepository;
import com.watersupervision.security.JwtUtil;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final JwtUtil jwtUtil;
    private final BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();

    public AuthService(UserRepository userRepository, JwtUtil jwtUtil) {
        this.userRepository = userRepository;
        this.jwtUtil = jwtUtil;
    }

    public LoginResponse register(RegisterRequest req) {
        if (userRepository.findByUsername(req.getUsername()).isPresent()) {
            throw new RuntimeException("用户名已存在");
        }
        User user = new User();
        user.setUsername(req.getUsername());
        user.setPassword(encoder.encode(req.getPassword()));
        user.setRealName(req.getRealName());
        user.setEmail(req.getEmail());
        user.setPhone(req.getPhone());
        user.setRole(User.UserRole.APPLICANT);
        userRepository.save(user);
        String token = jwtUtil.generateToken(user.getId(), user.getUsername(), user.getRole().name());
        return new LoginResponse(token, user.getId(), user.getUsername(), user.getRealName(), user.getRole().name());
    }

    public LoginResponse login(LoginRequest req) {
        User user = userRepository.findByUsername(req.getUsername())
                .orElseThrow(() -> new RuntimeException("用户名或密码错误"));
        if (!encoder.matches(req.getPassword(), user.getPassword())) {
            throw new RuntimeException("用户名或密码错误");
        }
        String token = jwtUtil.generateToken(user.getId(), user.getUsername(), user.getRole().name());
        return new LoginResponse(token, user.getId(), user.getUsername(), user.getRealName(), user.getRole().name());
    }

    public LoginResponse getCurrentUser(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("用户不存在"));
        return new LoginResponse(null, user.getId(), user.getUsername(), user.getRealName(), user.getRole().name());
    }
}
