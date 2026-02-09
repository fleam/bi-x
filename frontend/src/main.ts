import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import './style.css'

// 导入路由配置
import routes from './router'

// 创建路由
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫，检查登录状态
router.beforeEach((to, from, next) => {
  document.title = to.meta.title as string || 'BI报表工具'
  
  // 检查是否需要认证
  const requiresAuth = to.meta.requireAuth !== false
  const token = localStorage.getItem('token')
  
  console.log('Route guard checking:', {
    path: to.path,
    requiresAuth,
    hasToken: !!token
  })
  
  if (requiresAuth && !token) {
    // 未登录，跳转到登录页面
    console.log('Redirecting to login...')
    next('/login')
  } else {
    // 已登录或不需要认证，放行
    next()
  }
})

// 创建Pinia
const pinia = createPinia()

// 创建应用
const app = createApp(App)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 使用插件
app.use(router)
app.use(pinia)
app.use(ElementPlus)

// 挂载应用
app.mount('#app')
