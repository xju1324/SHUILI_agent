<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>用户名 <span class="required">*</span></label>
          <input v-model="form.username" required placeholder="请输入用户名" />
        </div>
        <div class="form-group">
          <label>密码 <span class="required">*</span></label>
          <input v-model="form.password" type="password" required placeholder="请输入密码" />
        </div>
        <div class="form-group">
          <label>真实姓名</label>
          <input v-model="form.realName" placeholder="请输入真实姓名" />
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="form.email" type="email" placeholder="请输入邮箱" />
        </div>
        <div class="form-group">
          <label>电话</label>
          <input v-model="form.phone" placeholder="请输入联系电话" />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      <p class="switch-link">已有账号？<router-link to="/login">立即登录</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../api'

const router = useRouter()
const form = reactive({ username: '', password: '', realName: '', email: '', phone: '' })
const error = ref('')
const loading = ref(false)

const handleRegister = async () => {
  error.value = ''
  loading.value = true
  try {
    await authApi.register(form)
    alert('注册成功，请登录')
    router.push('/login')
  } catch (e) {
    error.value = e.response?.data?.error || e.response?.data?.message || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { display: flex; justify-content: center; padding-top: 40px; }
.auth-card { background: white; padding: 40px; border-radius: 12px; width: 420px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
.auth-card h2 { text-align: center; margin-bottom: 28px; font-size: 22px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 6px; font-weight: 600; font-size: 14px; }
.form-group input { width: 100%; padding: 10px 12px; border: 1px solid #d9d9d9; border-radius: 6px; font-size: 14px; }
.required { color: #e74c3c; }
.error-msg { color: #e74c3c; font-size: 13px; margin-bottom: 12px; }
.btn { width: 100%; padding: 10px; border-radius: 6px; border: none; cursor: pointer; font-size: 15px; }
.btn-primary { background: #1a73e8; color: white; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.switch-link { text-align: center; margin-top: 20px; font-size: 14px; color: #666; }
.switch-link a { color: #1a73e8; text-decoration: none; }
</style>
