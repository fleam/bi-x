<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <h2>BI报表工具 - 登录</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-button" @click="handleLogin">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface FormData {
  username: string
  password: string
}

const formRef = ref<FormInstance>()
const form = reactive<FormData>({
  username: 'admin',
  password: 'admin123'
})

const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
})

const router = useRouter()

const handleLogin = async () => {
  try {
    await formRef.value?.validate()

    const response = await axios.post('/api/v1/auth/login', form)
    
    // 存储token到localStorage
    localStorage.setItem('token', response.data.access_token)
    
    // 跳转到首页
    router.push('/')
    ElMessage.success('登录成功')
  } catch (error: any) {
    console.error('Login error:', error)
    if (error.response) {
      ElMessage.error(`登录失败: ${error.response.data.detail || '用户名或密码错误'}`)
    } else {
      ElMessage.error('登录失败，请检查网络连接')
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.login-form-wrapper {
  width: 400px;
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.login-form-wrapper h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #409EFF;
}

.login-button {
  width: 100%;
}

@media (max-width: 768px) {
  .login-form-wrapper {
    width: 90%;
    padding: 30px;
  }
}
</style>