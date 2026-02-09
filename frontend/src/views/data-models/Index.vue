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
              <div class="card-header-actions">
                <el-input
                  v-model="searchQuery"
                  placeholder="搜索模型名称"
                  clearable
                  prefix-icon="el-icon-search"
                  style="width: 300px"
                  @input="handleSearch"
                />
              </div>
            </div>
          </template>
          <div class="card-content">
            <el-table 
              :data="paginatedDataModels" 
              style="width: 100%"
              @sort-change="handleSortChange"
              border
              v-loading="loading"
            >
              <el-table-column prop="id" label="ID" width="80" sortable />
              <el-table-column prop="name" label="模型名称" sortable />
              <el-table-column prop="description" label="描述" />
              <el-table-column label="数据集数量" width="120" sortable>
                <template #default="scope">
                  {{ scope.row.data_sets?.length || 0 }}
                </template>
              </el-table-column>
              <el-table-column label="维度数" width="100" sortable>
                <template #default="scope">
                  {{ scope.row.dimensions?.length || 0 }}
                </template>
              </el-table-column>
              <el-table-column label="度量数" width="100" sortable>
                <template #default="scope">
                  {{ scope.row.measures?.length || 0 }}
                </template>
              </el-table-column>
              <el-table-column label="层次数" width="100" sortable>
                <template #default="scope">
                  {{ scope.row.hierarchies?.length || 0 }}
                </template>
              </el-table-column>
              <el-table-column label="模型类型" width="120" sortable>
                <template #default="scope">
                  {{ scope.row.model_type || '星型' }}
                </template>
              </el-table-column>
              <el-table-column label="状态" width="100">
                <template #default="scope">
                  <el-switch 
                    v-model="scope.row.is_active" 
                    @change="handleStatusChange(scope.row)"
                    :loading="statusLoading[scope.row.id]"
                  />
                </template>
              </el-table-column>
              <el-table-column label="创建时间" width="180" sortable>
                <template #default="scope">
                  {{ formatDate(scope.row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="navigateTo(`/data-models/edit/${scope.row.id}`)">
                    编辑
                  </el-button>
                  <el-button type="danger" size="small" @click="handleDelete(scope.row.id)" :loading="deleteLoading[scope.row.id]">
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="filteredDataModels.length"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../../utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'

interface DataModel {
  id: number
  name: string
  description: string | null
  data_set_id?: number
  data_sets?: any[]
  dimensions: any[]
  measures: any[]
  hierarchies: any[]
  model_type?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

const router = useRouter()
const dataModels = ref<DataModel[]>([])
const loading = ref(false)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const sortField = ref('id')
const sortOrder = ref('ascending')
const statusLoading = ref<Record<number, boolean>>({})

onMounted(async () => {
  await fetchDataModels()
})

const fetchDataModels = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/v1/data-models')
    dataModels.value = response.data
  } catch (error) {
    ElMessage.error('获取数据模型列表失败')
    console.error('Failed to fetch data models:', error)
  } finally {
    loading.value = false
  }
}

const filteredDataModels = computed(() => {
  let result = [...dataModels.value]
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(model => 
      model.name.toLowerCase().includes(query)
    )
  }
  
  // 排序
  if (sortField.value) {
    result.sort((a, b) => {
      let aValue: any = a[sortField.value as keyof DataModel]
      let bValue: any = b[sortField.value as keyof DataModel]
      
      // 处理特殊字段的排序
      if (sortField.value === 'data_sets.length') {
        aValue = a.data_sets?.length || 0
        bValue = b.data_sets?.length || 0
      } else if (sortField.value === 'dimensions.length') {
        aValue = a.dimensions?.length || 0
        bValue = b.dimensions?.length || 0
      } else if (sortField.value === 'measures.length') {
        aValue = a.measures?.length || 0
        bValue = b.measures?.length || 0
      } else if (sortField.value === 'hierarchies.length') {
        aValue = a.hierarchies?.length || 0
        bValue = b.hierarchies?.length || 0
      }
      
      if (aValue < bValue) return sortOrder.value === 'ascending' ? -1 : 1
      if (aValue > bValue) return sortOrder.value === 'ascending' ? 1 : -1
      return 0
    })
  }
  
  return result
})

const paginatedDataModels = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize.value
  const endIndex = startIndex + pageSize.value
  return filteredDataModels.value.slice(startIndex, endIndex)
})

const navigateTo = (path: string) => {
  router.push(path)
}

const handleStatusChange = async (dataModel: DataModel) => {
  statusLoading.value[dataModel.id] = true
  try {
    await axios.put(`/api/v1/data-models/${dataModel.id}`, {
      is_active: dataModel.is_active
    })
    ElMessage.success('状态更新成功')
  } catch (error) {
    dataModel.is_active = !dataModel.is_active // 恢复原状态
    ElMessage.error('状态更新失败')
    console.error('Failed to update status:', error)
  } finally {
    statusLoading.value[dataModel.id] = false
  }
}

const deleteLoading = ref<Record<number, boolean>>({})

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该数据模型吗？删除后将无法恢复。', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    deleteLoading.value[id] = true
    await axios.delete(`/api/v1/data-models/${id}`)
    ElMessage.success('删除成功')
    await fetchDataModels()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
      console.error('Failed to delete data model:', error)
    }
  } finally {
    deleteLoading.value[id] = false
  }
}

const handleSearch = () => {
  currentPage.value = 1 // 重置到第一页
}

const handleSortChange = (sort: any) => {
  sortField.value = sort.prop
  sortOrder.value = sort.order === 'ascending' ? 'ascending' : 'descending'
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1 // 重置到第一页
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
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

.card-header-actions {
  display: flex;
  align-items: center;
}

.card-content {
  padding: 16px 0;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
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
  }

  .card-header-actions {
    margin-top: 10px;
    width: 100%;
  }

  .card-header-actions .el-input {
    width: 100% !important;
  }

  .pagination-container {
    justify-content: center;
  }
}
</style>
