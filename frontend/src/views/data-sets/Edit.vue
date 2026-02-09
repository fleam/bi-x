<template>
  <div class="data-sets-edit">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>编辑数据集</h1>
          <el-button @click="navigateTo('/data-sets')">
            返回列表
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card v-if="loading">
          <div class="loading-content">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载中...</span>
          </div>
        </el-card>
        <el-card v-else>
          <template #header>
            <div class="card-header">
              <span>数据集配置</span>
            </div>
          </template>
          <div class="card-content">
            <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
              <!-- 基本信息 -->
              <el-form-item label="数据集名称" prop="name">
                <el-input v-model="form.name" placeholder="请输入数据集名称" />
              </el-form-item>
              <el-form-item label="描述" prop="description">
                <el-input v-model="form.description" type="textarea" placeholder="请输入数据集描述" />
              </el-form-item>
              <el-form-item label="数据源" prop="data_source_id">
                <el-select v-model="form.data_source_id" placeholder="请选择数据源">
                  <el-option 
                    v-for="source in dataSources" 
                    :key="source.id" 
                    :label="source.name" 
                    :value="source.id" 
                  />
                </el-select>
              </el-form-item>
              <el-form-item label="创建模式" prop="creation_mode">
                <el-select v-model="form.creation_mode" placeholder="请选择创建模式" @change="handleModeChange">
                  <el-option label="可视化模式" value="visual" />
                  <el-option label="SQL模式" value="sql" />
                </el-select>
              </el-form-item>
              
              <!-- SQL模式 -->
              <template v-if="form.creation_mode === 'sql'">
                <el-form-item label="SQL查询" prop="sql_query">
                  <el-input v-model="form.sql_query" type="textarea" :rows="10" placeholder="请输入SQL查询语句" />
                </el-form-item>
              </template>
              
              <!-- 可视化模式 -->
              <template v-if="form.creation_mode === 'visual'">
                <el-form-item label="选择表" prop="visual_config.tables">
                  <el-select v-model="form.visual_config.tables" multiple placeholder="请选择表">
                    <el-option 
                      v-for="table in tables" 
                      :key="table" 
                      :label="table" 
                      :value="table" 
                    />
                  </el-select>
                </el-form-item>
                <el-form-item label="选择字段" prop="visual_config.fields">
                  <el-select v-model="selectedFields" multiple placeholder="请选择字段">
                    <el-option 
                      v-for="field in allFields" 
                      :key="field" 
                      :label="field" 
                      :value="field" 
                    />
                  </el-select>
                </el-form-item>
                <el-form-item label="筛选条件" prop="visual_config.filters">
                  <el-button type="primary" size="small" @click="addFilter">
                    添加筛选条件
                  </el-button>
                  <div v-for="(filter, index) in form.visual_config.filters" :key="index" class="filter-item">
                    <el-select v-model="filter.field" placeholder="字段">
                      <el-option 
                        v-for="field in selectedFields" 
                        :key="field" 
                        :label="field" 
                        :value="field" 
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
                </el-form-item>
                <el-form-item label="分组字段" prop="visual_config.groups">
                  <el-select v-model="form.visual_config.groups" multiple placeholder="请选择分组字段">
                    <el-option 
                      v-for="field in selectedFields" 
                      :key="field" 
                      :label="field" 
                      :value="field" 
                    />
                  </el-select>
                </el-form-item>
                <el-form-item label="聚合配置" prop="visual_config.aggregations">
                  <div v-for="field in selectedFields" :key="field" class="aggregation-item">
                    <span>{{ field }}:</span>
                    <el-select v-model="form.visual_config.aggregations[field]" placeholder="聚合方式">
                      <el-option label="无" value="none" />
                      <el-option label="求和" value="sum" />
                      <el-option label="平均值" value="avg" />
                      <el-option label="最大值" value="max" />
                      <el-option label="最小值" value="min" />
                      <el-option label="计数" value="count" />
                    </el-select>
                  </div>
                </el-form-item>
              </template>
              
              <!-- 字段配置 -->
              <el-form-item label="字段配置" prop="fields">
                <el-table :data="form.fields" style="width: 100%">
                  <el-table-column prop="name" label="字段名" />
                  <el-table-column prop="type" label="类型">
                    <template #default="scope">
                      <el-select v-model="scope.row.type">
                        <el-option label="字符串" value="string" />
                        <el-option label="数值" value="number" />
                        <el-option label="日期" value="date" />
                        <el-option label="布尔值" value="boolean" />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="alias" label="别名">
                    <template #default="scope">
                      <el-input v-model="scope.row.alias" />
                    </template>
                  </el-table-column>
                  <el-table-column prop="is_dimension" label="维度">
                    <template #default="scope">
                      <el-switch v-model="scope.row.is_dimension" />
                    </template>
                  </el-table-column>
                  <el-table-column prop="is_measure" label="度量">
                    <template #default="scope">
                      <el-switch v-model="scope.row.is_measure" />
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button type="danger" size="small" @click="removeField(scope.$index)">
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <el-button type="primary" size="small" @click="addField">
                  添加字段
                </el-button>
              </el-form-item>
              
              <!-- 刷新间隔 -->
              <el-form-item label="刷新间隔（秒）" prop="refresh_interval">
                <el-input-number v-model="form.refresh_interval" :min="1" placeholder="请输入刷新间隔" />
              </el-form-item>
              <el-form-item label="是否启用" prop="is_active">
                <el-switch v-model="form.is_active" />
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handleTest">
                  测试查询
                </el-button>
                <el-button type="success" @click="handleSubmit">
                  保存
                </el-button>
                <el-button @click="handleReset">
                  重置
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules, ElLoading } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'

interface FieldConfig {
  name: string
  type: string
  alias: string | null
  is_dimension: boolean
  is_measure: boolean
}

interface VisualConfig {
  tables: string[]
  fields: FieldConfig[]
  filters: any[]
  groups: string[]
  aggregations: Record<string, string>
}

interface FormData {
  id: number
  name: string
  description: string
  data_source_id: number
  creation_mode: string
  sql_query: string | null
  visual_config: VisualConfig
  fields: FieldConfig[]
  refresh_interval: number
  is_active: boolean
}

const router = useRouter()
const route = useRoute()
const formRef = ref<FormInstance>()
const loading = ref(true)
const dataSources = ref<any[]>([])
const tables = ref<string[]>(['table1', 'table2', 'table3']) // 模拟数据
const allFields = ref<string[]>(['field1', 'field2', 'field3', 'field4', 'field5']) // 模拟数据
const selectedFields = ref<string[]>([])

const form = reactive<FormData>({
  id: 0,
  name: '',
  description: '',
  data_source_id: 0,
  creation_mode: '',
  sql_query: null,
  visual_config: {
    tables: [],
    fields: [],
    filters: [],
    groups: [],
    aggregations: {}
  },
  fields: [],
  refresh_interval: 300,
  is_active: true
})

const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入数据集名称', trigger: 'blur' }
  ],
  data_source_id: [
    { required: true, message: '请选择数据源', trigger: 'change' }
  ],
  creation_mode: [
    { required: true, message: '请选择创建模式', trigger: 'change' }
  ],
  sql_query: [
    { required: form.creation_mode === 'sql', message: '请输入SQL查询语句', trigger: 'blur' }
  ],
  visual_config: [
    { required: form.creation_mode === 'visual', message: '请配置可视化参数', trigger: 'change' }
  ],
  fields: [
    { required: true, message: '请配置字段', trigger: 'change' }
  ]
})

onMounted(async () => {
  await fetchDataSources()
  await fetchDataSet()
})

const navigateTo = (path: string) => {
  router.push(path)
}

const fetchDataSources = async () => {
  try {
    const response = await axios.get('/api/v1/sources/')
    dataSources.value = response.data
  } catch (error) {
    ElMessage.error('获取数据源列表失败')
    console.error('Failed to fetch data sources:', error)
  }
}

const fetchDataSet = async () => {
  try {
    const id = route.params.id
    if (!id) {
      ElMessage.error('数据集ID不能为空')
      navigateTo('/data-sets')
      return
    }

    const response = await axios.get(`/api/v1/data-sets/${id}`)
    const dataSet = response.data

    // 填充表单数据
    form.id = dataSet.id
    form.name = dataSet.name
    form.description = dataSet.description || ''
    form.data_source_id = dataSet.data_source_id
    form.creation_mode = dataSet.creation_mode
    form.sql_query = dataSet.sql_query
    form.visual_config = dataSet.visual_config || {
      tables: [],
      fields: [],
      filters: [],
      groups: [],
      aggregations: {}
    }
    form.fields = dataSet.fields
    form.refresh_interval = dataSet.refresh_interval
    form.is_active = dataSet.is_active
  } catch (error) {
    ElMessage.error('加载数据集失败')
    console.error('Failed to fetch data set:', error)
    navigateTo('/data-sets')
  } finally {
    loading.value = false
  }
}

const handleModeChange = () => {
  // 重置相关字段
  if (form.creation_mode === 'sql') {
    form.sql_query = form.sql_query || ''
    form.visual_config = {
      tables: [],
      fields: [],
      filters: [],
      groups: [],
      aggregations: {}
    }
  } else if (form.creation_mode === 'visual') {
    form.sql_query = null
  }
}

const addFilter = () => {
  form.visual_config.filters.push({
    field: '',
    operator: '=',
    value: ''
  })
}

const removeFilter = (index: number) => {
  form.visual_config.filters.splice(index, 1)
}

const addField = () => {
  form.fields.push({
    name: '',
    type: 'string',
    alias: null,
    is_dimension: false,
    is_measure: false
  })
}

const removeField = (index: number) => {
  form.fields.splice(index, 1)
}

const handleTest = async () => {
  try {
    await formRef.value?.validate()
    // 这里可以添加测试查询的逻辑
    ElMessage.success('测试查询成功')
  } catch (error) {
    ElMessage.error('请填写完整的表单信息')
    console.error('Validation error:', error)
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()

    // 准备提交数据
    const submitData = {
      name: form.name,
      description: form.description,
      data_source_id: form.data_source_id,
      creation_mode: form.creation_mode,
      sql_query: form.sql_query,
      visual_config: form.visual_config,
      fields: form.fields,
      refresh_interval: form.refresh_interval,
      is_active: form.is_active
    }

    await axios.put(`/api/v1/data-sets/${form.id}`, submitData)
    ElMessage.success('数据集更新成功')
    navigateTo('/data-sets')
  } catch (error) {
    console.error('Submit error:', error)
    if (error.response) {
      ElMessage.error(`更新失败: ${error.response.data.detail}`)
    } else {
      ElMessage.error('更新失败，请检查输入信息')
    }
  }
}

const handleReset = () => {
  fetchDataSet()
}
</script>

<style scoped>
.data-sets-edit {
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

.loading-content {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
}

.loading-content .el-icon {
  margin-right: 10px;
  font-size: 24px;
}

.filter-item {
  display: flex;
  align-items: center;
  margin-top: 10px;
  gap: 10px;
}

.aggregation-item {
  display: flex;
  align-items: center;
  margin-top: 10px;
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

  .filter-item,
  .aggregation-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
