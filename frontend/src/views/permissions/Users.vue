<template>
  <div class="permissions-users">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>用户管理</h1>
          <el-button type="primary" @click="showAddUserDialog = true">
            新增用户
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>用户列表</span>
              <el-input
                v-model="searchQuery"
                placeholder="搜索用户"
                prefix-icon="el-icon-search"
                style="width: 300px"
              />
            </div>
          </template>
          <div class="card-content">
            <el-table :data="filteredUsers" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="username" label="用户名" />
              <el-table-column prop="email" label="邮箱" />
              <el-table-column prop="name" label="姓名" />
              <el-table-column prop="is_active" label="状态" width="100">
                <template #default="scope">
                  <el-switch v-model="scope.row.is_active" @change="handleUserStatusChange(scope.row)" />
                </template>
              </el-table-column>
              <el-table-column prop="roles" label="角色" min-width="150">
                <template #default="scope">
                  <el-tag 
                    v-for="role in scope.row.roles" 
                    :key="role.id"
                    size="small"
                    style="margin-right: 5px"
                  >
                    {{ role.name }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="editUser(scope.row)">
                    编辑
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteUser(scope.row.id)">
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
      </el-main>
    </el-container>

    <!-- 添加用户对话框 -->
    <el-dialog
      v-model="showAddUserDialog"
      title="新增用户"
      width="600px"
    >
      <el-form :model="userForm" :rules="userRules" ref="userFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="角色" prop="role_ids">
          <el-select v-model="userForm.role_ids" multiple placeholder="请选择角色">
            <el-option 
              v-for="role in roles" 
              :key="role.id" 
              :label="role.name" 
              :value="role.id" 
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddUserDialog = false">取消</el-button>
          <el-button type="primary" @click="addUser">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑用户对话框 -->
    <el-dialog
      v-model="showEditUserDialog"
      title="编辑用户"
      width="600px"
    >
      <el-form :model="userForm" :rules="userRules" ref="userFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码（不修改请留空）" />
        </el-form-item>
        <el-form-item label="角色" prop="role_ids">
          <el-select v-model="userForm.role_ids" multiple placeholder="请选择角色">
            <el-option 
              v-for="role in roles" 
              :key="role.id" 
              :label="role.name" 
              :value="role.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="userForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditUserDialog = false">取消</el-button>
          <el-button type="primary" @click="updateUser">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface User {
  id: number
  username: string
  email: string
  name: string
  is_active: boolean
  roles: Array<{ id: number, name: string }>
  created_at: string
  updated_at: string
}

interface UserFormData {
  username: string
  email: string
  name: string
  password: string
  role_ids: number[]
  is_active: boolean
}

const users = ref<User[]>([])
const roles = ref<any[]>([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddUserDialog = ref(false)
const showEditUserDialog = ref(false)
const userFormRef = ref<FormInstance>()
const editingUserId = ref<number>(0)

const userForm = reactive<UserFormData>({
  username: '',
  email: '',
  name: '',
  password: '',
  role_ids: [],
  is_active: true
})

const userRules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ],
  role_ids: [
    { required: true, message: '请至少选择一个角色', trigger: 'change' }
  ]
})

const filteredUsers = computed(() => {
  if (!searchQuery.value) {
    return users.value
  }
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(user => 
    user.username.toLowerCase().includes(query) ||
    user.email.toLowerCase().includes(query) ||
    user.name.toLowerCase().includes(query)
  )
})

onMounted(async () => {
  await fetchUsers()
  await fetchRoles()
})

const fetchUsers = async () => {
  try {
    const response = await axios.get('/api/v1/users')
    users.value = response.data
    total.value = response.data.length
  } catch (error) {
    ElMessage.error('获取用户列表失败')
    console.error('Failed to fetch users:', error)
  }
}

const fetchRoles = async () => {
  try {
    const response = await axios.get('/api/v1/roles')
    roles.value = response.data
  } catch (error) {
    ElMessage.error('获取角色列表失败')
    console.error('Failed to fetch roles:', error)
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
}

const handleUserStatusChange = async (user: User) => {
  try {
    await axios.put(`/api/v1/users/${user.id}`, {
      is_active: user.is_active
    })
    ElMessage.success('用户状态更新成功')
  } catch (error) {
    ElMessage.error('用户状态更新失败')
    console.error('Failed to update user status:', error)
    // 恢复原状态
    user.is_active = !user.is_active
  }
}

const addUser = async () => {
  try {
    await userFormRef.value?.validate()
    
    const response = await axios.post('/api/v1/users', userForm)
    users.value.push(response.data)
    total.value++
    
    showAddUserDialog.value = false
    resetUserForm()
    
    ElMessage.success('用户创建成功')
  } catch (error) {
    ElMessage.error('请填写完整的用户信息')
    console.error('Validation error:', error)
  }
}

const editUser = (user: User) => {
  editingUserId.value = user.id
  userForm.username = user.username
  userForm.email = user.email
  userForm.name = user.name
  userForm.password = ''
  userForm.role_ids = user.roles.map(role => role.id)
  userForm.is_active = user.is_active
  showEditUserDialog.value = true
}

const updateUser = async () => {
  try {
    await userFormRef.value?.validate()
    
    const response = await axios.put(`/api/v1/users/${editingUserId.value}`, userForm)
    const index = users.value.findIndex(u => u.id === editingUserId.value)
    if (index !== -1) {
      users.value[index] = response.data
    }
    
    showEditUserDialog.value = false
    resetUserForm()
    
    ElMessage.success('用户更新成功')
  } catch (error) {
    ElMessage.error('请填写完整的用户信息')
    console.error('Validation error:', error)
  }
}

const deleteUser = async (userId: number) => {
  try {
    await axios.delete(`/api/v1/users/${userId}`)
    users.value = users.value.filter(user => user.id !== userId)
    total.value--
    ElMessage.success('用户删除成功')
  } catch (error) {
    ElMessage.error('用户删除失败')
    console.error('Failed to delete user:', error)
  }
}

const resetUserForm = () => {
  userForm.username = ''
  userForm.email = ''
  userForm.name = ''
  userForm.password = ''
  userForm.role_ids = []
  userForm.is_active = true
}
</script>

<style scoped>
.permissions-users {
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
