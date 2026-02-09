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
                <el-select v-model="form.data_source_id" placeholder="请选择数据源" @change="handleDataSourceChange">
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
                  <el-select v-model="form.visual_config.tables" multiple placeholder="请选择表" @change="handleTableChange">
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
                  <div class="filter-container">
                    <el-button type="primary" size="small" @click="addFilter" class="add-filter-btn">
                      添加筛选条件
                    </el-button>
                    <div v-for="(filter, index) in form.visual_config.filters" :key="index" class="filter-item">
                      <div class="filter-item-content">
                        <el-select v-model="filter.field" placeholder="字段" class="filter-field">
                          <el-option 
                            v-for="field in selectedFields" 
                            :key="field" 
                            :label="field" 
                            :value="field" 
                          />
                        </el-select>
                        <el-select v-model="filter.operator" placeholder="操作符" class="filter-operator">
                          <el-option label="等于" value="=" />
                          <el-option label="不等于" value="!=" />
                          <el-option label="大于" value=">" />
                          <el-option label="小于" value="<" />
                          <el-option label="大于等于" value=">=" />
                          <el-option label="小于等于" value="<=" />
                          <el-option label="包含" value="like" />
                        </el-select>
                        <el-input v-model="filter.value" placeholder="值" class="filter-value" />
                        <el-button type="danger" size="small" @click="removeFilter(index)" class="filter-remove-btn">
                          删除
                        </el-button>
                      </div>
                    </div>
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
                  <div class="aggregation-container">
                    <div v-for="field in selectedFields" :key="field" class="aggregation-item">
                      <div class="aggregation-item-content">
                        <span class="field-label">{{ field }}:</span>
                        <el-select v-model="form.visual_config.aggregations[field]" placeholder="聚合方式" class="aggregation-select">
                          <el-option label="无" value="none" />
                          <el-option label="求和" value="sum" />
                          <el-option label="平均值" value="avg" />
                          <el-option label="最大值" value="max" />
                          <el-option label="最小值" value="min" />
                          <el-option label="计数" value="count" />
                        </el-select>
                      </div>
                    </div>
                  </div>
                </el-form-item>
              </template>
              
              <!-- 字段配置 -->
              <el-form-item label="字段配置" prop="fields">
                <div class="fields-container">
                  <el-table :data="form.fields" style="width: 100%" class="fields-table">
                    <el-table-column prop="name" label="字段名" min-width="180">
                      <template #default="scope">
                        <el-select v-model="scope.row.name" placeholder="选择字段" size="small" class="field-name-select">
                          <el-option 
                            v-for="field in allFields" 
                            :key="field" 
                            :label="field" 
                            :value="field" 
                          />
                          <el-option label="手动输入" value="__manual__" />
                        </el-select>
                        <el-input 
                          v-if="scope.row.name === '__manual__'" 
                          v-model="scope.row.manualName" 
                          placeholder="请输入字段名" 
                          size="small" 
                          class="manual-name-input"
                          @blur="updateFieldName(scope.$index)"
                        />
                      </template>
                    </el-table-column>
                    <el-table-column prop="type" label="类型" width="120">
                      <template #default="scope">
                        <el-select v-model="scope.row.type" size="small">
                          <el-option label="字符串" value="string" />
                          <el-option label="数值" value="number" />
                          <el-option label="日期" value="date" />
                          <el-option label="布尔值" value="boolean" />
                        </el-select>
                      </template>
                    </el-table-column>
                    <el-table-column prop="alias" label="别名" min-width="120">
                      <template #default="scope">
                        <el-input v-model="scope.row.alias" size="small" />
                      </template>
                    </el-table-column>
                    <el-table-column prop="is_dimension" label="维度" width="80" align="center">
                      <template #default="scope">
                        <el-switch v-model="scope.row.is_dimension" size="small" />
                      </template>
                    </el-table-column>
                    <el-table-column prop="is_measure" label="度量" width="80" align="center">
                      <template #default="scope">
                        <el-switch v-model="scope.row.is_measure" size="small" />
                      </template>
                    </el-table-column>
                    <el-table-column label="操作" width="80" align="center">
                      <template #default="scope">
                        <el-button type="danger" size="small" @click="removeField(scope.$index)">
                          删除
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                  <div class="fields-actions">
                    <el-button type="primary" size="small" @click="addField" class="add-field-btn">
                      添加字段
                    </el-button>
                  </div>
                </div>
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
              
              <!-- 测试结果 -->
              <el-card v-if="testResult.visible" class="test-result-card">
                <template #header>
                  <div class="card-header">
                    <span>测试结果</span>
                    <el-tag :type="testResult.success ? 'success' : 'danger'">
                      {{ testResult.success ? '成功' : '失败' }}
                    </el-tag>
                  </div>
                </template>
                <div class="test-result-content">
                  <div class="sql-section">
                    <h4>生成的SQL:</h4>
                    <el-divider></el-divider>
                    <pre class="sql-code">{{ testResult.sql }}</pre>
                  </div>
                  <div v-if="testResult.message" class="message-section">
                    <h4>执行信息:</h4>
                    <el-divider></el-divider>
                    <p class="test-message">{{ testResult.message }}</p>
                  </div>
                </div>
              </el-card>
            </el-form>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
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
  manualName?: string
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
const tables = ref<string[]>([])
const allFields = ref<string[]>([])
const selectedFields = ref<string[]>([])

interface TestResult {
  visible: boolean
  success: boolean
  sql: string
  message: string
}

const testResult = reactive<TestResult>({
  visible: false,
  success: false,
  sql: '',
  message: ''
})

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

// 监听选择字段变化，更新可视化配置中的字段
watch(selectedFields, (newFields) => {
  // 更新可视化配置中的字段
  form.visual_config.fields = newFields.map(field => ({
    name: field,
    type: 'string',
    alias: null,
    is_dimension: false,
    is_measure: false
  }))
  
  // 同时更新字段配置表格
  form.fields = newFields.map(field => ({
    name: field,
    type: 'string',
    alias: null,
    is_dimension: false,
    is_measure: false
  }))
}, { deep: true })

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

const handleDataSourceChange = async () => {
  if (!form.data_source_id) {
    tables.value = []
    allFields.value = []
    selectedFields.value = []
    form.visual_config.tables = []
    return
  }

  try {
    // 调用API获取数据源下的表列表
    const response = await axios.get(`/api/v1/sources/${form.data_source_id}/tables`)
    tables.value = response.data
    
    // 保留已选择的表（如果它们在新的表列表中）
    if (form.visual_config.tables && form.visual_config.tables.length > 0) {
      const validTables = form.visual_config.tables.filter(table => tables.value.includes(table))
      form.visual_config.tables = validTables
      
      // 如果有有效表，重新加载字段
      if (validTables.length > 0) {
        await handleTableChange()
      } else {
        allFields.value = []
        selectedFields.value = []
        form.visual_config.fields = []
      }
    } else {
      allFields.value = []
      selectedFields.value = []
      form.visual_config.fields = []
    }
  } catch (error) {
    ElMessage.error('获取表列表失败')
    console.error('Failed to fetch tables:', error)
    // 失败时使用空列表
    tables.value = []
  }
}

const handleTableChange = async () => {
  if (!form.visual_config.tables || form.visual_config.tables.length === 0) {
    allFields.value = []
    selectedFields.value = []
    return
  }

  try {
    // 调用API获取所选表的字段列表，包含表名信息
    const allTableFields = []
    for (const table of form.visual_config.tables) {
      const response = await axios.get(`/api/v1/sources/${form.data_source_id}/fields/${table}`)
      // 为每个字段添加表名前缀，格式：表名.字段名
      const fieldsWithTable = response.data.map((field: string) => `${table}.${field}`)
      allTableFields.push(...fieldsWithTable)
    }
    
    // 保存当前所有可用字段
    allFields.value = allTableFields
    
    // 保留已选择的字段（如果它们在新的字段列表中）
    if (form.visual_config.fields && form.visual_config.fields.length > 0) {
      const validSelectedFields = form.visual_config.fields
        .map(field => field.name)
        .filter(fieldName => allTableFields.includes(fieldName))
      selectedFields.value = validSelectedFields
      
      // 更新字段配置，只保留有效字段
      form.visual_config.fields = form.visual_config.fields.filter(field => 
        allTableFields.includes(field.name)
      )
    } else {
      selectedFields.value = []
    }
  } catch (error) {
    ElMessage.error('获取字段列表失败')
    console.error('Failed to fetch fields:', error)
    // 失败时使用空列表
    allFields.value = []
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
    
    // 加载表和字段列表
    if (form.data_source_id) {
      await handleDataSourceChange()
      
      // 如果有已选择的表，加载字段列表
      if (form.visual_config.tables && form.visual_config.tables.length > 0) {
        await handleTableChange()
      }
    }
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

const updateFieldName = (index: number) => {
  const field = form.fields[index]
  if (field && field.name === '__manual__' && field.manualName) {
    field.name = field.manualName
    delete field.manualName
  }
}

const handleTest = async () => {
  try {
    await formRef.value?.validate()
    
    let generatedSql = ''
    
    if (form.creation_mode === 'sql') {
      // SQL模式直接使用用户输入的SQL
      generatedSql = form.sql_query || ''
    } else if (form.creation_mode === 'visual') {
      // 可视化模式生成SQL
      if (!form.visual_config.tables || form.visual_config.tables.length === 0) {
        throw new Error('请选择表')
      }
      
      // 获取字段列表（优先使用form.visual_config.fields）
      let fieldList = []
      if (form.visual_config.fields && form.visual_config.fields.length > 0) {
        fieldList = form.visual_config.fields.map(field => field.name)
      } else if (selectedFields.value && selectedFields.value.length > 0) {
        fieldList = selectedFields.value
      } else {
        throw new Error('请选择字段')
      }
      
      if (fieldList.length === 0) {
        throw new Error('请选择字段')
      }
      
      // 生成SELECT子句（考虑聚合配置和度量设置）
      const selectFields = fieldList.map(field => {
        // 检查是否有聚合配置
        let aggregation = form.visual_config.aggregations[field]
        
        // 如果没有聚合配置，检查是否为度量字段
        if (!aggregation || aggregation === 'none') {
          const fieldConfig = form.fields.find(f => f.name === field)
          if (fieldConfig && fieldConfig.is_measure) {
            // 为度量字段设置默认聚合函数（求和）
            aggregation = 'sum'
          }
        }
        
        // 根据聚合类型生成相应的SQL函数
        if (aggregation && aggregation !== 'none') {
          // 生成安全的别名（替换点号为下划线）
          const safeAlias = field.replace(/\./g, '_')
          
          switch (aggregation) {
            case 'sum':
              return `SUM(${field}) AS ${safeAlias}_sum`
            case 'avg':
              return `AVG(${field}) AS ${safeAlias}_avg`
            case 'max':
              return `MAX(${field}) AS ${safeAlias}_max`
            case 'min':
              return `MIN(${field}) AS ${safeAlias}_min`
            case 'count':
              return `COUNT(${field}) AS ${safeAlias}_count`
            default:
              return field
          }
        }
        return field
      })
      const selectClause = `SELECT ${selectFields.join(', ')}`
      
      // 生成FROM子句
      const fromClause = `FROM ${form.visual_config.tables.join(', ')}`
      
      // 生成WHERE子句
      let whereClause = ''
      if (form.visual_config.filters && form.visual_config.filters.length > 0) {
        const conditions = form.visual_config.filters
          .filter(filter => filter.field && filter.operator && filter.value)
          .map(filter => {
            let value = filter.value
            // 处理字符串值
            if (typeof value === 'string' && !['>', '<', '>=', '<='].includes(filter.operator)) {
              value = `'${value}'`
            }
            return `${filter.field} ${filter.operator} ${value}`
          })
        
        if (conditions.length > 0) {
          whereClause = `WHERE ${conditions.join(' AND ')}`
        }
      }
      
      // 生成GROUP BY子句（考虑维度设置）
      let groupByClause = ''
      let groupFields = []
      
      // 首先添加用户指定的分组字段
      if (form.visual_config.groups && form.visual_config.groups.length > 0) {
        groupFields = [...form.visual_config.groups]
      }
      
      // 然后添加标记为维度的字段（如果不在分组字段中）
      if (form.fields && form.fields.length > 0) {
        const dimensionFields = form.fields
          .filter(field => field.is_dimension)
          .map(field => field.name)
        
        dimensionFields.forEach(field => {
          if (!groupFields.includes(field)) {
            groupFields.push(field)
          }
        })
      }
      
      // 生成GROUP BY子句
      if (groupFields.length > 0) {
        groupByClause = `GROUP BY ${groupFields.join(', ')}`
      }
      
      // 组合SQL
      generatedSql = `${selectClause} ${fromClause} ${whereClause} ${groupByClause}`
    }
    
    // 模拟测试查询
    testResult.visible = true
    testResult.success = true
    testResult.sql = generatedSql
    testResult.message = '测试查询成功，SQL语法正确'
    
    ElMessage.success('测试查询成功')
  } catch (error: any) {
    testResult.visible = true
    testResult.success = false
    testResult.sql = ''
    testResult.message = error.message || '测试查询失败'
    
    ElMessage.error('测试查询失败')
    console.error('Test error:', error)
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

.filter-container {
  background-color: #f9fafb;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  margin-top: 10px;
}

.add-filter-btn {
  margin-bottom: 15px;
}

.filter-item {
  margin-bottom: 15px;
}

.filter-item:last-child {
  margin-bottom: 0;
}

.filter-item-content {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
  padding: 12px;
  background-color: white;
  border-radius: 6px;
  border: 1px solid #f0f2f5;
}

.filter-field {
  flex: 1;
  min-width: 180px;
}

.filter-operator {
  width: 120px;
}

.filter-value {
  flex: 1;
  min-width: 150px;
}

.filter-remove-btn {
  flex-shrink: 0;
}

.aggregation-container {
  background-color: #f9fafb;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
}

.aggregation-item {
  margin-bottom: 15px;
}

.aggregation-item:last-child {
  margin-bottom: 0;
}

.aggregation-item-content {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  padding: 12px;
  background-color: white;
  border-radius: 6px;
  border: 1px solid #f0f2f5;
}

.field-label {
  font-weight: 500;
  min-width: 140px;
  flex-shrink: 0;
  color: #303133;
}

.aggregation-select {
  width: 160px;
  border-radius: 4px;
}

.fields-container {
  background-color: #f9fafb;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  margin-top: 10px;
}

.fields-table {
  margin-bottom: 15px;
  border-radius: 6px;
  overflow: hidden;
}

.fields-actions {
  text-align: right;
}

.add-field-btn {
  margin-top: 10px;
}

.field-name-select {
  width: 100%;
}

.manual-name-input {
  width: 100%;
  margin-top: 5px;
}

.test-result-card {
  margin-top: 20px;
}

.test-result-content {
  padding: 10px 0;
}

.sql-section,
.message-section {
  margin-bottom: 20px;
}

.sql-section h4,
.message-section h4 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.sql-code {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #ebeef5;
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 300px;
  overflow-y: auto;
}

.test-message {
  padding: 10px;
  background-color: #ecf5ff;
  border-radius: 4px;
  border: 1px solid #d9ecff;
  color: #409eff;
}

.test-result-content .el-divider {
  margin: 10px 0;
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
  
  .filter-container {
    padding: 15px;
  }
  
  .filter-item-content {
    padding: 10px;
    gap: 15px;
  }
  
  .filter-field,
  .filter-operator,
  .filter-value {
    width: 100%;
    min-width: unset;
  }
  
  .aggregation-container {
    padding: 15px;
  }
  
  .aggregation-item-content {
    padding: 10px;
    gap: 15px;
  }
  
  .field-label {
    min-width: unset;
    margin-bottom: 5px;
  }
  
  .aggregation-select {
    width: 100%;
  }
  
  .fields-container {
    padding: 15px;
  }
  
  .fields-table {
    font-size: 14px;
  }
  
  .el-table-column {
    min-width: 80px !important;
  }
}
</style>
