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
                <el-input v-model="name" placeholder="请输入模型名称" />
              </el-form-item>
              <el-form-item label="描述" prop="description">
                <el-input v-model="description" type="textarea" placeholder="请输入模型描述" />
              </el-form-item>
              <el-form-item label="模型类型" prop="model_type">
                <el-select v-model="modelType" placeholder="请选择模型类型">
                  <el-option label="星型模型" value="star" />
                  <el-option label="雪花模型" value="snowflake" />
                </el-select>
              </el-form-item>
              
              <!-- 数据集配置 -->
              <el-form-item label="数据集配置" prop="data_sets">
                <el-alert
                  title="说明"
                  type="info"
                  :closable="false"
                  show-icon
                >
                  <p>数据集配置用于添加数据模型中需要使用的数据集，支持多个数据集。</p>
                  <p>角色说明：</p>
                  <ul>
                    <li>事实表：存储业务事实数据，如销售记录、订单信息等，通常包含度量值。</li>
                    <li>维度表：存储描述性数据，如产品信息、客户信息等，通常用于分析的分类和过滤。</li>
                  </ul>
                </el-alert>
                <br />
                <el-table :data="dataSetsRef" style="width: 100%">
                  <el-table-column prop="data_set_id" label="数据集">
                    <template #default="scope">
                      <el-select v-model="scope.row.data_set_id" @change="fetchDataSetFields(scope.row.data_set_id)">
                        <el-option 
                          v-for="dataSet in dataSets" 
                          :key="dataSet.id" 
                          :label="dataSet.name" 
                          :value="dataSet.id" 
                        />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="role" label="角色">
                    <template #default="scope">
                      <el-select v-model="scope.row.role">
                        <el-option label="事实表" value="fact" />
                        <el-option label="维度表" value="dimension" />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="alias" label="别名">
                    <template #default="scope">
                      <el-input v-model="scope.row.alias" placeholder="可选" />
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button type="danger" size="small" @click="removeDataSet(scope.$index)">
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <el-button type="primary" size="small" @click="addDataSet">
                  添加数据集
                </el-button>
              </el-form-item>
              
              <!-- 关系配置 -->
              <el-form-item label="关系配置" prop="relationships">
                <el-alert
                  title="关系配置"
                  type="info"
                  description="请配置数据集之间的关联关系，支持内连接、左连接、右连接"
                  show-icon
                  :closable="false"
                />
                <br />
                <el-table :data="relationshipsRef" style="width: 100%">
                  <el-table-column prop="source_data_set" label="源数据集">
                    <template #default="scope">
                      <el-select v-model="scope.row.source_data_set" @change="fetchDataSetFields(scope.row.source_data_set)">
                        <el-option 
                          v-for="dataSet in dataSetsRef" 
                          :key="dataSet.data_set_id" 
                          :label="dataSets.find(ds => ds.id === dataSet.data_set_id)?.name || dataSet.data_set_id" 
                          :value="dataSet.data_set_id" 
                        />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="source_field" label="源字段">
                    <template #default="scope">
                      <el-select v-model="scope.row.source_field">
                        <el-option 
                          v-for="field in getDataSetFields(scope.row.source_data_set)" 
                          :key="field.name" 
                          :label="field.name" 
                          :value="field.name" 
                        />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="target_data_set" label="目标数据集">
                    <template #default="scope">
                      <el-select v-model="scope.row.target_data_set" @change="fetchDataSetFields(scope.row.target_data_set)">
                        <el-option 
                          v-for="dataSet in dataSetsRef" 
                          :key="dataSet.data_set_id" 
                          :label="dataSets.find(ds => ds.id === dataSet.data_set_id)?.name || dataSet.data_set_id" 
                          :value="dataSet.data_set_id" 
                        />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="target_field" label="目标字段">
                    <template #default="scope">
                      <el-select v-model="scope.row.target_field">
                        <el-option 
                          v-for="field in getDataSetFields(scope.row.target_data_set)" 
                          :key="field.name" 
                          :label="field.name" 
                          :value="field.name" 
                        />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column prop="join_type" label="连接类型">
                    <template #default="scope">
                      <el-select v-model="scope.row.join_type">
                        <el-option label="内连接" value="inner" />
                        <el-option label="左连接" value="left" />
                        <el-option label="右连接" value="right" />
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button type="danger" size="small" @click="removeRelationship(scope.$index)">
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <el-button type="primary" size="small" @click="addRelationship" :disabled="dataSetsRef.length < 2">
                  添加关系
                </el-button>
              </el-form-item>
              
              <!-- 维度配置 -->
              <el-form-item label="维度配置" prop="dimensions">
                <el-alert
                  title="说明"
                  type="info"
                  :closable="false"
                  show-icon
                >
                  <p>维度是用于分析数据的分类属性，如产品、地区、时间等，通常用于分组和过滤。</p>
                  <p>配置说明：</p>
                  <ul>
                    <li>维度名称：维度的显示名称，如 "产品类别"、"销售地区" 等</li>
                    <li>关联字段：维度对应的数据源字段，格式为 "数据集ID.字段名"</li>
                    <li>类型：维度字段的数据类型，如字符串、数值、日期等</li>
                    <li>层次结构：维度所属的层次结构，如时间层次结构（年-季-月-日）</li>
                  </ul>
                </el-alert>
                <br />
                <el-table :data="dimensionsRef" style="width: 100%">
                  <el-table-column prop="name" label="维度名称">
                    <template #default="scope">
                      <el-input v-model="scope.row.name" />
                    </template>
                  </el-table-column>
                  <el-table-column prop="field" label="关联字段">
                    <template #default="scope">
                      <el-select v-model="scope.row.field">
                        <template v-for="item in filteredDataSetsRef" :key="`ds-${item.data_set_id}`">
                          <el-option-group :label="dataSets.find(ds => ds.id === item.data_set_id)?.name || '未知数据集'">
                            <el-option 
                              v-for="field in getDataSetFields(item.data_set_id)" 
                              :key="`${item.data_set_id}-${field.name}`" 
                              :label="field.name" 
                              :value="`${item.data_set_id}.${field.name}`" 
                            />
                          </el-option-group>
                        </template>
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
                      <el-select v-model="scope.row.hierarchy" placeholder="选择层次结构">
                        <el-option label="无" value="" />
                        <el-option 
                          v-for="hierarchy in hierarchiesRef" 
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
                <el-alert
                  title="说明"
                  type="info"
                  :closable="false"
                  show-icon
                >
                  <p>度量是用于分析数据的数值指标，如销售额、订单数量、利润率等，通常需要进行聚合计算。</p>
                  <p>配置说明：</p>
                  <ul>
                    <li>度量名称：度量的显示名称，如 "销售额"、"订单数量" 等</li>
                    <li>关联字段：度量对应的数据源字段，格式为 "数据集ID.字段名"</li>
                    <li>聚合方式：度量的计算方法，如求和、平均值、最大值、最小值、计数等</li>
                    <li>格式化：度量值的显示格式，如货币格式、百分比格式等</li>
                  </ul>
                </el-alert>
                <br />
                <el-table :data="measuresRef" style="width: 100%">
                  <el-table-column prop="name" label="度量名称">
                    <template #default="scope">
                      <el-input v-model="scope.row.name" />
                    </template>
                  </el-table-column>
                  <el-table-column prop="field" label="关联字段">
                    <template #default="scope">
                      <el-select v-model="scope.row.field">
                        <template v-for="item in filteredDataSetsRef" :key="`ds-${item.data_set_id}`">
                          <el-option-group :label="dataSets.find(ds => ds.id === item.data_set_id)?.name || '未知数据集'">
                            <el-option 
                              v-for="field in getDataSetFields(item.data_set_id)" 
                              :key="`${item.data_set_id}-${field.name}`" 
                              :label="field.name" 
                              :value="`${item.data_set_id}.${field.name}`" 
                            />
                          </el-option-group>
                        </template>
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
                <el-alert
                  title="层次结构配置"
                  type="info"
                  description="请添加数据模型的层次结构，层次结构用于钻取分析"
                  show-icon
                  :closable="false"
                />
                <br />
                <el-table :data="hierarchiesRef" style="width: 100%">
                  <el-table-column prop="name" label="层次名称">
                    <template #default="scope">
                      <el-input v-model="scope.row.name" />
                    </template>
                  </el-table-column>
                  <el-table-column prop="levels" label="层级">
                    <template #default="scope">
                      <el-select v-model="scope.row.levels" multiple>
                        <el-option 
                          v-for="dimension in dimensionsRef" 
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
              
              <el-form-item>
                <el-button type="success" @click="handleSubmit" :loading="submitLoading">
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from '../../utils/axios'
import { ElMessage, FormInstance, FormRules, ElLoading } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'

interface DataSetConfig {
  id: number
  data_set_id: number
  role: string
  alias: string | null
}

interface RelationshipConfig {
  source_data_set: number
  source_field: string
  target_data_set: number
  target_field: string
  join_type: string
}

interface DimensionConfig {
  name: string
  field: string
  type: string
  hierarchy: string
}

interface MeasureConfig {
  name: string
  field: string
  aggregation: string
  format: string
}

interface HierarchyConfig {
  name: string
  levels: string[]
}

interface FormData {
  name: string
  description: string
  model_type: string
  data_sets: DataSetConfig[]
  relationships: RelationshipConfig[]
  dimensions: DimensionConfig[]
  measures: MeasureConfig[]
  hierarchies: HierarchyConfig[]
}

const router = useRouter()
const route = useRoute()
const formRef = ref<FormInstance>()
const loading = ref(true)
const submitLoading = ref(false)
const dataSets = ref<any[]>([])
const dataSetFieldsMap = ref<Record<number, any[]>>({})

// 使用 ref 创建响应式数组
const dataSetsRef = ref<DataSetConfig[]>([])
const relationshipsRef = ref<RelationshipConfig[]>([])
const dimensionsRef = ref<DimensionConfig[]>([])
const measuresRef = ref<MeasureConfig[]>([])
const hierarchiesRef = ref<HierarchyConfig[]>([])

// 表单数据
const name = ref('')
const description = ref('')
const modelType = ref('star')

// 计算属性，用于表单验证
const form = computed(() => ({
  name: name.value,
  description: description.value,
  model_type: modelType.value,
  data_sets: dataSetsRef.value,
  relationships: relationshipsRef.value,
  dimensions: dimensionsRef.value,
  measures: measuresRef.value,
  hierarchies: hierarchiesRef.value
}))

// 计算属性，过滤掉无效数据集
const filteredDataSetsRef = computed(() => {
  return dataSetsRef.value.filter(item => item && item.data_set_id)
})

const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入模型名称', trigger: 'blur' }
  ],
  model_type: [
    { required: true, message: '请选择模型类型', trigger: 'change' }
  ],
  data_sets: [
    { required: true, message: '请至少添加一个数据集', trigger: 'change' }
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
    name.value = dataModel.name
    description.value = dataModel.description || ''
    modelType.value = dataModel.model_type || 'star'
    dataSetsRef.value = dataModel.data_sets || []
    relationshipsRef.value = dataModel.relationships || []
    dimensionsRef.value = dataModel.dimensions || []
    measuresRef.value = dataModel.measures || []
    hierarchiesRef.value = dataModel.hierarchies || []

    // 获取所有数据集的字段
    for (const dataSet of dataSetsRef.value) {
      if (dataSet.data_set_id) {
        await fetchDataSetFields(dataSet.data_set_id)
      }
    }
  } catch (error) {
    ElMessage.error('加载数据模型失败')
    console.error('Failed to fetch data model:', error)
    navigateTo('/data-models')
  } finally {
    loading.value = false
  }
}

const fetchDataSetFields = async (dataSetId: number) => {
  if (!dataSetId) return
  
  try {
    const response = await axios.get(`/api/v1/data-sets/${dataSetId}`)
    dataSetFieldsMap.value[dataSetId] = response.data.fields
  } catch (error) {
    ElMessage.error(`获取数据集 ${dataSetId} 的字段失败`)
    console.error('Failed to fetch data set fields:', error)
    dataSetFieldsMap.value[dataSetId] = []
  }
}

const getDataSetFields = (dataSetId: number) => {
  return dataSetFieldsMap.value[dataSetId] || []
}

const addDataSet = () => {
  const newId = dataSetsRef.value.length + 1
  const newDataSet = {
    id: newId,
    data_set_id: 0,
    role: 'dimension',
    alias: null
  }
  dataSetsRef.value = [...dataSetsRef.value, newDataSet]
}

const removeDataSet = (index: number) => {
  const removedDataSet = dataSetsRef.value[index]
  dataSetsRef.value = dataSetsRef.value.filter((_, i) => i !== index)
  
  // 清理相关关系
  relationshipsRef.value = relationshipsRef.value.filter(rel => 
    rel.source_data_set !== removedDataSet.data_set_id && 
    rel.target_data_set !== removedDataSet.data_set_id
  )
}

const addRelationship = () => {
  const newRelationship = {
    source_data_set: 0,
    source_field: '',
    target_data_set: 0,
    target_field: '',
    join_type: 'inner'
  }
  relationshipsRef.value = [...relationshipsRef.value, newRelationship]
}

const removeRelationship = (index: number) => {
  relationshipsRef.value = relationshipsRef.value.filter((_, i) => i !== index)
}

const addDimension = () => {
  const newDimension = {
    name: '',
    field: '',
    type: 'string',
    hierarchy: null
  }
  dimensionsRef.value = [...dimensionsRef.value, newDimension]
}

const removeDimension = (index: number) => {
  dimensionsRef.value = dimensionsRef.value.filter((_, i) => i !== index)
}

const addMeasure = () => {
  const newMeasure = {
    name: '',
    field: '',
    aggregation: 'sum',
    format: null
  }
  measuresRef.value = [...measuresRef.value, newMeasure]
}

const removeMeasure = (index: number) => {
  measuresRef.value = measuresRef.value.filter((_, i) => i !== index)
}

const addHierarchy = () => {
  const newHierarchy = {
    name: '',
    levels: []
  }
  hierarchiesRef.value = [...hierarchiesRef.value, newHierarchy]
}

const removeHierarchy = (index: number) => {
  hierarchiesRef.value = hierarchiesRef.value.filter((_, i) => i !== index)
}

const handleSubmit = async () => {
  submitLoading.value = true
  try {
    await formRef.value?.validate()

    // 准备提交数据
    const submitData = {
      ...form.value,
      // 处理维度的层次结构，将空字符串转换为null
      dimensions: form.value.dimensions.map(dim => ({
        ...dim,
        hierarchy: dim.hierarchy === '' ? null : dim.hierarchy
      }))
    }

    await axios.put(`/api/v1/data-models/${route.params.id}`, submitData)
    ElMessage.success('数据模型更新成功')
    navigateTo('/data-models')
  } catch (error: any) {
    console.error('Submit error:', error)
    if (error.response) {
      ElMessage.error(`更新失败: ${error.response.data.detail}`)
    } else if (error.message) {
      ElMessage.error(`更新失败: ${error.message}`)
    } else {
      ElMessage.error('更新失败，请检查输入信息')
    }
  } finally {
    submitLoading.value = false
  }
}

const handleReset = () => {
  // 重置表单引用
  formRef.value?.resetFields()
  
  // 重新加载数据模型
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
