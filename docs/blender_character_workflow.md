# Blender游戏角色制作完整流程

## 一、流程概览

```
参考收集 → 基础网格 → 高模雕刻 → 低模重拓扑 → UV展开 → 烘焙 → 材质绘制 → 骨骼绑定 → 蒙皮权重 → 动画制作 → 引擎导出
```

---

## 二、阶段1：参考收集与准备

### 1.1 收集参考图
- 正面/侧面概念图（比例标注）
- 背面参考（如有）
- 细节特写（武器、配饰、纹样）
- 颜色/材质参考
- 同类风格参考

### 1.2 Blender设置
```
1. 打开Blender，删除默认立方体
2. 添加背景图：
   - 侧边栏(N面板) → View → Background Images
   - Add Image → 选择正面/侧面参考图
   - 设置Axis为Front/Side
   - 调整Opacity和Size

3. 设置单位：
   - Scene Properties → Units
   - Unit System: Metric
   - Length: Meters
   - 1单位 = 1米（角色约1.7-1.8单位高）
```

### 1.3 推荐插件安装
| 插件 | 用途 | 获取方式 |
|------|------|---------|
| LoopTools | 布线辅助 | 内置插件 |
| F2 | 快速建面 | 内置插件 |
| Bool Tool | 布尔运算 | 内置插件 |
| RetopoFlow | 重拓扑 | Blender Market |
| UVPackMaster | UV排列 | Blender Market |
| Auto-Rig Pro | 自动绑定 | Blender Market |
| Rigify | 骨骼系统 | 内置插件 |

---

## 三、阶段2：基础网格建模（Blocking）

### 3.1 人体基础比例

**成人男性标准比例（8头身）**：
```
头顶 → 下巴 = 1头
下巴 → 胸线 = 1头
胸线 → 肚脐 = 1头
肚脐 → 胯部 = 1头
胯部 → 膝盖 = 2头
膝盖 → 脚底 = 2头
```

**关键比例点**：
- 肩宽 ≈ 2.5头宽
- 肘部与肚脐齐平
- 手腕与胯部齐平
- 手臂展开 ≈ 身高

### 3.2 基础网格创建方法

**方法A：从立方体开始**
```
1. Add → Mesh → Cube
2. 进入Edit Mode (Tab)
3. Subdivide多次获得足够布线
4. 使用Proportional Editing (O)调整大形
5. 逐步塑造人体轮廓
```

**方法B：使用基础体拼接**
```
1. 分别创建：
   - Cube → 躯干
   - Cylinder → 四肢
   - Sphere → 关节
   - Cube → 手脚
2. 使用Join (Ctrl+J)合并
3. 用Merge (M)焊接顶点
4. 调整整体比例
```

**方法C：使用MakeHuman/MB-Lab**
```
1. 安装MB-Lab插件
2. Create → Choose Base Model
3. 调整参数生成基础人体
4. Apply生成Mesh
5. 删除不需要的部分
```

### 3.3 布线基础规则

```
- 四边形为主（动画变形需要）
- 边线走向跟随肌肉方向
- 关节处保持足够环线
- 避免三角面和N-gon
- 保持均匀面密度
```

**关键布线区域**：
```
眼睛：8边环线
嘴巴：环形布线
肩膀：3-4圈环线
肘部/膝盖：2-3圈环线
手指：2-3圈环线
```

---

## 四、阶段3：高模雕刻（Sculpting）

### 3.1 雕刻准备

```
1. 选择模型 → 右键 → Shade Smooth
2. 添加Multiresolution修改器
3. 点击Subdivide 2-3次（根据需要）
4. 或直接使用Sculpt Mode雕刻
```

### 3.2 雕刻流程

**第一步：大型塑造**
```
工具：Grab、Clay Strips、Smooth
目标：确定整体比例和大体积
技巧：
- 对称雕刻 (Tool Settings → Symmetry → X)
- 低细分级别工作
- 频繁旋转检查各角度
```

**第二步：结构细化**
```
工具：Clay Strips、Crease、Inflate
目标：塑造肌肉/服装结构
关键区域：
- 头部：头骨、颧骨、下颌
- 躯干：胸肌、腹肌、背阔肌
- 四肢：三角肌、肱二头肌、股四头肌
```

**第三步：细节雕刻**
```
工具：Dam Standard、Standard、Alpha笔刷
目标：添加毛孔、褶皱、纹理
技巧：
- 使用Alpha贴图快速添加细节
- 善用Layer笔刷保留可逆性
- 分层管理不同细节
```

### 3.3 服装/装备雕刻

**布料雕刻**：
```
1. 从身体Extract提取表面
2. 使用Solidify增加厚度
3. 雕刻褶皱：
   - 悬垂褶皱（Drapery）
   - 拉伸褶皱（Tension Folds）
   - 扭曲褶皱（Twist Folds）
4. 添加边缘磨损
```

**硬表面雕刻**（盔甲、武器）：
```
方法1：Mask + Extract
- 用Mask划定区域
- Extract提取网格
- 雕刻细节

方法2：布尔运算
- 用基础形状切割
- 添加倒角细节

方法3：Insert Mesh
- 使用预制Insert笔刷
- 组合拼接
```

### 3.4 雕刻快捷键速查

| 操作 | 快捷键 |
|------|--------|
| 旋转视图 | 鼠标中键 |
| 平移视图 | Shift+中键 |
| 缩放视口 | Ctrl+中键 / 滚轮 |
| 笔刷大小 | F |
| 笔刷强度 | Shift+F |
| 撤销 | Ctrl+Z |
| 切换对称 | X/Y/Z |
| 遮罩绘制 | Ctrl+笔刷 |
| 清除遮罩 | Ctrl+D |
| 反转遮罩 | Ctrl+I |
| 细分级别切换 | Ctrl+0/1/2/3 |

---

## 五、阶段4：低模重拓扑（Retopology）

### 5.1 重拓扑准备

```
1. 保留高模用于烘焙
2. 复制高模（Shift+D）作为低模基础
3. 或新建Mesh开始拓扑
4. 开启Snap to Face（吸附到面）
```

### 5.2 吸附设置

```
1. 开启吸附：工具栏磁铁图标 或 按钮（Shift+Tab）
2. 吸附模式：Face
3. 勾选Project onto Self
4. 编辑模式下，新顶点会自动吸附到高模表面
```

### 5.3 RetopoFlow插件使用

```
安装后：
1. 选择高模
2. 切换到RetopoFlow模式
3. 使用工具：
   - Strokes：画线自动布线
   - PolyPen：逐点创建多边形
   - Contours：沿环线拓扑
   - Relax：松弛布线
```

### 5.4 手动重拓扑流程

**步骤1：创建起始面**
```
1. 新建Mesh (Add → Mesh → Plane)
2. 进入Edit Mode
3. 开启Snap to Face
4. 将平面贴合到高模表面
```

**步骤2：扩展拓扑**
```
使用快捷键：
- E：挤出边
- F：填面
- Ctrl+R：环切
- J：连接顶点
- K：切割工具
```

**步骤3：关键区域布线**

**头部拓扑**：
```
眼睛周围：8边环线
嘴巴周围：环形布线
鼻翼：连接眼嘴环线
额头：横向布线
下巴：扇形展开
```

**躯干拓扑**：
```
胸肌：环形跟随肌肉走向
腹肌：纵向分割
背部：跟随肩胛骨方向
侧面：连接前后布线
```

**关节拓扑**：
```
肩膀/肘部/膝盖：
- 至少3圈环线
- 中间环线在关节中心
- 便于弯曲变形
```

### 5.5 面数参考

| 部位 | 主机/PC | 移动端 |
|------|---------|--------|
| 头部 | 2000-4000 | 500-1000 |
| 躯干 | 3000-6000 | 800-1500 |
| 手臂(单) | 1500-3000 | 400-800 |
| 手(单) | 1000-2000 | 300-600 |
| 腿(单) | 2000-4000 | 500-1000 |
| 脚(单) | 800-1500 | 200-400 |
| **总计** | **15K-60K** | **3K-10K** |

---

## 六、阶段5：UV展开（UV Unwrapping）

### 6.1 UV接缝规划

**接缝放置原则**：
```
- 隐藏位置（内侧、底部）
- 自然边界（服装边缘、装备接缝）
- 对称模型可只展一半
- 减少接缝数量
```

**角色接缝位置**：
```
头部：头顶→耳后→下巴底部
躯干：背面中线、腋下
手臂：内侧中线
腿：内侧中线
手：手腕→中指内侧
脚：脚底中线
```

### 6.2 UV展开流程

**步骤1：标记接缝**
```
1. 进入Edit Mode
2. 选择要作为接缝的边
3. Ctrl+E → Mark Seam
4. 接缝边显示为红色
```

**步骤2：展开UV**
```
1. 全选Mesh (A)
2. U键 → Unwrap
3. 或使用：
   - Smart UV Project（自动展开）
   - Cube Projection（盒式投影）
   - Follow Active Quads（跟随活动四边面）
```

**步骤3：调整UV**
```
在UV Editor中：
- G：移动
- R：旋转
- S：缩放
- Alt+S：沿法线缩放（松弛拉伸）
- Stitch (V)：缝合UV岛
```

### 6.3 UV排列优化

**手动排列**：
```
1. 保持UV岛朝向一致
2. 排列紧凑，减少空白
3. 保持岛之间间距（防止泄漏）
```

**使用UVPackMaster**：
```
1. 安装UVPackMaster插件
2. 全选UV岛
3. Pack Islands (Ctrl+P)
4. 设置参数：
   - Rotation: 45度或自由
   - Margin: 0.005-0.01
5. 执行排列
```

### 6.4 UV检查

```
1. 添加棋盘格纹理检查拉伸
2. UV → Display → Stretch
3. 确保无重叠（Select → Select Overlap）
4. 检查UV利用率
```

---

## 七、阶段6：贴图烘焙（Baking）

### 7.1 Blender内置烘焙设置

**准备高低模**：
```
1. 确保高低模位置重合
2. 高模可略微放大（防止漏光）
3. 低模UV展开完成
```

**烘焙设置**：
```
1. 选择低模 → 材质属性 → 新建材质
2. 添加Image Texture节点
3. 新建贴图（分辨率2048或4096）
4. 选中Image Texture节点（重要！）
5. 渲染属性 → Bake：
   - Bake Type: Normal / AO / etc.
   - Selected to Active: 勾选
   - Ray Distance: 调整（防止漏光）
6. 先选高模，再Shift选低模（低模为活动对象）
7. 点击Bake
```

### 7.2 分部件烘焙

```
1. 将模型分成多个部分（头、身、手、脚等）
2. 每个部分单独烘焙
3. 避免部件间相互干扰
4. 最终合成到同一张贴图
```

### 7.3 使用Marmoset Toolbag烘焙（推荐）

```
1. 导出高低模为FBX
2. 在Toolbag中创建Baker对象
3. 导入高低模
4. 配置烘焙参数：
   - Cage调整
   - 法线格式（OpenGL/DirectX）
   - 输出分辨率
5. 一键烘焙所有贴图
6. 导出贴图集
```

### 7.4 烘焙贴图类型

| 贴图 | 用途 | Blender设置 |
|------|------|------------|
| Normal | 凹凸细节 | Bake Type: Normal |
| AO | 环境遮蔽 | Bake Type: AO |
| Curvature | 边缘信息 | 需插件或外部工具 |
| Position | 位置数据 | Bake Type: Position |
| Emission | 自发光 | Bake Type: Emit |

---

## 八、阶段7：材质绘制（Texturing）

### 8.1 Blender纹理绘制模式

**进入纹理绘制**：
```
1. 选择模型
2. 切换到Texture Paint工作区
3. 或Tab → Texture Paint模式
```

**绘制设置**：
```
侧边栏(T)：
- Brush: 笔刷类型
- Radius: 大小 (F)
- Strength: 强度 (Shift+F)
- Color: 颜色选择
- Texture: Alpha纹理
```

### 8.2 使用Substance Painter（推荐）

**导出准备**：
```
1. 确保模型已烘焙贴图
2. 导出为FBX（包含UV）
3. 导出AO、Normal等烘焙贴图
```

**Substance Painter流程**：
```
1. File → New Project
2. 选择模板（PBR Metallic Roughness）
3. 导入模型
4. 导入烘焙贴图
5. 添加材质层：
   - Base Material（基础材质）
   - Color Variation（颜色变化）
   - Dirt（污渍）
   - Wear（磨损）
6. 导出贴图集
```

### 8.3 贴图导出设置

**Unity (URP)**：
```
- BaseColor (RGB)
- Normal Map (OpenGL)
- Metallic (R) + Smoothness (A) 或
- Metallic (R) + Roughness (A) 取决于设置
```

**Unreal Engine**：
```
- BaseColor (RGB)
- Normal (DirectX)
- OcclusionRoughnessMetallic (RGA)
```

---

## 九、阶段8：骨骼绑定（Rigging）

### 9.1 使用Rigify

**步骤1：启用插件**
```
1. Edit → Preferences → Add-ons
2. 搜索"Rigify"
3. 勾选启用
```

**步骤2：生成骨骼**
```
1. Add → Armature → Human (Meta-Rig)
2. 调整骨骼位置匹配角色：
   - 进入Edit Mode
   - 移动/缩放骨骼
   - 对齐到角色关节位置
3. 生成完整Rig：
   - 选择Meta-Rig
   - Properties → Armature → Generate Rig
```

**步骤3：Rigify控制说明**
```
控制骨骼类型：
- 绿色：FK控制器
- 蓝色：IK控制器
- 黄色：特殊控制（脊椎、手指等）

常用控制器：
- 脚部：Cube控制器（IK/FK切换）
- 手部：圆形控制器
- 脊椎：方形控制器
- 头部：圆形控制器
```

### 9.2 Auto-Rig Pro

```
1. 安装Auto-Rig Pro插件
2. 启动Smart功能：
   - 放置标记点（头部、手、脚、脊椎）
   - 自动检测比例
   - 生成骨骼
3. 微调骨骼位置
4. 生成控制器
5. 绑定到网格
```

### 9.3 手动绑定流程

```
1. 创建骨骼链：
   - Add → Armature
   - 进入Edit Mode
   - E挤出骨骼
   - 命名规范：DEF-upper_arm.L

2. 骨骼层级：
   - Parent (Ctrl+P)建立父子关系
   - Root → Hips → Spine → ...

3. 添加约束：
   - IK Constraint（反向运动学）
   - Copy Rotation/Location
   - Track To
```

---

## 十、阶段9：蒙皮权重（Weight Painting）

### 10.1 自动权重

```
1. 先选择模型，再Shift选择骨骼
2. Ctrl+P → Armature Deform → With Automatic Weights
3. 测试变形是否正常
```

### 10.2 手动权重绘制

**进入权重绘制模式**：
```
1. 选择模型
2. 切换到Weight Paint模式
3. 或在Object Mode选择骨骼后自动切换
```

**绘制工具**：
```
- Draw：绘制权重
- Blur：模糊过渡
- Add：增加权重
- Subtract：减少权重
- Multiply：乘以权重
- Average：平均权重
```

**绘制技巧**：
```
1. 选择骨骼：Ctrl+点击 或 侧边栏选择
2. 颜色说明：
   - 红色：权重1.0（完全跟随）
   - 蓝色：权重0.0（不跟随）
   - 渐变：平滑过渡
3. 使用Mirror功能对称绘制
4. 善用Blur工具平滑过渡
```

### 10.3 常见权重问题修复

**肩部塌陷**：
```
1. 减少肩膀对锁骨的权重
2. 增加胸椎对肩膀的权重
3. 添加Shoulder骨骼控制
```

**肘部/膝盖扭曲**：
```
1. 检查骨骼朝向（Roll角度）
2. 调整关节处权重渐变
3. 添加Twist骨骼
```

**手指变形**：
```
1. 确保每根手指独立权重
2. 检查手指骨骼命名
3. 绘制精确权重
```

---

## 十一、阶段10：动画制作（Animation）

### 11.1 动画基础设置

**时间轴设置**：
```
1. Timeline面板 → 设置帧率（24/30/60fps）
2. 设置起始/结束帧
3. Scene Properties → Units → Time
```

**动画工作区**：
```
1. Animation工作区布局：
   - 3D Viewport（查看动画）
   - Timeline（时间轴）
   - Dope Sheet（关键帧编辑）
   - Graph Editor（曲线编辑）
```

### 11.2 关键帧动画

**插入关键帧**：
```
1. 选择骨骼
2. 移动到目标帧
3. 调整姿势
4. I键 → 插入关键帧：
   - Location（位置）
   - Rotation（旋转）
   - Scale（缩放）
   - LocRotScale（全部）
```

**常用快捷键**：
```
- I：插入关键帧
- Alt+I：删除关键帧
- Ctrl+Tab：切换Pose/Object模式
- A：全选骨骼
- Alt+R：清除旋转
- Alt+G：清除位置
- Alt+S：清除缩放
```

### 11.3 基础动画制作

**待机动画（Idle）**：
```
1. 第1帧：标准站立姿势
2. 第15帧：微微下沉（膝盖微弯）
3. 第30帧：回到站立（或轻微变化）
4. 设置循环：
   - Graph Editor → Add Modifier → Cycles
   - 或手动复制首尾帧
```

**行走循环（Walk Cycle）**：
```
关键姿势（4帧法）：
1. Contact（接触）：双脚着地
2. Down（下沉）：重心最低
3. Passing（过渡）：单脚支撑
4. Up（上升）：重心最高

30帧循环：
Frame 1: Contact (右脚前)
Frame 8: Down
Frame 15: Passing (左脚支撑)
Frame 22: Up
Frame 30: Contact (同Frame 1)
```

**跑步循环（Run Cycle）**：
```
特点：
- 腾空阶段（双脚离地）
- 更大的手臂摆动
- 身体前倾角度更大

24帧循环：
Frame 1: Contact
Frame 6: Down
Frame 12: Passing
Frame 18: Up/Flight
Frame 24: Contact
```

### 11.4 动画层与动作库

**使用动画层**：
```
1. Properties → Object Data → Animation Layers
2. 添加新层
3. 在不同层制作动画
4. 调整层权重混合
```

**NLA编辑器**：
```
1. 将动作转换为Strip
2. 在NLA中排列、混合动作
3. 创建动画状态机
```

**动作库**：
```
1. 创建动作：Action Editor → New
2. 保存动作：Asset Browser → Mark as Asset
3. 拖拽使用已保存的动作
```

---

## 十二、阶段11：引擎导出

### 12.1 FBX导出设置

**Unity导出**：
```
File → Export → FBX
- Scale: 1.0
- Forward: -Z Forward
- Up: Y Up
- Apply Transform: 勾选
- Mesh → Smoothing: Face
- Armature → Add Leaf Bones: 取消勾选
- Animation → Baked Animation: 勾选
```

**Unreal导出**：
```
File → Export → FBX
- Scale: 1.0
- Forward: -Y Forward（或X Forward取决于设置）
- Up: Z Up
- Apply Transform: 勾选
- Armature → Primary/Secondary Bone Axis调整
```

### 12.2 glTF导出

```
File → Export → glTF 2.0
- Format: glTF Binary (.glb)
- Apply Modifiers: 勾选
- UV: 勾选
- Normals: 勾选
- Tangents: 勾选
- Vertex Colors: 根据需要
- Materials: 勾选
- Animations: 勾选
```

### 12.3 导出检查清单

```
模型：
- [ ] 缩放正确（1单位=1米）
- [ ] 应用所有变换 (Ctrl+A → All Transforms)
- [ ] 法线正确
- [ ] 无重叠顶点
- [ ] 无孤立顶点/边

UV：
- [ ] UV展开完成
- [ ] 无重叠
- [ ] 贴图已烘焙/绘制

骨骼：
- [ ] 骨骼命名规范
- [ ] 无多余骨骼
- [ ] 骨骼朝向一致

动画：
- [ ] 关键帧已烘焙
- [ ] 起止帧正确
- [ ] 循环动画首尾帧一致
```

---

## 十三、Blender快捷键速查表

### 常用全局

| 操作 | 快捷键 |
|------|--------|
| 撤销 | Ctrl+Z |
| 重做 | Ctrl+Shift+Z |
| 保存 | Ctrl+S |
| 全选 | A |
| 取消选择 | Alt+A |
| 删除 | X |
| 搜索菜单 | F3 |
| 快速收藏夹 | Q |

### 编辑模式

| 操作 | 快捷键 |
|------|--------|
| 切换模式 | Tab |
| 点选择 | 1 |
| 边选择 | 2 |
| 面选择 | 3 |
| 挤出 | E |
| 内插面 | I |
| 环切 | Ctrl+R |
| 倒角 | Ctrl+B |
| 合并 | M |
| 填充 | F |
| 切割 | K |
| 桥接 | Ctrl+E → Bridge |

### 雕刻模式

| 操作 | 快捷键 |
|------|--------|
| Draw | X |
| Clay Strips | C |
| Grab | G |
| Smooth | Shift |
| Flatten | Shift+T |
| Crease | Shift+C |
| Mask | Ctrl+笔刷 |
| 隐藏 | H |
| 显示隐藏 | Alt+H |
| 细分 | Ctrl+D |
| 简化 | Ctrl+D反向 |

### 权重绘制

| 操作 | 快捷键 |
|------|--------|
| 绘制 | 左键 |
| 模糊 | Shift |
| 添加 | Ctrl |
| 减少 | Ctrl+Shift |
| 选择骨骼 | Ctrl+点击 |
| 镜像 | Ctrl+Shift+M |

### 动画

| 操作 | 快捷键 |
|------|--------|
| 插入关键帧 | I |
| 删除关键帧 | Alt+I |
| 播放/暂停 | Space |
| 前一帧 | Left |
| 后一帧 | Right |
| 跳到开头 | Shift+Left |
| 跳到结尾 | Shift+Right |
| 设置帧范围 | Ctrl+点击时间轴 |

---

## 十四、资源推荐

### 学习资源

| 资源 | 类型 | 网址 |
|------|------|------|
| Blender Guru | 视频教程 | YouTube |
| CG Cookie | 系统课程 | cgcookie.com |
| FlippedNormals | 专业教程 | flippednormals.com |
| Blender Artists | 社区论坛 | blenderartists.org |
| Polycount | 游戏美术社区 | polycount.com |

### 免费资源

| 资源 | 内容 | 网址 |
|------|------|------|
| Mixamo | 自动绑定+动画 | mixamo.com |
| Poly Haven | HDR/材质/模型 | polyhaven.com |
| AmbientCG | PBR材质 | ambientcg.com |
| Sketchfab | 3D模型库 | sketchfab.com |
| Blend Swap | Blender模型 | blendswap.com |

### 插件市场

| 平台 | 说明 |
|------|------|
| Blender Market | 官方市场 |
| Gumroad | 独立开发者 |
| GitHub | 开源插件 |

---

## 十五、常见问题FAQ

**Q: 雕刻时模型变模糊？**
A: 增加Multiresolution细分级别，或检查是否应用了Smooth修改器。

**Q: 烘焙时出现黑色接缝？**
A: 增加Ray Distance，或使用Cage投射。确保低模完全包裹高模。

**Q: 导出FBX后骨骼变形异常？**
A: 应用所有变换（Ctrl+A），检查骨骼朝向，确保Scale为1。

**Q: 权重绘制后关节变形扭曲？**
A: 检查骨骼Roll角度，增加关节处环线数量，平滑权重过渡。

**Q: 动画导出到引擎后不播放？**
A: 确保导出时勾选Baked Animation，检查动画名称和帧范围。
