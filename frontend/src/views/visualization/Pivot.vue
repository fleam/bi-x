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
            <div class="sort-container">
              <el-select v-model="form.sort_by" placeholder="选择排序字段" class="sort-field-select">
                <el-option 
                  v-for="field in allFields" 
                  :key="field.name" 
                  :label="field.name" 
                  :value="field.name" 
                />
              </el-select>
              <el-select v-model="form.sort_order" placeholder="排序顺序" class="sort-order-select">
                <el-option label="升序" value="asc" />
                <el-option label="降序" value="desc" />
              </el-select>
            </div>
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
          <el-alert
            v-if="result.sql"
            title="生成的SQL查询（简化版）"
            type="info"
            :closable="false"
            show-icon
            class="sql-alert"
          >
            <pre class="sql-code">{{ result.sql }}</pre>
          </el-alert>
          <el-alert
            v-if="result.model_sql"
            title="通过模型解析的SQL查询（原生版）"
            type="success"
            :closable="false"
            show-icon
            class="sql-alert"
          >
            <pre class="sql-code">{{ result.model_sql }}</pre>
          </el-alert>
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
  sql: string
  model_sql: string
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
  sql: '',
  model_sql: '',
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
  const dimensions = selectedModel.value.dimensions || []
  // 确保返回的是包含name属性的对象数组
  return dimensions.map(item => {
    if (typeof item === 'string') {
      return { name: item }
    } else if (typeof item === 'object' && item !== null) {
      // 如果是对象但没有name属性，尝试使用其他属性作为name
      if (!item.name) {
        // 优先使用field属性，然后是其他可能的属性
        if (item.field) {
          return { ...item, name: item.field }
        } else if (item.field_name) {
          return { ...item, name: item.field_name }
        } else {
          // 如果没有合适的属性，使用对象的字符串表示
          return { ...item, name: String(item) }
        }
      }
    }
    return item
  })
})

const availableMeasures = computed(() => {
  if (!selectedModel.value) return []
  const measures = selectedModel.value.measures || []
  // 确保返回的是包含name属性的对象数组
  return measures.map(item => {
    if (typeof item === 'string') {
      return { name: item }
    } else if (typeof item === 'object' && item !== null) {
      // 如果是对象但没有name属性，尝试使用其他属性作为name
      if (!item.name) {
        // 优先使用field属性，然后是其他可能的属性
        if (item.field) {
          return { ...item, name: item.field }
        } else if (item.field_name) {
          return { ...item, name: item.field_name }
        } else {
          // 如果没有合适的属性，使用对象的字符串表示
          return { ...item, name: String(item) }
        }
      }
    }
    return item
  })
})

const allFields = computed(() => {
  if (!selectedModel.value) return []
  const dimensions = (selectedModel.value.dimensions || []).map(item => {
    if (typeof item === 'string') {
      return { name: item }
    } else if (typeof item === 'object' && item !== null) {
      // 如果是对象但没有name属性，尝试使用其他属性作为name
      if (!item.name) {
        // 优先使用field属性，然后是其他可能的属性
        if (item.field) {
          return { ...item, name: item.field }
        } else if (item.field_name) {
          return { ...item, name: item.field_name }
        } else {
          // 如果没有合适的属性，使用对象的字符串表示
          return { ...item, name: String(item) }
        }
      }
    }
    return item
  })
  const measures = (selectedModel.value.measures || []).map(item => {
    if (typeof item === 'string') {
      return { name: item }
    } else if (typeof item === 'object' && item !== null) {
      // 如果是对象但没有name属性，尝试使用其他属性作为name
      if (!item.name) {
        // 优先使用field属性，然后是其他可能的属性
        if (item.field) {
          return { ...item, name: item.field }
        } else if (item.field_name) {
          return { ...item, name: item.field_name }
        } else {
          // 如果没有合适的属性，使用对象的字符串表示
          return { ...item, name: String(item) }
        }
      }
    }
    return item
  })
  return [...dimensions, ...measures]
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
    // 确保数据模型对象都有name属性
    dataModels.value = (response.data || []).map(model => {
      if (typeof model === 'object' && model !== null && !model.name) {
        // 如果没有name属性，尝试使用其他属性
        if (model.title) {
          return { ...model, name: model.title }
        } else if (model.label) {
          return { ...model, name: model.label }
        } else {
          return { ...model, name: `模型 ${model.id}` }
        }
      }
      return model
    })
  } catch (error) {
    ElMessage.error('获取数据模型列表失败')
    console.error('Failed to fetch data models:', error)
  }
}

const handleModelChange = async () => {
  try {
    const model = dataModels.value.find(m => m.id === form.data_model_id)
    if (model) {
      // 确保模型对象及其维度和度量都有正确的格式
      const processedModel = {
        ...model,
        // 处理维度
        dimensions: (model.dimensions || []).map(dimension => {
          if (typeof dimension === 'string') {
            return { name: dimension }
          } else if (typeof dimension === 'object' && dimension !== null) {
            if (!dimension.name) {
              if (dimension.field) {
                return { ...dimension, name: dimension.field }
              } else if (dimension.field_name) {
                return { ...dimension, name: dimension.field_name }
              } else {
                return { ...dimension, name: String(dimension) }
              }
            }
          }
          return dimension
        }),
        // 处理度量
        measures: (model.measures || []).map(measure => {
          if (typeof measure === 'string') {
            return { name: measure }
          } else if (typeof measure === 'object' && measure !== null) {
            if (!measure.name) {
              if (measure.field) {
                return { ...measure, name: measure.field }
              } else if (measure.field_name) {
                return { ...measure, name: measure.field_name }
              } else {
                return { ...measure, name: String(measure) }
              }
            }
          }
          return measure
        })
      }
      
      selectedModel.value = processedModel
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
        sql: '',
        model_sql: '',
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
    sql: '',
    model_sql: '',
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

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.page-card {
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

.button-group {
  display: flex;
  gap: 10px;
}

.filter-item {
  display: flex;
  align-items: center;
  margin-top: 10px;
  gap: 12px;
  flex-wrap: wrap;
  padding: 12px;
  background-color: #f9f9f9;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.filter-item .el-select {
  flex: 1;
  min-width: 150px;
  max-width: 200px;
}

.filter-item .el-input {
  flex: 1;
  min-width: 150px;
  max-width: 200px;
}

.filter-item .el-button {
  flex-shrink: 0;
  min-width: 80px;
}

.result-actions {
  margin-top: 20px;
  text-align: right;
}

.sql-alert {
  margin-bottom: 20px;
  overflow-x: auto;
}

.sql-code {
  margin: 0;
  padding: 12px;
  background-color: #f5f5f5;
  border-radius: 4px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  color: #333;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 300px;
  overflow-y: auto;
}

.sort-container {
  display: flex;
  gap: 15px;
  align-items: center;
  width: 100%;
  max-width: 400px;
}

.sort-field-select {
  flex: 1;
  min-width: 200px;
}

.sort-order-select {
  width: 120px;
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
    align-items: stretch;
    gap: 8px;
    padding: 10px;
  }
  
  .filter-item .el-select,
  .filter-item .el-input,
  .filter-item .el-button {
    min-width: 100%;
    max-width: 100%;
    width: 100%;
  }
  
  .sort-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    max-width: 100%;
  }
  
  .sort-field-select,
  .sort-order-select {
    width: 100%;
    min-width: unset;
  }
}
</style>
