<template>
  <div class="data-models-edit">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>编辑数据模型</h1>
          <el-button @click="navigateTo('/data-models')">
            返回列表
          </el-button>
        </div>
      </el-header>
      <el-main>
        <el-card v-if="loading">
          <div class="loading-content">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载中...</span>
          </div>
        </el-card>
        <el-card v-else>
          <template #header>
            <div class="card-header">
              <span>数据模型配置</span>
            </div>
          </template>
          <div class="card-content">
            <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
              <!-- 基本信息 -->
              <el-form-item label="模型名称" prop="name">
                <el-input v-model="form.name" placeholder="请输入模型名称" />
              </el-form-item>
              <el-form-item label="描述" prop="description">
                <el-input v-model="form.description" type="textarea" placeholder="请输入模型描述" />
              </el-form-item>
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
              
              <!-- 维度配置 -->
              <el-form-item label="维度配置" prop="dimensions">
                <el-table :data="form.dimensions" style="width: 100%">
                  <el-table-column prop="name" label="维度名称">
                    <template #default="scope">
                      <el-input v-model="scope.row.name" />
                    </template>
                  </el-table-column>
                  <el-table-column prop="field" label="关联字段">
                    <template #default="scope">
                      <el-select v-model="scope.row.field">
                        <el-option 
                          v-for="field in dataSetFields" 
                          :key="field.name" 
                          :label="field.name" 
                          :value="field.name" 
                        />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="type" label="类型">
                    <template #default="scope">
                      <el-select v-model="scope.row.type">
                        <el-option label="字符串" value="string" />
                        <el-option label="数值" value="number" />
                        <el-option label="日期" value="date" />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="hierarchy" label="层次结构">
                    <template #default="scope">
                      <el-select v-model="scope.row.hierarchy">
                        <el-option 
                          v-for="hierarchy in form.hierarchies" 
                          :key="hierarchy.name" 
                          :label="hierarchy.name" 
                          :value="hierarchy.name" 
                        />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button type="danger" size="small" @click="removeDimension(scope.$index)">
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <el-button type="primary" size="small" @click="addDimension">
                  添加维度
                </el-button>
              </el-form-item>
              
              <!-- 度量配置 -->
              <el-form-item label="度量配置" prop="measures">
                <el-table :data="form.measures" style="width: 100%">
                  <el-table-column prop="name" label="度量名称">
                    <template #default="scope">
                      <el-input v-model="scope.row.name" />
                    </template>
                  </el-table-column>
                  <el-table-column prop="field" label="关联字段">
                    <template #default="scope">
                      <el-select v-model="scope.row.field">
                        <el-option 
                          v-for="field in dataSetFields" 
                          :key="field.name" 
                          :label="field.name" 
                          :value="field.name" 
                        />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="aggregation" label="聚合方式">
                    <template #default="scope">
                      <el-select v-model="scope.row.aggregation">
                        <el-option label="求和" value="sum" />
                        <el-option label="平均值" value="avg" />
                        <el-option label="最大值" value="max" />
                        <el-option label="最小值" value="min" />
                        <el-option label="计数" value="count" />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="format" label="格式化">
                    <template #default="scope">
                      <el-input v-model="scope.row.format" placeholder="如: #,##0.00" />
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button type="danger" size="small" @click="removeMeasure(scope.$index)">
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <el-button type="primary" size="small" @click="addMeasure">
                  添加度量
                </el-button>
              </el-form-item>
              
              <!-- 层次结构配置 -->
              <el-form-item label="层次结构配置" prop="hierarchies">
                <el-table :data="form.hierarchies" style="width: 100%">
                  <el-table-column prop="name" label="层次名称">
                    <template #default="scope">
                      <el-input v-model="scope.row.name" />
                    </template>
                  </el-table-column>
                  <el-table-column prop="levels" label="层级">
                    <template #default="scope">
                      <el-select v-model="scope.row.levels" multiple>
                        <el-option 
                          v-for="dimension in form.dimensions" 
                          :key="dimension.name" 
                          :label="dimension.name" 
                          :value="dimension.name" 
                        />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button type="danger" size="small" @click="removeHierarchy(scope.$index)">
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <el-button type="primary" size="small" @click="addHierarchy">
                  添加层次结构
                </el-button>
              </el-form-item>
              
              <el-form-item label="是否启用" prop="is_active">
                <el-switch v-model="form.is_active" />
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
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules, ElLoading } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'

interface DimensionConfig {
  name: string
  field: string
  type: string
  hierarchy: string | null
}

interface MeasureConfig {
  name: string
  field: string
  aggregation: string
  format: string | null
}

interface HierarchyConfig {
  name: string
  levels: string[]
}

interface FormData {
  id: number
  name: string
  description: string
  data_set_id: number
  dimensions: DimensionConfig[]
  measures: MeasureConfig[]
  hierarchies: HierarchyConfig[]
  is_active: boolean
}

const router = useRouter()
const route = useRoute()
const formRef = ref<FormInstance>()
const loading = ref(true)
const dataSets = ref<any[]>([])
const dataSetFields = ref<any[]>([])

const form = reactive<FormData>({
  id: 0,
  name: '',
  description: '',
  data_set_id: 0,
  dimensions: [],
  measures: [],
  hierarchies: [],
  is_active: true
})

const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入模型名称', trigger: 'blur' }
  ],
  data_set_id: [
    { required: true, message: '请选择数据集', trigger: 'change' }
  ],
  dimensions: [
    { required: true, message: '请至少添加一个维度', trigger: 'change' }
  ],
  measures: [
    { required: true, message: '请至少添加一个度量', trigger: 'change' }
  ]
})

onMounted(async () => {
  await fetchDataSets()
  await fetchDataModel()
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

const fetchDataModel = async () => {
  try {
    const id = route.params.id
    if (!id) {
      ElMessage.error('数据模型ID不能为空')
      navigateTo('/data-models')
      return
    }

    const response = await axios.get(`/api/v1/data-models/${id}`)
    const dataModel = response.data

    // 填充表单数据
    form.id = dataModel.id
    form.name = dataModel.name
    form.description = dataModel.description || ''
    form.data_set_id = dataModel.data_set_id
    form.dimensions = dataModel.dimensions
    form.measures = dataModel.measures
    form.hierarchies = dataModel.hierarchies || []
    form.is_active = dataModel.is_active

    // 获取数据集字段
    await handleDataSetChange()
  } catch (error) {
    ElMessage.error('加载数据模型失败')
    console.error('Failed to fetch data model:', error)
    navigateTo('/data-models')
  } finally {
    loading.value = false
  }
}

const handleDataSetChange = async () => {
  // 当选择数据集时，获取数据集的字段信息
  if (form.data_set_id) {
    try {
      const response = await axios.get(`/api/v1/data-sets/${form.data_set_id}`)
      dataSetFields.value = response.data.fields
    } catch (error) {
      ElMessage.error('获取数据集字段失败')
      console.error('Failed to fetch data set fields:', error)
      dataSetFields.value = []
    }
  } else {
    dataSetFields.value = []
  }
}

const addDimension = () => {
  form.dimensions.push({
    name: '',
    field: '',
    type: 'string',
    hierarchy: null
  })
}

const removeDimension = (index: number) => {
  form.dimensions.splice(index, 1)
}

const addMeasure = () => {
  form.measures.push({
    name: '',
    field: '',
    aggregation: 'sum',
    format: null
  })
}

const removeMeasure = (index: number) => {
  form.measures.splice(index, 1)
}

const addHierarchy = () => {
  form.hierarchies.push({
    name: '',
    levels: []
  })
}

const removeHierarchy = (index: number) => {
  form.hierarchies.splice(index, 1)
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()

    // 准备提交数据
    const submitData = {
      name: form.name,
      description: form.description,
      data_set_id: form.data_set_id,
      dimensions: form.dimensions,
      measures: form.measures,
      hierarchies: form.hierarchies,
      is_active: form.is_active
    }

    await axios.put(`/api/v1/data-models/${form.id}`, submitData)
    ElMessage.success('数据模型更新成功')
    navigateTo('/data-models')
  } catch (error) {
    console.error('Submit error:', error)
    if (error.response) {
      ElMessage.error(`更新失败: ${error.response.data.detail}`)
    } else {
      ElMessage.error('更新失败，请检查输入信息')
    }
  }
}

const handleReset = () => {
  fetchDataModel()
}
</script>

<style scoped>
.data-models-edit {
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

.loading-content {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
}

.loading-content .el-icon {
  margin-right: 10px;
  font-size: 24px;
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
