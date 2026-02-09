<template>
  <div class="data-models-index">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>数据模型管理</h1>
          <el-button type="primary" @click="navigateTo('/data-models/create')">
            新建数据模型
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>数据模型列表</span>
            </div>
          </template>
          <div class="card-content">
            <el-table :data="dataModels" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="模型名称" />
              <el-table-column prop="description" label="描述" />
              <el-table-column prop="data_set_id" label="数据集ID" width="120" />
              <el-table-column prop="dimensions.length" label="维度数" width="100" />
              <el-table-column prop="measures.length" label="度量数" width="100" />
              <el-table-column prop="hierarchies.length" label="层次数" width="100" />
              <el-table-column prop="is_active" label="状态" width="100">
                <template #default="scope">
                  <el-switch v-model="scope.row.is_active" @change="handleStatusChange(scope.row)" />
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="navigateTo(`/data-models/edit/${scope.row.id}`)">
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

interface DataModel {
  id: number
  name: string
  description: string | null
  data_set_id: number
  dimensions: any[]
  measures: any[]
  hierarchies: any[]
  is_active: boolean
  created_at: string
  updated_at: string
}

const router = useRouter()
const dataModels = ref<DataModel[]>([])

onMounted(async () => {
  await fetchDataModels()
})

const fetchDataModels = async () => {
  try {
    const response = await axios.get('/api/v1/data-models')
    dataModels.value = response.data
  } catch (error) {
    ElMessage.error('获取数据模型列表失败')
    console.error('Failed to fetch data models:', error)
  }
}

const navigateTo = (path: string) => {
  router.push(path)
}

const handleStatusChange = async (dataModel: DataModel) => {
  try {
    await axios.put(`/api/v1/data-models/${dataModel.id}`, {
      is_active: dataModel.is_active
    })
    ElMessage.success('状态更新成功')
  } catch (error) {
    dataModel.is_active = !dataModel.is_active // 恢复原状态
    ElMessage.error('状态更新失败')
    console.error('Failed to update status:', error)
  }
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该数据模型吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await axios.delete(`/api/v1/data-models/${id}`)
    ElMessage.success('删除成功')
    await fetchDataModels()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('Failed to delete data model:', error)
    }
  }
}
</script>

<style scoped>
.data-models-index {
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
