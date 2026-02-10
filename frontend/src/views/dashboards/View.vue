<template>
  <div class="dashboard-view">
    <div class="page-header">
      <h1>{{ dashboard?.name || '仪表盘展示' }}</h1>
      <el-button @click="navigateTo('/dashboards')">
        返回管理
      </el-button>
    </div>
    
    <el-card v-if="dashboard" class="dashboard-card">
      <template #header>
        <div class="card-header">
          <span>{{ dashboard.description || '仪表盘预览' }}</span>
          <el-button type="primary" size="small" @click="refreshDashboard">
            刷新数据
          </el-button>
        </div>
      </template>
      <div class="dashboard-content" :style="{ height: '80vh' }">
        <div class="dashboard-grid" :style="gridStyle">
          <div 
            v-for="(widget, index) in dashboard.widgets" 
            :key="index"
            class="dashboard-widget"
            :style="getWidgetStyle(widget)"
          >
            <div class="widget-header">
              <span>{{ widget.name }}</span>
            </div>
            <div class="widget-content">
              <div v-if="widget.type === 'chart'" class="chart-container" ref="chartRefs" :data-chart-id="widget.chart_id">
                <!-- 图表将通过 ECharts 渲染 -->
              </div>
              <div v-else class="widget-placeholder">
                {{ widget.type }} 组件
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-card>
    
    <el-empty v-else description="加载中..." style="margin-top: 100px;">
      <el-button type="primary" @click="navigateTo('/dashboards')">
        返回仪表盘管理
      </el-button>
    </el-empty>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from '../../utils/axios'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'

interface Dashboard {
  id: number
  name: string
  description: string | null
  layout: any
  widgets: any[]
  refresh_interval: number
  is_active: boolean
  created_at: string
  updated_at: string
}

interface Chart {
  id: number
  name: string
  description: string | null
  chart_type: string
  data_model_id: number
  dimensions: any[]
  measures: any[]
  filters: any[]
  style: any
  is_active: boolean
  created_at: string
  updated_at: string
}

const router = useRouter()
const route = useRoute()
const dashboard = ref<Dashboard | null>(null)
const chartInstances = ref<{ [key: number]: echarts.ECharts }>({})
const chartRefs = ref<HTMLElement[]>([])

const dashboardId = computed(() => {
  return Number(route.params.id || 1)
})

const gridStyle = computed(() => {
  if (!dashboard.value?.layout) {
    return {}
  }
  const { rows, cols } = dashboard.value.layout
  return {
    gridTemplateColumns: `repeat(${cols}, 1fr)`,
    gridTemplateRows: `repeat(${rows}, 1fr)`
  }
})

const getWidgetStyle = (widget: any) => {
  if (!widget.position) {
    return {}
  }
  const { x, y, width, height } = widget.position
  return {
    gridColumnStart: x + 1,
    gridColumnEnd: x + width + 1,
    gridRowStart: y + 1,
    gridRowEnd: y + height + 1
  }
}

const fetchDashboard = async () => {
  try {
    const response = await axios.get(`/api/v1/dashboards/${dashboardId.value}`)
    dashboard.value = response.data
  } catch (error) {
    console.error('Failed to fetch dashboard:', error)
    ElMessage.error('加载仪表盘失败')
  }
}

const fetchChartData = async (chartId: number) => {
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
    
    if (resultData.success && resultData.data && resultData.columns) {
      // 提取x轴数据
      const xAxisData = resultData.data.map((row: any) => {
        const dimField = chartConfig.dimensions[0]?.name
        return dimField ? row[dimField] : ''
      }).filter((val: any) => val)
      
      // 提取系列数据
      const seriesData = chartConfig.measures.map((measure: any) => {
        const measureField = measure.name
        return {
          name: measure.name,
          type: chartConfig.chart_type,
          data: resultData.data.map((row: any) => row[measureField] || 0)
        }
      })
      
      return {
        xAxis: xAxisData,
        series: seriesData
      }
    }
    return null
  } catch (error) {
    console.error(`Failed to fetch chart data for chart ${chartId}:`, error)
    return null
  }
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
    chartInstances.value[chartId] = chartInstance
    
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
        left: 'center'
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
        bottom: 10
      },
      xAxis: {
        type: 'category',
        data: chartData.xAxis
      },
      yAxis: {
        type: 'value'
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
          fontSize: 12,
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
    
    // 设置图表选项
    chartInstance.setOption(option)
    
    // 监听窗口大小变化
    window.addEventListener('resize', () => {
      chartInstance.resize()
    })
  } catch (error) {
    console.error(`Failed to render chart ${chartId}:`, error)
    
    // 出错时显示错误信息（与新建图表页面的错误处理一致）
    const chartInstance = echarts.init(container)
    chartInstances.value[chartId] = chartInstance
    
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
          color: '#ff4d4f'
        }
      },
      graphic: [
        {
          type: 'text',
          left: 'center',
          top: 'center',
          style: {
            text: errorMessage,
            fontSize: 14,
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
  }
}

const renderAllCharts = () => {
  if (!dashboard.value) {
    return
  }
  
  // 清除现有图表实例
  Object.values(chartInstances.value).forEach(instance => {
    instance.dispose()
  })
  chartInstances.value = {}
  
  // 渲染所有图表
  dashboard.value.widgets.forEach(widget => {
    if (widget.type === 'chart' && widget.chart_id) {
      const containers = document.querySelectorAll(`[data-chart-id="${widget.chart_id}"]`)
      containers.forEach(container => {
        renderChart(widget.chart_id, container as HTMLElement)
      })
    }
  })
}

const refreshDashboard = async () => {
  await fetchDashboard()
  renderAllCharts()
  ElMessage.success('仪表盘已刷新')
}

const navigateTo = (path: string) => {
  router.push(path)
}

onMounted(async () => {
  await fetchDashboard()
  
  // 延迟渲染图表，确保 DOM 已经更新
  setTimeout(() => {
    renderAllCharts()
  }, 100)
  
  // 如果设置了自动刷新间隔，启动定时器
  if (dashboard.value?.refresh_interval > 0) {
    setInterval(() => {
      refreshDashboard()
    }, dashboard.value.refresh_interval * 1000)
  }
})

// 监听仪表盘变化，重新渲染图表
watch(() => dashboard.value, () => {
  setTimeout(() => {
    renderAllCharts()
  }, 100)
}, { deep: true })
</script>

<style scoped>
.dashboard-view {
  padding: 20px;
  min-height: 100vh;
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

.dashboard-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-content {
  position: relative;
  overflow: hidden;
}

.dashboard-grid {
  display: grid;
  gap: 20px;
  height: 100%;
  padding: 20px;
}

.dashboard-widget {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.widget-header {
  padding: 12px 16px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
  font-weight: 500;
  color: #303133;
}

.widget-content {
  flex: 1;
  padding: 16px;
  overflow: hidden;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
}

.widget-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background-color: #f9f9f9;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
  color: #909399;
}

@media (max-width: 768px) {
  .dashboard-view {
    padding: 10px;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr !important;
    padding: 10px;
  }
  
  .chart-container {
    min-height: 200px;
  }
}
</style>