<template>
  <div class="material-detail" v-if="material">
    <div class="page-header">
      <h2>材料详情 #{{ material.id }}</h2>
      <div>
        <button v-if="material.status === 'DRAFT'" class="btn btn-success" @click="handleSubmit">提交审查</button>
        <button class="btn btn-danger" @click="handleDelete" style="margin-left:8px">删除</button>
      </div>
    </div>

    <div class="detail-card">
      <div class="detail-grid">
        <div class="detail-item"><label>材料标题</label><span>{{ material.title }}</span></div>
        <div class="detail-item"><label>审查状态</label><span :class="statusClass(material.status)">{{ statusLabel(material.status) }}</span></div>
        <div class="detail-item"><label>建设项目名称</label><span>{{ material.projectName || '-' }}</span></div>
        <div class="detail-item"><label>申请单位</label><span>{{ material.applicantCompany || '-' }}</span></div>
        <div class="detail-item"><label>法定代表人</label><span>{{ material.applicantLegalPerson || '-' }}</span></div>
        <div class="detail-item"><label>营业执照号</label><span>{{ material.businessLicenseNo || '-' }}</span></div>
        <div class="detail-item"><label>取水地点</label><span>{{ material.waterIntakeLocation || '-' }}</span></div>
        <div class="detail-item"><label>取水用途</label><span>{{ material.waterIntakePurpose || '-' }}</span></div>
        <div class="detail-item"><label>年取水量(万m³)</label><span>{{ material.annualWaterVolume || '-' }}</span></div>
        <div class="detail-item"><label>联系电话</label><span>{{ material.contactPhone || '-' }}</span></div>
        <div class="detail-item"><label>提交时间</label><span>{{ material.submitTime || '未提交' }}</span></div>
        <div class="detail-item"><label>审查完成时间</label><span>{{ material.reviewTime || '-' }}</span></div>
      </div>

      <!-- 附件列表 -->
      <div class="files-section">
        <h3>附件文件</h3>
        <ul>
          <li v-if="material.applicationFormPath">申请表: {{ material.applicationFormPath }}</li>
          <li v-if="material.businessLicensePath">营业执照: {{ material.businessLicensePath }}</li>
          <li v-if="material.idCardPath">身份证件: {{ material.idCardPath }}</li>
          <li v-if="material.waterCertificatePath">水资源论证报告: {{ material.waterCertificatePath }}</li>
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
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.detail-card { background: white; padding: 32px; border-radius: 8px; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.detail-item { margin-bottom: 8px; }
.detail-item label { font-weight: 600; color: #666; margin-right: 8px; display: inline-block; width: 120px; }
.files-section { margin-top: 24px; padding-top: 20px; border-top: 1px solid #eee; }
.files-section h3 { margin-bottom: 12px; }
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
