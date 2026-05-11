<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="form.username" required placeholder="请输入用户名" />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="form.password" type="password" required placeholder="请输入密码" />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      <p class="switch-link">还没有账号？<router-link to="/register">立即注册</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../api'

const router = useRouter()
const form = reactive({ username: '', password: '' })
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  try {
    const res = await authApi.login(form)
    localStorage.setItem('token', res.data.token)
    localStorage.setItem('user', JSON.stringify(res.data))
    window.dispatchEvent(new Event('auth-change'))
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.error || e.response?.data?.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { display: flex; justify-content: center; padding-top: 60px; }
.auth-card { background: white; padding: 40px; border-radius: 12px; width: 400px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
.auth-card h2 { text-align: center; margin-bottom: 28px; font-size: 22px; }
.form-group { margin-bottom: 18px; }
.form-group label { display: block; margin-bottom: 6px; font-weight: 600; font-size: 14px; }
.form-group input { width: 100%; padding: 10px 12px; border: 1px solid #d9d9d9; border-radius: 6px; font-size: 14px; }
.error-msg { color: #e74c3c; font-size: 13px; margin-bottom: 12px; }
.btn { width: 100%; padding: 10px; border-radius: 6px; border: none; cursor: pointer; font-size: 15px; }
.btn-primary { background: #1a73e8; color: white; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.switch-link { text-align: center; margin-top: 20px; font-size: 14px; color: #666; }
.switch-link a { color: #1a73e8; text-decoration: none; }
</style>
