"""
MCP Tool: check_completeness — 申请材料完整性检查
接收申请材料数据，对照各类审批的检查清单，返回缺失项报告
"""
from typing import Dict, List

# 六类涉水审批必需字段与附件清单
_CHECKLIST: Dict[str, Dict[str, List[str]]] = {
    "WATER_INTAKE": {
        "fields": [
            "title", "projectName", "waterIntakeLocation", "waterIntakePurpose",
            "annualWaterVolume", "applicantCompany", "applicantLegalPerson",
            "businessLicenseNo", "contactPhone",
        ],
        "files": [
            "applicationFormPath", "businessLicensePath",
            "idCardPath", "waterCertificatePath",
        ],
    },
    "FLOOD_IMPACT": {
        "fields": [
            "title", "projectName", "projectLocation", "riverName",
            "floodControlStandard", "constructionContent",
            "applicantCompany", "applicantLegalPerson", "businessLicenseNo",
        ],
        "files": [
            "applicationFormPath", "businessLicensePath", "idCardPath",
        ],
    },
    "SOIL_CONSERVATION": {
        "fields": [
            "title", "projectName", "projectLocation", "projectArea",
            "soilLossAmount", "conservationMeasures",
            "applicantCompany", "applicantLegalPerson", "businessLicenseNo",
        ],
        "files": [
            "applicationFormPath", "businessLicensePath", "idCardPath",
        ],
    },
    "RIVER_CONSTRUCTION": {
        "fields": [
            "title", "projectName", "riverName", "constructionType",
            "occupationLength", "constructionContent",
            "applicantCompany", "applicantLegalPerson", "businessLicenseNo",
        ],
        "files": [
            "applicationFormPath", "businessLicensePath", "idCardPath",
        ],
    },
    "SEWAGE_OUTLET": {
        "fields": [
            "title", "projectName", "outletLocation", "sewageType",
            "dischargeAmount", "dischargeStandard", "receivingWater",
            "applicantCompany", "applicantLegalPerson", "businessLicenseNo",
        ],
        "files": [
            "applicationFormPath", "businessLicensePath", "idCardPath",
        ],
    },
    "SAND_MINING": {
        "fields": [
            "title", "projectName", "riverName", "riverSection",
            "sandType", "annualMiningAmount", "miningMethod",
            "applicantCompany", "applicantLegalPerson", "businessLicenseNo",
        ],
        "files": [
            "applicationFormPath", "businessLicensePath", "idCardPath",
        ],
    },
}

_CATEGORY_NAMES = {
    "WATER_INTAKE": "取水许可",
    "FLOOD_IMPACT": "洪水影响评价",
    "SOIL_CONSERVATION": "水土保持方案",
    "RIVER_CONSTRUCTION": "河道管理范围建设项目",
    "SEWAGE_OUTLET": "入河排污口设置",
    "SAND_MINING": "河道采砂许可",
}

_FIELD_LABELS = {
    "title": "材料标题", "projectName": "建设项目名称",
    "waterIntakeLocation": "取水地点", "waterIntakePurpose": "取水用途",
    "annualWaterVolume": "年取水量", "waterSourceType": "水源类型",
    "projectLocation": "项目地点", "riverName": "河流名称",
    "floodControlStandard": "防洪标准", "constructionContent": "建设内容",
    "projectArea": "占地面积", "soilLossAmount": "土壤流失量",
    "conservationMeasures": "水土保持措施",
    "constructionType": "建设类型", "occupationLength": "占用河道长度",
    "outletLocation": "排污口位置", "sewageType": "污水类型",
    "dischargeAmount": "排放量", "dischargeStandard": "排放标准",
    "receivingWater": "受纳水体",
    "riverSection": "采砂河段", "sandType": "砂石种类",
    "annualMiningAmount": "年开采量", "miningMethod": "开采方式",
    "applicantCompany": "申请单位名称", "applicantLegalPerson": "法定代表人",
    "businessLicenseNo": "营业执照号", "contactPhone": "联系电话",
}

_FILE_LABELS = {
    "applicationFormPath": "申请表",
    "businessLicensePath": "营业执照扫描件",
    "idCardPath": "身份证件",
    "waterCertificatePath": "涉水相关报告",
}


async def check_completeness(material_data: Dict) -> str:
    """检查涉水审批申请材料的完整性。

    Args:
        material_data: 材料数据字典，至少包含 category 字段。
            示例: {"category": "WATER_INTAKE", "title": "XX水库取水申请", ...}

    Returns:
        完整性检查报告，列出缺失的字段和附件
    """
    category = material_data.get("category", "WATER_INTAKE")
    if category not in _CHECKLIST:
        category = "WATER_INTAKE"

    checklist = _CHECKLIST[category]
    cat_name = _CATEGORY_NAMES.get(category, category)

    missing_fields = []
    for field in checklist["fields"]:
        val = material_data.get(field)
        if val is None or (isinstance(val, str) and val.strip() == ""):
            missing_fields.append(_FIELD_LABELS.get(field, field))

    missing_files = []
    for file_field in checklist["files"]:
        val = material_data.get(file_field)
        if val is None or (isinstance(val, str) and val.strip() == ""):
            missing_files.append(_FILE_LABELS.get(file_field, file_field))

    total = len(checklist["fields"]) + len(checklist["files"])
    missing_count = len(missing_fields) + len(missing_files)

    lines = [
        f"=== 材料完整性检查报告 ===",
        f"审批类型: {cat_name} ({category})",
        f"必需字段: {len(checklist['fields'])} 项 | 必需附件: {len(checklist['files'])} 项",
        f"缺失合计: {missing_count} 项 / 共 {total} 项",
        "",
    ]

    if missing_fields:
        lines.append(f"【缺失字段】({len(missing_fields)} 项):")
        for f in missing_fields:
            lines.append(f"  - {f}")

    if missing_files:
        lines.append(f"【缺失附件】({len(missing_files)} 项):")
        for f in missing_files:
            lines.append(f"  - {f}")

    if missing_count == 0:
        lines.append("✓ 材料齐全，所有必需字段和附件已填写完整，可提交审查。")
    else:
        lines.append(f"✗ 共缺失 {missing_count} 项，请补充后重新提交。")

    return "\n".join(lines)
