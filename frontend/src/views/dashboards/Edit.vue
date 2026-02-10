<template>
  <div class="dashboards-edit">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>编辑仪表盘</h1>
          <el-button @click="navigateTo('/dashboards')">
            返回列表
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>仪表盘配置</span>
            </div>
          </template>
          <div class="card-content">
            <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
              <!-- 基本信息 -->
              <el-form-item label="仪表盘名称" prop="name">
                <el-input v-model="form.name" placeholder="请输入仪表盘名称" />
              </el-form-item>
              <el-form-item label="描述" prop="description">
                <el-input v-model="form.description" type="textarea" placeholder="请输入仪表盘描述" />
              </el-form-item>
              <el-form-item label="刷新间隔(秒)" prop="refresh_interval">
                <el-input-number v-model="form.refresh_interval" :min="30" :max="3600" :step="30" />
              </el-form-item>
              <el-form-item label="状态" prop="is_active">
                <el-switch v-model="form.is_active" />
              </el-form-item>
              
              <!-- 布局配置 -->
              <el-form-item label="布局行数" prop="layout.rows">
                <el-input-number v-model="form.layout.rows" :min="1" :max="20" :step="1" />
              </el-form-item>
              <el-form-item label="布局列数" prop="layout.cols">
                <el-input-number v-model="form.layout.cols" :min="1" :max="12" :step="1" />
              </el-form-item>
              <el-form-item label="组件间距(px)" prop="layout.gap">
                <el-input-number v-model="form.layout.gap" :min="0" :max="50" :step="1" />
              </el-form-item>
              
              <!-- 组件管理 -->
              <el-form-item label="组件管理">
                <el-button type="primary" size="small" @click="showAddWidgetDialog = true">
                  添加组件
                </el-button>
                <el-table :data="form.widgets" style="width: 100%; margin-top: 10px;">
                  <el-table-column prop="id" label="组件ID" width="100" />
                  <el-table-column prop="type" label="组件类型" width="120">
                    <template #default="scope">
                      {{ getWidgetTypeLabel(scope.row.type) }}
                    </template>
                  </el-table-column>
                  <el-table-column prop="chart_id" label="图表ID" width="100" />
                  <el-table-column label="操作" width="200" fixed="right">
                    <template #default="scope">
                      <el-button type="primary" size="small" @click="editWidget(scope.row)">
                        编辑
                      </el-button>
                      <el-button type="danger" size="small" @click="removeWidget(scope.row.id)">
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
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
              <span>仪表盘预览</span>
            </div>
          </template>
          <div class="card-content">
            <div class="dashboard-preview" :style="{
              display: 'grid',
              gridTemplateRows: `repeat(${form.layout.rows}, 1fr)`,
              gridTemplateColumns: `repeat(${form.layout.cols}, 1fr)`,
              gap: `${form.layout.gap}px`,
              height: '500px',
              padding: '10px',
              border: '1px solid #e4e7ed'
            }">
              <div 
                v-for="widget in form.widgets" 
                :key="widget.id"
                class="widget-preview"
                :style="{
                  gridRow: `span ${widget.size.row}`,
                  gridColumn: `span ${widget.size.col}`,
                  background: '#f0f2f5',
                  padding: '10px',
                  border: '1px solid #d9d9d9',
                  borderRadius: '4px',
                  overflow: 'hidden'
                }"
              >
                <div class="widget-header">
                  <strong>{{ getWidgetTypeLabel(widget.type) }}</strong>
                  <span v-if="widget.chart_id">(图表ID: {{ widget.chart_id }})</span>
                </div>
                <div class="widget-content" v-if="widget.type === 'chart' && widget.chart_id">
                  <div 
                    :id="`preview-chart-${widget.id}`" 
                    class="preview-chart-container"
                    style="width: 100%; height: 200px;"
                  ></div>
                </div>
                <div class="widget-content" v-else>
                  {{ getWidgetTypeLabel(widget.type) }} 内容预览
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-main>
    </el-container>

    <!-- 添加组件对话框 -->
    <el-dialog
      v-model="showAddWidgetDialog"
      title="添加组件"
      width="500px"
    >
      <el-form :model="widgetForm" :rules="widgetRules" ref="widgetFormRef" label-width="100px">
        <el-form-item label="组件类型" prop="type">
          <el-select v-model="widgetForm.type" placeholder="请选择组件类型" @change="handleWidgetTypeChange">
            <el-option label="图表" value="chart" />
            <el-option label="指标卡" value="metric" />
            <el-option label="文本" value="text" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="widgetForm.type === 'chart'" label="图表" prop="chart_id">
          <el-select v-model="widgetForm.chart_id" placeholder="请选择图表">
            <el-option 
              v-for="chart in charts" 
              :key="chart.id" 
              :label="chart.name" 
              :value="chart.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="行数" prop="size.row">
          <el-input-number v-model="widgetForm.size.row" :min="1" :max="form.layout.rows" :step="1" />
        </el-form-item>
        <el-form-item label="列数" prop="size.col">
          <el-input-number v-model="widgetForm.size.col" :min="1" :max="form.layout.cols" :step="1" />
        </el-form-item>
        <el-form-item label="配置" prop="config">
          <el-input v-model="widgetForm.config" type="textarea" placeholder="请输入组件配置（JSON格式）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddWidgetDialog = false">取消</el-button>
          <el-button type="primary" @click="addWidget">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑组件对话框 -->
    <el-dialog
      v-model="showEditWidgetDialog"
      title="编辑组件"
      width="500px"
    >
      <el-form :model="widgetForm" :rules="widgetRules" ref="widgetFormRef" label-width="100px">
        <el-form-item label="组件类型" prop="type">
          <el-select v-model="widgetForm.type" placeholder="请选择组件类型" @change="handleWidgetTypeChange">
            <el-option label="图表" value="chart" />
            <el-option label="指标卡" value="metric" />
            <el-option label="文本" value="text" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="widgetForm.type === 'chart'" label="图表" prop="chart_id">
          <el-select v-model="widgetForm.chart_id" placeholder="请选择图表">
            <el-option 
              v-for="chart in charts" 
              :key="chart.id" 
              :label="chart.name" 
              :value="chart.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="行数" prop="size.row">
          <el-input-number v-model="widgetForm.size.row" :min="1" :max="form.layout.rows" :step="1" />
        </el-form-item>
        <el-form-item label="列数" prop="size.col">
          <el-input-number v-model="widgetForm.size.col" :min="1" :max="form.layout.cols" :step="1" />
        </el-form-item>
        <el-form-item label="配置" prop="config">
          <el-input v-model="widgetForm.config" type="textarea" placeholder="请输入组件配置（JSON格式）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditWidgetDialog = false">取消</el-button>
          <el-button type="primary" @click="updateWidget">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, nextTick, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import * as echarts from 'echarts'

interface WidgetSize {
  row: number
  col: number
}

interface WidgetPosition {
  x: number
  y: number
}

interface WidgetFormData {
  type: string
  chart_id: number | null
  size: WidgetSize
  config: string
}

interface WidgetData {
  id: string
  type: string
  chart_id: number | null
  position: WidgetPosition
  size: WidgetSize
  config: any
}

interface LayoutConfig {
  rows: number
  cols: number
  gap: number
}

interface FormData {
  name: string
  description: string
  layout: LayoutConfig
  widgets: WidgetData[]
  refresh_interval: number
  is_active: boolean
}

const router = useRouter()
const route = useRoute()
const formRef = ref<FormInstance>()
const widgetFormRef = ref<FormInstance>()
const charts = ref<any[]>([])
const previewVisible = ref(false)
const showAddWidgetDialog = ref(false)
const showEditWidgetDialog = ref(false)
const editingWidgetId = ref<string>('')
const chartInstances = ref<Map<string, echarts.ECharts>>(new Map())

const form = reactive<FormData>({
  name: '',
  description: '',
  layout: {
    rows: 4,
    cols: 3,
    gap: 10
  },
  widgets: [],
  refresh_interval: 300,
  is_active: true
})

const widgetForm = reactive<WidgetFormData>({
  type: 'chart',
  chart_id: null,
  size: {
    row: 1,
    col: 1
  },
  config: '{}'
})

const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入仪表盘名称', trigger: 'blur' }
  ],
  layout: [
    {
      validator: (rule, value, callback) => {
        if (!value.rows || !value.cols) {
          callback(new Error('请设置布局行数和列数'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]
})

const widgetRules = reactive<FormRules>({
  type: [
    { required: true, message: '请选择组件类型', trigger: 'change' }
  ],
  'size.row': [
    { required: true, message: '请设置组件行数', trigger: 'change' }
  ],
  'size.col': [
    { required: true, message: '请设置组件列数', trigger: 'change' }
  ]
})

onMounted(async () => {
  await fetchCharts()
  await loadDashboardData()
})

onUnmounted(() => {
  // 清理所有图表实例
  chartInstances.value.forEach(instance => {
    instance.dispose()
  })
  chartInstances.value.clear()
})

const navigateTo = (path: string) => {
  router.push(path)
}

const fetchCharts = async () => {
  try {
    const response = await axios.get('/api/v1/charts')
    charts.value = response.data
  } catch (error) {
    ElMessage.error('获取图表列表失败')
    console.error('Failed to fetch charts:', error)
  }
}

const loadDashboardData = async () => {
  const dashboardId = route.params.id as string
  if (!dashboardId) {
    ElMessage.error('仪表盘ID不存在')
    return
  }

  try {
    const response = await axios.get(`/api/v1/dashboards/${dashboardId}`)
    const dashboardData = response.data
    
    // 填充表单数据
    form.name = dashboardData.name
    form.description = dashboardData.description || ''
    form.layout = dashboardData.layout || {
      rows: 4,
      cols: 3,
      gap: 10
    }
    
    // 为每个widget添加id和position字段（如果不存在），确保id是字符串类型
    form.widgets = (dashboardData.widgets || []).map((widget: any, index: number) => ({
      id: typeof widget.id === 'string' ? widget.id : `widget_${Date.now()}_${index}`,
      type: widget.type,
      chart_id: widget.chart_id,
      position: widget.position || { x: 0, y: 0 },
      size: widget.size,
      config: widget.config
    }))
    
    form.refresh_interval = dashboardData.refresh_interval || 300
    form.is_active = dashboardData.is_active !== undefined ? dashboardData.is_active : true
    
  } catch (error) {
    ElMessage.error('加载仪表盘数据失败')
    console.error('Failed to load dashboard data:', error)
  }
}

const getWidgetTypeLabel = (type: string): string => {
  const typeMap: Record<string, string> = {
    'chart': '图表',
    'metric': '指标卡',
    'text': '文本'
  }
  return typeMap[type] || type
}

const handleWidgetTypeChange = () => {
  if (widgetForm.type !== 'chart') {
    widgetForm.chart_id = null
  }
}

const addWidget = async () => {
  try {
    await widgetFormRef.value?.validate()
    
    // 生成唯一ID（使用字符串格式）
    const widgetId = `widget_${Date.now()}`
    
    // 创建新组件
    const newWidget: WidgetData = {
      id: widgetId,
      type: widgetForm.type,
      chart_id: widgetForm.chart_id,
      position: {
        x: 0,
        y: 0
      },
      size: { ...widgetForm.size },
      config: JSON.parse(widgetForm.config)
    }
    
    // 添加到组件列表
    form.widgets.push(newWidget)
    
    // 关闭对话框并重置表单
    showAddWidgetDialog.value = false
    resetWidgetForm()
    
    ElMessage.success('组件添加成功')
  } catch (error) {
    ElMessage.error('请填写完整的组件信息')
    console.error('Validation error:', error)
  }
}

const editWidget = (widget: WidgetData) => {
  editingWidgetId.value = widget.id
  widgetForm.type = widget.type
  widgetForm.chart_id = widget.chart_id
  widgetForm.size = { ...widget.size }
  widgetForm.config = JSON.stringify(widget.config, null, 2)
  showEditWidgetDialog.value = true
}

const updateWidget = async () => {
  try {
    await widgetFormRef.value?.validate()
    
    // 找到要更新的组件
    const widgetIndex = form.widgets.findIndex(w => w.id === editingWidgetId.value)
    if (widgetIndex === -1) {
      ElMessage.error('组件不存在')
      return
    }
    
    // 更新组件
    form.widgets[widgetIndex] = {
      ...form.widgets[widgetIndex],
      type: widgetForm.type,
      chart_id: widgetForm.chart_id,
      size: { ...widgetForm.size },
      config: JSON.parse(widgetForm.config)
    }
    
    // 关闭对话框并重置表单
    showEditWidgetDialog.value = false
    resetWidgetForm()
    editingWidgetId.value = ''
    
    ElMessage.success('组件更新成功')
  } catch (error) {
    ElMessage.error('请填写完整的组件信息')
    console.error('Validation error:', error)
  }
}

const removeWidget = (widgetId: string) => {
  const widgetIndex = form.widgets.findIndex(w => w.id === widgetId)
  if (widgetIndex !== -1) {
    // 清理对应的图表实例
    const chartId = `preview-chart-${widgetId}`
    if (chartInstances.value.has(chartId)) {
      chartInstances.value.get(chartId)?.dispose()
      chartInstances.value.delete(chartId)
    }
    
    form.widgets.splice(widgetIndex, 1)
    ElMessage.success('组件删除成功')
  }
}

const resetWidgetForm = () => {
  widgetForm.type = 'chart'
  widgetForm.chart_id = null
  widgetForm.size = {
    row: 1,
    col: 1
  }
  widgetForm.config = '{}'
}

const renderChart = async (chartId: number, container: HTMLElement) => {
  try {
    // 获取图表配置
    const chartResponse = await axios.get(`/api/v1/charts/${chartId}`)
    const chartConfig = chartResponse.data
    
    // 构建提交数据（与新建图表页面的预览功能一致）
    const submitData = {
      data_model_id: chartConfig.data_model_id,
      dimensions: chartConfig.dimensions.map((dim: any) => dim.name),
      measures: chartConfig.measures.map((meas: any) => meas.name),
      filters: chartConfig.filters
    }
    
    // 从后端获取真实数据
    const response = await axios.post('/api/v1/visualization/pivot-analysis', submitData)
    const resultData = response.data
    
    if (!resultData.success || !resultData.data || !resultData.columns) {
      let errorMessage = '数据加载失败'
      if (resultData.message) {
        errorMessage = resultData.message
      }
      throw new Error(errorMessage)
    }
    
    // 提取x轴数据
    const xAxisData = resultData.data.map((row: any) => {
      const dimField = chartConfig.dimensions[0]?.name
      if (!dimField) return ''
      
      // 查找实际的维度字段名（可能是pivot_前缀的）
      let actualField = dimField
      const matchedColumn = resultData.columns.find((col: string) => 
        col === dimField || 
        col === `pivot_${dimField}` ||
        col.endsWith(dimField)
      )
      if (matchedColumn) {
        actualField = matchedColumn
      }
      
      return row[actualField] || ''
    }).filter((val: any) => val)
    
    // 提取系列数据
    const seriesData = chartConfig.measures.map((measure: any) => {
      const measureField = measure.name
      
      // 查找实际的度量字段名（可能是pivot_前缀的）
      let actualField = measureField
      const matchedColumn = resultData.columns.find((col: string) => 
        col === measureField || 
        col === `pivot_${measureField}` ||
        col.endsWith(measureField)
      )
      if (matchedColumn) {
        actualField = matchedColumn
      }
      
      return {
        name: measure.name,
        type: chartConfig.chart_type,
        data: resultData.data.map((row: any) => row[actualField] || 0)
      }
    })
    
    const chartData = {
      xAxis: xAxisData,
      series: seriesData
    }
    
    if (chartData.xAxis.length === 0) {
      throw new Error('无数据可显示')
    }
    
    // 初始化 ECharts 实例
    const chartInstance = echarts.init(container)
    
    // 状态字段颜色映射
    const statusColors = [
      '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de',
      '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#2ec7c9'
    ]

    // 检测状态字段（通常包含status、state等关键词，包括pivot_前缀的情况）
    const statusField = chartConfig.dimensions.find((dim: any) => {
      const cleanDim = dim.name.replace(/^pivot_/, '').toLowerCase()
      return cleanDim.includes('status') || cleanDim.includes('state') || cleanDim.includes('状态')
    })

    // 获取状态字段的所有唯一值
    const statusValues = statusField 
      ? [...new Set(resultData.data.map((row: any) => {
          // 查找实际的状态字段名（可能是pivot_前缀的）
          let actualField = statusField.name
          // 首先检查columns中是否有完全匹配的字段
          const matchedColumn = resultData.columns.find((col: string) => 
            col === statusField.name || 
            col === `pivot_${statusField.name}` ||
            col.endsWith(statusField.name)
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
      const matchedColumn = resultData.columns.find((col: string) => 
        col === statusField.name || 
        col === `pivot_${statusField.name}` ||
        col.endsWith(statusField.name)
      )
      return matchedColumn || statusField.name
    }
    const actualStatusField = getStatusFieldName()

    // 根据图表类型和数据生成配置
    const option: any = {
      title: {
        text: chartConfig.name,
        left: 'center',
        textStyle: {
          fontSize: 12
        }
      },
      tooltip: {
        trigger: chartConfig.chart_type === 'pie' ? 'item' : 'axis',
        formatter: (params: any) => {
          if (chartConfig.chart_type === 'pie') {
            return `${params.name}: ${params.value} (${params.percent}%)`
          }
          if (Array.isArray(params)) {
            const xAxisValue = params[0]?.axisValue || params[0]?.name || ''
            let tooltipResult = xAxisValue + '<br/>'
            
            // 获取当前数据点的状态值
            let statusInfo = ''
            if (actualStatusField && params[0]?.dataIndex !== undefined) {
              const dataIndex = params[0].dataIndex
              const row = resultData.data[dataIndex]
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
              const row = resultData.data[dataIndex]
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
        data: chartConfig.measures.map((m: any) => m.name),
        bottom: 10,
        textStyle: {
          fontSize: 10
        }
      },
      xAxis: {
        type: 'category',
        data: chartData.xAxis,
        axisLabel: {
          fontSize: 10,
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          fontSize: 10
        }
      },
      series: chartData.series.map((seriesItem: any, index: number) => {
        const seriesConfig: any = {
          name: seriesItem.name,
          type: seriesItem.type,
          data: seriesItem.data
        }

        // 添加数据标签
        seriesConfig.label = {
          show: true,
          position: chartConfig.chart_type === 'pie' ? 'outside' : 'top',
          formatter: (params: any) => {
            if (chartConfig.chart_type === 'pie') {
              return `${params.name}: ${params.value}`
            }
            const displayValue = params.value || 0
            
            // 如果有状态字段，显示状态值
            if (actualStatusField && params.dataIndex !== undefined) {
              const dataIndex = params.dataIndex
              const row = resultData.data[dataIndex]
              if (row && actualStatusField in row) {
                const statusValue = row[actualStatusField]
                return `${displayValue}\n状态: ${statusValue}`
              }
            }
            
            return String(displayValue)
          },
          fontSize: 10,
          color: '#666'
        }

        // 如果有状态字段，为每个数据点应用对应的颜色
        if (statusField && statusValues.length > 0) {
          seriesConfig.data = seriesItem.data.map((value: any, dataIndex: number) => {
            const row = resultData.data[dataIndex]
            let statusValue = ''
            if (row && actualStatusField in row) {
              statusValue = row[actualStatusField]
            }
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
    if (chartConfig.chart_type === 'pie') {
      const pieData = chartData.xAxis.map((xValue: string, index: number) => {
        const measureValue = chartData.series[0].data[index]
        return {
          name: xValue,
          value: measureValue || 0
        }
      })

      option.series = [{
        name: chartConfig.measures[0].name,
        type: 'pie',
        radius: ['40%', '70%'],
        data: pieData,
        label: {
          show: true,
          formatter: '{b}: {c} ({d}%)',
          fontSize: 10
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

    // 设置图表选项
    chartInstance.setOption(option)

    // 监听窗口大小变化
    window.addEventListener('resize', () => {
      chartInstance.resize()
    })

    return chartInstance
  } catch (error) {
    console.error(`Failed to render chart ${chartId}:`, error)
    
    // 出错时显示错误信息
    const chartInstance = echarts.init(container)
    
    let errorMessage = '图表加载失败'
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
    
    const option = {
      title: {
        text: '图表加载失败',
        left: 'center',
        textStyle: {
          color: '#ff4d4f',
          fontSize: 12
        }
      },
      graphic: [
        {
          type: 'text',
          left: 'center',
          top: 'center',
          style: {
            text: errorMessage,
            fontSize: 10,
            fill: '#999',
            align: 'center'
          }
        }
      ]
    }
    
    chartInstance.setOption(option)

    // 监听窗口大小变化
    window.addEventListener('resize', () => {
      chartInstance.resize()
    })

    return chartInstance
  }
}

const handlePreview = async () => {
  try {
    await formRef.value?.validate()
    previewVisible.value = true
    
    // 等待DOM更新
    await nextTick()
    
    // 渲染所有图表
    for (const widget of form.widgets) {
      if (widget.type === 'chart' && widget.chart_id) {
        const containerId = `preview-chart-${widget.id}`
        const container = document.getElementById(containerId)
        if (container) {
          // 清理之前的图表实例
          if (chartInstances.value.has(containerId)) {
            chartInstances.value.get(containerId)?.dispose()
            chartInstances.value.delete(containerId)
          }
          
          // 渲染新图表
          const chartInstance = await renderChart(widget.chart_id, container)
          chartInstances.value.set(containerId, chartInstance)
        }
      }
    }
  } catch (error) {
    ElMessage.error('请填写完整的仪表盘信息')
    console.error('Validation error:', error)
  }
}

const handleSubmit = async () => {
  try {
    const dashboardId = route.params.id as string
    if (!dashboardId) {
      ElMessage.error('仪表盘ID不存在')
      return
    }

    await formRef.value?.validate()

    // 准备提交数据，确保widgets符合后端要求
    const submitData = {
      ...form,
      widgets: form.widgets.map(widget => ({
        id: widget.id.toString(), // 确保id是字符串
        type: widget.type,
        chart_id: widget.chart_id,
        position: widget.position,
        size: widget.size,
        config: widget.config
      }))
    }

    await axios.put(`/api/v1/dashboards/${dashboardId}`, submitData)
    ElMessage.success('仪表盘更新成功')
    navigateTo('/dashboards')
  } catch (error) {
    console.error('Submit error:', error)
    if (error.response) {
      let errorMessage = '更新失败，请检查输入信息'
      const detail = error.response.data.detail
      if (typeof detail === 'string') {
        errorMessage = `更新失败: ${detail}`
      } else if (Array.isArray(detail)) {
        // 处理错误数组
        const errorMessages = detail.map((err: any) => {
          if (typeof err === 'string') {
            return err
          } else if (err.msg) {
            return err.msg
          } else {
            return JSON.stringify(err)
          }
        })
        errorMessage = `更新失败: ${errorMessages.join('; ')}`
      } else if (typeof detail === 'object') {
        errorMessage = `更新失败: ${JSON.stringify(detail)}`
      }
      ElMessage.error(errorMessage)
    } else {
      ElMessage.error('更新失败，请检查输入信息')
    }
  }
}

const handleReset = async () => {
  // 清理所有图表实例
  chartInstances.value.forEach(instance => {
    instance.dispose()
  })
  chartInstances.value.clear()
  
  await loadDashboardData()
}
</script>

<style scoped>
.dashboards-edit {
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

.dashboard-preview {
  background: #fafafa;
}

.widget-preview {
  display: flex;
  flex-direction: column;
}

.widget-header {
  margin-bottom: 8px;
}

.widget-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border-radius: 4px;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
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
}
</style>
