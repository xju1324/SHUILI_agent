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

      <!-- 审核记录 -->
      <div class="reviews-section" v-if="reviewRecords.length">
        <div class="section-title">AI 审核结果 ({{ reviewRecords.length }} 条)</div>
        <div class="review-record" v-for="r in reviewRecords" :key="r.id" :class="recordClass(r)">
          <div class="record-header">
            <span class="record-type">{{ typeLabel(r.reviewType) }}</span>
            <span class="record-severity" :class="'sev-' + (r.severity || 'INFO')">{{ severityLabel(r.severity) }}</span>
          </div>
          <div class="record-body">{{ r.issueDescription }}</div>
          <div class="record-footer" v-if="r.suggestion">
            <strong>建议：</strong>{{ r.suggestion }}
          </div>
        </div>
      </div>
      <div class="reviews-section" v-else-if="material.status === 'REVIEWING'">
        <div class="section-title">AI 审核结果</div>
        <p class="reviewing-hint">正在审查中，请稍候...</p>
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
const reviewRecords = ref([])

const categoryMap = {
  WATER_INTAKE: '取水许可', FLOOD_IMPACT: '洪水影响评价', SOIL_CONSERVATION: '水土保持方案',
  RIVER_CONSTRUCTION: '河道管理范围建设项目', SEWAGE_OUTLET: '入河排污口设置', SAND_MINING: '河道采砂许可'
}

const fieldLabelMap = {
  waterIntakeLocation: '取水地点', waterIntakePurpose: '取水用途', annualWaterVolume: '年取水量(万m³)',
  waterSourceType: '水源类型', projectLocation: '项目地点', riverName: '河流名称',
  floodControlStandard: '防洪标准', constructionContent: '建设内容', projectArea: '占地面积(hm²)',
  soilLossAmount: '土壤流失量(t/a)', conservationMeasures: '水土保持措施',
  constructionType: '建设类型', occupationLength: '占用河道长度(m)',
  outletLocation: '排污口位置', sewageType: '污水类型', dischargeAmount: '排放量(m³/d)',
  dischargeStandard: '排放标准', receivingWater: '受纳水体', riverSection: '采砂河段',
  sandType: '砂石种类', annualMiningAmount: '年开采量(万t)', miningMethod: '开采方式'
}

const categoryLabel = computed(() => categoryMap[material.value?.category] || '未知类型')

const typeFieldItems = computed(() => {
  if (!material.value) return []
  let fd = {}
  try {
    if (material.value.formData) fd = JSON.parse(material.value.formData)
  } catch (e) { /* ignore */ }
  if (material.value.category === 'WATER_INTAKE' && !fd.waterIntakeLocation && material.value.waterIntakeLocation) {
    fd.waterIntakeLocation = material.value.waterIntakeLocation
    fd.waterIntakePurpose = material.value.waterIntakePurpose
    if (material.value.annualWaterVolume) fd.annualWaterVolume = material.value.annualWaterVolume
  }
  return Object.entries(fd).map(([k, v]) => ({ label: fieldLabelMap[k] || k, value: v }))
})

const statusMap = { DRAFT: '草稿', SUBMITTED: '已提交', REVIEWING: '审查中', APPROVED: '已通过', REJECTED: '未通过' }
const statusLabel = (s) => statusMap[s] || s
const statusClass = (s) => 'tag ' + ({ DRAFT: 'tag-gray', SUBMITTED: 'tag-blue', REVIEWING: 'tag-orange', APPROVED: 'tag-green', REJECTED: 'tag-red' }[s] || '')

const typeLabel = (t) => ({ FORMAT: '格式审查', DATA_STANDARD: '数据规范', COMPLIANCE: '合规审查' }[t] || t)
const severityLabel = (s) => ({ INFO: '信息', WARNING: '警告', ERROR: '错误' }[s] || s)

const recordClass = (r) => {
  if (r.severity === 'ERROR' && r.isPass === false) return 'record-error'
  if (r.severity === 'WARNING') return 'record-warning'
  return 'record-info'
}

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
    // 新接口返回 { material, reviewRecords }
    if (res.data.material) {
      material.value = res.data.material
      reviewRecords.value = res.data.reviewRecords || []
    } else {
      // 兼容旧格式
      material.value = res.data
      reviewRecords.value = []
    }
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
.files-section li { margin-bottom: 6px; color: #1a73e8; font-size: 14px; }
.no-files { color: #999; }
.tag { padding: 2px 10px; border-radius: 12px; font-size: 13px; }
.tag-gray { background: #e8e8e8; }
.tag-blue { background: #d6e4ff; color: #1a73e8; }
.tag-orange { background: #ffe7ba; color: #d46b08; }
.tag-green { background: #d9f7be; color: #389e0d; }
.tag-red { background: #ffd8d2; color: #cf1322; }
.btn { padding: 8px 20px; border-radius: 6px; border: none; cursor: pointer; font-size: 14px; text-decoration: none; display: inline-block; }
.btn-success { background: #52c41a; color: white; }
.btn-danger { background: #e74c3c; color: white; }
.btn-back { margin-top: 20px; background: #f0f0f0; color: #666; }
/* 审核记录样式 */
.reviews-section { margin-top: 0; }
.review-record { border: 1px solid #eee; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px; }
.record-error { border-left: 3px solid #e74c3c; background: #fff5f5; }
.record-warning { border-left: 3px solid #f0ad4e; background: #fffdf5; }
.record-info { border-left: 3px solid #52c41a; background: #f6ffed; }
.record-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
.record-type { font-weight: 700; font-size: 13px; color: #333; }
.record-severity { font-size: 12px; padding: 1px 8px; border-radius: 10px; }
.sev-INFO { background: #d9f7be; color: #389e0d; }
.sev-WARNING { background: #ffe7ba; color: #d46b08; }
.sev-ERROR { background: #ffd8d2; color: #cf1322; }
.record-body { font-size: 14px; color: #555; line-height: 1.6; }
.record-footer { font-size: 13px; color: #888; margin-top: 6px; }
.reviewing-hint { color: #999; font-size: 14px; padding: 16px 0; }
</style>