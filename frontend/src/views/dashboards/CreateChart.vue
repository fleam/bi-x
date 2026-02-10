<template>
  <div class="dashboards-create-chart">
    <div class="page-header">
      <h1>新建图表</h1>
      <el-button @click="navigateTo('/dashboards')">
        返回列表
      </el-button>
    </div>
    
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>图表配置</span>
        </div>
      </template>
      <div class="card-content">
        <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" class="page-form">
              <!-- 基本信息 -->
              <el-form-item label="图表名称" prop="name">
                <el-input v-model="form.name" placeholder="请输入图表名称" />
              </el-form-item>
              <el-form-item label="描述" prop="description">
                <el-input v-model="form.description" type="textarea" placeholder="请输入图表描述" />
              </el-form-item>
              <el-form-item label="图表类型" prop="chart_type">
                <el-select v-model="form.chart_type" placeholder="请选择图表类型">
                  <el-option label="折线图" value="line" />
                  <el-option label="柱状图" value="bar" />
                  <el-option label="饼图" value="pie" />
                  <el-option label="散点图" value="scatter" />
                  <el-option label="雷达图" value="radar" />
                  <el-option label="仪表盘" value="gauge" />
                  <el-option label="热力图" value="heatmap" />
                </el-select>
              </el-form-item>
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
              
              <!-- 维度配置 -->
              <el-form-item label="维度" prop="dimensions">
                <el-select v-model="selectedDimensions" multiple placeholder="请选择维度">
                  <el-option 
                    v-for="dimension in availableDimensions" 
                    :key="dimension.name" 
                    :label="dimension.name" 
                    :value="dimension.name" 
                  />
                </el-select>
              </el-form-item>
              
              <!-- 度量配置 -->
              <el-form-item label="度量" prop="measures">
                <el-select v-model="selectedMeasures" multiple placeholder="请选择度量">
                  <el-option 
                    v-for="measure in availableMeasures" 
                    :key="measure.name" 
                    :label="measure.name" 
                    :value="measure.name" 
                  />
                </el-select>
              </el-form-item>
              
              <!-- 筛选条件 -->
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
              
              <!-- 样式配置 -->
              <el-form-item label="样式配置" prop="style">
                <el-input v-model="form.style" type="textarea" placeholder="请输入样式配置（JSON格式）" />
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handlePreview">
                  预览
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

    <el-card v-if="previewVisible" class="page-card">
      <template #header>
        <div class="card-header">
          <span>图表预览</span>
        </div>
      </template>
      <div class="card-content">
        <div ref="chartRef" class="chart-container"></div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../../utils/axios'
import * as echarts from 'echarts'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface FilterConfig {
  field: string
  operator: string
  value: string
}

interface FormData {
  name: string
  description: string
  chart_type: string
  data_model_id: number
  dimensions: any[]
  measures: any[]
  filters: FilterConfig[]
  style: string
}

interface ResultData {
  success: boolean
  data: Record<string, any>[] // 明确 data 为对象数组
  columns: string[]
  sql: string
  model_sql: string
  message: string
}

const router = useRouter()
const formRef = ref<FormInstance>()
const chartRef = ref<HTMLElement>()
const dataModels = ref<any[]>([])
const selectedModel = ref<any>(null)
const previewVisible = ref(false)
const result = ref<ResultData>({
  success: false,
  data: [],
  columns: [],
  sql: '',
  model_sql: '',
  message: ''
})
let chartInstance: echarts.ECharts | null = null

const form = reactive<FormData>({
  name: '',
  description: '',
  chart_type: '',
  data_model_id: 0,
  dimensions: [],
  measures: [],
  filters: [],
  style: '{}'
})

const selectedDimensions = ref<string[]>([])
const selectedMeasures = ref<string[]>([])

const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入图表名称', trigger: 'blur' }
  ],
  chart_type: [
    { required: true, message: '请选择图表类型', trigger: 'change' }
  ],
  data_model_id: [
    { required: true, message: '请选择数据模型', trigger: 'change' }
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

const chartData = computed(() => {
  if (!previewVisible.value || !result.value.success || !result.value.data || result.value.data.length === 0) {
    return {
      xAxis: [],
      series: []
    }
  }

  const data = result.value.data
  const columns = result.value.columns || []
  const dimensions = selectedDimensions.value
  const measures = selectedMeasures.value

  if (data.length === 0 || dimensions.length === 0 || measures.length === 0) {
    return {
      xAxis: [],
      series: []
    }
  }

  // 构建字段名映射：原始字段名 -> 实际列名
  const fieldMapping = new Map<string, string>()
  for (const originalField of [...dimensions, ...measures]) {
    // 查找对应的列名（可能是pivot_前缀的）
    const matchedColumn = columns.find(col => 
      col === originalField || 
      col === `pivot_${originalField}` ||
      col.endsWith(originalField)
    )
    if (matchedColumn) {
      fieldMapping.set(originalField, matchedColumn)
    }
  }

  // 提取x轴数据（第一个维度）
  const firstDimField = fieldMapping.get(dimensions[0]) || dimensions[0]
  const xAxisData = data.map(row => {
    const dimValue = row[firstDimField]
    return dimValue !== undefined ? dimValue : ''
  })

  // 生成series数据（每个度量一个series）
  const seriesData = measures.map(measure => {
    const measureField = fieldMapping.get(measure) || measure
    const measureValues = data.map(row => {
      const measureValue = row[measureField]
      return measureValue !== undefined && measureValue !== null ? Number(measureValue) : 0
    })
    
    return {
      name: measure,
      type: form.chart_type,
      data: measureValues
    }
  })

  return {
    xAxis: xAxisData,
    series: seriesData
  }
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
      // 重置选择
      selectedDimensions.value = []
      selectedMeasures.value = []
      form.dimensions = []
      form.measures = []
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

const handlePreview = async () => {
  try {
    await formRef.value?.validate()
    
    // 验证维度和度量
    if (selectedDimensions.value.length === 0) {
      ElMessage.warning('请至少选择一个维度')
      return
    }
    if (selectedMeasures.value.length === 0) {
      ElMessage.warning('请至少选择一个度量')
      return
    }

    // 调用后端API获取真实数据（使用字符串数组，与透视分析保持一致）
    const submitData = {
      data_model_id: form.data_model_id,
      dimensions: selectedDimensions.value,
      measures: selectedMeasures.value,
      filters: form.filters
    }

    const response = await axios.post('/api/v1/visualization/pivot-analysis', submitData)
    result.value = response.data

    previewVisible.value = true
    await nextTick()
    renderChart()
  } catch (error) {
    console.error('Validation error:', error)
    
    let errorMessage = '请填写完整的表单信息'
    if (error.response) {
      const detail = error.response.data.detail
      if (typeof detail === 'string') {
        errorMessage = detail
      } else if (typeof detail === 'object') {
        errorMessage = JSON.stringify(detail)
      } else {
        errorMessage = String(detail)
      }
    } else if (error.message) {
      errorMessage = error.message
    }
    
    ElMessage.error(errorMessage)
  }
}

const renderChart = () => {
  if (!chartRef.value) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  // 状态字段颜色映射
  const statusColors = [
    '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de',
    '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#2ec7c9'
  ]

  // 检测状态字段（通常包含status、state等关键词，包括pivot_前缀的情况）
  const statusField = selectedDimensions.value.find(dim => {
    const cleanDim = dim.replace(/^pivot_/, '').toLowerCase()
    return cleanDim.includes('status') || cleanDim.includes('state') || cleanDim.includes('状态')
  })

  // 获取状态字段的所有唯一值
  const statusValues = statusField 
    ? [...new Set(result.value.data.map(row => {
        // 查找实际的状态字段名（可能是pivot_前缀的）
        let actualField = statusField
        // 首先检查columns中是否有完全匹配的字段
        const matchedColumn = result.value.columns.find(col => 
          col === statusField || 
          col === `pivot_${statusField}` ||
          col.endsWith(statusField)
        )
        if (matchedColumn) {
          actualField = matchedColumn
        }
        return row[actualField]
      }))]
    : []

  // 为状态值分配颜色
  const statusColorMap = new Map<string, string>()
  statusValues.forEach((value, index) => {
    statusColorMap.set(String(value), statusColors[index % statusColors.length])
  })

  // 获取状态字段的实际字段名（用于后续显示具体数值）
  const getStatusFieldName = () => {
    if (!statusField) return null
    // 查找实际的状态字段名（可能是pivot_前缀的）
    const matchedColumn = result.value.columns.find(col => 
      col === statusField || 
      col === `pivot_${statusField}` ||
      col.endsWith(statusField)
    )
    return matchedColumn || statusField
  }
  const actualStatusField = getStatusFieldName()

  // 根据图表类型和数据生成配置
  const option: any = {
    title: {
      text: form.name,
      left: 'center'
    },
    tooltip: {
      trigger: form.chart_type === 'pie' ? 'item' : 'axis',
      formatter: (params: any) => {
        if (form.chart_type === 'pie') {
          return `${params.name}: ${params.value} (${params.percent}%)`
        }
        if (Array.isArray(params)) {
          const xAxisValue = params[0]?.axisValue || params[0]?.name || ''
          let tooltipResult = xAxisValue + '<br/>'
          
          // 获取当前数据点的状态值
          let statusInfo = ''
          if (actualStatusField && params[0]?.dataIndex !== undefined) {
            const dataIndex = params[0].dataIndex
            const row = result.value.data[dataIndex]
            if (row && actualStatusField in row) {
              const statusValue = row[actualStatusField]
              statusInfo = `状态: ${statusValue}<br/>`
            }
          }
          
          tooltipResult += statusInfo
          
          params.forEach((item: any) => {
            const displayValue = item.value || 0
            tooltipResult += `${item.marker} ${item.seriesName}: ${displayValue}<br/>`
          })
          return tooltipResult
        } else {
          const xAxisValue = params.axisValue || params.name || ''
          let tooltipResult = xAxisValue + '<br/>'
          
          // 获取当前数据点的状态值
          let statusInfo = ''
          if (actualStatusField && params.dataIndex !== undefined) {
            const dataIndex = params.dataIndex
            const row = result.value.data[dataIndex]
            if (row && actualStatusField in row) {
              const statusValue = row[actualStatusField]
              statusInfo = `状态: ${statusValue}<br/>`
            }
          }
          
          tooltipResult += statusInfo
          
          const displayValue = params.value || 0
          tooltipResult += `${params.marker} ${params.seriesName}: ${displayValue}`
          return tooltipResult
        }
      }
    },
    legend: {
      data: selectedMeasures.value,
      bottom: 10
    },
    xAxis: {
      type: 'category',
      data: chartData.value.xAxis
    },
    yAxis: {
      type: 'value'
    },
    series: chartData.value.series.map((seriesItem: any, index: number) => {
      const seriesConfig: any = {
        name: seriesItem.name,
        type: seriesItem.type,
        data: seriesItem.data
      }

      // 添加数据标签
      seriesConfig.label = {
        show: true,
        position: form.chart_type === 'pie' ? 'outside' : 'top',
        formatter: (params: any) => {
          if (form.chart_type === 'pie') {
            return `${params.name}: ${params.value}`
          }
          const displayValue = params.value || 0
          
          // 如果有状态字段，显示状态值
          if (actualStatusField && params.dataIndex !== undefined) {
            const dataIndex = params.dataIndex
            const row = result.value.data[dataIndex]
            if (row && actualStatusField in row) {
              const statusValue = row[actualStatusField]
              return `${displayValue}\n状态: ${statusValue}`
            }
          }
          
          return String(displayValue)
        },
        fontSize: 12,
        color: '#666'
      }

      // 如果有状态字段，为每个数据点应用对应的颜色
      if (statusField && statusValues.length > 0) {
        const fieldMapping = new Map<string, string>()
        result.value.columns.forEach(col => {
          if (col === statusField || col === `pivot_${statusField}` || col.endsWith(statusField)) {
            fieldMapping.set(statusField, col)
          }
        })
        const actualField = fieldMapping.get(statusField) || statusField
        
        seriesConfig.data = seriesItem.data.map((value: any, dataIndex: number) => {
          const row = result.value.data[dataIndex]
          const statusValue = row[actualField]
          return {
            value: value,
            itemStyle: {
              color: statusColorMap.get(String(statusValue)) || statusColors[index % statusColors.length]
            }
          }
        })
      } else {
        // 没有状态字段时，每个series使用不同颜色
        seriesConfig.itemStyle = {
          color: statusColors[index % statusColors.length]
        }
      }

      return seriesConfig
    })
  }

  // 饼图特殊处理
  if (form.chart_type === 'pie') {
    const pieData = chartData.value.xAxis.map((xValue: string, index: number) => {
      const measureValue = chartData.value.series[0].data[index]
      return {
        name: xValue,
        value: measureValue || 0
      }
    })

    option.series = [{
      name: selectedMeasures.value[0],
      type: 'pie',
      radius: ['40%', '70%'],
      data: pieData,
      label: {
        show: true,
        formatter: '{b}: {c} ({d}%)'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
    delete option.xAxis
    delete option.yAxis
  }

  chartInstance.setOption(option)

  // 响应式调整
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    
    // 验证维度和度量
    if (selectedDimensions.value.length === 0) {
      ElMessage.warning('请至少选择一个维度')
      return
    }
    if (selectedMeasures.value.length === 0) {
      ElMessage.warning('请至少选择一个度量')
      return
    }

    // 准备提交数据（转换为对象数组格式）
    const submitData = {
      name: form.name,
      description: form.description,
      chart_type: form.chart_type,
      data_model_id: form.data_model_id,
      dimensions: selectedDimensions.value.map(dim => ({ name: dim })),
      measures: selectedMeasures.value.map(measure => ({ name: measure })),
      filters: form.filters,
      style: JSON.parse(form.style)
    }

    await axios.post('/api/v1/charts', submitData)
    ElMessage.success('图表创建成功')
    navigateTo('/dashboards')
  } catch (error) {
    console.error('Submit error:', error)
    
    let errorMessage = '创建失败，请检查输入信息'
    if (error.response) {
      const detail = error.response.data.detail
      if (typeof detail === 'string') {
        errorMessage = `创建失败: ${detail}`
      } else if (typeof detail === 'object') {
        errorMessage = `创建失败: ${JSON.stringify(detail)}`
      } else {
        errorMessage = `创建失败: ${String(detail)}`
      }
    } else if (error.message) {
      errorMessage = `创建失败: ${error.message}`
    }
    
    ElMessage.error(errorMessage)
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
  selectedDimensions.value = []
  selectedMeasures.value = []
  form.dimensions = []
  form.measures = []
  form.filters = []
  form.style = '{}'
  previewVisible.value = false
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
}
</script>

<style scoped>
.dashboards-create-chart {
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

.chart-container {
  width: 100%;
  height: 400px;
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
  
  .chart-container {
    height: 300px;
  }
}
</style>
