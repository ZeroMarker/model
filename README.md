# Blender 3D模型项目

使用Blender Python API程序化生成的3D模型项目。

## 项目结构

```
├── .github/workflows/     # GitHub Actions工作流
├── blender/               # Blender脚本
│   ├── create_tiananmen.py    # 天安门城楼
│   ├── maodie_cat.py          # 耄耋橘猫（基础版）
│   ├── maodie_cat_detail.py   # 耄耋橘猫（细化版）
│   └── output/                # 生成的blend文件
├── docs/                  # 文档
│   ├── 3d_formats.md          # 3D格式参考
│   ├── blender_character_workflow.md  # 角色制作流程
│   ├── game_model_workflow.md         # 游戏模型流程
│   ├── maodie_cat_doc.md              # 耄耋模型文档
│   ├── project_documentation.md       # 项目文档
│   └── tiananmen_doc.md               # 天安门文档
├── README.md
├── LICENSE
└── .gitignore
```

## 模型列表

### 天安门城楼
- 中国标志性建筑
- 包含城墙、城楼、华表、金水桥等元素
- 重檐歇山顶设计

### 圆头耄耋（橘猫）
- 网络热梗角色
- 特征：圆头、飞机耳、哈气状态
- 细化版包含：精细眼睛、泪痕、虎斑纹、毛发质感

## 快速开始

### 安装Blender

```bash
# Windows (winget)
winget install BlenderFoundation.Blender

# 或LTS版本
winget install BlenderFoundation.Blender.LTS.4.5
```

### 生成模型

```bash
# 天安门城楼
blender --background --python blender/create_tiananmen.py

# 耄耋橘猫（细化版）
blender --background --python blender/maodie_cat_detail.py
```

### 查看模型

```bash
# 打开生成的模型文件
blender blender/output/tiananmen.blend
blender blender/output/maodie_cat_detail.blend
```

## GitHub Actions

项目包含3个自动化工作流：

| 工作流 | 功能 |
|--------|------|
| `render.yml` | 渲染模型预览图 |
| `export.yml` | 导出多格式（GLB/FBX/OBJ/STL） |
| `pages.yml` | 部署3D展示网页 |

## 在线展示

访问 [GitHub Pages](https://zeromarker.github.io/model/) 查看交互式3D模型。

## 文档

详细文档请查看 [docs/](docs/) 目录。

## 许可证

MIT License
