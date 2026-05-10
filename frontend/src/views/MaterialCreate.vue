<template>
  <div class="material-form">
    <h2>新建取水许可申请材料</h2>

    <form @submit.prevent="handleCreate" class="form-card">
      <div class="form-group">
        <label>材料标题 <span class="required">*</span></label>
        <input v-model="form.title" required placeholder="请输入材料标题" />
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>建设项目名称</label>
          <input v-model="form.projectName" placeholder="如：XX水库工程" />
        </div>
        <div class="form-group">
          <label>申请单位名称</label>
          <input v-model="form.applicantCompany" placeholder="申请企业全称" />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>法定代表人</label>
          <input v-model="form.applicantLegalPerson" placeholder="法定代表人姓名" />
        </div>
        <div class="form-group">
          <label>营业执照号</label>
          <input v-model="form.businessLicenseNo" placeholder="统一社会信用代码" />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>取水地点</label>
          <input v-model="form.waterIntakeLocation" placeholder="取水具体位置" />
        </div>
        <div class="form-group">
          <label>取水用途</label>
          <select v-model="form.waterIntakePurpose">
            <option value="">请选择</option>
            <option value="农业灌溉">农业灌溉</option>
            <option value="工业用水">工业用水</option>
            <option value="生活用水">生活用水</option>
            <option value="生态用水">生态用水</option>
            <option value="其他">其他</option>
          </select>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>年取水量 (万m³)</label>
          <input v-model.number="form.annualWaterVolume" type="number" step="0.01" placeholder="年取水量" />
        </div>
        <div class="form-group">
          <label>联系电话</label>
          <input v-model="form.contactPhone" placeholder="联系电话" />
        </div>
      </div>

      <!-- 文件上传区域 -->
      <div class="upload-section">
        <h3>附件上传</h3>
        <div class="upload-item" v-for="item in uploadItems" :key="item.field">
          <label>{{ item.label }}</label>
          <input type="file" @change="(e) => handleUpload(e, item.field)" :accept="item.accept" />
          <span v-if="uploadedFiles[item.field]" class="upload-ok">已上传: {{ uploadedFiles[item.field] }}</span>
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary">保存草稿</button>
        <router-link to="/" class="btn btn-cancel">取消</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { materialApi } from '../api'

const router = useRouter()

const form = reactive({
  title: '',
  projectName: '',
  applicantCompany: '',
  applicantLegalPerson: '',
  businessLicenseNo: '',
  waterIntakeLocation: '',
  waterIntakePurpose: '',
  annualWaterVolume: null,
  contactPhone: ''
})

const uploadItems = [
  { field: 'applicationForm', label: '申请表', accept: '.doc,.docx,.pdf' },
  { field: 'businessLicense', label: '营业执照扫描件', accept: '.jpg,.png,.pdf' },
  { field: 'idCard', label: '身份证件', accept: '.jpg,.png' },
  { field: 'waterCertificate', label: '水资源论证报告', accept: '.pdf,.doc,.docx' }
]

const uploadedFiles = reactive({})

const handleUpload = async (e, field) => {
  const file = e.target.files[0]
  if (!file) return
  try {
    const res = await materialApi.upload(file)
    uploadedFiles[field] = res.data.filename
  } catch (err) {
    alert('上传失败: ' + err.message)
  }
}

const handleCreate = async () => {
  try {
    const data = {
      ...form,
      applicationFormPath: uploadedFiles.applicationForm || null,
      businessLicensePath: uploadedFiles.businessLicense || null,
      idCardPath: uploadedFiles.idCard || null,
      waterCertificatePath: uploadedFiles.waterCertificate || null
    }
    await materialApi.create(data)
    router.push('/')
  } catch (e) {
    alert('创建失败: ' + (e.response?.data?.message || e.message))
  }
}
</script>

<style scoped>
.material-form { max-width: 800px; }
.form-card { background: white; padding: 32px; border-radius: 8px; }
.form-group { margin-bottom: 18px; }
.form-group label { display: block; margin-bottom: 6px; font-weight: 600; font-size: 14px; }
.form-group input, .form-group select { width: 100%; padding: 8px 12px; border: 1px solid #d9d9d9; border-radius: 6px; font-size: 14px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.required { color: #e74c3c; }
.upload-section { margin-top: 24px; padding-top: 20px; border-top: 1px solid #eee; }
.upload-section h3 { margin-bottom: 16px; }
.upload-item { margin-bottom: 12px; display: flex; align-items: center; gap: 12px; }
.upload-item label { width: 140px; font-weight: 600; font-size: 14px; flex-shrink: 0; }
.upload-ok { color: #52c41a; font-size: 13px; }
.form-actions { margin-top: 28px; display: flex; gap: 12px; }
.btn { padding: 10px 28px; border-radius: 6px; border: none; cursor: pointer; font-size: 15px; text-decoration: none; display: inline-block; }
.btn-primary { background: #1a73e8; color: white; }
.btn-cancel { background: #f0f0f0; color: #666; }
</style>
