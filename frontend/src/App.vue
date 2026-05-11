<template>
  <div id="app">
    <header class="app-header">
      <router-link to="/" class="logo">涉水审批智能审核系统</router-link>
      <nav>
        <router-link to="/">首页</router-link>
        <template v-if="user">
          <router-link to="/profile" class="user-info">{{ user.realName || user.username }}</router-link>
          <a href="#" @click.prevent="handleLogout">退出</a>
        </template>
        <template v-else>
          <router-link to="/login">登录</router-link>
          <router-link to="/register">注册</router-link>
        </template>
      </nav>
    </header>
    <div class="app-body">
      <main class="app-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const user = ref(null)
const router = useRouter()

const loadUser = () => {
  const stored = localStorage.getItem('user')
  if (stored) {
    try { user.value = JSON.parse(stored) } catch (e) { user.value = null }
  }
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  user.value = null
  router.push('/login')
}

const onAuthChange = () => loadUser()

onMounted(() => {
  loadUser()
  window.addEventListener('auth-change', onAuthChange)
})

onUnmounted(() => {
  window.removeEventListener('auth-change', onAuthChange)
})
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Microsoft YaHei', sans-serif; background: #f0f2f5; color: #333; }
.app-header {
  background: #1a73e8;
  color: white;
  padding: 0 32px;
  height: 56px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}
.logo { color: white; font-size: 18px; font-weight: 700; text-decoration: none; }
.app-header nav { display: flex; align-items: center; gap: 16px; }
.app-header nav a {
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-size: 14px;
}
.app-header nav a:hover { color: white; }
.app-header nav a.router-link-active { color: white; font-weight: bold; }
.user-info { color: white; font-size: 14px; padding: 4px 10px; background: rgba(255,255,255,0.15); border-radius: 12px; }
.app-body { display: flex; min-height: calc(100vh - 56px); }
.app-main { flex: 1; max-width: 1200px; margin: 0 auto; padding: 24px 16px; width: 100%; }
</style>
