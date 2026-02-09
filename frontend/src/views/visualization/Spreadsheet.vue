<template>
  <div class="visualization-spreadsheet">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>电子表格</h1>
          <el-button @click="navigateTo('/visualization')">
            返回
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>电子表格配置</span>
            </div>
          </template>
          <div class="card-content">
            <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
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
                <el-button type="primary" @click="handleSubmit">
                  生成报表
                </el-button>
                <el-button @click="handleReset">
                  重置
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>

        <el-card v-if="result.success">
          <template #header>
            <div class="card-header">
              <span>报表结果</span>
            </div>
          </template>
          <div class="card-content">
            <el-table :data="spreadsheetData" style="width: 100%">
              <el-table-column 
                v-for="column in spreadsheetColumns" 
                :key="column" 
                :prop="column" 
                :label="column" 
              />
            </el-table>
            <div class="result-actions">
              <el-button type="primary" @click="exportExcel">
                导出Excel
              </el-button>
              <el-button type="success" @click="exportPDF">
                导出PDF
              </el-button>
            </div>
          </div>
        </el-card>
      </el-main>
    </el-container>
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
  parameters: '{}'
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
  
  // 提取表头
  const headers = []
  for (const [key, value] of Object.entries(cells)) {
    if (key.endsWith('1')) { // 第一行是表头
      headers.push({ key, value })
    }
  }
  
  // 按列排序表头
  headers.sort((a, b) => a.key.localeCompare(b.key))
  
  // 提取数据行
  const rows = new Map()
  for (const [key, value] of Object.entries(cells)) {
    if (!key.endsWith('1')) { // 非表头行
      const rowNum = parseInt(key.replace(/[^0-9]/g, ''))
      if (!rows.has(rowNum)) {
        rows.set(rowNum, {})
      }
      const colName = headers.find(h => h.key.charAt(0) === key.charAt(0))?.value || key.charAt(0)
      rows.get(rowNum)[colName] = value
    }
  }
  
  // 按行号排序并转换为数组
  Array.from(rows.entries())
    .sort((a, b) => a[0] - b[0])
    .forEach(([_, rowData]) => {
      data.push(rowData)
    })
  
  return data
})

const spreadsheetColumns = computed(() => {
  if (!result.value.success || !result.value.data.cells) return ['字段名', '值']
  
  const cells = result.value.data.cells
  const headers = []
  
  // 提取表头
  for (const [key, value] of Object.entries(cells)) {
    if (key.endsWith('1')) { // 第一行是表头
      headers.push({ key, value })
    }
  }
  
  // 按列排序并返回表头值
  return headers
    .sort((a, b) => a.key.localeCompare(b.key))
    .map(h => h.value)
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
      // 重置结果
      result.value = {
        success: false,
        data: {},
        message: ''
      }
    }
  } catch (error) {
    ElMessage.error('加载数据集失败')
    console.error('Failed to load data set:', error)
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()

    // 准备提交数据
    const submitData = {
      data_set_id: form.data_set_id,
      template_id: form.template_id,
      parameters: JSON.parse(form.parameters)
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
  }
}

const handleReset = () => {
  formRef.value?.resetFields()
  form.parameters = '{}'
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
</script>

<style scoped>
.visualization-spreadsheet {
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

.result-actions {
  margin-top: 20px;
  text-align: right;
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
