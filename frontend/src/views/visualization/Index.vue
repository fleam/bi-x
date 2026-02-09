<template>
  <div class="visualization-index">
    <div class="page-header">
      <h1>可视化分析</h1>
    </div>
    
    <div class="welcome-section">
      <h2>数据可视化分析工具</h2>
      <p>通过多种方式探索和分析你的数据</p>
    </div>
    <div class="feature-grid">
      <el-card class="feature-card page-card" @click="navigateTo('/visualization/pivot')">
        <template #header>
          <div class="card-header">
            <span>透视分析</span>
          </div>
        </template>
        <div class="card-content">
          <p>类Excel数据透视表，拖拽维度与度量，快速实现汇总、钻取、切片等OLAP分析</p>
        </div>
      </el-card>
      <el-card class="feature-card page-card" @click="navigateTo('/visualization/adhoc')">
        <template #header>
          <div class="card-header">
            <span>即席查询</span>
          </div>
        </template>
        <div class="card-content">
          <p>自由查询数据明细，支持大数据量导出，聚焦具体业务问题</p>
        </div>
      </el-card>
      <el-card class="feature-card page-card" @click="navigateTo('/visualization/spreadsheet')">
        <template #header>
          <div class="card-header">
            <span>电子表格</span>
          </div>
        </template>
        <div class="card-content">
          <p>通过Excel/WPS插件，用熟悉的表格操作设计中国式报表，兼容Excel公式与模板</p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.visualization-index {
  width: 100%;
  height: 100%;
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
  padding-top: 20px;
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
  padding: 0 20px;
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
