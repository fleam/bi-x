<template>
  <div class="permissions-index">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>权限管理</h1>
        </div>
      </el-header>
      <el-main>
        <div class="card-grid">
          <el-card shadow="hover" class="feature-card" @click="navigateTo('/permissions/users')">
            <template #header>
              <div class="card-header">
                <span>用户管理</span>
              </div>
            </template>
            <div class="card-content">
              <div class="icon-container">
                <el-icon :size="48" class="feature-icon"><User /></el-icon>
              </div>
              <p class="feature-description">管理系统用户，包括创建、编辑、删除用户和分配角色</p>
              <el-button type="primary" class="action-button">查看详情</el-button>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="feature-card" @click="navigateTo('/permissions/roles')">
            <template #header>
              <div class="card-header">
                <span>角色管理</span>
              </div>
            </template>
            <div class="card-content">
              <div class="icon-container">
                <el-icon :size="48" class="feature-icon"><Avatar /></el-icon>
              </div>
              <p class="feature-description">创建和管理角色，为角色分配权限</p>
              <el-button type="primary" class="action-button">查看详情</el-button>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="feature-card" @click="navigateTo('/permissions/permissions')">
            <template #header>
              <div class="card-header">
                <span>权限管理</span>
              </div>
            </template>
            <div class="card-content">
              <div class="icon-container">
                <el-icon :size="48" class="feature-icon"><Lock /></el-icon>
              </div>
              <p class="feature-description">管理系统权限，包括创建和编辑权限</p>
              <el-button type="primary" class="action-button">查看详情</el-button>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="feature-card" @click="navigateTo('/permissions/resources')">
            <template #header>
              <div class="card-header">
                <span>资源管理</span>
              </div>
            </template>
            <div class="card-content">
              <div class="icon-container">
                <el-icon :size="48" class="feature-icon"><Folder /></el-icon>
              </div>
              <p class="feature-description">管理系统资源，为资源分配权限</p>
              <el-button type="primary" class="action-button">查看详情</el-button>
            </div>
          </el-card>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { User, Avatar, Lock, Folder } from '@element-plus/icons-vue'

const router = useRouter()

const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.permissions-index {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 100%;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.feature-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.icon-container {
  margin-bottom: 20px;
}

.feature-icon {
  color: #409EFF;
}

.feature-description {
  text-align: center;
  margin-bottom: 20px;
  color: #666;
  line-height: 1.5;
}

.action-button {
  margin-top: 10px;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    padding: 10px;
  }

  .header-content h1 {
    margin-bottom: 10px;
  }

  .card-grid {
    grid-template-columns: 1fr;
  }

  .feature-card {
    margin-bottom: 10px;
  }
}
</style>
