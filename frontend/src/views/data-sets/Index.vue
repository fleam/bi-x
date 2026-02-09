<template>
  <div class="data-sets-index">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>数据集管理</h1>
          <el-button type="primary" @click="navigateTo('/data-sets/create')">
            新建数据集
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>数据集列表</span>
            </div>
          </template>
          <div class="card-content">
            <el-table :data="dataSets" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="数据集名称" />
              <el-table-column prop="description" label="描述" />
              <el-table-column prop="data_source_id" label="数据源ID" width="120" />
              <el-table-column prop="creation_mode" label="创建模式" width="120">
                <template #default="scope">
                  <el-tag :type="getModeTagType(scope.row.creation_mode)">
                    {{ scope.row.creation_mode }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="fields.length" label="字段数" width="100" />
              <el-table-column prop="refresh_interval" label="刷新间隔(秒)" width="120" />
              <el-table-column prop="is_active" label="状态" width="100">
                <template #default="scope">
                  <el-switch v-model="scope.row.is_active" @change="handleStatusChange(scope.row)" />
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="navigateTo(`/data-sets/edit/${scope.row.id}`)">
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
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../../utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'

interface DataSet {
  id: number
  name: string
  description: string | null
  data_source_id: number
  creation_mode: string
  sql_query: string | null
  visual_config: any | null
  fields: any[]
  refresh_interval: number
  is_active: boolean
  created_at: string
  updated_at: string
}

const router = useRouter()
const dataSets = ref<DataSet[]>([])

onMounted(async () => {
  await fetchDataSets()
})

const fetchDataSets = async () => {
  try {
    const response = await axios.get('/api/v1/data-sets')
    dataSets.value = response.data
  } catch (error) {
    ElMessage.error('获取数据集列表失败')
    console.error('Failed to fetch data sets:', error)
  }
}

const navigateTo = (path: string) => {
  router.push(path)
}

const getModeTagType = (mode: string): string => {
  switch (mode) {
    case 'visual':
      return 'success'
    case 'sql':
      return 'warning'
    default:
      return 'default'
  }
}

const handleStatusChange = async (dataSet: DataSet) => {
  try {
    await axios.put(`/api/v1/data-sets/${dataSet.id}`, {
      is_active: dataSet.is_active
    })
    ElMessage.success('状态更新成功')
  } catch (error) {
    dataSet.is_active = !dataSet.is_active // 恢复原状态
    ElMessage.error('状态更新失败')
    console.error('Failed to update status:', error)
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该数据集吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await axios.delete(`/api/v1/data-sets/${id}`)
    ElMessage.success('删除成功')
    await fetchDataSets()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('Failed to delete data set:', error)
    }
  }
}
</script>

<style scoped>
.data-sets-index {
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

.card-content {
  padding: 16px 0;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    padding: 10px;
  }

  .header-content h1 {
    margin-bottom: 10px;
  }
}
</style>
