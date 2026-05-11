<template>
  <div class="profile">
    <h2>个人主页</h2>

    <!-- 个人信息卡片 -->
    <div class="card">
      <div class="section-title">个人信息</div>
      <div class="info-grid">
        <div class="info-item"><label>用户名</label><span>{{ user.username }}</span></div>
        <div class="info-item"><label>真实姓名</label><span>{{ user.realName || '-' }}</span></div>
        <div class="info-item"><label>角色</label><span>{{ roleMap[user.role] || user.role }}</span></div>
        <div class="info-item"><label>邮箱</label><span>{{ user.email || '-' }}</span></div>
        <div class="info-item"><label>电话</label><span>{{ user.phone || '-' }}</span></div>
      </div>
    </div>

    <!-- 我的申请 -->
    <div class="card">
      <div class="section-title">
        我的申请
        <router-link to="/create" class="btn btn-sm btn-primary">+ 新建申请</router-link>
      </div>
      <table class="data-table" v-if="materials.length">
        <thead>
          <tr>
            <th>ID</th>
            <th>审批类型</th>
            <th>项目名称</th>
            <th>状态</th>
            <th>提交时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in materials" :key="m.id">
            <td>{{ m.id }}</td>
            <td><span class="type-tag">{{ categoryMap[m.category] || m.category }}</span></td>
            <td>{{ m.projectName || m.title }}</td>
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
      <div v-else class="empty-state">暂无申请</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authApi, materialApi } from '../api'

const user = ref({})
const materials = ref([])

const categoryMap = {
  WATER_INTAKE: '取水许可', FLOOD_IMPACT: '洪水影响评价', SOIL_CONSERVATION: '水土保持方案',
  RIVER_CONSTRUCTION: '河道管理范围建设项目', SEWAGE_OUTLET: '入河排污口设置', SAND_MINING: '河道采砂许可'
}
const roleMap = { ADMIN: '管理员', REVIEWER: '审批员', APPLICANT: '申请人' }
const statusMap = { DRAFT: '草稿', SUBMITTED: '已提交', REVIEWING: '审查中', APPROVED: '已通过', REJECTED: '未通过' }
const statusClassMap = { DRAFT: 'tag tag-gray', SUBMITTED: 'tag tag-blue', REVIEWING: 'tag tag-orange', APPROVED: 'tag tag-green', REJECTED: 'tag tag-red' }
const statusLabel = (s) => statusMap[s] || s
const statusClass = (s) => statusClassMap[s] || 'tag'

const fetchData = async () => {
  try {
    const [userRes, matRes] = await Promise.all([authApi.me(), materialApi.myList()])
    user.value = userRes.data
    localStorage.setItem('user', JSON.stringify(userRes.data))
    materials.value = matRes.data
  } catch (e) { /* ignore */ }
}

const handleSubmit = async (id) => {
  if (!confirm('确认提交审查？')) return
  try {
    await materialApi.submit(id)
    await fetchData()
  } catch (e) { alert('提交失败: ' + e.message) }
}

onMounted(fetchData)
</script>

<style scoped>
.profile { max-width: 900px; }
.profile h2 { margin-bottom: 24px; font-size: 22px; }
.card { background: white; border-radius: 8px; padding: 28px; margin-bottom: 24px; }
.section-title { font-size: 16px; font-weight: 700; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.info-item { display: flex; }
.info-item label { width: 90px; font-weight: 600; color: #666; font-size: 14px; flex-shrink: 0; }
.info-item span { font-size: 14px; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 10px 14px; text-align: left; border-bottom: 1px solid #eee; font-size: 14px; }
.data-table th { background: #f0f2f5; font-weight: 600; }
.type-tag { background: #e8f0fe; color: #1a73e8; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.tag { padding: 2px 10px; border-radius: 12px; font-size: 13px; }
.tag-gray { background: #e8e8e8; }
.tag-blue { background: #d6e4ff; color: #1a73e8; }
.tag-orange { background: #ffe7ba; color: #d46b08; }
.tag-green { background: #d9f7be; color: #389e0d; }
.tag-red { background: #ffd8d2; color: #cf1322; }
.btn { padding: 6px 16px; border-radius: 6px; border: none; cursor: pointer; font-size: 13px; text-decoration: none; display: inline-block; }
.btn-sm { padding: 4px 12px; font-size: 13px; margin-right: 4px; background: #f0f0f0; border: 1px solid #d9d9d9; border-radius: 4px; color: #333; }
.btn-primary { background: #1a73e8; color: white; border: none; }
.btn-success { background: #52c41a; color: white; border: none; }
.empty-state { text-align: center; padding: 40px; color: #999; font-size: 14px; }
</style>
