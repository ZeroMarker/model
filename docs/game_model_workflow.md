# 游戏开发模型制作流程

## 一、流程总览

```
概念设计 → 高模雕刻 → 低模拓扑 → UV展开 → 烘焙贴图 → 材质绘制 → 引擎导入 → 优化调试
```

---

## 二、阶段详解

### 阶段1：概念设计（Concept）

**目标**：确定角色/场景的视觉风格

**工作内容**：
- 绘制概念图（正面/侧面/3/4角度）
- 确定配色方案
- 标注材质和细节说明
- 制作情绪板（Mood Board）

**工具**：
- Photoshop、Procreate（2D绘制）
- Blender Grease Pencil（3D概念）
- PureRef（参考图整理）

**输出**：概念图、参考板

---

### 阶段2：高模雕刻（High-Poly Sculpting）

**目标**：制作高精度模型，用于烘焙细节

**工作内容**：
- 基础体块搭建（Blocking）
- 大型塑造（Major Forms）
- 中等细节雕刻（Medium Details）
- 精细细节雕刻（Fine Details）：毛孔、褶皱、划痕

**工具**：
- ZBrush（行业标准）
- Blender Sculpt Mode
- 3D Coat

**技术要点**：
- 从低细分开始，逐级提升
- 使用对称工具提高效率
- 善用遮罩（Mask）和变形（Deformation）
- 适时使用Extract提取部件

**输出**：高模（百万~千万面）

---

### 阶段3：低模拓扑（Retopology）

**目标**：创建游戏可用的低面数模型

**面数参考**：
| 类型 | 主机/PC | 移动端 |
|------|---------|--------|
| 主角 | 15K-60K三角面 | 3K-10K三角面 |
| NPC | 5K-20K三角面 | 1K-5K三角面 |
| 场景物件 | 50-2K三角面 | 20-500三角面 |
| 武器 | 1K-5K三角面 | 200-1K三角面 |

**拓扑原则**：
- 边线走向跟随肌肉/结构
- 关节处保持足够布线（便于变形）
- 避免三角面和多边面（尽量全四边形）
- 保持均匀的面密度
- 边缘环（Edge Loop）卡住转折处

**工具**：
- Blender RetopoFlow插件
- TopoGun
- 3D Coat Auto-Retopo
- ZRemesher（ZBrush自动拓扑）

**输出**：低模（游戏面数）

---

### 阶段4：UV展开（UV Unwrapping）

**目标**：将3D表面映射到2D平面，用于贴图绘制

**展开原则**：
- 接缝（Seam）放在隐蔽位置
- 减少拉伸变形
- 保持UV岛（Island）大小比例一致
- 充分利用UV空间（利用率>85%）
- 对称部件可重叠UV节省空间

**UV集策略**：
- 角色：身体/头部/装备分离
- 场景：按材质/贴图集分组
- 使用UDIM支持多张贴图

**工具**：
- Blender UV Editor + UVPackMaster
- RizomUV（专业UV工具）
- UVLayout

**输出**：展开好的UV

---

### 阶段5：贴图烘焙（Texture Baking）

**目标**：将高模细节投射到低模贴图上

**烘焙贴图类型**：
| 贴图类型 | 用途 | 常见命名 |
|---------|------|---------|
| Normal Map | 表面凹凸细节 | _n, _normal |
| AO (Ambient Occlusion) | 环境遮蔽阴影 | _ao |
| Curvature | 边缘/凹凸信息 | _curv |
| World Space Normal | 世界法线 | _wsn |
| Position | 位置信息 | _pos |
| Thickness | 厚度/透光 | _thick |
| ID Map | 材质分区 | _id |

**烘焙流程**：
1. 高低模对齐匹配
2. 设置Cage（投射笼）或手动调整偏移
3. 分部件烘焙（避免穿插）
4. 检查并修复烘焙错误（翻转、丢失细节）

**工具**：
- Marmoset Toolbag（烘焙首选）
- Substance Painter（内置烘焙）
- Blender Cycles烘焙
- XNormal（免费）

**输出**：烘焙贴图集

---

### 阶段6：材质绘制（Texturing）

**目标**：制作PBR材质

**PBR工作流**：

**Metal/Roughness（金属/粗糙度）**：
- BaseColor（基础颜色）
- Metallic（金属度）
- Roughness（粗糙度）
- Normal（法线）
- AO（环境遮蔽）
- Emission（自发光）

**Specular/Glossiness（高光/光泽度）**：
- Diffuse（漫反射）
- Specular（高光）
- Glossiness（光泽度）
- Normal（法线）

**绘制层次**：
1. 基础材质层（Base Material）
2. 颜色变化层（Color Variation）
3. 磨损层（Wear）：边缘磨损、划痕
4. 污渍层（Dirt）：灰尘、油污
5. 细节层（Details）：图案、文字

**工具**：
- Substance Painter（行业标准）
- Substance Designer（程序化材质）
- Quixel Mixer
- Mari（高精度角色）

**输出**：PBR贴图集

---

### 阶段7：骨骼绑定（Rigging）

**目标**：为角色创建骨骼控制系统

**骨骼层级**：
```
Root
├── Hips（骨盆）
│   ├── Spine → Spine1 → Spine2 → Chest
│   │   ├── Neck → Head
│   │   │   └── Jaw, Eye_L, Eye_R
│   │   ├── Shoulder_L → UpperArm_L → LowerArm_L → Hand_L
│   │   └── Shoulder_R → UpperArm_R → LowerArm_R → Hand_R
│   ├── UpperLeg_L → LowerLeg_L → Foot_L → Toe_L
│   └── UpperLeg_R → LowerLeg_R → Foot_R → Toe_R
```

**绑定方式**：
- **FK（正向运动学）**：父骨骼带动子骨骼
- **IK（反向运动学）**：末端控制整条链
- **混合IK/FK**：根据动画需求切换

**控制器类型**：
- 变形骨骼（Deform Bones）
- 控制器（Controllers）
- 约束器（Constraints）

**工具**：
- Blender Armature系统
- Maya HumanIK
- Mixamo（自动绑定）
- AccuRIG

**输出**：绑定好的角色

---

### 阶段8：蒙皮权重（Skinning）

**目标**：定义网格如何跟随骨骼变形

**权重绘制原则**：
- 平滑过渡，避免突变
- 关节处权重渐变（肩部、膝盖）
- 手指独立权重
- 使用镜像功能对称绘制

**常见问题**：
- 肩部塌陷：增加锁骨权重
- 膝盖/肘部扭曲：调整骨骼朝向
- 腹部变形：优化脊椎权重分布

**工具**：
- Blender Weight Paint
- Maya Paint Skin Weights
- 智能权重（自动蒙皮）

**输出**：权重数据

---

### 阶段9：动画制作（Animation）

**动画类型**：
| 类型 | 说明 | 帧率 |
|------|------|------|
| 待机（Idle） | 站立呼吸动画 | 30-60帧循环 |
| 行走（Walk） | 移动动画 | 30-60帧循环 |
| 跑步（Run） | 快速移动 | 20-40帧循环 |
| 攻击（Attack） | 战斗动作 | 15-30帧 |
| 受击（Hit） | 被击反应 | 10-20帧 |
| 死亡（Death） | 死亡动画 | 30-60帧 |

**动画原则**（迪士尼12原则）：
1. 挤压与拉伸（Squash & Stretch）
2. 预备动作（Anticipation）
3. 演出（Staging）
4. 连贯动作（Straight Ahead）& 关键姿势（Pose to Pose）
5. 跟随与重叠（Follow Through）
6. 慢入慢出（Slow In & Out）
7. 弧线运动（Arcs）
8. 次要动作（Secondary Action）
9. 时间节奏（Timing）
10. 夸张（Exaggeration）
11. 扎实绘画（Solid Drawing）
12. 吸引力（Appeal）

**工具**：
- Blender动画系统
- Maya动画工具
- MotionBuilder（动捕数据处理）
- Mixamo（预制动画）

**输出**：动画数据（关键帧/动捕）

---

### 阶段10：引擎导入与优化

**Unity导入**：
1. 设置模型导入设置（Scale、Normals）
2. 配置材质（Standard/URP/HDRP）
3. 设置动画控制器（Animator Controller）
4. 配置LOD组
5. 设置碰撞体（Collider）
6. 优化：Static Batching、GPU Instancing

**Unreal导入**：
1. FBX导入设置
2. 创建材质实例（Material Instance）
3. 设置骨骼网格体（Skeletal Mesh）
4. 配置动画蓝图（Animation Blueprint）
5. 设置物理资产（Physics Asset）
6. 优化：Nanite（UE5）、LOD、HLOD

**优化检查清单**：
- [ ] 面数控制在目标范围
- [ ] 贴图尺寸合理（不超过2K/4K）
- [ ] 使用纹理图集减少Draw Call
- [ ] 启用Mipmap
- [ ] 压缩贴图格式
- [ ] 设置合适的LOD层级
- [ ] 合并静态网格体
- [ ] 遮挡剔除配置

**输出**：引擎内可用资产

---

## 三、常用软件组合

### 专业管线

| 环节 | 软件 | 备选 |
|------|------|------|
| 概念设计 | Photoshop | Procreate |
| 高模雕刻 | ZBrush | Blender |
| 低模建模 | Maya / 3ds Max | Blender |
| UV展开 | RizomUV | Blender |
| 贴图烘焙 | Marmoset Toolbag | Substance Painter |
| 材质绘制 | Substance Painter | Mari |
| 骨骼绑定 | Maya | Blender |
| 动画制作 | Maya / MotionBuilder | Blender |
| 引擎 | Unity / Unreal | Godot |

### 独立开发者管线

| 环节 | 软件 |
|------|------|
| 全流程 | Blender |
| 材质绘制 | Substance Painter |
| 烘焙 | Marmoset Toolbag / Blender |
| 引擎 | Unity / Unreal / Godot |

---

## 四、文件命名规范

### 模型文件
```
[类型]_[名称]_[变体]_[版本]
例：CH_Hero_A_v01.fbx
    SM_Chair_01_v02.blend
    WP_Sword_A_v01.fbx
```

前缀说明：
- CH = Character（角色）
- SM = Static Mesh（静态网格）
- WP = Weapon（武器）
- VEH = Vehicle（载具）
- ENV = Environment（环境）

### 贴图文件
```
[名称]_[贴图类型].[格式]
例：Hero_BaseColor.png
    Hero_Normal.png
    Hero_Metallic.png
    Hero_Roughness.png
    Hero_AO.png
```

### 动画文件
```
[角色]_[动画类型]_[变体]
例：Hero_Idle_01.fbx
    Hero_Walk_Forward.fbx
    Hero_Attack_A.fbx
```

---

## 五、性能预算模板

### 角色性能预算

| 项目 | 主机/PC | 移动端 |
|------|---------|--------|
| 三角面数 | 30K-60K | 3K-10K |
| 骨骼数 | 60-100 | 30-50 |
| 贴图尺寸 | 2K-4K | 512-1K |
| 贴图数量 | 4-6张 | 2-3张 |
| 材质球数 | 1-2个 | 1个 |

### 场景性能预算

| 项目 | 主机/PC | 移动端 |
|------|---------|--------|
| 同屏三角面 | 1-5M | 100K-500K |
| Draw Call | 2000-5000 | 100-300 |
| 贴图内存 | 2-4GB | 256-512MB |
| LOD层级 | 3-4级 | 2-3级 |

---

## 六、检查清单

### 模型检查
- [ ] 面数符合预算
- [ ] 布线合理（四边形为主）
- [ ] 无孤立顶点/边
- [ ] 法线方向正确
- [ ] 比例正确（1单位=1米）

### UV检查
- [ ] 无重叠（除非有意复用）
- [ ] 拉伸最小化
- [ ] 接缝位置合理
- [ ] UV利用率>85%
- [ ] 岛屿间距足够

### 贴图检查
- [ ] 分辨率是2的幂次（512,1024,2048...）
- [ ] 无明显接缝
- [ ] 金属度/粗糙度范围正确
- [ ] 法线贴图无翻转
- [ ] 文件大小合理

### 引擎检查
- [ ] 导入设置正确（缩放、朝向）
- [ ] 材质参数匹配
- [ ] 碰撞体设置
- [ ] LOD配置
- [ ] 光照测试通过

---

## 参考资源

- [Polycount Wiki](http://wiki.polycount.com/)
- [FlippedNormals](https://flippednormals.com/)
- [80 Level](https://80.lv/)
- [ArtStation Learning](https://www.artstation.com/learning)
- [Substance 3D Documentation](https://helpx.adobe.com/substance-3d/)
