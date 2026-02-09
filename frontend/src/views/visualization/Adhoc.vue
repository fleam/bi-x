<template>
  <div class="visualization-adhoc">
    <div class="page-header">
      <h1>即席查询</h1>
      <el-button @click="navigateTo('/visualization')">
        返回
      </el-button>
    </div>
    
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>即席查询配置</span>
        </div>
      </template>
      <div class="card-content">
        <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" class="page-form">
          <el-form-item label="数据集" prop="data_set_id">
            <el-select v-model="form.data_set_id" placeholder="请选择数据集" @change="handleDataSetChange">
              <el-option 
                v-for="dataSet in dataSets" 
                :key="dataSet.id" 
                :label="dataSet.name" 
                :value="dataSet.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="查询字段" prop="fields">
            <el-select v-model="form.fields" multiple placeholder="请选择查询字段">
              <el-option 
                v-for="field in availableFields" 
                :key="field.name" 
                :label="field.name" 
                :value="field.name" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="筛选条件" prop="filters">
            <div v-for="(filter, index) in form.filters" :key="index" class="filter-item">
              <el-select v-model="filter.field" placeholder="字段">
                <el-option 
                  v-for="field in availableFields" 
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
                  v-for="field in availableFields" 
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
          <el-form-item label="分页" prop="limit">
            <el-input-number v-model="form.limit" :min="1" :max="10000" placeholder="每页行数" />
          </el-form-item>
          <el-form-item>
            <div class="button-group">
              <el-button type="primary" @click="handleSubmit">
                执行查询
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
          <span>查询结果</span>
          <span class="result-info">共 {{ result.total }} 条记录</span>
        </div>
      </template>
      <div class="card-content">
        <el-table :data="result.data" style="width: 100%" class="page-table">
          <el-table-column 
            v-for="field in form.fields" 
            :key="field" 
            :prop="field.includes('.') ? field.split('.')[1] : field" 
            :label="field.includes('.') ? field.split('.')[1] : field" 
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
  data_set_id: number
  fields: string[]
  filters: FilterConfig[]
  sort_by: string
  sort_order: string
  limit: number
  offset: number
}

interface ResultData {
  success: boolean
  data: any[]
  total: number
  message: string
}

const router = useRouter()
const formRef = ref<FormInstance>()
const dataSets = ref<any[]>([])
const selectedDataSet = ref<any>(null)
const result = ref<ResultData>({
  success: false,
  data: [],
  total: 0,
  message: ''
})

const form = reactive<FormData>({
  data_set_id: 0,
  fields: [],
  filters: [],
  sort_by: '',
  sort_order: 'asc',
  limit: 1000,
  offset: 0
})

const rules = reactive<FormRules>({
  data_set_id: [
    { required: true, message: '请选择数据集', trigger: 'change' }
  ],
  fields: [
    { required: true, message: '请至少选择一个查询字段', trigger: 'change' }
  ]
})

const availableFields = computed(() => {
  if (!selectedDataSet.value) return []
  return selectedDataSet.value.fields || []
})

onMounted(async () => {
  await fetchDataSets()
})

const navigateTo = (path: string) => {
  router.push(path)
}

const fetchDataSets = async () => {
  try {
    const response = await axios.get('/api/v1/data-sets')
    dataSets.value = response.data
  } catch (error) {
    ElMessage.error('获取数据集列表失败')
    console.error('Failed to fetch data sets:', error)
  }
}

const handleDataSetChange = async () => {
  try {
    const dataSet = dataSets.value.find(ds => ds.id === form.data_set_id)
    if (dataSet) {
      selectedDataSet.value = dataSet
      // 重置表单
      form.fields = []
      form.filters = []
      form.limit = 1000
      form.offset = 0
      // 重置结果
      result.value = {
        success: false,
        data: [],
        total: 0,
        message: ''
      }
    }
  } catch (error) {
    ElMessage.error('加载数据集失败')
    console.error('Failed to load data set:', error)
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
      data_set_id: form.data_set_id,
      fields: form.fields,
      filters: form.filters,
      sort_by: form.sort_by,
      sort_order: form.sort_order,
      limit: form.limit,
      offset: form.offset
    }

    const response = await axios.post('/api/v1/visualization/adhoc-query', submitData)
    result.value = response.data
    ElMessage.success('即席查询成功')
  } catch (error) {
    console.error('Submit error:', error)
    if (error.response) {
      ElMessage.error(`查询失败: ${error.response.data.detail}`)
    } else {
      ElMessage.error('查询失败，请检查输入信息')
    }
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
  form.fields = []
  form.filters = []
  form.sort_by = ''
  form.sort_order = 'asc'
  form.limit = 1000
  form.offset = 0
  result.value = {
    success: false,
    data: [],
    total: 0,
    message: ''
  }
}

const exportResult = () => {
  // 导出结果的逻辑
  ElMessage.success('导出功能开发中')
}
</script>

<style scoped>
.visualization-adhoc {
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

.result-info {
  font-size: 14px;
  color: #666;
}

.card-content {
  padding: 16px 0;
}

.button-group {
  display: flex;
  gap: 10px;
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
