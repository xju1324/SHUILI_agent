<template>
  <div class="home">
    <div class="hero">
      <h2>涉水审批智能审核</h2>
      <p>选择审批类型，开始办理</p>
    </div>

    <div class="card-grid">
      <div class="type-card" v-for="item in categories" :key="item.key"
           @click="$router.push(`/list/${item.key}`)">
        <div class="card-icon">{{ item.icon }}</div>
        <div class="card-title">{{ item.label }}</div>
        <div class="card-desc">{{ item.desc }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const categories = [
  { key: 'WATER_INTAKE',       icon: '💧', label: '取水许可',         desc: '取水许可审批申请' },
  { key: 'FLOOD_IMPACT',       icon: '🌊', label: '洪水影响评价',      desc: '洪水影响评价类审批' },
  { key: 'SOIL_CONSERVATION',  icon: '🌱', label: '水土保持方案',      desc: '水土保持方案审批' },
  { key: 'RIVER_CONSTRUCTION', icon: '🏗️', label: '河道管理范围建设项目', desc: '涉河建设项目审批' },
  { key: 'SEWAGE_OUTLET',      icon: '🚰', label: '入河排污口设置',     desc: '入河排污口设置审批' },
  { key: 'SAND_MINING',        icon: '⛏️', label: '河道采砂许可',      desc: '河道采砂许可审批' }
]
</script>

<style scoped>
.hero { text-align: center; padding: 40px 0 32px; }
.hero h2 { font-size: 28px; color: #1a1a2e; margin-bottom: 8px; }
.hero p { color: #888; font-size: 15px; }
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  padding: 0 20px;
}
.type-card {
  background: white;
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.25s;
  border: 1px solid #eee;
}
.type-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(26,115,232,0.12);
  border-color: #1a73e8;
}
.card-icon { font-size: 48px; margin-bottom: 16px; }
.card-title { font-size: 18px; font-weight: 700; color: #1a1a2e; margin-bottom: 8px; }
.card-desc { font-size: 13px; color: #999; }
</style>
