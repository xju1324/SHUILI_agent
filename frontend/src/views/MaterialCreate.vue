<template>
  <div class="material-form">
    <h2>新建涉水审批申请材料</h2>

    <form @submit.prevent="handleCreate" class="form-card">
      <!-- 审批类型选择 -->
      <div class="form-group">
        <label>审批类型 <span class="required">*</span></label>
        <select v-model="selectedCategory" class="category-select">
          <option v-for="cat in categories" :key="cat.key" :value="cat.key">{{ cat.label }}</option>
        </select>
      </div>

      <!-- 公共字段 -->
      <div class="section-title">基本信息</div>
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
          <label>联系电话</label>
          <input v-model="form.contactPhone" placeholder="联系电话" />
        </div>
        <div class="form-group"></div>
      </div>

      <!-- 取水许可专属字段 -->
      <template v-if="selectedCategory === 'WATER_INTAKE'">
        <div class="section-title">取水许可信息</div>
        <div class="form-row">
          <div class="form-group">
            <label>取水地点</label>
            <input v-model="typeFields.waterIntakeLocation" placeholder="取水具体位置" />
          </div>
          <div class="form-group">
            <label>取水用途</label>
            <select v-model="typeFields.waterIntakePurpose">
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
            <input v-model.number="typeFields.annualWaterVolume" type="number" step="0.01" placeholder="年取水量" />
          </div>
          <div class="form-group">
            <label>水源类型</label>
            <select v-model="typeFields.waterSourceType">
              <option value="">请选择</option>
              <option value="地表水">地表水</option>
              <option value="地下水">地下水</option>
              <option value="混合">混合</option>
            </select>
          </div>
        </div>
      </template>

      <!-- 洪水影响评价专属字段 -->
      <template v-if="selectedCategory === 'FLOOD_IMPACT'">
        <div class="section-title">洪水影响评价信息</div>
        <div class="form-row">
          <div class="form-group">
            <label>项目地点</label>
            <input v-model="typeFields.projectLocation" placeholder="项目具体位置" />
          </div>
          <div class="form-group">
            <label>涉及河流名称</label>
            <input v-model="typeFields.riverName" placeholder="河流名称" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>防洪标准</label>
            <select v-model="typeFields.floodControlStandard">
              <option value="">请选择</option>
              <option value="10年一遇">10年一遇</option>
              <option value="20年一遇">20年一遇</option>
              <option value="50年一遇">50年一遇</option>
              <option value="100年一遇">100年一遇</option>
            </select>
          </div>
          <div class="form-group"></div>
        </div>
        <div class="form-group">
          <label>建设内容描述</label>
          <textarea v-model="typeFields.constructionContent" rows="3" placeholder="请描述建设项目的主要内容"></textarea>
        </div>
      </template>

      <!-- 水土保持方案专属字段 -->
      <template v-if="selectedCategory === 'SOIL_CONSERVATION'">
        <div class="section-title">水土保持方案信息</div>
        <div class="form-row">
          <div class="form-group">
            <label>项目地点</label>
            <input v-model="typeFields.projectLocation" placeholder="项目具体位置" />
          </div>
          <div class="form-group">
            <label>项目占地面积 (hm²)</label>
            <input v-model.number="typeFields.projectArea" type="number" step="0.01" placeholder="占地面积" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>土壤流失量 (t/a)</label>
            <input v-model.number="typeFields.soilLossAmount" type="number" step="0.01" placeholder="预计土壤流失量" />
          </div>
          <div class="form-group"></div>
        </div>
        <div class="form-group">
          <label>水土保持措施</label>
          <textarea v-model="typeFields.conservationMeasures" rows="3" placeholder="请描述水土保持措施方案"></textarea>
        </div>
      </template>

      <!-- 河道管理范围建设项目专属字段 -->
      <template v-if="selectedCategory === 'RIVER_CONSTRUCTION'">
        <div class="section-title">涉河建设项目信息</div>
        <div class="form-row">
          <div class="form-group">
            <label>河流名称</label>
            <input v-model="typeFields.riverName" placeholder="河流名称" />
          </div>
          <div class="form-group">
            <label>建设类型</label>
            <select v-model="typeFields.constructionType">
              <option value="">请选择</option>
              <option value="桥梁">桥梁</option>
              <option value="管线">管线</option>
              <option value="码头">码头</option>
              <option value="其他">其他</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>占用河道长度 (m)</label>
            <input v-model.number="typeFields.occupationLength" type="number" step="0.1" placeholder="占用长度" />
          </div>
          <div class="form-group"></div>
        </div>
        <div class="form-group">
          <label>建设内容描述</label>
          <textarea v-model="typeFields.constructionContent" rows="3" placeholder="请描述建设项目的主要内容"></textarea>
        </div>
      </template>

      <!-- 入河排污口设置专属字段 -->
      <template v-if="selectedCategory === 'SEWAGE_OUTLET'">
        <div class="section-title">入河排污口信息</div>
        <div class="form-row">
          <div class="form-group">
            <label>排污口位置</label>
            <input v-model="typeFields.outletLocation" placeholder="排污口具体位置" />
          </div>
          <div class="form-group">
            <label>污水类型</label>
            <select v-model="typeFields.sewageType">
              <option value="">请选择</option>
              <option value="工业废水">工业废水</option>
              <option value="生活污水">生活污水</option>
              <option value="混合">混合</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>排放量 (m³/d)</label>
            <input v-model.number="typeFields.dischargeAmount" type="number" step="0.1" placeholder="日排放量" />
          </div>
          <div class="form-group">
            <label>排放标准</label>
            <select v-model="typeFields.dischargeStandard">
              <option value="">请选择</option>
              <option value="一级A">一级A</option>
              <option value="一级B">一级B</option>
              <option value="二级">二级</option>
              <option value="三级">三级</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>受纳水体</label>
          <input v-model="typeFields.receivingWater" placeholder="受纳水体名称（如XX河）" />
        </div>
      </template>

      <!-- 河道采砂许可专属字段 -->
      <template v-if="selectedCategory === 'SAND_MINING'">
        <div class="section-title">河道采砂许可信息</div>
        <div class="form-row">
          <div class="form-group">
            <label>河道名称</label>
            <input v-model="typeFields.riverName" placeholder="河道名称" />
          </div>
          <div class="form-group">
            <label>采砂河段</label>
            <input v-model="typeFields.riverSection" placeholder="具体采砂河段" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>砂石种类</label>
            <select v-model="typeFields.sandType">
              <option value="">请选择</option>
              <option value="建筑用砂">建筑用砂</option>
              <option value="河道砾石">河道砾石</option>
              <option value="混合砂石">混合砂石</option>
            </select>
          </div>
          <div class="form-group">
            <label>年开采量 (万t)</label>
            <input v-model.number="typeFields.annualMiningAmount" type="number" step="0.1" placeholder="年开采量" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>开采方式</label>
            <select v-model="typeFields.miningMethod">
              <option value="">请选择</option>
              <option value="机械">机械</option>
              <option value="人工">人工</option>
              <option value="混合">混合</option>
            </select>
          </div>
          <div class="form-group"></div>
        </div>
      </template>

      <!-- 文件上传 -->
      <div class="upload-section">
        <div class="section-title">附件上传</div>
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
import { ref, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { materialApi } from '../api'

const route = useRoute()
const router = useRouter()

const categories = [
  { key: 'WATER_INTAKE',       label: '取水许可' },
  { key: 'FLOOD_IMPACT',       label: '洪水影响评价' },
  { key: 'SOIL_CONSERVATION',  label: '水土保持方案' },
  { key: 'RIVER_CONSTRUCTION', label: '河道管理范围建设项目' },
  { key: 'SEWAGE_OUTLET',      label: '入河排污口设置' },
  { key: 'SAND_MINING',        label: '河道采砂许可' }
]

const selectedCategory = ref(route.query.category || 'WATER_INTAKE')

const form = reactive({
  title: '',
  projectName: '',
  applicantCompany: '',
  applicantLegalPerson: '',
  businessLicenseNo: '',
  contactPhone: ''
})

const typeFields = reactive({
  waterIntakeLocation: '', waterIntakePurpose: '', annualWaterVolume: null, waterSourceType: '',
  projectLocation: '', riverName: '', floodControlStandard: '', constructionContent: '',
  projectArea: null, soilLossAmount: null, conservationMeasures: '',
  constructionType: '', occupationLength: null,
  outletLocation: '', sewageType: '', dischargeAmount: null, dischargeStandard: '', receivingWater: '',
  riverSection: '', sandType: '', annualMiningAmount: null, miningMethod: ''
})

const uploadItems = [
  { field: 'applicationForm', label: '申请表', accept: '.doc,.docx,.pdf' },
  { field: 'businessLicense', label: '营业执照扫描件', accept: '.jpg,.png,.pdf' },
  { field: 'idCard', label: '身份证件', accept: '.jpg,.png' },
  { field: 'waterCertificate', label: '论证报告', accept: '.pdf,.doc,.docx' }
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

const getTypeFieldKeys = (cat) => {
  const map = {
    WATER_INTAKE:       ['waterIntakeLocation', 'waterIntakePurpose', 'annualWaterVolume', 'waterSourceType'],
    FLOOD_IMPACT:       ['projectLocation', 'riverName', 'floodControlStandard', 'constructionContent'],
    SOIL_CONSERVATION:  ['projectLocation', 'projectArea', 'soilLossAmount', 'conservationMeasures'],
    RIVER_CONSTRUCTION: ['riverName', 'constructionType', 'occupationLength', 'constructionContent'],
    SEWAGE_OUTLET:      ['outletLocation', 'sewageType', 'dischargeAmount', 'dischargeStandard', 'receivingWater'],
    SAND_MINING:        ['riverName', 'riverSection', 'sandType', 'annualMiningAmount', 'miningMethod']
  }
  return map[cat] || []
}

const handleCreate = async () => {
  const formData = {}
  const keys = getTypeFieldKeys(selectedCategory.value)
  keys.forEach(k => {
    if (typeFields[k] !== '' && typeFields[k] !== null) formData[k] = typeFields[k]
  })

  try {
    const data = {
      ...form,
      category: selectedCategory.value,
      formData: JSON.stringify(formData),
      waterIntakeLocation: typeFields.waterIntakeLocation || null,
      waterIntakePurpose: typeFields.waterIntakePurpose || null,
      annualWaterVolume: typeFields.annualWaterVolume || null,
      applicationFormPath: uploadedFiles.applicationForm || null,
      businessLicensePath: uploadedFiles.businessLicense || null,
      idCardPath: uploadedFiles.idCard || null,
      waterCertificatePath: uploadedFiles.waterCertificate || null
    }
    await materialApi.create(data)
    router.push(`/list/${selectedCategory.value}`)
  } catch (e) {
    alert('创建失败: ' + (e.response?.data?.message || e.message))
  }
}
</script>

<style scoped>
.material-form { max-width: 800px; }
.material-form h2 { margin-bottom: 20px; font-size: 22px; }
.form-card { background: white; padding: 32px; border-radius: 8px; }
.section-title { font-size: 15px; font-weight: 700; color: #1a73e8; margin: 24px 0 16px; padding-top: 16px; border-top: 1px solid #eee; }
.section-title:first-of-type { border-top: none; margin-top: 0; padding-top: 0; }
.form-group { margin-bottom: 18px; }
.form-group label { display: block; margin-bottom: 6px; font-weight: 600; font-size: 14px; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 8px 12px; border: 1px solid #d9d9d9; border-radius: 6px; font-size: 14px; }
.form-group textarea { resize: vertical; font-family: inherit; }
.category-select { font-size: 16px !important; font-weight: 600; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.required { color: #e74c3c; }
.upload-section { margin-top: 24px; }
.upload-item { margin-bottom: 12px; display: flex; align-items: center; gap: 12px; }
.upload-item label { width: 140px; font-weight: 600; font-size: 14px; flex-shrink: 0; }
.upload-ok { color: #52c41a; font-size: 13px; }
.form-actions { margin-top: 28px; display: flex; gap: 12px; }
.btn { padding: 10px 28px; border-radius: 6px; border: none; cursor: pointer; font-size: 15px; text-decoration: none; display: inline-block; }
.btn-primary { background: #1a73e8; color: white; }
.btn-cancel { background: #f0f0f0; color: #666; }
</style>
