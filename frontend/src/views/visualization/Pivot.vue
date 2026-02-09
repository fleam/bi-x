<template>
  <div class="visualization-pivot">
    <div class="page-header">
      <h1>透视分析</h1>
      <el-button @click="navigateTo('/visualization')">
        返回
      </el-button>
    </div>
    
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>透视分析配置</span>
        </div>
      </template>
      <div class="card-content">
        <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" class="page-form">
          <el-form-item label="数据模型" prop="data_model_id">
            <el-select v-model="form.data_model_id" placeholder="请选择数据模型" @change="handleModelChange">
              <el-option 
                v-for="model in dataModels" 
                :key="model.id" 
                :label="model.name" 
                :value="model.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="维度" prop="dimensions">
            <el-select v-model="form.dimensions" multiple placeholder="请选择维度">
              <el-option 
                v-for="dimension in availableDimensions" 
                :key="dimension.name" 
                :label="dimension.name" 
                :value="dimension.name" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="度量" prop="measures">
            <el-select v-model="form.measures" multiple placeholder="请选择度量">
              <el-option 
                v-for="measure in availableMeasures" 
                :key="measure.name" 
                :label="measure.name" 
                :value="measure.name" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="筛选条件" prop="filters">
            <div v-for="(filter, index) in form.filters" :key="index" class="filter-item">
              <el-select v-model="filter.field" placeholder="字段">
                <el-option 
                  v-for="field in allFields" 
                  :key="field.name" 
                  :label="field.name" 
                  :value="field.name" 
                />
              </el-select>
              <el-select v-model="filter.operator" placeholder="操作符">
                <el-option label="等于" value="=" />
                <el-option label="不等于" value="!=" />
                <el-option label="大于" value=">" />
                <el-option label="小于" value="<" />
                <el-option label="大于等于" value=">=" />
                <el-option label="小于等于" value="<=" />
                <el-option label="包含" value="like" />
              </el-select>
              <el-input v-model="filter.value" placeholder="值" />
              <el-button type="danger" size="small" @click="removeFilter(index)">
                删除
              </el-button>
            </div>
            <el-button type="primary" size="small" @click="addFilter">
              添加筛选条件
            </el-button>
          </el-form-item>
          <el-form-item label="排序" prop="sort_by">
            <el-select v-model="form.sort_by" placeholder="选择排序字段">
              <el-option 
                v-for="field in allFields" 
                :key="field.name" 
                :label="field.name" 
                :value="field.name" 
              />
            </el-select>
            <el-select v-model="form.sort_order" placeholder="排序顺序" style="margin-left: 10px;">
              <el-option label="升序" value="asc" />
              <el-option label="降序" value="desc" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <div class="button-group">
              <el-button type="primary" @click="handleSubmit">
                执行分析
              </el-button>
              <el-button @click="handleReset">
                重置
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </el-card>

    <el-card v-if="result.success" class="page-card">
      <template #header>
        <div class="card-header">
          <span>分析结果</span>
        </div>
      </template>
      <div class="card-content">
        <el-table :data="result.data" style="width: 100%" class="page-table">
          <el-table-column 
            v-for="column in result.columns" 
            :key="column" 
            :prop="column" 
            :label="column" 
          />
        </el-table>
        <div class="result-actions">
          <el-button type="primary" @click="exportResult">
            导出结果
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface FilterConfig {
  field: string
  operator: string
  value: string
}

interface FormData {
  data_model_id: number
  dimensions: string[]
  measures: string[]
  filters: FilterConfig[]
  sort_by: string
  sort_order: string
}

interface ResultData {
  success: boolean
  data: any[]
  columns: string[]
  message: string
}

const router = useRouter()
const formRef = ref<FormInstance>()
const dataModels = ref<any[]>([])
const selectedModel = ref<any>(null)
const result = ref<ResultData>({
  success: false,
  data: [],
  columns: [],
  message: ''
})

const form = reactive<FormData>({
  data_model_id: 0,
  dimensions: [],
  measures: [],
  filters: [],
  sort_by: '',
  sort_order: 'asc'
})

const rules = reactive<FormRules>({
  data_model_id: [
    { required: true, message: '请选择数据模型', trigger: 'change' }
  ],
  dimensions: [
    { required: true, message: '请至少选择一个维度', trigger: 'change' }
  ],
  measures: [
    { required: true, message: '请至少选择一个度量', trigger: 'change' }
  ]
})

const availableDimensions = computed(() => {
  if (!selectedModel.value) return []
  return selectedModel.value.dimensions || []
})

const availableMeasures = computed(() => {
  if (!selectedModel.value) return []
  return selectedModel.value.measures || []
})

const allFields = computed(() => {
  if (!selectedModel.value) return []
  return [...(selectedModel.value.dimensions || []), ...(selectedModel.value.measures || [])]
})

onMounted(async () => {
  await fetchDataModels()
})

const navigateTo = (path: string) => {
  router.push(path)
}

const fetchDataModels = async () => {
  try {
    const response = await axios.get('/api/v1/data-models')
    dataModels.value = response.data
  } catch (error) {
    ElMessage.error('获取数据模型列表失败')
    console.error('Failed to fetch data models:', error)
  }
}

const handleModelChange = async () => {
  try {
    const model = dataModels.value.find(m => m.id === form.data_model_id)
    if (model) {
      selectedModel.value = model
      // 重置表单
      form.dimensions = []
      form.measures = []
      form.filters = []
      form.sort_by = ''
      form.sort_order = 'asc'
      // 重置结果
      result.value = {
        success: false,
        data: [],
        columns: [],
        message: ''
      }
    }
  } catch (error) {
    ElMessage.error('加载数据模型失败')
    console.error('Failed to load data model:', error)
  }
}

const addFilter = () => {
  form.filters.push({
    field: '',
    operator: '=',
    value: ''
  })
}

const removeFilter = (index: number) => {
  form.filters.splice(index, 1)
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()

    // 准备提交数据
    const submitData = {
      data_model_id: form.data_model_id,
      dimensions: form.dimensions,
      measures: form.measures,
      filters: form.filters,
      sort_by: form.sort_by,
      sort_order: form.sort_order
    }

    const response = await axios.post('/api/v1/visualization/pivot-analysis', submitData)
    result.value = response.data
    ElMessage.success('透视分析成功')
  } catch (error) {
    console.error('Submit error:', error)
    if (error.response) {
      ElMessage.error(`分析失败: ${error.response.data.detail}`)
    } else {
      ElMessage.error('分析失败，请检查输入信息')
    }
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
  form.dimensions = []
  form.measures = []
  form.filters = []
  form.sort_by = ''
  form.sort_order = 'asc'
  result.value = {
    success: false,
    data: [],
    columns: [],
    message: ''
  }
}

const exportResult = () => {
  // 导出结果的逻辑
  ElMessage.success('导出功能开发中')
}
</script>

<style scoped>
.visualization-pivot {
  width: 100%;
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  padding: 16px 0;
}

.filter-item {
  display: flex;
  align-items: center;
  margin-top: 10px;
  gap: 10px;
  flex-wrap: wrap;
}

.result-actions {
  margin-top: 20px;
  text-align: right;
}

@media (max-width: 768px) {
  .page-form {
    max-width: 100%;
  }
  
  .el-form {
    label-width: 100px;
  }
  
  .filter-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
