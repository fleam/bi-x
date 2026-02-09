<template>
  <div class="home">
    <div class="page-container">
      <div class="welcome-section">
        <h2>欢迎使用BI报表工具</h2>
        <p>快速构建数据驱动的业务分析系统</p>
      </div>
      <div class="feature-grid">
        <el-card class="feature-card page-card" @click="navigateTo('/data-sources')">
          <template #header>
            <div class="card-header">
              <span>数据源管理</span>
            </div>
          </template>
          <div class="card-content">
            <p>支持多种数据源接入，包括数据库、Excel文件和API接口</p>
          </div>
        </el-card>
        <el-card class="feature-card page-card" @click="navigateTo('/data-models')">
          <template #header>
            <div class="card-header">
              <span>数据建模</span>
            </div>
          </template>
          <div class="card-content">
            <p>通过可视化或SQL模式创建数据集，支持数据加工和模型构建</p>
          </div>
        </el-card>
        <el-card class="feature-card page-card" @click="navigateTo('/visualization')">
          <template #header>
            <div class="card-header">
              <span>可视化分析</span>
            </div>
          </template>
          <div class="card-content">
            <p>使用透视分析、即席查询和电子表格进行数据探索</p>
          </div>
        </el-card>
        <el-card class="feature-card page-card" @click="navigateTo('/dashboards')">
          <template #header>
            <div class="card-header">
              <span>仪表盘管理</span>
            </div>
          </template>
          <div class="card-content">
            <p>创建交互式仪表盘，添加图表、指标卡和文本组件</p>
          </div>
        </el-card>
        <el-card class="feature-card page-card" @click="navigateTo('/advanced')">
          <template #header>
            <div class="card-header">
              <span>高级分析</span>
            </div>
          </template>
          <div class="card-content">
            <p>使用AI分析、预测模型、宏管理等功能，实现深度数据挖掘</p>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.home {
  width: 100%;
  height: 100%;
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-section h2 {
  font-size: 32px;
  color: #333;
  margin-bottom: 16px;
}

.welcome-section p {
  font-size: 18px;
  color: #666;
  margin: 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.feature-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  padding: 16px 0;
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .welcome-section {
    padding-top: 10px;
    margin-bottom: 20px;
  }
  
  .welcome-section h2 {
    font-size: 24px;
  }
  
  .welcome-section p {
    font-size: 16px;
  }
}
</style>
