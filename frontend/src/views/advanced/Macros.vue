<template>
  <div class="advanced-macros">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>宏管理</h1>
          <el-button type="primary" @click="showAddMacroDialog = true">
            新增宏
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>宏列表</span>
              <el-input
                v-model="searchQuery"
                placeholder="搜索宏"
                prefix-icon="el-icon-search"
                style="width: 300px"
              />
            </div>
          </template>
          <div class="card-content">
            <el-table :data="filteredMacros" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="宏名称" />
              <el-table-column prop="is_active" label="状态" width="100">
                <template #default="scope">
                  <el-switch v-model="scope.row.is_active" @change="handleMacroStatusChange(scope.row)" />
                </template>
              </el-table-column>
              <el-table-column prop="created_by" label="创建人" width="100" />
              <el-table-column prop="created_at" label="创建时间" width="180" />
              <el-table-column label="操作" width="250" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="editMacro(scope.row)">
                    编辑
                  </el-button>
                  <el-button type="success" size="small" @click="openExecuteMacroDialog(scope.row)" :disabled="!scope.row.is_active">
                    执行
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteMacro(scope.row.id)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination" v-if="total > 0">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </div>
        </el-card>

        <el-card v-if="selectedMacro">
          <template #header>
            <div class="card-header">
              <span>宏详情</span>
            </div>
          </template>
          <div class="card-content">
            <el-descriptions :column="2">
              <el-descriptions-item label="宏名称">
                {{ selectedMacro.name }}
              </el-descriptions-item>
              <el-descriptions-item label="状态">
                <el-switch v-model="selectedMacro.is_active" @change="handleMacroStatusChange(selectedMacro)" />
              </el-descriptions-item>
              <el-descriptions-item label="创建人">
                {{ selectedMacro.created_by }}
              </el-descriptions-item>
              <el-descriptions-item label="创建时间">
                {{ selectedMacro.created_at }}
              </el-descriptions-item>
              <el-descriptions-item label="更新时间">
                {{ selectedMacro.updated_at }}
              </el-descriptions-item>
              <el-descriptions-item label="描述" :span="2">
                {{ selectedMacro.description || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="参数" :span="2">
                <pre>{{ JSON.stringify(selectedMacro.parameters, null, 2) }}</pre>
              </el-descriptions-item>
              <el-descriptions-item label="宏代码" :span="2">
                <pre>{{ selectedMacro.code }}</pre>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-main>
    </el-container>

    <!-- 添加宏对话框 -->
    <el-dialog
      v-model="showAddMacroDialog"
      title="新增宏"
      width="600px"
    >
      <el-form :model="macroForm" :rules="macroRules" ref="macroFormRef" label-width="100px">
        <el-form-item label="宏名称" prop="name">
          <el-input v-model="macroForm.name" placeholder="请输入宏名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="macroForm.description" type="textarea" placeholder="请输入宏描述" />
        </el-form-item>
        <el-form-item label="宏代码" prop="code">
          <el-input v-model="macroForm.code" type="textarea" placeholder="请输入宏代码" rows="6" />
        </el-form-item>
        <el-form-item label="参数" prop="parameters">
          <el-input v-model="macroForm.parameters" type="textarea" placeholder="请输入宏参数（JSON格式）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddMacroDialog = false">取消</el-button>
          <el-button type="primary" @click="addMacro">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑宏对话框 -->
    <el-dialog
      v-model="showEditMacroDialog"
      title="编辑宏"
      width="600px"
    >
      <el-form :model="macroForm" :rules="macroRules" ref="macroFormRef" label-width="100px">
        <el-form-item label="宏名称" prop="name">
          <el-input v-model="macroForm.name" placeholder="请输入宏名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="macroForm.description" type="textarea" placeholder="请输入宏描述" />
        </el-form-item>
        <el-form-item label="宏代码" prop="code">
          <el-input v-model="macroForm.code" type="textarea" placeholder="请输入宏代码" rows="6" />
        </el-form-item>
        <el-form-item label="参数" prop="parameters">
          <el-input v-model="macroForm.parameters" type="textarea" placeholder="请输入宏参数（JSON格式）" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="macroForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditMacroDialog = false">取消</el-button>
          <el-button type="primary" @click="updateMacro">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 执行宏对话框 -->
    <el-dialog
      v-model="showExecuteMacroDialogRef"
      title="执行宏"
      width="600px"
    >
      <el-form :model="executeForm" :rules="executeRules" ref="executeFormRef" label-width="100px">
        <el-form-item label="宏名称">
          <el-input v-model="executeForm.macroName" disabled />
        </el-form-item>
        <el-form-item label="执行参数" prop="params">
          <el-input v-model="executeForm.params" type="textarea" placeholder="请输入执行参数（JSON格式）" rows="4" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showExecuteMacroDialogRef = false">取消</el-button>
          <el-button type="primary" @click="executeMacro">执行</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface Macro {
  id: number
  name: string
  description: string
  code: string
  parameters: any
  is_active: boolean
  created_by: number
  created_at: string
  updated_at: string
}

interface MacroFormData {
  name: string
  description: string
  code: string
  parameters: string
  is_active: boolean
}

interface ExecuteFormData {
  macroName: string
  params: string
}

const macros = ref<Macro[]>([])
const selectedMacro = ref<Macro | null>(null)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddMacroDialog = ref(false)
const showEditMacroDialog = ref(false)
const showExecuteMacroDialogRef = ref(false)
const macroFormRef = ref<FormInstance>()
const executeFormRef = ref<FormInstance>()
const editingMacroId = ref<number>(0)
const executingMacroId = ref<number>(0)

const macroForm = reactive<MacroFormData>({
  name: '',
  description: '',
  code: '',
  parameters: '{}',
  is_active: true
})

const executeForm = reactive<ExecuteFormData>({
  macroName: '',
  params: '{}'
})

const macroRules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入宏名称', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入宏代码', trigger: 'blur' }
  ],
  parameters: [
    { required: true, message: '请输入宏参数', trigger: 'blur' }
  ]
})

const executeRules = reactive<FormRules>({
  params: [
    { required: true, message: '请输入执行参数', trigger: 'blur' }
  ]
})

const filteredMacros = computed(() => {
  if (!searchQuery.value) {
    return macros.value
  }
  const query = searchQuery.value.toLowerCase()
  return macros.value.filter(macro => 
    macro.name.toLowerCase().includes(query) ||
    macro.description.toLowerCase().includes(query) ||
    macro.code.toLowerCase().includes(query)
  )
})

onMounted(async () => {
  await fetchMacros()
})

const fetchMacros = async () => {
  try {
    const response = await axios.get('/api/v1/macros')
    macros.value = response.data
    total.value = response.data.length
  } catch (error) {
    ElMessage.error('获取宏列表失败')
    console.error('Failed to fetch macros:', error)
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
}

const handleMacroStatusChange = async (macro: Macro) => {
  try {
    await axios.put(`/api/v1/macros/${macro.id}`, {
      is_active: macro.is_active
    })
    ElMessage.success('宏状态更新成功')
  } catch (error) {
    ElMessage.error('宏状态更新失败')
    console.error('Failed to update macro status:', error)
    // 恢复原状态
    macro.is_active = !macro.is_active
  }
}

const addMacro = async () => {
  try {
    await macroFormRef.value?.validate()
    
    const response = await axios.post('/api/v1/macros', {
      ...macroForm,
      parameters: JSON.parse(macroForm.parameters)
    })
    macros.value.push(response.data)
    total.value++
    
    showAddMacroDialog.value = false
    resetMacroForm()
    
    ElMessage.success('宏创建成功')
  } catch (error) {
    ElMessage.error('请填写完整的宏信息')
    console.error('Validation error:', error)
  }
}

const editMacro = (macro: Macro) => {
  editingMacroId.value = macro.id
  macroForm.name = macro.name
  macroForm.description = macro.description || ''
  macroForm.code = macro.code
  macroForm.parameters = JSON.stringify(macro.parameters, null, 2)
  macroForm.is_active = macro.is_active
  selectedMacro.value = macro
  showEditMacroDialog.value = true
}

const updateMacro = async () => {
  try {
    await macroFormRef.value?.validate()
    
    const response = await axios.put(`/api/v1/macros/${editingMacroId.value}`, {
      ...macroForm,
      parameters: JSON.parse(macroForm.parameters)
    })
    const index = macros.value.findIndex(m => m.id === editingMacroId.value)
    if (index !== -1) {
      macros.value[index] = response.data
    }
    if (selectedMacro.value?.id === editingMacroId.value) {
      selectedMacro.value = response.data
    }
    
    showEditMacroDialog.value = false
    resetMacroForm()
    
    ElMessage.success('宏更新成功')
  } catch (error) {
    ElMessage.error('请填写完整的宏信息')
    console.error('Validation error:', error)
  }
}

const deleteMacro = async (macroId: number) => {
  try {
    await axios.delete(`/api/v1/macros/${macroId}`)
    macros.value = macros.value.filter(macro => macro.id !== macroId)
    total.value--
    if (selectedMacro.value?.id === macroId) {
      selectedMacro.value = null
    }
    ElMessage.success('宏删除成功')
  } catch (error) {
    ElMessage.error('宏删除失败')
    console.error('Failed to delete macro:', error)
  }
}

const openExecuteMacroDialog = (macro: Macro) => {
  executingMacroId.value = macro.id
  executeForm.macroName = macro.name
  executeForm.params = JSON.stringify(macro.parameters, null, 2)
  showExecuteMacroDialogRef.value = true
}

const executeMacro = async () => {
  try {
    await executeFormRef.value?.validate()
    
    const response = await axios.post(`/api/v1/macros/${executingMacroId.value}/execute`, {
      params: JSON.parse(executeForm.params)
    })
    
    showExecuteMacroDialogRef.value = false
    
    ElMessage.success('宏执行成功')
    console.log('Macro execution result:', response.data)
  } catch (error) {
    ElMessage.error('宏执行失败')
    console.error('Failed to execute macro:', error)
  }
}

const resetMacroForm = () => {
  macroForm.name = ''
  macroForm.description = ''
  macroForm.code = ''
  macroForm.parameters = '{}'
  macroForm.is_active = true
}
</script>

<style scoped>
.advanced-macros {
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

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 14px;
  max-height: 300px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    padding: 10px;
  }

  .header-content h1 {
    margin-bottom: 10px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .card-header .el-input {
    width: 100%;
  }
}
</style>
