<template>
  <div class="advanced-ai-analyses">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>AI分析</h1>
          <el-button type="primary" @click="showAddAnalysisDialog = true">
            新增分析
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>AI分析列表</span>
              <el-input
                v-model="searchQuery"
                placeholder="搜索分析"
                prefix-icon="el-icon-search"
                style="width: 300px"
              />
            </div>
          </template>
          <div class="card-content">
            <el-table :data="filteredAnalyses" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="分析名称" />
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
                  <el-button type="primary" size="small" @click="editAnalysis(scope.row)">
                    编辑
                  </el-button>
                  <el-button type="success" size="small" @click="runAnalysis(scope.row.id)" :disabled="scope.row.status === 'running'">
                    执行
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteAnalysis(scope.row.id)">
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

        <el-card v-if="selectedAnalysis">
          <template #header>
            <div class="card-header">
              <span>分析详情</span>
            </div>
          </template>
          <div class="card-content">
            <el-descriptions :column="2">
              <el-descriptions-item label="分析名称">
                {{ selectedAnalysis.name }}
              </el-descriptions-item>
              <el-descriptions-item label="模型类型">
                {{ selectedAnalysis.model_type }}
              </el-descriptions-item>
              <el-descriptions-item label="状态">
                <el-tag :type="getStatusType(selectedAnalysis.status)">
                  {{ getStatusLabel(selectedAnalysis.status) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="创建人">
                {{ selectedAnalysis.created_by }}
              </el-descriptions-item>
              <el-descriptions-item label="创建时间">
                {{ selectedAnalysis.created_at }}
              </el-descriptions-item>
              <el-descriptions-item label="更新时间">
                {{ selectedAnalysis.updated_at }}
              </el-descriptions-item>
              <el-descriptions-item label="描述" :span="2">
                {{ selectedAnalysis.description || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="参数" :span="2">
                <pre>{{ JSON.stringify(selectedAnalysis.parameters, null, 2) }}</pre>
              </el-descriptions-item>
              <el-descriptions-item label="数据源" :span="2">
                <pre>{{ JSON.stringify(selectedAnalysis.data_source, null, 2) }}</pre>
              </el-descriptions-item>
              <el-descriptions-item label="结果" :span="2">
                <pre v-if="selectedAnalysis.result">{{ JSON.stringify(selectedAnalysis.result, null, 2) }}</pre>
                <span v-else>-</span>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-main>
    </el-container>

    <!-- 添加分析对话框 -->
    <el-dialog
      v-model="showAddAnalysisDialog"
      title="新增分析"
      width="600px"
    >
      <el-form :model="analysisForm" :rules="analysisRules" ref="analysisFormRef" label-width="100px">
        <el-form-item label="分析名称" prop="name">
          <el-input v-model="analysisForm.name" placeholder="请输入分析名称" />
        </el-form-item>
        <el-form-item label="模型类型" prop="model_type">
          <el-select v-model="analysisForm.model_type" placeholder="请选择模型类型">
            <el-option label="趋势分析" value="trend_analysis" />
            <el-option label="异常检测" value="anomaly_detection" />
            <el-option label="预测模型" value="prediction" />
            <el-option label="聚类分析" value="clustering" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="analysisForm.description" type="textarea" placeholder="请输入分析描述" />
        </el-form-item>
        <el-form-item label="参数" prop="parameters">
          <el-input v-model="analysisForm.parameters" type="textarea" placeholder="请输入参数（JSON格式）" />
        </el-form-item>
        <el-form-item label="数据源" prop="data_source">
          <el-input v-model="analysisForm.data_source" type="textarea" placeholder="请输入数据源配置（JSON格式）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddAnalysisDialog = false">取消</el-button>
          <el-button type="primary" @click="addAnalysis">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑分析对话框 -->
    <el-dialog
      v-model="showEditAnalysisDialog"
      title="编辑分析"
      width="600px"
    >
      <el-form :model="analysisForm" :rules="analysisRules" ref="analysisFormRef" label-width="100px">
        <el-form-item label="分析名称" prop="name">
          <el-input v-model="analysisForm.name" placeholder="请输入分析名称" />
        </el-form-item>
        <el-form-item label="模型类型" prop="model_type">
          <el-select v-model="analysisForm.model_type" placeholder="请选择模型类型">
            <el-option label="趋势分析" value="trend_analysis" />
            <el-option label="异常检测" value="anomaly_detection" />
            <el-option label="预测模型" value="prediction" />
            <el-option label="聚类分析" value="clustering" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="analysisForm.description" type="textarea" placeholder="请输入分析描述" />
        </el-form-item>
        <el-form-item label="参数" prop="parameters">
          <el-input v-model="analysisForm.parameters" type="textarea" placeholder="请输入参数（JSON格式）" />
        </el-form-item>
        <el-form-item label="数据源" prop="data_source">
          <el-input v-model="analysisForm.data_source" type="textarea" placeholder="请输入数据源配置（JSON格式）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditAnalysisDialog = false">取消</el-button>
          <el-button type="primary" @click="updateAnalysis">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface AIAnalysis {
  id: number
  name: string
  description: string
  model_type: string
  parameters: any
  data_source: any
  status: string
  result: any
  created_by: number
  created_at: string
  updated_at: string
}

interface AnalysisFormData {
  name: string
  description: string
  model_type: string
  parameters: string
  data_source: string
}

const analyses = ref<AIAnalysis[]>([])
const selectedAnalysis = ref<AIAnalysis | null>(null)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddAnalysisDialog = ref(false)
const showEditAnalysisDialog = ref(false)
const analysisFormRef = ref<FormInstance>()
const editingAnalysisId = ref<number>(0)

const analysisForm = reactive<AnalysisFormData>({
  name: '',
  description: '',
  model_type: 'trend_analysis',
  parameters: '{}',
  data_source: '{}'
})

const analysisRules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入分析名称', trigger: 'blur' }
  ],
  model_type: [
    { required: true, message: '请选择模型类型', trigger: 'change' }
  ],
  parameters: [
    { required: true, message: '请输入参数', trigger: 'blur' }
  ],
  data_source: [
    { required: true, message: '请输入数据源配置', trigger: 'blur' }
  ]
})

const filteredAnalyses = computed(() => {
  if (!searchQuery.value) {
    return analyses.value
  }
  const query = searchQuery.value.toLowerCase()
  return analyses.value.filter(analysis => 
    analysis.name.toLowerCase().includes(query) ||
    analysis.model_type.toLowerCase().includes(query) ||
    analysis.description.toLowerCase().includes(query)
  )
})

onMounted(async () => {
  await fetchAnalyses()
})

const fetchAnalyses = async () => {
  try {
    const response = await axios.get('/api/v1/ai-analyses')
    analyses.value = response.data
    total.value = response.data.length
  } catch (error) {
    ElMessage.error('获取AI分析列表失败')
    console.error('Failed to fetch AI analyses:', error)
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
    'pending': 'info',
    'running': 'warning',
    'completed': 'success',
    'failed': 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusLabel = (status: string): string => {
  const statusMap: Record<string, string> = {
    'pending': '待执行',
    'running': '执行中',
    'completed': '已完成',
    'failed': '失败'
  }
  return statusMap[status] || status
}

const addAnalysis = async () => {
  try {
    await analysisFormRef.value?.validate()
    
    const response = await axios.post('/api/v1/ai-analyses', {
      ...analysisForm,
      parameters: JSON.parse(analysisForm.parameters),
      data_source: JSON.parse(analysisForm.data_source)
    })
    analyses.value.push(response.data)
    total.value++
    
    showAddAnalysisDialog.value = false
    resetAnalysisForm()
    
    ElMessage.success('AI分析创建成功')
  } catch (error) {
    ElMessage.error('请填写完整的分析信息')
    console.error('Validation error:', error)
  }
}

const editAnalysis = (analysis: AIAnalysis) => {
  editingAnalysisId.value = analysis.id
  analysisForm.name = analysis.name
  analysisForm.description = analysis.description || ''
  analysisForm.model_type = analysis.model_type
  analysisForm.parameters = JSON.stringify(analysis.parameters, null, 2)
  analysisForm.data_source = JSON.stringify(analysis.data_source, null, 2)
  selectedAnalysis.value = analysis
  showEditAnalysisDialog.value = true
}

const updateAnalysis = async () => {
  try {
    await analysisFormRef.value?.validate()
    
    const response = await axios.put(`/api/v1/ai-analyses/${editingAnalysisId.value}`, {
      ...analysisForm,
      parameters: JSON.parse(analysisForm.parameters),
      data_source: JSON.parse(analysisForm.data_source)
    })
    const index = analyses.value.findIndex(a => a.id === editingAnalysisId.value)
    if (index !== -1) {
      analyses.value[index] = response.data
    }
    
    showEditAnalysisDialog.value = false
    resetAnalysisForm()
    
    ElMessage.success('AI分析更新成功')
  } catch (error) {
    ElMessage.error('请填写完整的分析信息')
    console.error('Validation error:', error)
  }
}

const deleteAnalysis = async (analysisId: number) => {
  try {
    await axios.delete(`/api/v1/ai-analyses/${analysisId}`)
    analyses.value = analyses.value.filter(analysis => analysis.id !== analysisId)
    total.value--
    if (selectedAnalysis.value?.id === analysisId) {
      selectedAnalysis.value = null
    }
    ElMessage.success('AI分析删除成功')
  } catch (error) {
    ElMessage.error('AI分析删除失败')
    console.error('Failed to delete AI analysis:', error)
  }
}

const runAnalysis = async (analysisId: number) => {
  try {
    const response = await axios.post(`/api/v1/ai-analyses/${analysisId}/run`)
    const index = analyses.value.findIndex(a => a.id === analysisId)
    if (index !== -1) {
      analyses.value[index] = response.data
    }
    if (selectedAnalysis.value?.id === analysisId) {
      selectedAnalysis.value = response.data
    }
    ElMessage.success('AI分析执行成功')
  } catch (error) {
    ElMessage.error('AI分析执行失败')
    console.error('Failed to run AI analysis:', error)
  }
}

const resetAnalysisForm = () => {
  analysisForm.name = ''
  analysisForm.description = ''
  analysisForm.model_type = 'trend_analysis'
  analysisForm.parameters = '{}'
  analysisForm.data_source = '{}'
}
</script>

<style scoped>
.advanced-ai-analyses {
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
