<template>
  <div class="permissions-roles">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>角色管理</h1>
          <el-button type="primary" @click="showAddRoleDialog = true">
            新增角色
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>角色列表</span>
              <el-input
                v-model="searchQuery"
                placeholder="搜索角色"
                prefix-icon="el-icon-search"
                style="width: 300px"
              />
            </div>
          </template>
          <div class="card-content">
            <el-table :data="filteredRoles" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="角色名称" />
              <el-table-column prop="description" label="描述" />
              <el-table-column prop="is_active" label="状态" width="100">
                <template #default="scope">
                  <el-switch v-model="scope.row.is_active" @change="handleRoleStatusChange(scope.row)" />
                </template>
              </el-table-column>
              <el-table-column prop="permissions" label="权限数量" width="120">
                <template #default="scope">
                  {{ scope.row.permissions.length }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="editRole(scope.row)">
                    编辑
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteRole(scope.row.id)">
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

    <!-- 添加角色对话框 -->
    <el-dialog
      v-model="showAddRoleDialog"
      title="新增角色"
      width="600px"
    >
      <el-form :model="roleForm" :rules="roleRules" ref="roleFormRef" label-width="100px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="roleForm.description" type="textarea" placeholder="请输入角色描述" />
        </el-form-item>
        <el-form-item label="权限" prop="permission_ids">
          <el-select v-model="roleForm.permission_ids" multiple placeholder="请选择权限">
            <el-option 
              v-for="permission in permissions" 
              :key="permission.id" 
              :label="permission.name" 
              :value="permission.id" 
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddRoleDialog = false">取消</el-button>
          <el-button type="primary" @click="addRole">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑角色对话框 -->
    <el-dialog
      v-model="showEditRoleDialog"
      title="编辑角色"
      width="600px"
    >
      <el-form :model="roleForm" :rules="roleRules" ref="roleFormRef" label-width="100px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="roleForm.description" type="textarea" placeholder="请输入角色描述" />
        </el-form-item>
        <el-form-item label="权限" prop="permission_ids">
          <el-select v-model="roleForm.permission_ids" multiple placeholder="请选择权限">
            <el-option 
              v-for="permission in permissions" 
              :key="permission.id" 
              :label="permission.name" 
              :value="permission.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="roleForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditRoleDialog = false">取消</el-button>
          <el-button type="primary" @click="updateRole">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface Role {
  id: number
  name: string
  description: string
  is_active: boolean
  permissions: Array<{ id: number, name: string }>
  created_at: string
  updated_at: string
}

interface RoleFormData {
  name: string
  description: string
  permission_ids: number[]
  is_active: boolean
}

const roles = ref<Role[]>([])
const permissions = ref<any[]>([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddRoleDialog = ref(false)
const showEditRoleDialog = ref(false)
const roleFormRef = ref<FormInstance>()
const editingRoleId = ref<number>(0)

const roleForm = reactive<RoleFormData>({
  name: '',
  description: '',
  permission_ids: [],
  is_active: true
})

const roleRules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' }
  ],
  permission_ids: [
    { required: true, message: '请至少选择一个权限', trigger: 'change' }
  ]
})

const filteredRoles = computed(() => {
  if (!searchQuery.value) {
    return roles.value
  }
  const query = searchQuery.value.toLowerCase()
  return roles.value.filter(role => 
    role.name.toLowerCase().includes(query) ||
    role.description.toLowerCase().includes(query)
  )
})

onMounted(async () => {
  await fetchRoles()
  await fetchPermissions()
})

const fetchRoles = async () => {
  try {
    const response = await axios.get('/api/v1/roles')
    roles.value = response.data
    total.value = response.data.length
  } catch (error) {
    ElMessage.error('获取角色列表失败')
    console.error('Failed to fetch roles:', error)
  }
}

const fetchPermissions = async () => {
  try {
    const response = await axios.get('/api/v1/permissions')
    permissions.value = response.data
  } catch (error) {
    ElMessage.error('获取权限列表失败')
    console.error('Failed to fetch permissions:', error)
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
}

const handleRoleStatusChange = async (role: Role) => {
  try {
    await axios.put(`/api/v1/roles/${role.id}`, {
      is_active: role.is_active
    })
    ElMessage.success('角色状态更新成功')
  } catch (error) {
    ElMessage.error('角色状态更新失败')
    console.error('Failed to update role status:', error)
    // 恢复原状态
    role.is_active = !role.is_active
  }
}

const addRole = async () => {
  try {
    await roleFormRef.value?.validate()
    
    const response = await axios.post('/api/v1/roles', roleForm)
    roles.value.push(response.data)
    total.value++
    
    showAddRoleDialog.value = false
    resetRoleForm()
    
    ElMessage.success('角色创建成功')
  } catch (error) {
    ElMessage.error('请填写完整的角色信息')
    console.error('Validation error:', error)
  }
}

const editRole = (role: Role) => {
  editingRoleId.value = role.id
  roleForm.name = role.name
  roleForm.description = role.description
  roleForm.permission_ids = role.permissions.map(permission => permission.id)
  roleForm.is_active = role.is_active
  showEditRoleDialog.value = true
}

const updateRole = async () => {
  try {
    await roleFormRef.value?.validate()
    
    const response = await axios.put(`/api/v1/roles/${editingRoleId.value}`, roleForm)
    const index = roles.value.findIndex(r => r.id === editingRoleId.value)
    if (index !== -1) {
      roles.value[index] = response.data
    }
    
    showEditRoleDialog.value = false
    resetRoleForm()
    
    ElMessage.success('角色更新成功')
  } catch (error) {
    ElMessage.error('请填写完整的角色信息')
    console.error('Validation error:', error)
  }
}

const deleteRole = async (roleId: number) => {
  try {
    await axios.delete(`/api/v1/roles/${roleId}`)
    roles.value = roles.value.filter(role => role.id !== roleId)
    total.value--
    ElMessage.success('角色删除成功')
  } catch (error) {
    ElMessage.error('角色删除失败')
    console.error('Failed to delete role:', error)
  }
}

const resetRoleForm = () => {
  roleForm.name = ''
  roleForm.description = ''
  roleForm.permission_ids = []
  roleForm.is_active = true
}
</script>

<style scoped>
.permissions-roles {
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
