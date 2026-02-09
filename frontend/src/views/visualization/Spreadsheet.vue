<template>
  <div class="visualization-spreadsheet">
    <div class="page-header">
      <h1>电子表格</h1>
      <el-button @click="navigateTo('/visualization')">
        返回
      </el-button>
    </div>
    
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>电子表格配置</span>
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
          <el-form-item label="模板" prop="template_id">
            <el-select v-model="form.template_id" placeholder="请选择模板">
              <el-option label="默认模板" value="1" />
              <el-option label="销售报表模板" value="2" />
              <el-option label="财务报表模板" value="3" />
            </el-select>
          </el-form-item>
          <el-form-item label="参数" prop="parameters">
            <el-input v-model="form.parameters" type="textarea" placeholder="请输入参数（JSON格式）" />
          </el-form-item>
          <el-form-item>
                <div class="button-group">
                  <el-button type="primary" @click="handleSubmit" :loading="loading">
                    生成报表
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
          <span>报表结果</span>
        </div>
      </template>
      <div class="card-content">
        <div class="table-container">
          <el-table 
            :data="spreadsheetData" 
            style="width: 100%" 
            height="500"
            border
            stripe
            class="page-table"
            :default-sort="{ prop: '字段名', order: 'ascending' }"
            v-loading="loading"
            element-loading-text="加载中..."
          >
            <el-table-column 
              v-for="column in spreadsheetColumns" 
              :key="column" 
              :prop="column" 
              :label="column" 
              :min-width="120"
              :show-overflow-tooltip="true"
            />
          </el-table>
        </div>
        <div class="result-actions">
          <el-button type="primary" @click="exportExcel">
            导出Excel
          </el-button>
          <el-button type="success" @click="exportPDF">
            导出PDF
          </el-button>
        </div>
        
        <div class="pagination-container" v-if="result.success && result.data.total > 0">
          <el-pagination
            v-model:current-page="form.page"
            v-model:page-size="form.page_size"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="result.data.total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
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

interface FormData {
  data_set_id: number
  template_id: number
  parameters: string
  page: number
  page_size: number
}

interface ResultData {
  success: boolean
  data: any
  message: string
}

const router = useRouter()
const formRef = ref<FormInstance>()
const dataSets = ref<any[]>([])
const selectedDataSet = ref<any>(null)
const result = ref<ResultData>({
  success: false,
  data: {},
  message: ''
})

const form = reactive<FormData>({
  data_set_id: 0,
  template_id: 1,
  parameters: '{}',
  page: 1,
  page_size: 10
})

const rules = reactive<FormRules>({
  data_set_id: [
    { required: true, message: '请选择数据集', trigger: 'change' }
  ]
})

const spreadsheetData = computed(() => {
  if (!result.value.success || !result.value.data.cells) return []
  
  const cells = result.value.data.cells
  const data = []
  
  // 提取表头（按列字母顺序）
  const headers = []
  const colLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  
  for (const colLetter of colLetters) {
    const cellKey = `${colLetter}1`
    if (cells[cellKey] !== undefined) {
      const value = cells[cellKey]
      const stringValue = String(value)
      const cleanValue = stringValue.includes('.') ? stringValue.split('.').pop() : stringValue
      headers.push({ key: cellKey, value: cleanValue, colLetter })
    }
  }
  
  // 提取数据行（排除表头和总计行）
  const rows = new Map()
  for (const [key, value] of Object.entries(cells)) {
    if (!key.endsWith('1') && value !== '总计') { // 非表头行且不是总计行
      const rowNum = parseInt(key.replace(/[^0-9]/g, ''))
      if (!rows.has(rowNum)) {
        rows.set(rowNum, {})
      }
      // 提取列字母
      const colLetter = key.replace(/[0-9]/g, '')
      // 获取对应的列名
      const header = headers.find(h => h.colLetter === colLetter)
      if (header) {
        rows.get(rowNum)[header.value] = value
      }
    }
  }
  
  // 按行号排序并转换为数组
  Array.from(rows.entries())
    .sort((a, b) => a[0] - b[0])
    .forEach(([_, rowData]) => {
      data.push(rowData)
    })
  
  console.log('Spreadsheet data:', data)
  return data
})

const spreadsheetColumns = computed(() => {
  if (!result.value.success || !result.value.data.cells) return ['字段名', '值']
  
  const cells = result.value.data.cells
  
  // 提取表头（按列字母顺序）
  const colLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  const headers = []
  
  for (const colLetter of colLetters) {
    const cellKey = `${colLetter}1`
    if (cells[cellKey] !== undefined) {
      const value = cells[cellKey]
      const stringValue = String(value)
      const cleanValue = stringValue.includes('.') ? stringValue.split('.').pop() : stringValue
      headers.push(cleanValue)
    }
  }
  
  console.log('Spreadsheet columns:', headers)
  return headers
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
    console.log('Fetched data sets:', response.data)
  } catch (error) {
    ElMessage.error('获取数据集列表失败')
    console.error('Failed to fetch data sets:', error)
  }
}

const loading = ref(false)

const handleDataSetChange = async () => {
  try {
    const dataSet = dataSets.value.find(ds => ds.id === form.data_set_id)
    if (dataSet) {
      selectedDataSet.value = dataSet
      // 重置结果
      result.value = {
        success: false,
        data: {},
        message: ''
      }
      console.log('Selected data set:', dataSet)
      // 自动加载数据
      await handleSubmit()
    }
  } catch (error) {
    ElMessage.error('加载数据集失败')
    console.error('Failed to load data set:', error)
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    
    // 显示加载状态
    loading.value = true

    // 准备提交数据
    const submitData = {
      data_set_id: form.data_set_id,
      template_id: form.template_id,
      parameters: JSON.parse(form.parameters),
      page: form.page,
      page_size: form.page_size
    }

    const response = await axios.post('/api/v1/visualization/spreadsheet', submitData)
    result.value = response.data
    ElMessage.success('报表生成成功')
  } catch (error) {
    console.error('Submit error:', error)
    if (error.response) {
      ElMessage.error(`生成失败: ${error.response.data.detail}`)
    } else {
      ElMessage.error('生成失败，请检查输入信息')
    }
  } finally {
    // 隐藏加载状态
    loading.value = false
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
  form.parameters = '{}'
  form.page = 1
  form.page_size = 10
  result.value = {
    success: false,
    data: {},
    message: ''
  }
}

const exportExcel = () => {
  if (!result.value.success || !result.value.data.workbook_base64) {
    ElMessage.error('没有可导出的Excel文件')
    return
  }
  
  try {
    // 从base64字符串创建Blob对象
    const base64Data = result.value.data.workbook_base64
    const binaryString = window.atob(base64Data)
    const binaryLen = binaryString.length
    const bytes = new Uint8Array(binaryLen)
    for (let i = 0; i < binaryLen; i++) {
      bytes[i] = binaryString.charCodeAt(i)
    }
    const blob = new Blob([bytes], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    
    // 创建下载链接
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = result.value.data.file_name || `数据集_${form.data_set_id}_导出.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    
    ElMessage.success('Excel文件导出成功')
  } catch (error) {
    console.error('导出Excel失败:', error)
    ElMessage.error('导出Excel失败，请稍后重试')
  }
}

const exportPDF = () => {
  // 导出PDF的逻辑
  ElMessage.success('导出PDF功能开发中')
}

const handleSizeChange = (size: number) => {
  form.page_size = size
  form.page = 1
  handleSubmit()
}

const handleCurrentChange = (current: number) => {
  form.page = current
  handleSubmit()
}
</script>

<style scoped>
.visualization-spreadsheet {
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  padding: 0 20px;
  box-sizing: border-box;
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
  width: 100%;
  box-sizing: border-box;
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

.table-container {
  max-height: 600px;
  overflow: auto;
  width: 100%;
  box-sizing: border-box;
  max-width: 1200px;
}

.table-container ::v-deep .el-table {
  width: 100%;
  min-width: 800px;
}

.result-actions {
  margin-top: 20px;
  text-align: right;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .visualization-spreadsheet {
    padding: 0 10px;
  }
  
  .page-form {
    max-width: 100%;
  }
  
  .el-form {
    label-width: 100px;
  }
  
  .button-group {
    flex-direction: column;
    width: 100%;
  }
  
  .button-group .el-button {
    width: 100%;
  }
  
  .table-container {
    max-width: 100%;
  }
}
</style>
