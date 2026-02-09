<template>
  <div class="data-sources-create">
    <div class="page-header">
      <h1>新建数据源</h1>
      <el-button @click="navigateTo('/data-sources')">
        返回列表
      </el-button>
    </div>
    
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>数据源配置</span>
        </div>
      </template>
      <div class="card-content">
        <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" class="page-form">
          <el-form-item label="数据源名称" prop="name">
            <el-input v-model="form.name" placeholder="请输入数据源名称" />
          </el-form-item>
          <el-form-item label="数据源类型" prop="type">
            <el-select v-model="form.type" placeholder="请选择数据源类型" @change="handleTypeChange">
              <el-option label="数据库" value="database" />
              <el-option label="Excel文件" value="excel" />
              <el-option label="API接口" value="api" />
            </el-select>
          </el-form-item>
          
          <!-- 数据库配置 -->
          <template v-if="form.type === 'database'">
            <el-form-item label="数据库类型" prop="db_type">
              <el-select v-model="form.db_type" placeholder="请选择数据库类型">
                <el-option label="MySQL" value="mysql" />
                <el-option label="Oracle" value="oracle" />
                <el-option label="PostgreSQL" value="postgresql" />
              </el-select>
            </el-form-item>
            <el-form-item label="主机地址" prop="host">
              <el-input v-model="form.host" placeholder="请输入主机地址" />
            </el-form-item>
            <el-form-item label="端口" prop="port">
              <el-input-number v-model="form.port" :min="1" :max="65535" placeholder="请输入端口" />
            </el-form-item>
            <el-form-item label="数据库名称" prop="database">
              <el-input v-model="form.database" placeholder="请输入数据库名称" />
            </el-form-item>
            <el-form-item label="用户名" prop="username">
              <el-input v-model="form.username" placeholder="请输入用户名" />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="form.password" type="password" placeholder="请输入密码" />
            </el-form-item>
          </template>
          
          <!-- Excel配置 -->
          <template v-if="form.type === 'excel'">
            <el-form-item label="文件路径" prop="file_path">
              <el-input v-model="form.file_path" placeholder="请输入Excel文件路径" />
            </el-form-item>
          </template>
          
          <!-- API配置 -->
          <template v-if="form.type === 'api'">
            <el-form-item label="API地址" prop="api_url">
              <el-input v-model="form.api_url" placeholder="请输入API接口地址" />
            </el-form-item>
            <el-form-item label="请求方法" prop="api_method">
              <el-select v-model="form.api_method" placeholder="请选择请求方法">
                <el-option label="GET" value="get" />
                <el-option label="POST" value="post" />
              </el-select>
            </el-form-item>
            <el-form-item label="请求头" prop="api_headers">
              <el-input v-model="form.api_headers" type="textarea" placeholder="请输入请求头（JSON格式）" />
            </el-form-item>
            <el-form-item label="请求体" prop="api_body">
              <el-input v-model="form.api_body" type="textarea" placeholder="请输入请求体（JSON格式）" />
            </el-form-item>
          </template>
          
          <!-- 通用配置 -->
          <el-form-item label="连接池大小" prop="connection_pool">
            <el-input-number v-model="form.connection_pool" :min="1" :max="100" placeholder="请输入连接池大小" />
          </el-form-item>
          <el-form-item label="刷新间隔（秒）" prop="refresh_interval">
            <el-input-number v-model="form.refresh_interval" :min="1" placeholder="请输入刷新间隔" />
          </el-form-item>
          
          <el-form-item>
            <div class="button-group">
              <el-button type="primary" @click="handleTestConnection">
                测试连接
              </el-button>
              <el-button type="success" @click="handleSubmit">
                保存
              </el-button>
              <el-button @click="handleReset">
                重置
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface FormData {
  name: string
  type: string
  db_type: string | null
  host: string | null
  port: number | null
  database: string | null
  username: string | null
  password: string | null
  file_path: string | null
  api_url: string | null
  api_method: string | null
  api_headers: string | null
  api_body: string | null
  connection_pool: number
  refresh_interval: number
}

const router = useRouter()
const formRef = ref<FormInstance>()

const form = reactive<FormData>({
  name: '',
  type: '',
  db_type: null,
  host: null,
  port: null,
  database: null,
  username: null,
  password: null,
  file_path: null,
  api_url: null,
  api_method: null,
  api_headers: null,
  api_body: null,
  connection_pool: 10,
  refresh_interval: 300
})

const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入数据源名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择数据源类型', trigger: 'change' }
  ],
  db_type: [
    { required: form.type === 'database', message: '请选择数据库类型', trigger: 'change' }
  ],
  host: [
    { required: form.type === 'database', message: '请输入主机地址', trigger: 'blur' }
  ],
  port: [
    { required: form.type === 'database', message: '请输入端口', trigger: 'blur' }
  ],
  database: [
    { required: form.type === 'database', message: '请输入数据库名称', trigger: 'blur' }
  ],
  username: [
    { required: form.type === 'database', message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: form.type === 'database', message: '请输入密码', trigger: 'blur' }
  ],
  file_path: [
    { required: form.type === 'excel', message: '请输入文件路径', trigger: 'blur' }
  ],
  api_url: [
    { required: form.type === 'api', message: '请输入API地址', trigger: 'blur' }
  ],
  api_method: [
    { required: form.type === 'api', message: '请选择请求方法', trigger: 'change' }
  ]
})

const navigateTo = (path: string) => {
  router.push(path)
}

const handleTypeChange = () => {
  // 重置相关字段
  if (form.type !== 'database') {
    form.db_type = null
    form.host = null
    form.port = null
    form.database = null
    form.username = null
    form.password = null
  }
  if (form.type !== 'excel') {
    form.file_path = null
  }
  if (form.type !== 'api') {
    form.api_url = null
    form.api_method = null
    form.api_headers = null
    form.api_body = null
  }
}

const handleTestConnection = async () => {
  try {
    await formRef.value?.validate()

    // 准备测试请求数据
    const testRequest = {
      type: form.type,
      db_type: form.db_type,
      host: form.host,
      port: form.port,
      database: form.database,
      username: form.username,
      password: form.password,
      file_path: form.file_path,
      api_url: form.api_url,
      api_method: form.api_method,
      api_headers: form.api_headers ? JSON.parse(form.api_headers) : null,
      api_body: form.api_body ? JSON.parse(form.api_body) : null
    }

    const response = await axios.post('/api/v1/sources/test-connection', testRequest)
    if (response.data.success) {
      ElMessage.success('连接测试成功')
    } else {
      ElMessage.error(`连接测试失败: ${response.data.message}`)
    }
  } catch (error) {
    ElMessage.error('请填写完整的连接信息')
    console.error('Validation error:', error)
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()

    // 准备提交数据
    const submitData = {
      ...form,
      api_headers: form.api_headers ? JSON.parse(form.api_headers) : null,
      api_body: form.api_body ? JSON.parse(form.api_body) : null
    }

    await axios.post('/api/v1/sources/', submitData)
    ElMessage.success('数据源创建成功')
    navigateTo('/data-sources')
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
  handleTypeChange()
}
</script>

<style scoped>
.data-sources-create {
  width: 100%;
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  padding: 16px 0;
}

@media (max-width: 768px) {
  .page-form {
    max-width: 100%;
  }
  
  .el-form {
    label-width: 100px;
  }
}
</style>
