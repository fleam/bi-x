<template>
  <div class="dashboards-create">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>新建仪表盘</h1>
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
                  <el-table-column label="操作" width="150" fixed="right">
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
                  borderRadius: '4px'
                }"
              >
                <div class="widget-header">
                  <strong>{{ getWidgetTypeLabel(widget.type) }}</strong>
                  <span v-if="widget.chart_id">(图表ID: {{ widget.chart_id }})</span>
                </div>
                <div class="widget-content">
                  组件内容预览
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

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
}

const router = useRouter()
const formRef = ref<FormInstance>()
const widgetFormRef = ref<FormInstance>()
const charts = ref<any[]>([])
const previewVisible = ref(false)
const showAddWidgetDialog = ref(false)
const showEditWidgetDialog = ref(false)
const editingWidgetId = ref<string>('')

const form = reactive<FormData>({
  name: '',
  description: '',
  layout: {
    rows: 4,
    cols: 3,
    gap: 10
  },
  widgets: [],
  refresh_interval: 300
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
    
    // 生成唯一ID
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

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()

    // 准备提交数据
    const submitData = {
      name: form.name,
      description: form.description,
      layout: form.layout,
      widgets: form.widgets,
      refresh_interval: form.refresh_interval
    }

    await axios.post('/api/v1/dashboards', submitData)
    ElMessage.success('仪表盘创建成功')
    navigateTo('/dashboards')
  } catch (error) {
    console.error('Submit error:', error)
    if (error.response) {
      ElMessage.error(`创建失败: ${error.response.data.detail}`)
    } else {
      ElMessage.error('创建失败，请检查输入信息')
    }
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
  form.layout = {
    rows: 4,
    cols: 3,
    gap: 10
  }
  form.widgets = []
  form.refresh_interval = 300
}
</script>

<style scoped>
.dashboards-create {
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
