<template>
  <div class="data-sources-index">
    <div class="page-container">
      <div class="page-header">
        <h1>数据源管理</h1>
        <el-button type="primary" @click="navigateTo('/data-sources/create')">
          新建数据源
        </el-button>
      </div>
      
      <el-card class="page-card">
        <template #header>
          <div class="card-header">
            <span>数据源列表</span>
          </div>
        </template>
        <div class="card-content">
          <el-table :data="dataSources" style="width: 100%" class="page-table">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="数据源名称" />
            <el-table-column prop="type" label="类型" width="120">
              <template #default="scope">
                <el-tag :type="getTypeTagType(scope.row.type)">
                  {{ scope.row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="db_type" label="数据库类型" width="120" />
            <el-table-column prop="host" label="主机地址" width="180" />
            <el-table-column prop="port" label="端口" width="80" />
            <el-table-column prop="database" label="数据库" width="150" />
            <el-table-column prop="is_active" label="状态" width="100">
              <template #default="scope">
                <el-switch v-model="scope.row.is_active" @change="handleStatusChange(scope.row)" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="scope">
                <el-button type="primary" size="small" @click="navigateTo(`/data-sources/edit/${scope.row.id}`)">
                  编辑
                </el-button>
                <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">
                  删除
                </el-button>
                <el-button type="info" size="small" @click="handleTestConnection(scope.row.id)">
                  测试连接
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../../utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'

interface DataSource {
  id: number
  name: string
  type: string
  db_type: string | null
  host: string | null
  port: number | null
  database: string | null
  username: string | null
  password: string | null
  file_path: string | null
  api_url: string | null
  api_method: string | null
  api_headers: any | null
  api_body: any | null
  connection_pool: number
  refresh_interval: number
  is_active: boolean
  created_at: string
  updated_at: string
}

const router = useRouter()
const dataSources = ref<DataSource[]>([])

onMounted(async () => {
  await fetchDataSources()
})

const fetchDataSources = async () => {
  try {
    const response = await axios.get('/api/v1/sources/')
    dataSources.value = response.data
  } catch (error) {
    ElMessage.error('获取数据源列表失败')
    console.error('Failed to fetch data sources:', error)
  }
}

const navigateTo = (path: string) => {
  router.push(path)
}

const getTypeTagType = (type: string): string => {
  switch (type) {
    case 'database':
      return 'success'
    case 'excel':
      return 'warning'
    case 'api':
      return 'info'
    default:
      return 'default'
  }
}

const handleStatusChange = async (dataSource: DataSource) => {
  try {
    await axios.put(`/api/v1/sources/${dataSource.id}`, {
      is_active: dataSource.is_active
    })
    ElMessage.success('状态更新成功')
  } catch (error) {
    dataSource.is_active = !dataSource.is_active // 恢复原状态
    ElMessage.error('状态更新失败')
    console.error('Failed to update status:', error)
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该数据源吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await axios.delete(`/api/v1/sources/${id}`)
    ElMessage.success('删除成功')
    await fetchDataSources()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('Failed to delete data source:', error)
    }
  }
}

const handleTestConnection = async (id: number) => {
  try {
    const dataSource = dataSources.value.find(ds => ds.id === id)
    if (!dataSource) {
      ElMessage.error('数据源不存在')
      return
    }

    const testRequest = {
      type: dataSource.type,
      db_type: dataSource.db_type,
      host: dataSource.host,
      port: dataSource.port,
      database: dataSource.database,
      username: dataSource.username,
      password: dataSource.password,
      file_path: dataSource.file_path,
      api_url: dataSource.api_url,
      api_method: dataSource.api_method,
      api_headers: dataSource.api_headers,
      api_body: dataSource.api_body
    }

    const response = await axios.post('/api/v1/sources/test-connection', testRequest)
    if (response.data.success) {
      ElMessage.success('连接测试成功')
    } else {
      ElMessage.error(`连接测试失败: ${response.data.message}`)
    }
  } catch (error) {
    ElMessage.error('连接测试失败')
    console.error('Failed to test connection:', error)
  }
}
</script>

<style scoped>
.data-sources-index {
  width: 100%;
  height: 100%;
}

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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  padding: 16px 0;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .page-header h1 {
    font-size: 20px;
  }
}
</style>
