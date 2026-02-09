# 贡献指南

感谢你对 BI报表工具项目的关注！我们欢迎任何形式的贡献，包括但不限于：

- 报告 Bug
- 提出新功能建议
- 提交代码改进
- 改进文档
- 分享使用经验

## AI 辅助开发

本项目特色是使用 AI 辅助开发，我们鼓励你在贡献过程中利用 AI 工具来提高开发效率：

### 推荐的 AI 工具

- **代码生成**：使用 AI 生成初始代码和测试
- **代码审查**：使用 AI 辅助识别代码问题
- **文档生成**：使用 AI 生成和更新文档
- **问题解决**：使用 AI 辅助解决技术难题

### 最佳实践

1. **保持原始性**：确保 AI 生成的代码符合项目规范
2. **人工审查**：所有 AI 生成的代码必须经过人工审查
3. **测试验证**：确保 AI 生成的代码通过测试
4. **持续改进**：提供反馈以改进 AI 辅助开发流程

### 免责声明

- AI 生成的代码可能存在问题，需要人工验证
- 请确保遵守相关开源协议和法律法规
- 保持对代码质量的高标准要求

## 开发环境设置

### 1. Fork 仓库

点击 GitHub 仓库页面右上角的 "Fork" 按钮，将仓库 fork 到你的 GitHub 账号下。

### 2. 克隆仓库

```bash
git clone https://github.com/your-username/bi-x.git
cd bi-x
```

### 3. 添加上游仓库

```bash
git remote add upstream https://github.com/original-owner/bi-x.git
```

### 4. 创建开发分支

```bash
git checkout -b feature/your-feature-name
```

## 开发流程

### 代码规范

#### Python 代码规范

- 遵循 PEP 8 编码规范
- 使用有意义的变量和函数名
- 添加适当的注释和文档字符串
- 保持函数简短，单一职责

示例：
```python
def get_user_by_id(user_id: int) -> Optional[User]:
    """
    根据用户ID获取用户信息
    
    Args:
        user_id: 用户ID
        
    Returns:
        User对象，如果不存在则返回None
    """
    return db.query(User).filter(User.id == user_id).first()
```

#### TypeScript/Vue 代码规范

- 使用 TypeScript 类型注解
- 组件命名使用 PascalCase
- 函数命名使用 camelCase
- 添加适当的注释

示例：
```typescript
interface User {
  id: number
  name: string
  email: string
}

const getUserById = async (userId: number): Promise<User> => {
  const response = await axios.get(`/api/users/${userId}`)
  return response.data
}
```

### 提交规范

使用清晰的提交信息格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型**：
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 重构代码
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**：
```
feat(auth): add JWT token refresh functionality

- Implement token refresh endpoint
- Add automatic token refresh in axios interceptor
- Update login component to handle token expiration

Closes #123
```

## Pull Request 流程

### 1. 确保代码是最新的

```bash
git fetch upstream
git rebase upstream/main
```

### 2. 运行测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

### 3. 代码格式化

```bash
# 后端格式化
cd backend
black .
isort .

# 前端格式化
cd frontend
npm run lint
npm run format
```

### 4. 提交 PR

- 推送到你的 fork 仓库
- 在 GitHub 上创建 Pull Request
- 填写 PR 模板，详细描述你的更改

### PR 模板

```markdown
## 描述
简要描述这个 PR 的目的和实现的功能

## 更改类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 代码重构
- [ ] 文档更新
- [ ] 性能优化

## 测试
描述你如何测试这些更改

## 截图
如果是 UI 相关的更改，请提供截图

## 检查清单
- [ ] 代码遵循项目的代码规范
- [ ] 已添加必要的测试
- [ ] 已更新相关文档
- [ ] 所有测试通过
- [ ] 代码已格式化
```

## 报告 Bug

### Bug 报告模板

```markdown
**问题描述**
清晰简洁地描述问题

**复现步骤**
1. 进入 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**预期行为**
描述你期望发生的事情

**实际行为**
描述实际发生的事情

**截图**
如果适用，添加截图来帮助解释问题

**环境信息**
- OS: [e.g. Windows 10, macOS 12]
- Browser: [e.g. Chrome 96, Safari 15]
- Python Version: [e.g. 3.10]
- Node Version: [e.g. 16.13]

**附加信息**
添加任何其他关于问题的信息
```

## 功能建议

### 功能建议模板

```markdown
**问题描述**
清晰简洁地描述你想要的功能

**解决方案**
描述你希望如何实现这个功能

**替代方案**
描述你考虑过的任何替代解决方案或功能

**附加信息**
添加任何其他关于功能请求的信息
```

## 开发指南

### 后端开发

1. **添加新的 API 端点**

在 `app/api/v1/` 下创建新的模块：

```python
# app/api/v1/your_module/__init__.py
from fastapi import APIRouter
from app.api.v1.your_module import endpoints

router = APIRouter(prefix="/your-module", tags=["your-module"])
router.include_router(endpoints.router)
```

2. **创建数据模型**

在 `app/models/` 下定义模型：

```python
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class YourModel(Base):
    __tablename__ = "your_table"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
```

3. **创建 Pydantic 模式**

在 `app/schemas/` 下定义模式：

```python
from pydantic import BaseModel

class YourModelBase(BaseModel):
    name: str

class YourModelCreate(YourModelBase):
    pass

class YourModelResponse(YourModelBase):
    id: int
    
    class Config:
        from_attributes = True
```

### 前端开发

1. **创建新页面**

在 `src/views/` 下创建页面组件：

```vue
<template>
  <div class="your-page">
    <h1>Your Page</h1>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const data = ref('')
</script>

<style scoped>
.your-page {
  padding: 20px;
}
</style>
```

2. **添加路由**

在 `src/router.ts` 中配置路由：

```typescript
{
  path: '/your-page',
  name: 'YourPage',
  component: () => import('@/views/your-page/Index.vue'),
  meta: {
    title: 'Your Page',
    requireAuth: true
  }
}
```

## 代码审查

所有 Pull Request 都需要经过代码审查。审查者会检查：

- 代码质量和可读性
- 是否遵循项目规范
- 是否有足够的测试
- 是否有性能问题
- 是否有安全问题

## 发布流程

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建 Git tag
4. 发布 GitHub Release

## 行为准则

- 尊重所有贡献者
- 接受建设性批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

## 获取帮助

如果你有任何问题：

- 查看 [文档](README.md)
- 搜索现有的 [Issues](https://github.com/your-username/bi-x/issues)
- 创建新的 Issue 描述你的问题

## 许可证

通过贡献代码，你同意你的贡献将在 [MIT License](LICENSE) 下发布。
