<template>
  <div class="auth-login">
    <div class="login-background"></div>
    <div class="login-container">
      <div class="login-form-wrapper">
        <div class="login-header">
          <div class="login-logo">
            <el-icon class="logo-icon"><DataAnalysis /></el-icon>
          </div>
          <h1 class="login-title">BI报表工具</h1>
          <p class="login-subtitle">数据驱动决策，智能洞察未来</p>
        </div>
        
        <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="0">
          <el-form-item prop="username">
            <el-input 
              v-model="loginForm.username" 
              placeholder="请输入用户名" 
              prefix-icon="UserFilled"
              class="login-input"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input 
              v-model="loginForm.password" 
              type="password" 
              placeholder="请输入密码" 
              prefix-icon="Lock"
              show-password
              class="login-input"
            />
          </el-form-item>
          <el-form-item>
            <el-button 
              type="primary" 
              class="login-button" 
              @click="handleLogin" 
              :loading="loading"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="login-footer">
          <span>© 2026 BI报表工具</span>
          <span class="version">v1.0.0</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../../utils/axios'
import { isAxiosError } from 'axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { UserFilled, Lock, DataAnalysis } from '@element-plus/icons-vue'

interface LoginFormData {
  username: string
  password: string
}

const router = useRouter()
const loginFormRef = ref<FormInstance>()
const loading = ref(false)

const loginForm = reactive<LoginFormData>({
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

const handleLogin = async () => {
  try {
    await loginFormRef.value?.validate()
    loading.value = true

    // 发送登录请求
    const response = await axios.post('/api/v1/auth/login', {
      username: loginForm.username,
      password: loginForm.password
    })

    // 保存token和用户信息
    const token = response.data.access_token
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(response.data.user))

    // 跳转到首页
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error: any) {
    console.error('Login error:', error)
    
    if (isAxiosError(error)) {
      if (error.response) {
        const status = error.response.status
        const detail = error.response.data?.detail
        
        if (status === 401) {
          ElMessage.error(detail || '用户名或密码错误')
        } else if (status === 404) {
          ElMessage.error('登录接口不存在，请联系管理员')
        } else if (status === 500) {
          ElMessage.error('服务器错误，请稍后重试')
        } else {
          ElMessage.error(detail || '登录失败，请稍后重试')
        }
      } else if (error.request) {
        ElMessage.error('网络连接失败，请检查网络设置')
      } else {
        ElMessage.error('请求配置错误，请重试')
      }
    } else {
      ElMessage.error('登录失败，请检查网络连接')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-login {
  height: 100vh;
  width: 100vw;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  z-index: 1;
}

.login-background::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMzLjMxNCAwIDYtMi42ODYgNi02cy0yLjY4Ni02LTYtNmMtMy4zMTQgMC02IDIuNjg2LTYgNnMyLjY4NiA2IDYgNnptMC0xOGMzLjMxNCAwIDYtMi42ODYgNi02cy0yLjY4Ni02LTYtNmMtMy4zMTQgMC02IDIuNjg2LTYgNnMyLjY4NiA2IDYgNnptLTM2IDBjMy4zMTQgMCA2LTIuNjg2IDYtNnMtMi42ODYtNi02LTZjLTMuMzE0IDAtNiAyLjY4Ni02IDZzMi42ODYgNiA2IDZ6bTAgMThjMy4zMTQgMCA2LTIuNjg2IDYtNnMtMi42ODYtNi02LTZjLTMuMzE0IDAtNiAyLjY4Ni02IDZzMi42ODYgNiA2IDZ6IiBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iMC41IiBmaWxsPSJ1cmwoI2JhY2tncm91bmQpIi8+PC9nPjwvc3ZnPg==');
  opacity: 0.1;
  z-index: -1;
}

.login-container {
  width: 100%;
  max-width: 420px;
  padding: 0 20px;
  z-index: 2;
}

.login-form-wrapper {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 48px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.18);
  animation: fadeInUp 0.6s ease-out;
}

.login-header {
  margin-bottom: 40px;
}

.login-logo {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
  animation: pulse 2s infinite;
}

.logo-icon {
  font-size: 40px;
  color: white;
}

.login-title {
  margin: 0 0 12px 0;
  font-size: 28px;
  font-weight: 700;
  color: #1e3c72;
  letter-spacing: -0.5px;
}

.login-subtitle {
  margin: 0 0 32px 0;
  font-size: 16px;
  color: #666;
  line-height: 1.5;
}

.login-input {
  border-radius: 10px;
  height: 50px;
  font-size: 16px;
  border: 1px solid #e1e8ed;
  transition: all 0.3s ease;
}

.login-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.login-button {
  width: 100%;
  height: 50px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
  margin-top: 24px;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.login-button:loading {
  transform: none;
}

.login-footer {
  margin-top: 32px;
  font-size: 14px;
  color: #999;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.version {
  opacity: 0.8;
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
  }
  50% {
    box-shadow: 0 6px 24px rgba(102, 126, 234, 0.5);
  }
  100% {
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-form-wrapper {
    padding: 36px 24px;
    margin: 0 16px;
  }
  
  .login-logo {
    width: 64px;
    height: 64px;
  }
  
  .logo-icon {
    font-size: 32px;
  }
  
  .login-title {
    font-size: 24px;
  }
  
  .login-subtitle {
    font-size: 14px;
  }
  
  .login-input {
    height: 44px;
    font-size: 14px;
  }
  
  .login-button {
    height: 44px;
    font-size: 14px;
  }
  
  .login-footer {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .login-form-wrapper {
    padding: 28px 20px;
  }
  
  .login-title {
    font-size: 20px;
  }
  
  .login-subtitle {
    font-size: 13px;
  }
}
</style>
