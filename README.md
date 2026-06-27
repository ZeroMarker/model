# 天安门城楼Blender模型

这是一个使用Blender Python API创建的天安门城楼3D模型脚本。

## 模型特点

- 城墙基础（带城门洞）
- 城墙垛口
- 城楼主体（带柱子）
- 重檐歇山顶（双层屋顶）
- 屋脊装饰
- 窗户和匾额
- 华表（2座）
- 石狮子（2座）
- 金水桥
- 完整场景设置（灯光、相机、材质）

## 使用方法

### 方法一：在Blender中运行脚本

1. 打开Blender
2. 切换到"脚本"工作区
3. 点击"打开"按钮，选择 `create_tiananmen.py` 文件
4. 点击"运行脚本"按钮（或按 Alt+P）
5. 模型将自动创建在场景中

### 方法二：通过命令行运行

```bash
# 后台运行（不显示Blender界面）
blender --background --python create_tiananmen.py

# 显示Blender界面运行
blender --python create_tiananmen.py
```

### 方法三：作为插件安装（可选）

1. 在Blender中，选择 "编辑" > "偏好设置" > "插件"
2. 点击 "安装" 按钮
3. 选择 `create_tiananmen.py` 文件
4. 启用插件

## 渲染设置

- 渲染引擎：Cycles
- 分辨率：1920×1080
- 背景：天蓝色
- 已配置相机和灯光

## 自定义修改

脚本中的参数可以调整：

- `wall.scale`：城墙尺寸
- `tower_body.scale`：城楼尺寸
- `roof_lower.scale`：屋顶尺寸
- 材质颜色：修改 `create_material` 函数的参数
- 相机位置：修改 `camera.location`

## 系统要求

- Blender 2.8 或更高版本（推荐 5.1.2）
- 支持Cycles渲染引擎

## 快速开始

### 安装Blender（Windows）

```bash
# 使用winget安装最新版Blender
winget install BlenderFoundation.Blender

# 或安装LTS版本
winget install BlenderFoundation.Blender.LTS.4.5
```

### 生成模型

```bash
# 命令行生成（后台模式）
"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --background --python create_tiananmen.py

# 或打开Blender GUI后运行脚本
```

生成完成后会自动创建 `tiananmen.blend` 文件。

## 注意事项

1. 首次运行可能需要编译着色器，请耐心等待
2. 模型为简化版本，适合学习和展示使用
3. 如需更精细的模型，可以调整细分级别
4. 运行脚本后会自动生成 `tiananmen.blend` 文件

## 项目文件

- `create_tiananmen.py` - 模型创建脚本
- `tiananmen.blend` - 生成的Blender模型文件
- `README.md` - 说明文档

## 许可证

MIT License