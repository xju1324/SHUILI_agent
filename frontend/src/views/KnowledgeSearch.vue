<template>
  <div class="ks-page">
    <div class="page-header">
      <h2>📚 知识库向量检索</h2>
      <span class="status-badge" :class="{ ready: kbReady }">{{ kbReady ? `就绪 · ${docCount} 文档块` : '未就绪' }}</span>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <input v-model="query" @keyup.enter="doSearch" placeholder="输入检索关键词，如：取水许可申请条件..." class="search-input" />
      <select v-model="category" class="cat-select">
        <option value="">全部类型</option>
        <option v-for="c in categories" :key="c.key" :value="c.key">{{ c.label }}</option>
      </select>
      <button @click="doSearch" :disabled="searching" class="btn btn-search">
        {{ searching ? '检索中...' : '🔍 检索' }}
      </button>
    </div>

    <!-- 主体区域 -->
    <div class="main-area" v-if="results.length">
      <!-- 散点可视化 -->
      <div class="viz-panel">
        <div class="viz-title">向量空间分布（相似度映射）</div>
        <div class="scatter-plot" ref="scatterRef">
          <div v-for="(r, i) in scatterPoints" :key="i"
               class="scatter-dot"
               :style="{
                 left: r.x + '%',
                 top: r.y + '%',
                 width: r.size + 'px',
                 height: r.size + 'px',
                 background: r.color,
                 boxShadow: r.selected ? `0 0 ${r.size}px ${r.color}` : 'none',
                 zIndex: r.selected ? 10 : 1
               }"
               @mouseenter="highlightResult(i)"
               @mouseleave="highlightResult(-1)"
               :title="r.label"></div>
        </div>
        <div class="viz-legend">
          <span><i style="background:#52c41a"></i> 高相似 (≥0.5)</span>
          <span><i style="background:#faad14"></i> 中 (0.3-0.5)</span>
          <span><i style="background:#ff7a45"></i> 低 (&lt;0.3)</span>
        </div>
      </div>

      <!-- 结果列表 -->
      <div class="results-panel">
        <div class="viz-title">检索结果 ({{ results.length }} 条)</div>
        <div class="result-card" v-for="(r, i) in results" :key="i"
             :class="{ highlighted: highlighted === i }"
             @mouseenter="highlightResult(i)"
             @mouseleave="highlightResult(-1)">
          <div class="card-header">
            <span class="card-source">📄 {{ r.source }}</span>
            <span class="card-score" :style="{ color: scoreColor(r.score) }">
              {{ (r.score * 100).toFixed(1) }}%
            </span>
          </div>
          <div class="score-bar-bg">
            <div class="score-bar-fill" :style="{ width: (r.score * 100) + '%', background: scoreColor(r.score) }"></div>
          </div>
          <div class="card-content">{{ r.content }}</div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div class="empty-state" v-else-if="searched">
      <p>未找到相关结果，试试其他关键词</p>
    </div>
    <div class="empty-state" v-else>
      <p>输入关键词检索知识库中的法规文档</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const AI_BASE = 'http://localhost:8000'

const query = ref('')
const category = ref('')
const results = ref([])
const searching = ref(false)
const searched = ref(false)
const highlighted = ref(-1)
const kbReady = ref(false)
const docCount = ref(0)

const categories = [
  { key: 'WATER_INTAKE', label: '取水许可' },
  { key: 'FLOOD_IMPACT', label: '洪水影响评价' },
  { key: 'SOIL_CONSERVATION', label: '水土保持方案' },
  { key: 'RIVER_CONSTRUCTION', label: '河道建设项目' },
  { key: 'SEWAGE_OUTLET', label: '入河排污口' },
  { key: 'SAND_MINING', label: '河道采砂' },
]

const scoreColor = (s) => {
  if (s >= 0.5) return '#52c41a'
  if (s >= 0.3) return '#faad14'
  return '#ff7a45'
}

// 将检索结果映射为 2D 散点
const scatterPoints = computed(() => {
  return results.value.map((r, i) => {
    // 用相似度决定气泡大小和颜色
    const score = r.score
    const size = 10 + score * 40
    const color = scoreColor(score)
    // 用确定性算法映射位置：分数决定 y，source hash 决定 x
    const y = 90 - score * 80
    const hash = r.source.split('').reduce((a, c) => a + c.charCodeAt(0), i * 31) % 100
    const x = 5 + hash * 0.9
    return {
      x, y, size, color,
      selected: highlighted.value === i,
      label: `${r.source} (${(score * 100).toFixed(0)}%)`
    }
  })
})

const doSearch = async () => {
  if (!query.value.trim()) return
  searching.value = true
  searched.value = true
  try {
    const res = await axios.post(`${AI_BASE}/api/knowledge/search`, {
      query: query.value,
      category: category.value || null,
      top_k: 15
    })
    results.value = res.data.results || []
  } catch (e) {
    alert('检索失败: ' + e.message)
    results.value = []
  } finally {
    searching.value = false
  }
}

const highlightResult = (i) => { highlighted.value = i }

const checkStatus = async () => {
  try {
    const res = await axios.get(`${AI_BASE}/api/knowledge/status`)
    kbReady.value = res.data.ready
    docCount.value = res.data.doc_count
  } catch (e) { /* AI 服务未启动 */ }
}

onMounted(checkStatus)
</script>

<style scoped>
.ks-page { max-width: 1200px; margin: 0 auto; padding: 20px; }
.page-header { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
.page-header h2 { font-size: 22px; margin: 0; }
.status-badge { font-size: 12px; padding: 3px 12px; border-radius: 12px; background: #fff1f0; color: #cf1322; }
.status-badge.ready { background: #f6ffed; color: #389e0d; }

.search-bar { display: flex; gap: 10px; margin-bottom: 24px; }
.search-input { flex: 1; padding: 10px 16px; border: 1px solid #d9d9d9; border-radius: 8px; font-size: 15px; outline: none; }
.search-input:focus { border-color: #1a73e8; box-shadow: 0 0 0 2px rgba(26,115,232,.15); }
.cat-select { padding: 10px; border: 1px solid #d9d9d9; border-radius: 8px; font-size: 14px; min-width: 140px; }
.btn { padding: 10px 24px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; }
.btn-search { background: #1a73e8; color: white; }
.btn-search:disabled { opacity: 0.6; cursor: not-allowed; }

.main-area { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.viz-panel { background: white; border-radius: 12px; padding: 20px; }
.results-panel { background: white; border-radius: 12px; padding: 20px; max-height: 70vh; overflow-y: auto; }
.viz-title { font-size: 14px; font-weight: 700; color: #333; margin-bottom: 16px; }

/* 散点图 */
.scatter-plot { position: relative; width: 100%; height: 300px; background: linear-gradient(135deg, #f0f5ff 0%, #e6f7ff 100%); border-radius: 8px; overflow: hidden; }
.scatter-dot { position: absolute; border-radius: 50%; transition: all 0.3s; transform: translate(-50%, -50%); cursor: pointer; }
.viz-legend { display: flex; gap: 16px; margin-top: 12px; font-size: 12px; color: #666; }
.viz-legend i { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 4px; }

/* 结果卡片 */
.result-card { border: 1px solid #f0f0f0; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px; transition: all 0.2s; cursor: default; }
.result-card:hover, .result-card.highlighted { border-color: #1a73e8; box-shadow: 0 2px 8px rgba(26,115,232,.12); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.card-source { font-size: 12px; color: #888; }
.card-score { font-size: 16px; font-weight: 700; }
.score-bar-bg { height: 4px; background: #f0f0f0; border-radius: 2px; margin-bottom: 8px; overflow: hidden; }
.score-bar-fill { height: 100%; border-radius: 2px; transition: width 0.6s ease; }
.card-content { font-size: 13px; color: #555; line-height: 1.8; max-height: 120px; overflow-y: auto; }

.empty-state { text-align: center; padding: 80px; color: #999; font-size: 16px; background: white; border-radius: 12px; }
</style>