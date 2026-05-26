import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'
import MaterialList from '../views/MaterialList.vue'
import MaterialCreate from '../views/MaterialCreate.vue'
import MaterialDetail from '../views/MaterialDetail.vue'
import KnowledgeSearch from '../views/KnowledgeSearch.vue'

const routes = [
  { path: '/login', name: 'login', component: Login, meta: { guest: true } },
  { path: '/register', name: 'register', component: Register, meta: { guest: true } },
  { path: '/', name: 'home', component: Home },
  { path: '/profile', name: 'profile', component: Profile },
  { path: '/list/:category', name: 'list', component: MaterialList, props: true },
  { path: '/create', name: 'create', component: MaterialCreate },
  { path: '/detail/:id', name: 'detail', component: MaterialDetail },
  { path: '/knowledge', name: 'knowledge', component: KnowledgeSearch }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.guest) {
    if (token) return next('/')
    return next()
  }
  if (!token) {
    return next('/login')
  }
  next()
})

export default router