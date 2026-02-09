<template>
  <div class="advanced-integrations">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>集成管理</h1>
          <el-button type="primary" @click="showAddIntegrationDialog = true">
            新增集成
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>集成列表</span>
              <el-input
                v-model="searchQuery"
                placeholder="搜索集成"
                prefix-icon="el-icon-search"
                style="width: 300px"
              />
            </div>
          </template>
          <div class="card-content">
            <el-table :data="filteredIntegrations" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="集成名称" />
              <el-table-column prop="type" label="集成类型" width="120" />
              <el-table-column prop="is_active" label="状态" width="100">
                <template #default="scope">
                  <el-switch v-model="scope.row.is_active" @change="handleIntegrationStatusChange(scope.row)" />
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="创建时间" width="180" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="editIntegration(scope.row)">
                    编辑
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteIntegration(scope.row.id)">
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

        <el-card v-if="selectedIntegration">
          <template #header>
            <div class="card-header">
              <span>集成详情</span>
            </div>
          </template>
          <div class="card-content">
            <el-descriptions :column="2">
              <el-descriptions-item label="集成名称">
                {{ selectedIntegration.name }}
              </el-descriptions-item>
              <el-descriptions-item label="集成类型">
                {{ selectedIntegration.type }}
              </el-descriptions-item>
              <el-descriptions-item label="状态">
                <el-switch v-model="selectedIntegration.is_active" @change="handleIntegrationStatusChange(selectedIntegration)" />
              </el-descriptions-item>
              <el-descriptions-item label="创建时间">
                {{ selectedIntegration.created_at }}
              </el-descriptions-item>
              <el-descriptions-item label="更新时间">
                {{ selectedIntegration.updated_at }}
              </el-descriptions-item>
              <el-descriptions-item label="描述" :span="2">
                {{ selectedIntegration.description || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="配置" :span="2">
                <pre>{{ JSON.stringify(selectedIntegration.config, null, 2) }}</pre>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-main>
    </el-container>

    <!-- 添加集成对话框 -->
    <el-dialog
      v-model="showAddIntegrationDialog"
      title="新增集成"
      width="600px"
    >
      <el-form :model="integrationForm" :rules="integrationRules" ref="integrationFormRef" label-width="100px">
        <el-form-item label="集成名称" prop="name">
          <el-input v-model="integrationForm.name" placeholder="请输入集成名称" />
        </el-form-item>
        <el-form-item label="集成类型" prop="type">
          <el-select v-model="integrationForm.type" placeholder="请选择集成类型">
            <el-option label="第三方API" value="third_party_api" />
            <el-option label="数据存储" value="data_storage" />
            <el-option label="通知服务" value="notification" />
            <el-option label="认证服务" value="authentication" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="integrationForm.description" type="textarea" placeholder="请输入集成描述" />
        </el-form-item>
        <el-form-item label="配置" prop="config">
          <el-input v-model="integrationForm.config" type="textarea" placeholder="请输入集成配置（JSON格式）" rows="4" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="integrationForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddIntegrationDialog = false">取消</el-button>
          <el-button type="primary" @click="addIntegration">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑集成对话框 -->
    <el-dialog
      v-model="showEditIntegrationDialog"
      title="编辑集成"
      width="600px"
    >
      <el-form :model="integrationForm" :rules="integrationRules" ref="integrationFormRef" label-width="100px">
        <el-form-item label="集成名称" prop="name">
          <el-input v-model="integrationForm.name" placeholder="请输入集成名称" />
        </el-form-item>
        <el-form-item label="集成类型" prop="type">
          <el-select v-model="integrationForm.type" placeholder="请选择集成类型" disabled>
            <el-option label="第三方API" value="third_party_api" />
            <el-option label="数据存储" value="data_storage" />
            <el-option label="通知服务" value="notification" />
            <el-option label="认证服务" value="authentication" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="integrationForm.description" type="textarea" placeholder="请输入集成描述" />
        </el-form-item>
        <el-form-item label="配置" prop="config">
          <el-input v-model="integrationForm.config" type="textarea" placeholder="请输入集成配置（JSON格式）" rows="4" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="integrationForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditIntegrationDialog = false">取消</el-button>
          <el-button type="primary" @click="updateIntegration">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface Integration {
  id: number
  name: string
  description: string
  type: string
  config: any
  is_active: boolean
  created_at: string
  updated_at: string
}

interface IntegrationFormData {
  name: string
  description: string
  type: string
  config: string
  is_active: boolean
}

const integrations = ref<Integration[]>([])
const selectedIntegration = ref<Integration | null>(null)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddIntegrationDialog = ref(false)
const showEditIntegrationDialog = ref(false)
const integrationFormRef = ref<FormInstance>()
const editingIntegrationId = ref<number>(0)

const integrationForm = reactive<IntegrationFormData>({
  name: '',
  description: '',
  type: 'third_party_api',
  config: '{}',
  is_active: true
})

const integrationRules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入集成名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择集成类型', trigger: 'change' }
  ],
  config: [
    { required: true, message: '请输入集成配置', trigger: 'blur' }
  ]
})

const filteredIntegrations = computed(() => {
  if (!searchQuery.value) {
    return integrations.value
  }
  const query = searchQuery.value.toLowerCase()
  return integrations.value.filter(integration => 
    integration.name.toLowerCase().includes(query) ||
    integration.description.toLowerCase().includes(query) ||
    integration.type.toLowerCase().includes(query)
  )
})

onMounted(async () => {
  await fetchIntegrations()
})

const fetchIntegrations = async () => {
  try {
    const response = await axios.get('/api/v1/integrations')
    integrations.value = response.data
    total.value = response.data.length
  } catch (error) {
    ElMessage.error('获取集成列表失败')
    console.error('Failed to fetch integrations:', error)
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
}

const handleIntegrationStatusChange = async (integration: Integration) => {
  try {
    await axios.put(`/api/v1/integrations/${integration.id}`, {
      is_active: integration.is_active
    })
    ElMessage.success('集成状态更新成功')
  } catch (error) {
    ElMessage.error('集成状态更新失败')
    console.error('Failed to update integration status:', error)
    // 恢复原状态
    integration.is_active = !integration.is_active
  }
}

const addIntegration = async () => {
  try {
    await integrationFormRef.value?.validate()
    
    const response = await axios.post('/api/v1/integrations', {
      ...integrationForm,
      config: JSON.parse(integrationForm.config)
    })
    integrations.value.push(response.data)
    total.value++
    
    showAddIntegrationDialog.value = false
    resetIntegrationForm()
    
    ElMessage.success('集成创建成功')
  } catch (error) {
    ElMessage.error('请填写完整的集成信息')
    console.error('Validation error:', error)
  }
}

const editIntegration = (integration: Integration) => {
  editingIntegrationId.value = integration.id
  integrationForm.name = integration.name
  integrationForm.description = integration.description || ''
  integrationForm.type = integration.type
  integrationForm.config = JSON.stringify(integration.config, null, 2)
  integrationForm.is_active = integration.is_active
  selectedIntegration.value = integration
  showEditIntegrationDialog.value = true
}

const updateIntegration = async () => {
  try {
    await integrationFormRef.value?.validate()
    
    const response = await axios.put(`/api/v1/integrations/${editingIntegrationId.value}`, {
      name: integrationForm.name,
      description: integrationForm.description,
      config: JSON.parse(integrationForm.config),
      is_active: integrationForm.is_active
    })
    const index = integrations.value.findIndex(i => i.id === editingIntegrationId.value)
    if (index !== -1) {
      integrations.value[index] = response.data
    }
    if (selectedIntegration.value?.id === editingIntegrationId.value) {
      selectedIntegration.value = response.data
    }
    
    showEditIntegrationDialog.value = false
    resetIntegrationForm()
    
    ElMessage.success('集成更新成功')
  } catch (error) {
    ElMessage.error('请填写完整的集成信息')
    console.error('Validation error:', error)
  }
}

const deleteIntegration = async (integrationId: number) => {
  try {
    await axios.delete(`/api/v1/integrations/${integrationId}`)
    integrations.value = integrations.value.filter(integration => integration.id !== integrationId)
    total.value--
    if (selectedIntegration.value?.id === integrationId) {
      selectedIntegration.value = null
    }
    ElMessage.success('集成删除成功')
  } catch (error) {
    ElMessage.error('集成删除失败')
    console.error('Failed to delete integration:', error)
  }
}

const resetIntegrationForm = () => {
  integrationForm.name = ''
  integrationForm.description = ''
  integrationForm.type = 'third_party_api'
  integrationForm.config = '{}'
  integrationForm.is_active = true
}
</script>

<style scoped>
.advanced-integrations {
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

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 14px;
  max-height: 300px;
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

  .card-header .el-input {
    width: 100%;
  }
}
</style>
