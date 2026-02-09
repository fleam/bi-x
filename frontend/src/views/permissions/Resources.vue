<template>
  <div class="permissions-resources">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>资源管理</h1>
          <el-button type="primary" @click="showAddResourceDialog = true">
            新增资源
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>资源列表</span>
              <el-input
                v-model="searchQuery"
                placeholder="搜索资源"
                prefix-icon="el-icon-search"
                style="width: 300px"
              />
            </div>
          </template>
          <div class="card-content">
            <el-table :data="filteredResources" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="资源名称" />
              <el-table-column prop="type" label="资源类型" width="120">
                <template #default="scope">
                  {{ getResourceTypeLabel(scope.row.type) }}
                </template>
              </el-table-column>
              <el-table-column prop="resource_id" label="对应ID" width="100" />
              <el-table-column prop="owner_id" label="所有者ID" width="100" />
              <el-table-column prop="is_public" label="是否公开" width="100">
                <template #default="scope">
                  <el-switch v-model="scope.row.is_public" @change="handleResourcePublicChange(scope.row)" />
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="editResource(scope.row)">
                    编辑
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteResource(scope.row.id)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
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
      </el-main>
    </el-container>

    <!-- 添加资源对话框 -->
    <el-dialog
      v-model="showAddResourceDialog"
      title="新增资源"
      width="600px"
    >
      <el-form :model="resourceForm" :rules="resourceRules" ref="resourceFormRef" label-width="100px">
        <el-form-item label="资源名称" prop="name">
          <el-input v-model="resourceForm.name" placeholder="请输入资源名称" />
        </el-form-item>
        <el-form-item label="资源类型" prop="type">
          <el-select v-model="resourceForm.type" placeholder="请选择资源类型">
            <el-option label="仪表盘" value="dashboard" />
            <el-option label="图表" value="chart" />
            <el-option label="数据集" value="dataset" />
          </el-select>
        </el-form-item>
        <el-form-item label="对应ID" prop="resource_id">
          <el-input v-model="resourceForm.resource_id" type="number" placeholder="请输入对应资源的ID" />
        </el-form-item>
        <el-form-item label="是否公开" prop="is_public">
          <el-switch v-model="resourceForm.is_public" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddResourceDialog = false">取消</el-button>
          <el-button type="primary" @click="addResource">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑资源对话框 -->
    <el-dialog
      v-model="showEditResourceDialog"
      title="编辑资源"
      width="600px"
    >
      <el-form :model="resourceForm" :rules="resourceRules" ref="resourceFormRef" label-width="100px">
        <el-form-item label="资源名称" prop="name">
          <el-input v-model="resourceForm.name" placeholder="请输入资源名称" />
        </el-form-item>
        <el-form-item label="资源类型" prop="type">
          <el-select v-model="resourceForm.type" placeholder="请选择资源类型" disabled>
            <el-option label="仪表盘" value="dashboard" />
            <el-option label="图表" value="chart" />
            <el-option label="数据集" value="dataset" />
          </el-select>
        </el-form-item>
        <el-form-item label="对应ID" prop="resource_id">
          <el-input v-model="resourceForm.resource_id" type="number" placeholder="请输入对应资源的ID" disabled />
        </el-form-item>
        <el-form-item label="是否公开" prop="is_public">
          <el-switch v-model="resourceForm.is_public" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditResourceDialog = false">取消</el-button>
          <el-button type="primary" @click="updateResource">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface Resource {
  id: number
  name: string
  type: string
  resource_id: number
  owner_id: number
  is_public: boolean
  created_at: string
  updated_at: string
}

interface ResourceFormData {
  name: string
  type: string
  resource_id: number
  is_public: boolean
}

const resources = ref<Resource[]>([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddResourceDialog = ref(false)
const showEditResourceDialog = ref(false)
const resourceFormRef = ref<FormInstance>()
const editingResourceId = ref<number>(0)

const resourceForm = reactive<ResourceFormData>({
  name: '',
  type: 'dashboard',
  resource_id: 0,
  is_public: false
})

const resourceRules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入资源名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择资源类型', trigger: 'change' }
  ],
  resource_id: [
    { required: true, message: '请输入对应资源的ID', trigger: 'blur' }
  ]
})

const filteredResources = computed(() => {
  if (!searchQuery.value) {
    return resources.value
  }
  const query = searchQuery.value.toLowerCase()
  return resources.value.filter(resource => 
    resource.name.toLowerCase().includes(query) ||
    resource.type.toLowerCase().includes(query)
  )
})

onMounted(async () => {
  await fetchResources()
})

const fetchResources = async () => {
  try {
    const response = await axios.get('/api/v1/resources')
    resources.value = response.data
    total.value = response.data.length
  } catch (error) {
    ElMessage.error('获取资源列表失败')
    console.error('Failed to fetch resources:', error)
  }
}

const getResourceTypeLabel = (type: string): string => {
  const typeMap: Record<string, string> = {
    'dashboard': '仪表盘',
    'chart': '图表',
    'dataset': '数据集'
  }
  return typeMap[type] || type
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
}

const handleResourcePublicChange = async (resource: Resource) => {
  try {
    await axios.put(`/api/v1/resources/${resource.id}`, {
      is_public: resource.is_public
    })
    ElMessage.success('资源状态更新成功')
  } catch (error) {
    ElMessage.error('资源状态更新失败')
    console.error('Failed to update resource status:', error)
    // 恢复原状态
    resource.is_public = !resource.is_public
  }
}

const addResource = async () => {
  try {
    await resourceFormRef.value?.validate()
    
    const response = await axios.post('/api/v1/resources', resourceForm)
    resources.value.push(response.data)
    total.value++
    
    showAddResourceDialog.value = false
    resetResourceForm()
    
    ElMessage.success('资源创建成功')
  } catch (error) {
    ElMessage.error('请填写完整的资源信息')
    console.error('Validation error:', error)
  }
}

const editResource = (resource: Resource) => {
  editingResourceId.value = resource.id
  resourceForm.name = resource.name
  resourceForm.type = resource.type
  resourceForm.resource_id = resource.resource_id
  resourceForm.is_public = resource.is_public
  showEditResourceDialog.value = true
}

const updateResource = async () => {
  try {
    await resourceFormRef.value?.validate()
    
    const response = await axios.put(`/api/v1/resources/${editingResourceId.value}`, {
      name: resourceForm.name,
      is_public: resourceForm.is_public
    })
    const index = resources.value.findIndex(r => r.id === editingResourceId.value)
    if (index !== -1) {
      resources.value[index] = response.data
    }
    
    showEditResourceDialog.value = false
    resetResourceForm()
    
    ElMessage.success('资源更新成功')
  } catch (error) {
    ElMessage.error('请填写完整的资源信息')
    console.error('Validation error:', error)
  }
}

const deleteResource = async (resourceId: number) => {
  try {
    await axios.delete(`/api/v1/resources/${resourceId}`)
    resources.value = resources.value.filter(resource => resource.id !== resourceId)
    total.value--
    ElMessage.success('资源删除成功')
  } catch (error) {
    ElMessage.error('资源删除失败')
    console.error('Failed to delete resource:', error)
  }
}

const resetResourceForm = () => {
  resourceForm.name = ''
  resourceForm.type = 'dashboard'
  resourceForm.resource_id = 0
  resourceForm.is_public = false
}
</script>

<style scoped>
.permissions-resources {
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

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
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

  .card-header .el-input {
    width: 100%;
  }
}
</style>
