<template>
  <div class="advanced-system-monitor">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>系统监控</h1>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>监控数据</span>
              <div class="filter-container">
                <el-select v-model="componentFilter" placeholder="选择组件" style="width: 150px; margin-right: 10px;">
                  <el-option label="全部" value="" />
                  <el-option label="API服务" value="api_service" />
                  <el-option label="数据库" value="database" />
                  <el-option label="缓存" value="cache" />
                  <el-option label="系统" value="system" />
                </el-select>
                <el-button type="primary" @click="fetchMonitorData">
                  查询
                </el-button>
              </div>
            </div>
          </template>
          <div class="card-content">
            <el-table :data="monitorData" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="component" label="组件" width="120" />
              <el-table-column prop="metric" label="指标" width="120" />
              <el-table-column prop="value" label="指标值">
                <template #default="scope">
                  <pre>{{ JSON.stringify(scope.row.value, null, 2) }}</pre>
                </template>
              </el-table-column>
              <el-table-column prop="timestamp" label="时间戳" width="180" />
            </el-table>
            <div class="pagination" v-if="total > 0">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </div>
        </el-card>

        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统状态概览</span>
            </div>
          </template>
          <div class="card-content">
            <div class="status-cards">
              <el-card shadow="hover" class="status-card">
                <template #header>
                  <div class="status-card-header">
                    <span>API服务状态</span>
                  </div>
                </template>
                <div class="status-card-content">
                  <div class="status-item">
                    <span class="status-label">响应时间:</span>
                    <span class="status-value">{{ apiStatus.responseTime || '-' }} ms</span>
                  </div>
                  <div class="status-item">
                    <span class="status-label">请求数:</span>
                    <span class="status-value">{{ apiStatus.requestCount || 0 }}</span>
                  </div>
                  <div class="status-item">
                    <span class="status-label">错误率:</span>
                    <span class="status-value">{{ apiStatus.errorRate || 0 }}%</span>
                  </div>
                </div>
              </el-card>
              
              <el-card shadow="hover" class="status-card">
                <template #header>
                  <div class="status-card-header">
                    <span>数据库状态</span>
                  </div>
                </template>
                <div class="status-card-content">
                  <div class="status-item">
                    <span class="status-label">连接数:</span>
                    <span class="status-value">{{ dbStatus.connectionCount || 0 }}</span>
                  </div>
                  <div class="status-item">
                    <span class="status-label">查询时间:</span>
                    <span class="status-value">{{ dbStatus.queryTime || '-' }} ms</span>
                  </div>
                  <div class="status-item">
                    <span class="status-label">缓存命中率:</span>
                    <span class="status-value">{{ dbStatus.cacheHitRate || 0 }}%</span>
                  </div>
                </div>
              </el-card>
              
              <el-card shadow="hover" class="status-card">
                <template #header>
                  <div class="status-card-header">
                    <span>系统资源</span>
                  </div>
                </template>
                <div class="status-card-content">
                  <div class="status-item">
                    <span class="status-label">CPU使用率:</span>
                    <span class="status-value">{{ systemStatus.cpuUsage || 0 }}%</span>
                  </div>
                  <div class="status-item">
                    <span class="status-label">内存使用率:</span>
                    <span class="status-value">{{ systemStatus.memoryUsage || 0 }}%</span>
                  </div>
                  <div class="status-item">
                    <span class="status-label">磁盘使用率:</span>
                    <span class="status-value">{{ systemStatus.diskUsage || 0 }}%</span>
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import axios from '../../utils/axios'
import { ElMessage } from 'element-plus'

interface SystemMonitorData {
  id: number
  component: string
  metric: string
  value: any
  timestamp: string
}

const monitorData = ref<SystemMonitorData[]>([])
const componentFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const apiStatus = reactive({
  responseTime: 0,
  requestCount: 0,
  errorRate: 0
})

const dbStatus = reactive({
  connectionCount: 0,
  queryTime: 0,
  cacheHitRate: 0
})

const systemStatus = reactive({
  cpuUsage: 0,
  memoryUsage: 0,
  diskUsage: 0
})

onMounted(async () => {
  await fetchMonitorData()
  fetchSystemStatus()
  
  // 定时刷新监控数据
  setInterval(() => {
    fetchMonitorData()
    fetchSystemStatus()
  }, 30000) // 每30秒刷新一次
})

const fetchMonitorData = async () => {
  try {
    const params: any = {
      limit: pageSize.value
    }
    if (componentFilter.value) {
      params.component = componentFilter.value
    }
    
    const response = await axios.get('/api/v1/system-monitors', { params })
    monitorData.value = response.data
    total.value = response.data.length
  } catch (error) {
    // 只在控制台打印错误，不显示错误消息，避免频繁弹窗
    console.error('Failed to fetch monitor data:', error)
    // 如果需要，可以添加一个状态变量来记录错误状态，然后在界面上显示一个安静的错误提示
  }
}

const fetchSystemStatus = () => {
  // 模拟系统状态数据
  apiStatus.responseTime = Math.floor(Math.random() * 100)
  apiStatus.requestCount = Math.floor(Math.random() * 1000)
  apiStatus.errorRate = parseFloat((Math.random() * 5).toFixed(2))
  
  dbStatus.connectionCount = Math.floor(Math.random() * 50)
  dbStatus.queryTime = Math.floor(Math.random() * 50)
  dbStatus.cacheHitRate = parseFloat((Math.random() * 100).toFixed(2))
  
  systemStatus.cpuUsage = parseFloat((Math.random() * 100).toFixed(2))
  systemStatus.memoryUsage = parseFloat((Math.random() * 100).toFixed(2))
  systemStatus.diskUsage = parseFloat((Math.random() * 100).toFixed(2))
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  fetchMonitorData()
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
  fetchMonitorData()
}
</script>

<style scoped>
.advanced-system-monitor {
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-container {
  display: flex;
  align-items: center;
}

.card-content {
  padding: 16px 0;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.status-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.status-card {
  margin-bottom: 0;
}

.status-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-card-content {
  padding: 10px 0;
}

.status-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.status-label {
  font-weight: 500;
  color: #666;
}

.status-value {
  font-weight: 600;
  color: #333;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 14px;
  max-height: 150px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    padding: 10px;
  }

  .header-content h1 {
    margin-bottom: 10px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .filter-container {
    width: 100%;
    justify-content: space-between;
  }

  .filter-container .el-select {
    flex: 1;
  }

  .status-cards {
    grid-template-columns: 1fr;
  }
}
</style>
