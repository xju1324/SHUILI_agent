<template>
  <div class="material-detail" v-if="material">
    <div class="page-header">
      <div>
        <h2>材料详情 #{{ material.id }}</h2>
        <span class="category-badge">{{ categoryLabel }}</span>
      </div>
      <div>
        <button v-if="material.status === 'DRAFT'" class="btn btn-success" @click="handleSubmit">提交审查</button>
        <button class="btn btn-danger" @click="handleDelete" style="margin-left:8px">删除</button>
      </div>
    </div>

    <div class="detail-card">
      <!-- 基本信息 -->
      <div class="section-title">基本信息</div>
      <div class="detail-grid">
        <div class="detail-item"><label>材料标题</label><span>{{ material.title }}</span></div>
        <div class="detail-item"><label>审查状态</label><span :class="statusClass(material.status)">{{ statusLabel(material.status) }}</span></div>
        <div class="detail-item"><label>建设项目名称</label><span>{{ material.projectName || '-' }}</span></div>
        <div class="detail-item"><label>申请单位</label><span>{{ material.applicantCompany || '-' }}</span></div>
        <div class="detail-item"><label>法定代表人</label><span>{{ material.applicantLegalPerson || '-' }}</span></div>
        <div class="detail-item"><label>营业执照号</label><span>{{ material.businessLicenseNo || '-' }}</span></div>
        <div class="detail-item"><label>联系电话</label><span>{{ material.contactPhone || '-' }}</span></div>
        <div class="detail-item"><label>提交时间</label><span>{{ material.submitTime || '未提交' }}</span></div>
        <div class="detail-item"><label>审查完成时间</label><span>{{ material.reviewTime || '-' }}</span></div>
        <div class="detail-item"><label>创建时间</label><span>{{ material.createdAt || '-' }}</span></div>
        <div class="detail-item"></div>
      </div>

      <!-- 类型专属字段 -->
      <div class="section-title">{{ categoryLabel }} — 专属信息</div>
      <div class="detail-grid">
        <div class="detail-item" v-for="item in typeFieldItems" :key="item.label">
          <label>{{ item.label }}</label><span>{{ item.value || '-' }}</span>
        </div>
        <div v-if="!typeFieldItems.length" class="detail-item"><label></label><span>无额外信息</span></div>
      </div>

      <!-- 附件 -->
      <div class="files-section">
        <div class="section-title">附件文件</div>
        <ul>
          <li v-if="material.applicationFormPath">申请表: {{ material.applicationFormPath }}</li>
          <li v-if="material.businessLicensePath">营业执照: {{ material.businessLicensePath }}</li>
          <li v-if="material.idCardPath">身份证件: {{ material.idCardPath }}</li>
          <li v-if="material.waterCertificatePath">论证报告: {{ material.waterCertificatePath }}</li>
        </ul>
        <p v-if="!hasFiles" class="no-files">暂无附件</p>
      </div>
    </div>

    <router-link to="/" class="btn btn-back">返回列表</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { materialApi } from '../api'

const route = useRoute()
const router = useRouter()
const material = ref(null)

const categoryMap = {
  WATER_INTAKE: '取水许可', FLOOD_IMPACT: '洪水影响评价', SOIL_CONSERVATION: '水土保持方案',
  RIVER_CONSTRUCTION: '河道管理范围建设项目', SEWAGE_OUTLET: '入河排污口设置', SAND_MINING: '河道采砂许可'
}

const fieldLabelMap = {
  // 取水许可
  waterIntakeLocation: '取水地点', waterIntakePurpose: '取水用途', annualWaterVolume: '年取水量(万m³)', waterSourceType: '水源类型',
  // 洪水影响评价
  projectLocation: '项目地点', riverName: '河流名称', floodControlStandard: '防洪标准', constructionContent: '建设内容',
  // 水土保持方案
  projectArea: '占地面积(hm²)', soilLossAmount: '土壤流失量(t/a)', conservationMeasures: '水土保持措施',
  // 河道管理范围建设项目
  constructionType: '建设类型', occupationLength: '占用河道长度(m)',
  // 入河排污口设置
  outletLocation: '排污口位置', sewageType: '污水类型', dischargeAmount: '排放量(m³/d)', dischargeStandard: '排放标准', receivingWater: '受纳水体',
  // 河道采砂许可
  riverSection: '采砂河段', sandType: '砂石种类', annualMiningAmount: '年开采量(万t)', miningMethod: '开采方式'
}

const categoryLabel = computed(() => categoryMap[material.value?.category] || '未知类型')

const typeFieldItems = computed(() => {
  if (!material.value) return []
  // Try formData JSON first
  let fd = {}
  try {
    if (material.value.formData) fd = JSON.parse(material.value.formData)
  } catch (e) { /* ignore */ }
  // Also include legacy dedicated columns for WATER_INTAKE
  if (material.value.category === 'WATER_INTAKE' && !fd.waterIntakeLocation && material.value.waterIntakeLocation) {
    fd.waterIntakeLocation = material.value.waterIntakeLocation
    fd.waterIntakePurpose = material.value.waterIntakePurpose
    if (material.value.annualWaterVolume) fd.annualWaterVolume = material.value.annualWaterVolume
  }
  return Object.entries(fd).map(([k, v]) => ({
    label: fieldLabelMap[k] || k,
    value: v
  }))
})

const statusMap = { DRAFT: '草稿', SUBMITTED: '已提交', REVIEWING: '审查中', APPROVED: '已通过', REJECTED: '未通过' }
const statusLabel = (s) => statusMap[s] || s
const statusClass = (s) => 'tag ' + ({ DRAFT: 'tag-gray', SUBMITTED: 'tag-blue', APPROVED: 'tag-green', REJECTED: 'tag-red' }[s] || '')

const hasFiles = computed(() =>
  material.value && (
    material.value.applicationFormPath ||
    material.value.businessLicensePath ||
    material.value.idCardPath ||
    material.value.waterCertificatePath
  )
)

const fetchDetail = async () => {
  try {
    const res = await materialApi.detail(route.params.id)
    material.value = res.data
  } catch (e) {
    alert('加载详情失败')
    router.push('/')
  }
}

const handleSubmit = async () => {
  if (!confirm('确认提交审查？')) return
  try {
    await materialApi.submit(material.value.id)
    await fetchDetail()
  } catch (e) { alert('提交失败: ' + e.message) }
}

const handleDelete = async () => {
  if (!confirm('确认删除？')) return
  try {
    await materialApi.delete(material.value.id)
    router.push('/')
  } catch (e) { alert('删除失败: ' + e.message) }
}

onMounted(fetchDetail)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.page-header h2 { font-size: 22px; }
.category-badge { display: inline-block; background: #e8f0fe; color: #1a73e8; padding: 2px 12px; border-radius: 12px; font-size: 13px; margin-top: 6px; }
.detail-card { background: white; padding: 32px; border-radius: 8px; }
.section-title { font-size: 15px; font-weight: 700; color: #1a73e8; margin: 24px 0 16px; padding-top: 16px; border-top: 1px solid #eee; }
.section-title:first-of-type { border-top: none; margin-top: 0; padding-top: 0; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.detail-item { margin-bottom: 8px; display: flex; }
.detail-item label { font-weight: 600; color: #666; width: 140px; flex-shrink: 0; font-size: 13px; }
.detail-item span { font-size: 14px; }
.files-section { margin-top: 0; }
.files-section li { margin-bottom: 6px; color: #1a73e8; font-size: 14px; }
.no-files { color: #999; }
.tag { padding: 2px 10px; border-radius: 12px; font-size: 13px; }
.tag-gray { background: #e8e8e8; }
.tag-blue { background: #d6e4ff; color: #1a73e8; }
.tag-green { background: #d9f7be; color: #389e0d; }
.tag-red { background: #ffd8d2; color: #cf1322; }
.btn { padding: 8px 20px; border-radius: 6px; border: none; cursor: pointer; font-size: 14px; text-decoration: none; display: inline-block; }
.btn-success { background: #52c41a; color: white; }
.btn-danger { background: #e74c3c; color: white; }
.btn-back { margin-top: 20px; background: #f0f0f0; color: #666; }
</style>
