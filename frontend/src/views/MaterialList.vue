<template>
  <div class="material-list">
    <div class="page-header">
      <h2>材料列表</h2>
      <router-link to="/create" class="btn btn-primary">+ 新建材料</router-link>
    </div>

    <table class="data-table" v-if="materials.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>项目名称</th>
          <th>申请单位</th>
          <th>状态</th>
          <th>提交时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="m in materials" :key="m.id">
          <td>{{ m.id }}</td>
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

    <div v-else class="empty-state">暂无材料，请新建</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { materialApi } from '../api'

const materials = ref([])

const statusMap = { DRAFT: '草稿', SUBMITTED: '已提交', REVIEWING: '审查中', APPROVED: '已通过', REJECTED: '未通过' }
const statusClassMap = { DRAFT: 'tag-gray', SUBMITTED: 'tag-blue', REVIEWING: 'tag-orange', APPROVED: 'tag-green', REJECTED: 'tag-red' }

const statusLabel = (s) => statusMap[s] || s
const statusClass = (s) => 'tag ' + (statusClassMap[s] || '')

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
.data-table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }
.data-table th, .data-table td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #eee; }
.data-table th { background: #f0f2f5; font-weight: 600; }
.tag { padding: 2px 10px; border-radius: 12px; font-size: 13px; }
.tag-gray { background: #e8e8e8; }
.tag-blue { background: #d6e4ff; color: #1a73e8; }
.tag-orange { background: #ffe7ba; color: #d46b08; }
.tag-green { background: #d9f7be; color: #389e0d; }
.tag-red { background: #ffd8d2; color: #cf1322; }
.btn { padding: 8px 20px; border-radius: 6px; border: none; cursor: pointer; font-size: 14px; text-decoration: none; display: inline-block; }
.btn-primary { background: #1a73e8; color: white; }
.btn-success { background: #52c41a; color: white; }
.btn-sm { padding: 4px 12px; font-size: 13px; margin-right: 4px; background: #f0f0f0; border: 1px solid #d9d9d9; border-radius: 4px; }
.empty-state { text-align: center; padding: 80px; color: #999; font-size: 16px; background: white; border-radius: 8px; }
</style>
