<template>
  <div class="advanced-prediction-models">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>预测模型</h1>
          <el-button type="primary" @click="showAddModelDialog = true">
            新增模型
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>预测模型列表</span>
              <el-input
                v-model="searchQuery"
                placeholder="搜索模型"
                prefix-icon="el-icon-search"
                style="width: 300px"
              />
            </div>
          </template>
          <div class="card-content">
            <el-table :data="filteredModels" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="模型名称" />
              <el-table-column prop="model_type" label="模型类型" width="120" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getStatusType(scope.row.status)">
                    {{ getStatusLabel(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="created_by" label="创建人" width="100" />
              <el-table-column prop="created_at" label="创建时间" width="180" />
              <el-table-column label="操作" width="250" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="editModel(scope.row)">
                    编辑
                  </el-button>
                  <el-button type="success" size="small" @click="trainModel(scope.row.id)" :disabled="scope.row.status === 'training'">
                    训练
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteModel(scope.row.id)">
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

        <el-card v-if="selectedModel">
          <template #header>
            <div class="card-header">
              <span>模型详情</span>
            </div>
          </template>
          <div class="card-content">
            <el-descriptions :column="2">
              <el-descriptions-item label="模型名称">
                {{ selectedModel.name }}
              </el-descriptions-item>
              <el-descriptions-item label="模型类型">
                {{ selectedModel.model_type }}
              </el-descriptions-item>
              <el-descriptions-item label="状态">
                <el-tag :type="getStatusType(selectedModel.status)">
                  {{ getStatusLabel(selectedModel.status) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="创建人">
                {{ selectedModel.created_by }}
              </el-descriptions-item>
              <el-descriptions-item label="创建时间">
                {{ selectedModel.created_at }}
              </el-descriptions-item>
              <el-descriptions-item label="更新时间">
                {{ selectedModel.updated_at }}
              </el-descriptions-item>
              <el-descriptions-item label="模型路径">
                {{ selectedModel.model_path || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="描述" :span="2">
                {{ selectedModel.description || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="参数" :span="2">
                <pre>{{ JSON.stringify(selectedModel.parameters, null, 2) }}</pre>
              </el-descriptions-item>
              <el-descriptions-item label="训练数据" :span="2">
                <pre>{{ JSON.stringify(selectedModel.training_data, null, 2) }}</pre>
              </el-descriptions-item>
              <el-descriptions-item label="评估指标" :span="2">
                <pre v-if="selectedModel.metrics">{{ JSON.stringify(selectedModel.metrics, null, 2) }}</pre>
                <span v-else>-</span>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-main>
    </el-container>

    <!-- 添加模型对话框 -->
    <el-dialog
      v-model="showAddModelDialog"
      title="新增模型"
      width="600px"
    >
      <el-form :model="modelForm" :rules="modelRules" ref="modelFormRef" label-width="100px">
        <el-form-item label="模型名称" prop="name">
          <el-input v-model="modelForm.name" placeholder="请输入模型名称" />
        </el-form-item>
        <el-form-item label="模型类型" prop="model_type">
          <el-select v-model="modelForm.model_type" placeholder="请选择模型类型">
            <el-option label="线性回归" value="linear_regression" />
            <el-option label="逻辑回归" value="logistic_regression" />
            <el-option label="决策树" value="decision_tree" />
            <el-option label="随机森林" value="random_forest" />
            <el-option label="XGBoost" value="xgboost" />
            <el-option label="神经网络" value="neural_network" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="modelForm.description" type="textarea" placeholder="请输入模型描述" />
        </el-form-item>
        <el-form-item label="参数" prop="parameters">
          <el-input v-model="modelForm.parameters" type="textarea" placeholder="请输入模型参数（JSON格式）" />
        </el-form-item>
        <el-form-item label="训练数据" prop="training_data">
          <el-input v-model="modelForm.training_data" type="textarea" placeholder="请输入训练数据配置（JSON格式）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddModelDialog = false">取消</el-button>
          <el-button type="primary" @click="addModel">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑模型对话框 -->
    <el-dialog
      v-model="showEditModelDialog"
      title="编辑模型"
      width="600px"
    >
      <el-form :model="modelForm" :rules="modelRules" ref="modelFormRef" label-width="100px">
        <el-form-item label="模型名称" prop="name">
          <el-input v-model="modelForm.name" placeholder="请输入模型名称" />
        </el-form-item>
        <el-form-item label="模型类型" prop="model_type">
          <el-select v-model="modelForm.model_type" placeholder="请选择模型类型">
            <el-option label="线性回归" value="linear_regression" />
            <el-option label="逻辑回归" value="logistic_regression" />
            <el-option label="决策树" value="decision_tree" />
            <el-option label="随机森林" value="random_forest" />
            <el-option label="XGBoost" value="xgboost" />
            <el-option label="神经网络" value="neural_network" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="modelForm.description" type="textarea" placeholder="请输入模型描述" />
        </el-form-item>
        <el-form-item label="参数" prop="parameters">
          <el-input v-model="modelForm.parameters" type="textarea" placeholder="请输入模型参数（JSON格式）" />
        </el-form-item>
        <el-form-item label="训练数据" prop="training_data">
          <el-input v-model="modelForm.training_data" type="textarea" placeholder="请输入训练数据配置（JSON格式）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditModelDialog = false">取消</el-button>
          <el-button type="primary" @click="updateModel">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface PredictionModel {
  id: number
  name: string
  description: string
  model_type: string
  parameters: any
  training_data: any
  status: string
  model_path: string
  metrics: any
  created_by: number
  created_at: string
  updated_at: string
}

interface ModelFormData {
  name: string
  description: string
  model_type: string
  parameters: string
  training_data: string
}

const models = ref<PredictionModel[]>([])
const selectedModel = ref<PredictionModel | null>(null)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddModelDialog = ref(false)
const showEditModelDialog = ref(false)
const modelFormRef = ref<FormInstance>()
const editingModelId = ref<number>(0)

const modelForm = reactive<ModelFormData>({
  name: '',
  description: '',
  model_type: 'linear_regression',
  parameters: '{}',
  training_data: '{}'
})

const modelRules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入模型名称', trigger: 'blur' }
  ],
  model_type: [
    { required: true, message: '请选择模型类型', trigger: 'change' }
  ],
  parameters: [
    { required: true, message: '请输入模型参数', trigger: 'blur' }
  ],
  training_data: [
    { required: true, message: '请输入训练数据配置', trigger: 'blur' }
  ]
})

const filteredModels = computed(() => {
  if (!searchQuery.value) {
    return models.value
  }
  const query = searchQuery.value.toLowerCase()
  return models.value.filter(model => 
    model.name.toLowerCase().includes(query) ||
    model.model_type.toLowerCase().includes(query) ||
    model.description.toLowerCase().includes(query)
  )
})

onMounted(async () => {
  await fetchModels()
})

const fetchModels = async () => {
  try {
    const response = await axios.get('/api/v1/prediction-models')
    models.value = response.data
    total.value = response.data.length
  } catch (error) {
    ElMessage.error('获取预测模型列表失败')
    console.error('Failed to fetch prediction models:', error)
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
}

const getStatusType = (status: string): string => {
  const statusMap: Record<string, string> = {
    'created': 'info',
    'training': 'warning',
    'trained': 'success',
    'failed': 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusLabel = (status: string): string => {
  const statusMap: Record<string, string> = {
    'created': '已创建',
    'training': '训练中',
    'trained': '已训练',
    'failed': '失败'
  }
  return statusMap[status] || status
}

const addModel = async () => {
  try {
    await modelFormRef.value?.validate()
    
    const response = await axios.post('/api/v1/prediction-models', {
      ...modelForm,
      parameters: JSON.parse(modelForm.parameters),
      training_data: JSON.parse(modelForm.training_data)
    })
    models.value.push(response.data)
    total.value++
    
    showAddModelDialog.value = false
    resetModelForm()
    
    ElMessage.success('预测模型创建成功')
  } catch (error) {
    ElMessage.error('请填写完整的模型信息')
    console.error('Validation error:', error)
  }
}

const editModel = (model: PredictionModel) => {
  editingModelId.value = model.id
  modelForm.name = model.name
  modelForm.description = model.description || ''
  modelForm.model_type = model.model_type
  modelForm.parameters = JSON.stringify(model.parameters, null, 2)
  modelForm.training_data = JSON.stringify(model.training_data, null, 2)
  selectedModel.value = model
  showEditModelDialog.value = true
}

const updateModel = async () => {
  try {
    await modelFormRef.value?.validate()
    
    const response = await axios.put(`/api/v1/prediction-models/${editingModelId.value}`, {
      ...modelForm,
      parameters: JSON.parse(modelForm.parameters),
      training_data: JSON.parse(modelForm.training_data)
    })
    const index = models.value.findIndex(m => m.id === editingModelId.value)
    if (index !== -1) {
      models.value[index] = response.data
    }
    
    showEditModelDialog.value = false
    resetModelForm()
    
    ElMessage.success('预测模型更新成功')
  } catch (error) {
    ElMessage.error('请填写完整的模型信息')
    console.error('Validation error:', error)
  }
}

const deleteModel = async (modelId: number) => {
  try {
    await axios.delete(`/api/v1/prediction-models/${modelId}`)
    models.value = models.value.filter(model => model.id !== modelId)
    total.value--
    if (selectedModel.value?.id === modelId) {
      selectedModel.value = null
    }
    ElMessage.success('预测模型删除成功')
  } catch (error) {
    ElMessage.error('预测模型删除失败')
    console.error('Failed to delete prediction model:', error)
  }
}

const trainModel = async (modelId: number) => {
  try {
    const response = await axios.post(`/api/v1/prediction-models/${modelId}/train`)
    const index = models.value.findIndex(m => m.id === modelId)
    if (index !== -1) {
      models.value[index] = response.data
    }
    if (selectedModel.value?.id === modelId) {
      selectedModel.value = response.data
    }
    ElMessage.success('预测模型训练成功')
  } catch (error) {
    ElMessage.error('预测模型训练失败')
    console.error('Failed to train prediction model:', error)
  }
}

const resetModelForm = () => {
  modelForm.name = ''
  modelForm.description = ''
  modelForm.model_type = 'linear_regression'
  modelForm.parameters = '{}'
  modelForm.training_data = '{}'
}
</script>

<style scoped>
.advanced-prediction-models {
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
