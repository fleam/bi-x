<template>
  <div class="permissions-list">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>权限管理</h1>
          <el-button type="primary" @click="showAddPermissionDialog = true">
            新增权限
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <div class="card-header">
              <span>权限列表</span>
              <el-input
                v-model="searchQuery"
                placeholder="搜索权限"
                prefix-icon="el-icon-search"
                style="width: 300px"
              />
            </div>
          </template>
          <div class="card-content">
            <el-table :data="filteredPermissions" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="权限名称" />
              <el-table-column prop="code" label="权限代码" />
              <el-table-column prop="description" label="描述" />
              <el-table-column prop="is_active" label="状态" width="100">
                <template #default="scope">
                  <el-switch v-model="scope.row.is_active" @change="handlePermissionStatusChange(scope.row)" />
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="editPermission(scope.row)">
                    编辑
                  </el-button>
                  <el-button type="danger" size="small" @click="deletePermission(scope.row.id)">
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

    <!-- 添加权限对话框 -->
    <el-dialog
      v-model="showAddPermissionDialog"
      title="新增权限"
      width="600px"
    >
      <el-form :model="permissionForm" :rules="permissionRules" ref="permissionFormRef" label-width="100px">
        <el-form-item label="权限名称" prop="name">
          <el-input v-model="permissionForm.name" placeholder="请输入权限名称" />
        </el-form-item>
        <el-form-item label="权限代码" prop="code">
          <el-input v-model="permissionForm.code" placeholder="请输入权限代码，如 dashboard:view" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="permissionForm.description" type="textarea" placeholder="请输入权限描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddPermissionDialog = false">取消</el-button>
          <el-button type="primary" @click="addPermission">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑权限对话框 -->
    <el-dialog
      v-model="showEditPermissionDialog"
      title="编辑权限"
      width="600px"
    >
      <el-form :model="permissionForm" :rules="permissionRules" ref="permissionFormRef" label-width="100px">
        <el-form-item label="权限名称" prop="name">
          <el-input v-model="permissionForm.name" placeholder="请输入权限名称" />
        </el-form-item>
        <el-form-item label="权限代码" prop="code">
          <el-input v-model="permissionForm.code" placeholder="请输入权限代码，如 dashboard:view" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="permissionForm.description" type="textarea" placeholder="请输入权限描述" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="permissionForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditPermissionDialog = false">取消</el-button>
          <el-button type="primary" @click="updatePermission">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules } from 'element-plus'

interface Permission {
  id: number
  name: string
  code: string
  description: string
  is_active: boolean
  created_at: string
  updated_at: string
}

interface PermissionFormData {
  name: string
  code: string
  description: string
  is_active: boolean
}

const permissions = ref<Permission[]>([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddPermissionDialog = ref(false)
const showEditPermissionDialog = ref(false)
const permissionFormRef = ref<FormInstance>()
const editingPermissionId = ref<number>(0)

const permissionForm = reactive<PermissionFormData>({
  name: '',
  code: '',
  description: '',
  is_active: true
})

const permissionRules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入权限名称', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入权限代码', trigger: 'blur' }
  ]
})

const filteredPermissions = computed(() => {
  if (!searchQuery.value) {
    return permissions.value
  }
  const query = searchQuery.value.toLowerCase()
  return permissions.value.filter(permission => 
    permission.name.toLowerCase().includes(query) ||
    permission.code.toLowerCase().includes(query) ||
    permission.description.toLowerCase().includes(query)
  )
})

onMounted(async () => {
  await fetchPermissions()
})

const fetchPermissions = async () => {
  try {
    const response = await axios.get('/api/v1/permissions')
    permissions.value = response.data
    total.value = response.data.length
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

const handlePermissionStatusChange = async (permission: Permission) => {
  try {
    await axios.put(`/api/v1/permissions/${permission.id}`, {
      is_active: permission.is_active
    })
    ElMessage.success('权限状态更新成功')
  } catch (error) {
    ElMessage.error('权限状态更新失败')
    console.error('Failed to update permission status:', error)
    // 恢复原状态
    permission.is_active = !permission.is_active
  }
}

const addPermission = async () => {
  try {
    await permissionFormRef.value?.validate()
    
    const response = await axios.post('/api/v1/permissions', permissionForm)
    permissions.value.push(response.data)
    total.value++
    
    showAddPermissionDialog.value = false
    resetPermissionForm()
    
    ElMessage.success('权限创建成功')
  } catch (error) {
    ElMessage.error('请填写完整的权限信息')
    console.error('Validation error:', error)
  }
}

const editPermission = (permission: Permission) => {
  editingPermissionId.value = permission.id
  permissionForm.name = permission.name
  permissionForm.code = permission.code
  permissionForm.description = permission.description
  permissionForm.is_active = permission.is_active
  showEditPermissionDialog.value = true
}

const updatePermission = async () => {
  try {
    await permissionFormRef.value?.validate()
    
    const response = await axios.put(`/api/v1/permissions/${editingPermissionId.value}`, permissionForm)
    const index = permissions.value.findIndex(p => p.id === editingPermissionId.value)
    if (index !== -1) {
      permissions.value[index] = response.data
    }
    
    showEditPermissionDialog.value = false
    resetPermissionForm()
    
    ElMessage.success('权限更新成功')
  } catch (error) {
    ElMessage.error('请填写完整的权限信息')
    console.error('Validation error:', error)
  }
}

const deletePermission = async (permissionId: number) => {
  try {
    await axios.delete(`/api/v1/permissions/${permissionId}`)
    permissions.value = permissions.value.filter(permission => permission.id !== permissionId)
    total.value--
    ElMessage.success('权限删除成功')
  } catch (error) {
    ElMessage.error('权限删除失败')
    console.error('Failed to delete permission:', error)
  }
}

const resetPermissionForm = () => {
  permissionForm.name = ''
  permissionForm.code = ''
  permissionForm.description = ''
  permissionForm.is_active = true
}
</script>

<style scoped>
.permissions-list {
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
