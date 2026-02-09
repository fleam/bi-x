<template>
  <div class="dashboards-edit-chart">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>编辑图表</h1>
          <el-button @click="navigateTo('/dashboards')">
            返回列表
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>图表配置</span>
            </div>
          </template>
          <div class="card-content">
            <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
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
              
              <!-- 状态 -->
              <el-form-item label="状态" prop="is_active">
                <el-switch v-model="form.is_active" />
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

        <el-card v-if="previewVisible">
          <template #header>
            <div class="card-header">
              <span>图表预览</span>
            </div>
          </template>
          <div class="card-content">
            <div ref="chartRef" class="chart-container"></div>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
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
  is_active: boolean
}

const router = useRouter()
const route = useRoute()
const formRef = ref<FormInstance>()
const chartRef = ref<HTMLElement>()
const dataModels = ref<any[]>([])
const selectedModel = ref<any>(null)
const previewVisible = ref(false)
let chartInstance: echarts.ECharts | null = null

const form = reactive<FormData>({
  name: '',
  description: '',
  chart_type: '',
  data_model_id: 0,
  dimensions: [],
  measures: [],
  filters: [],
  style: '{}',
  is_active: true
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
  await loadChartData()
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

const loadChartData = async () => {
  const chartId = route.params.id as string
  if (!chartId) {
    ElMessage.error('图表ID不存在')
    return
  }

  try {
    const response = await axios.get(`/api/v1/charts/${chartId}`)
    const chartData = response.data
    
    // 填充表单数据
    form.name = chartData.name
    form.description = chartData.description || ''
    form.chart_type = chartData.chart_type
    form.data_model_id = chartData.data_model_id
    form.dimensions = chartData.dimensions || []
    form.measures = chartData.measures || []
    form.filters = chartData.filters || []
    form.style = JSON.stringify(chartData.style || {}, null, 2)
    form.is_active = chartData.is_active
    
    // 更新选择的维度和度量
    selectedDimensions.value = form.dimensions.map(dim => dim.name)
    selectedMeasures.value = form.measures.map(meas => meas.name)
    
    // 加载数据模型详情
    await handleModelChange()
  } catch (error) {
    ElMessage.error('加载图表数据失败')
    console.error('Failed to load chart data:', error)
  }
}

const handleModelChange = async () => {
  try {
    const model = dataModels.value.find(m => m.id === form.data_model_id)
    if (model) {
      selectedModel.value = model
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
    
    // 更新维度和度量配置
    form.dimensions = selectedDimensions.value.map(dim => ({
      name: dim,
      field: dim
    }))
    form.measures = selectedMeasures.value.map(meas => ({
      name: meas,
      field: meas
    }))

    previewVisible.value = true
    await nextTick()
    renderChart()
  } catch (error) {
    ElMessage.error('请填写完整的表单信息')
    console.error('Validation error:', error)
  }
}

const renderChart = () => {
  if (!chartRef.value) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  // 模拟图表数据
  const option = {
    title: {
      text: form.name,
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: selectedMeasures.value,
      bottom: 10
    },
    xAxis: {
      type: 'category',
      data: ['一月', '二月', '三月', '四月', '五月', '六月']
    },
    yAxis: {
      type: 'value'
    },
    series: selectedMeasures.value.map(measure => ({
      name: measure,
      type: form.chart_type,
      data: [120, 200, 150, 80, 70, 110]
    }))
  }

  chartInstance.setOption(option)

  // 响应式调整
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
}

const handleSubmit = async () => {
  try {
    const chartId = route.params.id as string
    if (!chartId) {
      ElMessage.error('图表ID不存在')
      return
    }

    await formRef.value?.validate()

    // 更新维度和度量配置
    form.dimensions = selectedDimensions.value.map(dim => ({
      name: dim,
      field: dim
    }))
    form.measures = selectedMeasures.value.map(meas => ({
      name: meas,
      field: meas
    }))

    // 准备提交数据
    const submitData = {
      ...form,
      style: JSON.parse(form.style)
    }

    await axios.put(`/api/v1/charts/${chartId}`, submitData)
    ElMessage.success('图表更新成功')
    navigateTo('/dashboards')
  } catch (error) {
    console.error('Submit error:', error)
    if (error.response) {
      ElMessage.error(`更新失败: ${error.response.data.detail}`)
    } else {
      ElMessage.error('更新失败，请检查输入信息')
    }
  }
}

const handleReset = async () => {
  await loadChartData()
}
</script>

<style scoped>
.dashboards-edit-chart {
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

.filter-item {
  display: flex;
  align-items: center;
  margin-top: 10px;
  gap: 10px;
}

.chart-container {
  width: 100%;
  height: 400px;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    padding: 10px;
  }

  .header-content h1 {
    margin-bottom: 10px;
  }

  .filter-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .chart-container {
    height: 300px;
  }
}
</style>
