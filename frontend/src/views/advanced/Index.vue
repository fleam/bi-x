<template>
  <div class="advanced-index">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>高级分析</h1>
        </div>
      </el-header>
      <el-main>
        <div class="card-grid">
          <el-card shadow="hover" class="feature-card" @click="navigateTo('/advanced/ai-analyses')">
            <template #header>
              <div class="card-header">
                <span>AI分析</span>
              </div>
            </template>
            <div class="card-content">
              <div class="icon-container">
                <el-icon :size="48" class="feature-icon"><ChatLineRound /></el-icon>
              </div>
              <p class="feature-description">使用AI技术对数据进行深度分析，生成智能洞察和建议</p>
              <el-button type="primary" class="action-button">查看详情</el-button>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="feature-card" @click="navigateTo('/advanced/prediction-models')">
            <template #header>
              <div class="card-header">
                <span>预测模型</span>
              </div>
            </template>
            <div class="card-content">
              <div class="icon-container">
                <el-icon :size="48" class="feature-icon"><TrendCharts /></el-icon>
              </div>
              <p class="feature-description">创建和训练预测模型，对未来趋势进行预测分析</p>
              <el-button type="primary" class="action-button">查看详情</el-button>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="feature-card" @click="navigateTo('/advanced/macros')">
            <template #header>
              <div class="card-header">
                <span>宏管理</span>
              </div>
            </template>
            <div class="card-content">
              <div class="icon-container">
                <el-icon :size="48" class="feature-icon"><Operation /></el-icon>
              </div>
              <p class="feature-description">管理和执行宏命令，自动化数据处理和分析任务</p>
              <el-button type="primary" class="action-button">查看详情</el-button>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="feature-card" @click="navigateTo('/advanced/system-monitor')">
            <template #header>
              <div class="card-header">
                <span>系统监控</span>
              </div>
            </template>
            <div class="card-content">
              <div class="icon-container">
                <el-icon :size="48" class="feature-icon"><Monitor /></el-icon>
              </div>
              <p class="feature-description">监控系统性能和资源使用情况，确保系统稳定运行</p>
              <el-button type="primary" class="action-button">查看详情</el-button>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="feature-card" @click="navigateTo('/advanced/integrations')">
            <template #header>
              <div class="card-header">
                <span>集成管理</span>
              </div>
            </template>
            <div class="card-content">
              <div class="icon-container">
                <el-icon :size="48" class="feature-icon"><Link /></el-icon>
              </div>
              <p class="feature-description">管理与第三方系统的集成，扩展系统功能</p>
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
import { ChatLineRound, TrendCharts, Operation, Monitor, Link } from '@element-plus/icons-vue'

const router = useRouter()

const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.advanced-index {
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
