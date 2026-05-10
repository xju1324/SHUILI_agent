import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import MaterialList from '../views/MaterialList.vue'
import MaterialCreate from '../views/MaterialCreate.vue'
import MaterialDetail from '../views/MaterialDetail.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/list/:category', name: 'list', component: MaterialList, props: true },
  { path: '/create', name: 'create', component: MaterialCreate },
  { path: '/detail/:id', name: 'detail', component: MaterialDetail }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
