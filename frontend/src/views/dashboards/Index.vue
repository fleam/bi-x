<template>
  <div class="dashboards-index">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>仪表盘管理</h1>
          <el-button type="primary" @click="navigateTo('/dashboards/create')">
            新建仪表盘
          </el-button>
        </div>
      </el-header>
      <el-main>
        <!-- 导航菜单 -->
        <el-menu :default-active="activeMenu" class="dashboard-menu" mode="horizontal" @select="handleMenuSelect">
          <el-menu-item index="dashboards">
            <el-icon><IEpGrid /></el-icon>
            <span>仪表盘列表</span>
          </el-menu-item>
          <el-menu-item index="charts">
            <el-icon><IEpDataLine /></el-icon>
            <span>图表管理</span>
          </el-menu-item>
          <el-menu-item index="view">
            <el-icon><IEpView /></el-icon>
            <span>查看仪表盘</span>
          </el-menu-item>
        </el-menu>
        
        <el-card v-show="activeMenu === 'dashboards'">
          <template #header>
            <div class="card-header">
              <span>仪表盘列表</span>
            </div>
          </template>
          <div class="card-content">
            <el-table :data="dashboards" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="仪表盘名称" />
              <el-table-column prop="description" label="描述" />
              <el-table-column prop="widgets.length" label="组件数" width="100" />
              <el-table-column prop="refresh_interval" label="刷新间隔(秒)" width="120" />
              <el-table-column prop="is_active" label="状态" width="100">
                <template #default="scope">
                  <el-switch v-model="scope.row.is_active" @change="handleStatusChange(scope.row)" />
                </template>
              </el-table-column>
              <el-table-column label="操作" width="250" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="navigateTo(`/dashboards/view/${scope.row.id}`)">
                    查看
                  </el-button>
                  <el-button type="success" size="small" @click="navigateTo(`/dashboards/edit/${scope.row.id}`)">
                    编辑
                  </el-button>
                  <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>

        <el-card v-show="activeMenu === 'charts'">
          <template #header>
            <div class="card-header">
              <span>图表管理</span>
            </div>
          </template>
          <div class="card-content">
            <el-table :data="charts" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="图表名称" />
              <el-table-column prop="chart_type" label="图表类型" width="120" />
              <el-table-column prop="data_model_id" label="数据模型ID" width="120" />
              <el-table-column prop="is_active" label="状态" width="100">
                <template #default="scope">
                  <el-switch v-model="scope.row.is_active" @change="handleChartStatusChange(scope.row)" />
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="navigateTo(`/dashboards/edit-chart/${scope.row.id}`)">
                    编辑
                  </el-button>
                  <el-button type="danger" size="small" @click="handleChartDelete(scope.row.id)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-button type="primary" size="small" @click="navigateTo('/dashboards/create-chart')" style="margin-top: 16px;">
              新建图表
            </el-button>
          </div>
        </el-card>

        <el-card v-show="activeMenu === 'view'">
          <template #header>
            <div class="card-header">
              <span>查看仪表盘</span>
            </div>
          </template>
          <div class="card-content">
            <div class="dashboard-list">
              <el-card 
                v-for="dashboard in dashboards" 
                :key="dashboard.id"
                class="dashboard-card"
                @click="navigateTo(`/dashboards/view/${dashboard.id}`)"
              >
                <div class="dashboard-info">
                  <h3>{{ dashboard.name }}</h3>
                  <p>{{ dashboard.description || '无描述' }}</p>
                  <div class="dashboard-stats">
                    <span>组件数: {{ dashboard.widgets.length }}</span>
                    <span>刷新间隔: {{ dashboard.refresh_interval }}秒</span>
                    <span v-if="dashboard.is_active" class="status-active">启用</span>
                    <span v-else class="status-inactive">禁用</span>
                  </div>
                  <el-button type="primary" size="small" class="view-button">
                    查看仪表盘
                  </el-button>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../../utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Grid as IEpGrid, 
  DataLine as IEpDataLine, 
  View as IEpView 
} from '@element-plus/icons-vue'

interface Dashboard {
  id: number
  name: string
  description: string | null
  layout: any
  widgets: any[]
  refresh_interval: number
  is_active: boolean
  created_at: string
  updated_at: string
}

interface Chart {
  id: number
  name: string
  description: string | null
  chart_type: string
  data_model_id: number
  dimensions: any[]
  measures: any[]
  filters: any[]
  style: any
  is_active: boolean
  created_at: string
  updated_at: string
}

const router = useRouter()
const dashboards = ref<Dashboard[]>([])
const charts = ref<Chart[]>([])
const activeMenu = ref('dashboards')

onMounted(async () => {
  await fetchDashboards()
  await fetchCharts()
})

const navigateTo = (path: string) => {
  router.push(path)
}

const handleMenuSelect = (index: string) => {
  activeMenu.value = index
}

const fetchDashboards = async () => {
  try {
    const response = await axios.get('/api/v1/dashboards')
    dashboards.value = response.data
  } catch (error) {
    ElMessage.error('获取仪表盘列表失败')
    console.error('Failed to fetch dashboards:', error)
  }
}

const fetchCharts = async () => {
  try {
    const response = await axios.get('/api/v1/charts')
    charts.value = response.data
  } catch (error) {
    ElMessage.error('获取图表列表失败')
    console.error('Failed to fetch charts:', error)
  }
}

const handleStatusChange = async (dashboard: Dashboard) => {
  try {
    await axios.put(`/api/v1/dashboards/${dashboard.id}`, {
      is_active: dashboard.is_active
    })
    ElMessage.success('状态更新成功')
  } catch (error) {
    dashboard.is_active = !dashboard.is_active // 恢复原状态
    ElMessage.error('状态更新失败')
    console.error('Failed to update status:', error)
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该仪表盘吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await axios.delete(`/api/v1/dashboards/${id}`)
    ElMessage.success('删除成功')
    await fetchDashboards()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('Failed to delete dashboard:', error)
    }
  }
}

const handleChartStatusChange = async (chart: Chart) => {
  try {
    await axios.put(`/api/v1/charts/${chart.id}`, {
      is_active: chart.is_active
    })
    ElMessage.success('状态更新成功')
  } catch (error) {
    chart.is_active = !chart.is_active // 恢复原状态
    ElMessage.error('状态更新失败')
    console.error('Failed to update chart status:', error)
  }
}

const handleChartDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该图表吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await axios.delete(`/api/v1/charts/${id}`)
    ElMessage.success('删除成功')
    await fetchCharts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('Failed to delete chart:', error)
    }
  }
}
</script>

<style scoped>
.dashboards-index {
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

.dashboard-menu {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  padding: 16px 0;
}

.dashboard-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.dashboard-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.dashboard-info h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #333;
}

.dashboard-info p {
  margin: 0 0 15px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

.dashboard-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 15px;
  font-size: 14px;
  color: #666;
}

.status-active {
  color: #67c23a;
  font-weight: 500;
}

.status-inactive {
  color: #909399;
}

.view-button {
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
  
  .dashboard-menu {
    font-size: 12px;
  }
  
  .dashboard-list {
    grid-template-columns: 1fr;
    padding: 10px;
  }
}
</style>
