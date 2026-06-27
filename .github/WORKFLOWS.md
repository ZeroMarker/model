# GitHub Actions 工作流

本项目包含以下自动化工作流：

## 工作流列表

### 1. Render Models (`render.yml`)

**触发条件：**
- 推送到 `main` 分支（修改 `.py` 或 `.blend` 文件）
- Pull Request 到 `main` 分支
- 手动触发

**功能：**
- 自动安装 Blender
- 运行 Python 脚本生成模型
- 渲染模型预览图
- 上传渲染结果为 Artifact

---

### 2. Export Models (`export.yml`)

**触发条件：**
- 推送标签 `v*`（版本发布）
- 手动触发（可选择导出格式）

**功能：**
- 并行导出两个模型
- 支持格式：GLB、FBX、OBJ、STL
- 上传导出文件为 Artifact（保留90天）

**手动触发示例：**
1. 进入 Actions 页面
2. 选择 "Export Models"
3. 点击 "Run workflow"
4. 选择导出格式

---

### 3. GitHub Pages (`pages.yml`)

**触发条件：**
- 推送到 `main` 分支
- 手动触发

**功能：**
- 生成 GLB 格式模型
- 创建交互式 3D 展示网页
- 使用 `<model-viewer>` 组件
- 自动部署到 GitHub Pages

**展示内容：**
- 天安门城楼 3D 模型
- 圆头耄耋橘猫 3D 模型
- 支持旋转、缩放交互

---

## 使用方法

### 自动触发

```bash
# 推送代码自动触发渲染
git add .
git commit -m "Update models"
git push origin main

# 发布版本触发导出
git tag v1.0.0
git push origin v1.0.0
```

### 手动触发

1. 进入 GitHub 仓库页面
2. 点击 "Actions" 标签
3. 选择要运行的工作流
4. 点击 "Run workflow"
5. 选择参数（如果有）
6. 点击绿色 "Run workflow" 按钮

---

## 查看结果

### Artifacts（构建产物）

1. 进入 Actions 页面
2. 点击完成的工作流运行
3. 在 "Artifacts" 部分下载文件

### GitHub Pages

1. 进入仓库 Settings → Pages
2. 确认 Source 为 "GitHub Actions"
3. 访问 `https://<username>.github.io/<repo>/`

---

## 自定义配置

### 修改触发条件

编辑 `on` 部分：

```yaml
on:
  push:
    branches: [ main, develop ]
    paths:
      - 'models/**'
```

### 修改 Blender 版本

```yaml
- name: Install specific Blender version
  run: |
    wget https://download.blender.org/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz
    tar -xf blender-4.0.2-linux-x64.tar.xz
    sudo mv blender-4.0.2-linux-x64 /opt/blender
```

### 添加渲染参数

```yaml
- name: Render with settings
  run: |
    blender --background --python render.py -- \
      --render-output renders/ \
      --render-frame 1 \
      --render-anim \
      --engine CYCLES
```

---

## 故障排除

### Blender 安装失败

```yaml
- name: Install Blender (alternative)
  run: |
    sudo snap install blender --classic
```

### 内存不足

```yaml
jobs:
  render:
    runs-on: ubuntu-latest-4-cores  # 使用更大实例
```

### 导出格式不支持

某些格式可能需要额外插件，检查 Blender 版本支持情况。

---

## 相关链接

- [Blender CLI 文档](https://docs.blender.org/manual/en/latest/advanced/command_line/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [model-viewer 组件](https://modelviewer.dev/)
