import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('./views/Home.vue'),
    meta: {
      title: '首页',
      requireAuth: true
    }
  },
  {
    path: '/login',
    component: () => import('./views/auth/Login.vue'),
    meta: {
      title: '登录',
      requireAuth: false
    }
  },
  {
    path: '/data-sources',
    component: () => import('./views/data-sources/Index.vue'),
    meta: {
      title: '数据源管理',
      requireAuth: true
    }
  },
  {
    path: '/data-sources/create',
    component: () => import('./views/data-sources/Create.vue'),
    meta: {
      title: '新建数据源',
      requireAuth: true
    }
  },
  {
    path: '/data-sources/edit/:id',
    component: () => import('./views/data-sources/Edit.vue'),
    meta: {
      title: '编辑数据源',
      requireAuth: true
    }
  },
  {
    path: '/data-sets',
    component: () => import('./views/data-sets/Index.vue'),
    meta: {
      title: '数据集管理',
      requireAuth: true
    }
  },
  {
    path: '/data-sets/create',
    component: () => import('./views/data-sets/Create.vue'),
    meta: {
      title: '新建数据集',
      requireAuth: true
    }
  },
  {
    path: '/data-sets/edit/:id',
    component: () => import('./views/data-sets/Edit.vue'),
    meta: {
      title: '编辑数据集',
      requireAuth: true
    }
  },
  {
    path: '/data-models',
    component: () => import('./views/data-models/Index.vue'),
    meta: {
      title: '数据模型管理',
      requireAuth: true
    }
  },
  {
    path: '/data-models/create',
    component: () => import('./views/data-models/Create.vue'),
    meta: {
      title: '新建数据模型',
      requireAuth: true
    }
  },
  {
    path: '/data-models/edit/:id',
    component: () => import('./views/data-models/Edit.vue'),
    meta: {
      title: '编辑数据模型',
      requireAuth: true
    }
  },
  {
    path: '/visualization',
    component: () => import('./views/visualization/Index.vue'),
    meta: {
      title: '可视化分析',
      requireAuth: true
    }
  },
  {
    path: '/visualization/pivot',
    component: () => import('./views/visualization/Pivot.vue'),
    meta: {
      title: '透视分析',
      requireAuth: true
    }
  },
  {
    path: '/visualization/adhoc',
    component: () => import('./views/visualization/Adhoc.vue'),
    meta: {
      title: '即席查询',
      requireAuth: true
    }
  },
  {
    path: '/visualization/spreadsheet',
    component: () => import('./views/visualization/Spreadsheet.vue'),
    meta: {
      title: '电子表格',
      requireAuth: true
    }
  },
  {
    path: '/dashboards',
    component: () => import('./views/dashboards/Index.vue'),
    meta: {
      title: '仪表盘管理',
      requireAuth: true
    }
  },
  {
    path: '/dashboards/create',
    component: () => import('./views/dashboards/Create.vue'),
    meta: {
      title: '新建仪表盘',
      requireAuth: true
    }
  },
  {
    path: '/dashboards/edit/:id',
    component: () => import('./views/dashboards/Edit.vue'),
    meta: {
      title: '编辑仪表盘',
      requireAuth: true
    }
  },
  {
    path: '/dashboards/create-chart',
    component: () => import('./views/dashboards/CreateChart.vue'),
    meta: {
      title: '新建图表',
      requireAuth: true
    }
  },
  {
    path: '/dashboards/edit-chart/:id',
    component: () => import('./views/dashboards/EditChart.vue'),
    meta: {
      title: '编辑图表',
      requireAuth: true
    }
  },
  {
    path: '/permissions',
    component: () => import('./views/permissions/Index.vue'),
    meta: {
      title: '权限管理',
      requireAuth: true
    }
  },
  {
    path: '/permissions/users',
    component: () => import('./views/permissions/Users.vue'),
    meta: {
      title: '用户管理',
      requireAuth: true
    }
  },
  {
    path: '/permissions/roles',
    component: () => import('./views/permissions/Roles.vue'),
    meta: {
      title: '角色管理',
      requireAuth: true
    }
  },
  {
    path: '/permissions/permissions',
    component: () => import('./views/permissions/Permissions.vue'),
    meta: {
      title: '权限管理',
      requireAuth: true
    }
  },
  {
    path: '/permissions/resources',
    component: () => import('./views/permissions/Resources.vue'),
    meta: {
      title: '资源管理',
      requireAuth: true
    }
  },
  {
    path: '/advanced',
    component: () => import('./views/advanced/Index.vue'),
    meta: {
      title: '高级分析',
      requireAuth: true
    }
  },
  {
    path: '/advanced/ai-analyses',
    component: () => import('./views/advanced/AIAnalyses.vue'),
    meta: {
      title: 'AI分析',
      requireAuth: true
    }
  },
  {
    path: '/advanced/prediction-models',
    component: () => import('./views/advanced/PredictionModels.vue'),
    meta: {
      title: '预测模型',
      requireAuth: true
    }
  },
  {
    path: '/advanced/macros',
    component: () => import('./views/advanced/Macros.vue'),
    meta: {
      title: '宏管理',
      requireAuth: true
    }
  },
  {
    path: '/advanced/system-monitor',
    component: () => import('./views/advanced/SystemMonitor.vue'),
    meta: {
      title: '系统监控',
      requireAuth: true
    }
  },
  {
    path: '/advanced/integrations',
    component: () => import('./views/advanced/Integrations.vue'),
    meta: {
      title: '集成管理',
      requireAuth: true
    }
  }
]

export default routes
