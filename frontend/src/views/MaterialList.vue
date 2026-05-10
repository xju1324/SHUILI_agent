<template>
  <div class="material-list">
    <div class="page-header">
      <h2>{{ currentCategory ? categoryMap[currentCategory] : '全部材料' }}</h2>
      <router-link :to="`/create${currentCategory ? '?category=' + currentCategory : ''}`" class="btn btn-primary">+ 新建材料</router-link>
    </div>

    <!-- 类型 Tab -->
    <div class="category-tabs">
      <span :class="['tab', { active: !currentCategory }]">
        <router-link to="/">全部</router-link>
      </span>
      <span v-for="cat in categories" :key="cat.key"
            :class="['tab', { active: currentCategory === cat.key }]">
        <router-link :to="`/list/${cat.key}`">{{ cat.label }}</router-link>
      </span>
    </div>

    <table class="data-table" v-if="filteredMaterials.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>审批类型</th>
          <th>项目名称</th>
          <th>申请单位</th>
          <th>状态</th>
          <th>提交时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="m in filteredMaterials" :key="m.id">
          <td>{{ m.id }}</td>
          <td><span class="type-tag">{{ categoryMap[m.category] || m.category }}</span></td>
          <td>{{ m.projectName || m.title }}</td>
          <td>{{ m.applicantCompany }}</td>
          <td><span :class="statusClass(m.status)">{{ statusLabel(m.status) }}</span></td>
          <td>{{ m.submitTime || '-' }}</td>
          <td>
            <router-link :to="`/detail/${m.id}`" class="btn btn-sm">查看</router-link>
            <button class="btn btn-sm btn-success"
                    v-if="m.status === 'DRAFT'"
                    @click="handleSubmit(m.id)">提交审查</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else class="empty-state">
      <p>暂无材料</p>
      <router-link :to="`/create${currentCategory ? '?category=' + currentCategory : ''}`" class="btn btn-primary" style="margin-top:16px">新建材料</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { materialApi } from '../api'

const props = defineProps({ category: { type: String, default: '' } })
const materials = ref([])

const currentCategory = computed(() => props.category || '')

const categories = [
  { key: 'WATER_INTAKE',       label: '取水许可' },
  { key: 'FLOOD_IMPACT',       label: '洪水影响评价' },
  { key: 'SOIL_CONSERVATION',  label: '水土保持方案' },
  { key: 'RIVER_CONSTRUCTION', label: '河道管理范围建设项目' },
  { key: 'SEWAGE_OUTLET',      label: '入河排污口设置' },
  { key: 'SAND_MINING',        label: '河道采砂许可' }
]

const categoryMap = Object.fromEntries(categories.map(c => [c.key, c.label]))

const statusMap = { DRAFT: '草稿', SUBMITTED: '已提交', REVIEWING: '审查中', APPROVED: '已通过', REJECTED: '未通过' }
const statusClassMap = { DRAFT: 'tag tag-gray', SUBMITTED: 'tag tag-blue', REVIEWING: 'tag tag-orange', APPROVED: 'tag tag-green', REJECTED: 'tag tag-red' }
const statusLabel = (s) => statusMap[s] || s
const statusClass = (s) => statusClassMap[s] || 'tag'

const filteredMaterials = computed(() => {
  if (!currentCategory.value) return materials.value
  return materials.value.filter(m => m.category === currentCategory.value)
})

const fetchList = async () => {
  try {
    const res = await materialApi.list()
    materials.value = res.data
  } catch (e) {
    alert('加载列表失败: ' + e.message)
  }
}

const handleSubmit = async (id) => {
  if (!confirm('确认提交审查？')) return
  try {
    await materialApi.submit(id)
    await fetchList()
  } catch (e) {
    alert('提交失败: ' + e.message)
  }
}

onMounted(fetchList)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { font-size: 22px; }
.category-tabs { display: flex; gap: 4px; margin-bottom: 20px; flex-wrap: wrap; }
.tab { padding: 6px 16px; border-radius: 20px; font-size: 13px; cursor: pointer; background: white; border: 1px solid #d9d9d9; }
.tab:hover { border-color: #1a73e8; }
.tab.active { background: #1a73e8; border-color: #1a73e8; }
.tab.active a { color: white; }
.tab a { text-decoration: none; color: #555; }
.data-table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }
.data-table th, .data-table td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #eee; font-size: 14px; }
.data-table th { background: #f0f2f5; font-weight: 600; }
.type-tag { background: #e8f0fe; color: #1a73e8; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.tag { padding: 2px 10px; border-radius: 12px; font-size: 13px; }
.tag-gray { background: #e8e8e8; }
.tag-blue { background: #d6e4ff; color: #1a73e8; }
.tag-orange { background: #ffe7ba; color: #d46b08; }
.tag-green { background: #d9f7be; color: #389e0d; }
.tag-red { background: #ffd8d2; color: #cf1322; }
.btn { padding: 8px 20px; border-radius: 6px; border: none; cursor: pointer; font-size: 14px; text-decoration: none; display: inline-block; }
.btn-primary { background: #1a73e8; color: white; }
.btn-success { background: #52c41a; color: white; }
.btn-sm { padding: 4px 12px; font-size: 13px; margin-right: 4px; background: #f0f0f0; border: 1px solid #d9d9d9; border-radius: 4px; color: #333; }
.empty-state { text-align: center; padding: 80px; color: #999; font-size: 16px; background: white; border-radius: 8px; }
</style>
