<template>
  <div class="app-root">
    <!-- 登录页面不显示导航 -->
    <template v-if="$route.path !== '/login'">
      <div class="app-container">
        <!-- 顶部导航栏 -->
        <header class="app-header">
          <div class="logo">
            <h1>BI报表工具</h1>
          </div>
          <div class="header-right">
            <span class="user-info">欢迎，管理员</span>
            <el-button type="text" @click="logout">退出登录</el-button>
          </div>
        </header>
        
        <div class="app-body">
          <!-- 左侧侧边栏 -->
          <aside class="app-sidebar">
            <el-menu
              :default-active="$route.path"
              class="sidebar-menu"
              router
              unique-opened
            >
              <el-menu-item index="/">
                <el-icon><HomeFilled /></el-icon>
                <span>首页</span>
              </el-menu-item>
              
              <el-sub-menu index="/data-sources">
                <template #title>
                  <el-icon><Files /></el-icon>
                  <span>数据源管理</span>
                </template>
                <el-menu-item index="/data-sources">数据源列表</el-menu-item>
                <el-menu-item index="/data-sources/create">新建数据源</el-menu-item>
              </el-sub-menu>
              
              <el-sub-menu index="/data-sets">
                <template #title>
                  <el-icon><Grid /></el-icon>
                  <span>数据集管理</span>
                </template>
                <el-menu-item index="/data-sets">数据集列表</el-menu-item>
                <el-menu-item index="/data-sets/create">新建数据集</el-menu-item>
              </el-sub-menu>
              
              <el-sub-menu index="/data-models">
                <template #title>
                  <el-icon><Menu /></el-icon>
                  <span>数据模型管理</span>
                </template>
                <el-menu-item index="/data-models">数据模型列表</el-menu-item>
                <el-menu-item index="/data-models/create">新建数据模型</el-menu-item>
              </el-sub-menu>
              
              <el-sub-menu index="/visualization">
                <template #title>
                  <el-icon><PieChart /></el-icon>
                  <span>可视化分析</span>
                </template>
                <el-menu-item index="/visualization">分析工具</el-menu-item>
                <el-menu-item index="/visualization/pivot">透视分析</el-menu-item>
                <el-menu-item index="/visualization/adhoc">即席查询</el-menu-item>
                <el-menu-item index="/visualization/spreadsheet">电子表格</el-menu-item>
              </el-sub-menu>
              
              <el-sub-menu index="/dashboards">
                <template #title>
                  <el-icon><Monitor /></el-icon>
                  <span>仪表盘管理</span>
                </template>
                <el-menu-item index="/dashboards">仪表盘列表</el-menu-item>
                <el-menu-item index="/dashboards/create">新建仪表盘</el-menu-item>
                <el-menu-item index="/dashboards/create-chart">新建图表</el-menu-item>
              </el-sub-menu>
              
              <el-sub-menu index="/permissions">
                <template #title>
                  <el-icon><Lock /></el-icon>
                  <span>权限管理</span>
                </template>
                <el-menu-item index="/permissions">权限设置</el-menu-item>
                <el-menu-item index="/permissions/users">用户管理</el-menu-item>
                <el-menu-item index="/permissions/roles">角色管理</el-menu-item>
                <el-menu-item index="/permissions/permissions">权限配置</el-menu-item>
                <el-menu-item index="/permissions/resources">资源管理</el-menu-item>
              </el-sub-menu>
              
              <el-sub-menu index="/advanced">
                <template #title>
                  <el-icon><MagicStick /></el-icon>
                  <span>高级分析</span>
                </template>
                <el-menu-item index="/advanced">高级工具</el-menu-item>
                <el-menu-item index="/advanced/ai-analyses">AI分析</el-menu-item>
                <el-menu-item index="/advanced/prediction-models">预测模型</el-menu-item>
                <el-menu-item index="/advanced/macros">宏管理</el-menu-item>
                <el-menu-item index="/advanced/system-monitor">系统监控</el-menu-item>
                <el-menu-item index="/advanced/integrations">集成管理</el-menu-item>
              </el-sub-menu>
            </el-menu>
          </aside>
          
          <!-- 主内容区域 -->
          <main class="app-content">
            <router-view />
          </main>
        </div>
      </div>
    </template>
    
    <!-- 登录页面 -->
    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useRouter } from 'vue-router'
import {
  HomeFilled,
  Grid,
  Menu,
  PieChart,
  Monitor,
  Lock,
  MagicStick,
  Files
} from '@element-plus/icons-vue'

const router = useRouter()

const logout = () => {
  // 清除登录状态
  localStorage.removeItem('token')
  // 跳转到登录页面
  router.push('/login')
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  background-color: #f5f7fa;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.app-root {
  min-height: 100vh;
}

/* 应用容器 */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* 顶部导航栏 */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  padding: 0 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.logo h1 {
  font-size: 20px;
  font-weight: 600;
  color: #409EFF;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  font-size: 14px;
  color: #606266;
}

/* 主体内容 */
.app-body {
  display: flex;
  flex: 1;
  position: relative;
}

/* 左侧侧边栏 */
.app-sidebar {
  width: 240px;
  background-color: #fff;
  border-right: 1px solid #e4e7ed;
  overflow-y: auto;
  position: sticky;
  top: 0;
  height: 100%;
}

.sidebar-menu {
  height: 100%;
}

.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
  margin: 0;
}

.sidebar-menu .el-sub-menu__title {
  height: 50px;
  line-height: 50px;
}

/* 主内容区域 */
.app-content {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100%;
}

/* 统一页面容器样式 */
.page-container {
  width: 100%;
  margin: 0;
}

/* 统一页面头部样式 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

/* 统一卡片样式 */
.page-card {
  margin-bottom: 20px;
  border-radius: 4px;
  overflow: hidden;
}

/* 统一表格样式 */
.page-table {
  width: 100%;
  margin-bottom: 20px;
}

/* 统一表单样式 */
.page-form {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

/* 统一按钮组样式 */
.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-sidebar {
    width: 200px;
  }
  
  .app-content {
    padding: 10px;
  }
  
  .logo h1 {
    font-size: 16px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .page-header h1 {
    font-size: 20px;
  }
  
  .button-group {
    flex-wrap: wrap;
  }
}

/* 确保登录页面全屏显示 */
@media (max-width: 480px) {
  .app-sidebar {
    display: none;
  }
}
</style>
