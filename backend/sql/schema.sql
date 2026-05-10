-- ============================================
-- 涉水审批智能审核系统 - 数据库初始化脚本
-- 数据库: MySQL 8.0
-- 编码: utf8mb4
-- ============================================
DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE water_supervision_review;
CREATE DATABASE IF NOT EXISTS water_supervision_review


-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '加密密码',
    real_name VARCHAR(50) COMMENT '真实姓名',
    role ENUM('ADMIN', 'REVIEWER', 'APPLICANT') DEFAULT 'APPLICANT' COMMENT '角色',
    email VARCHAR(100) COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '联系电话',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='系统用户表';

-- 涉水审批申请材料表
CREATE TABLE IF NOT EXISTS materials (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    applicant_id BIGINT COMMENT '申请人ID',
    title VARCHAR(200) NOT NULL COMMENT '材料标题/项目名称',
    status ENUM('DRAFT', 'SUBMITTED', 'REVIEWING', 'APPROVED', 'REJECTED') DEFAULT 'DRAFT' COMMENT '审查状态',
    -- 申请核心信息
    project_name VARCHAR(200) COMMENT '建设项目名称',
    water_intake_location VARCHAR(200) COMMENT '取水地点',
    water_intake_purpose VARCHAR(100) COMMENT '取水用途',
    annual_water_volume DECIMAL(15,2) COMMENT '年取水量(万m³)',
    applicant_company VARCHAR(200) COMMENT '申请单位名称',
    applicant_legal_person VARCHAR(50) COMMENT '法定代表人',
    business_license_no VARCHAR(50) COMMENT '营业执照号',
    contact_phone VARCHAR(20) COMMENT '联系电话',
    -- 文件路径
    application_form_path VARCHAR(500) COMMENT '申请表文件路径',
    business_license_path VARCHAR(500) COMMENT '营业执照扫描件路径',
    id_card_path VARCHAR(500) COMMENT '身份证件路径',
    water_certificate_path VARCHAR(500) COMMENT '水资源论证报告路径',
    other_files_path TEXT COMMENT '其他附件路径(JSON数组)',
    -- 时间戳
    submit_time DATETIME COMMENT '提交时间',
    review_time DATETIME COMMENT '审查完成时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (applicant_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB COMMENT='涉水审批申请材料表';

-- 审查记录表
CREATE TABLE IF NOT EXISTS review_records (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    material_id BIGINT NOT NULL COMMENT '关联材料ID',
    review_type ENUM('FORMAT', 'DATA_STANDARD', 'COMPLIANCE') NOT NULL COMMENT '审查类型',
    is_pass BOOLEAN COMMENT '是否通过',
    issue_category VARCHAR(100) COMMENT '问题类别',
    issue_description TEXT COMMENT '问题详细描述',
    suggestion TEXT COMMENT '修改建议',
    related_field VARCHAR(100) COMMENT '相关字段名',
    severity ENUM('INFO', 'WARNING', 'ERROR') DEFAULT 'WARNING' COMMENT '严重程度',
    ai_confidence DECIMAL(3,2) COMMENT 'AI置信度',
    reviewed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='AI审查记录表';

-- 知识库文档索引表
CREATE TABLE IF NOT EXISTS knowledge_documents (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    doc_name VARCHAR(200) NOT NULL COMMENT '文档名称',
    doc_type VARCHAR(50) COMMENT '文档类型(PDF/Word/TXT)',
    doc_path VARCHAR(500) COMMENT '文档存储路径',
    doc_category VARCHAR(100) COMMENT '文档分类(法规/标准/指南)',
    chunk_count INT DEFAULT 0 COMMENT '分块数量',
    is_vectorized BOOLEAN DEFAULT FALSE COMMENT '是否已向量化',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='知识库文档索引表';

-- 插入默认管理员用户
INSERT INTO users (username, password, real_name, role) VALUES
('admin', '$2a$10$placeholder_hash', '系统管理员', 'ADMIN');

-- ============================================
-- 节点二：六类涉水审批扩展
-- ============================================
ALTER TABLE materials
    ADD COLUMN category ENUM('WATER_INTAKE', 'FLOOD_IMPACT', 'SOIL_CONSERVATION',
                             'RIVER_CONSTRUCTION', 'SEWAGE_OUTLET', 'SAND_MINING')
    DEFAULT 'WATER_INTAKE' COMMENT '审批类型' AFTER title,
    ADD COLUMN form_data TEXT COMMENT '审批类型专属字段(JSON格式)' AFTER other_files_path;
