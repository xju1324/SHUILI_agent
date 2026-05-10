import { createRouter, createWebHistory } from 'vue-router'
import MaterialList from '../views/MaterialList.vue'
import MaterialCreate from '../views/MaterialCreate.vue'
import MaterialDetail from '../views/MaterialDetail.vue'

const routes = [
  { path: '/', name: 'list', component: MaterialList },
  { path: '/create', name: 'create', component: MaterialCreate },
  { path: '/detail/:id', name: 'detail', component: MaterialDetail }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
