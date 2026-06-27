# 3D模型常用格式文档

## 一、通用交换格式

### 1. OBJ (.obj)
- **开发公司**：Wavefront Technologies
- **特点**：纯文本格式，结构简单，兼容性最好
- **支持内容**：几何体、UV坐标、法线、材质(.mtl)
- **不支持**：动画、骨骼、场景层级
- **适用场景**：静态模型交换、3D打印、软件间数据传输
- **文件示例**：
  ```
  v 0.0 1.0 0.0
  v 1.0 0.0 0.0
  v -1.0 0.0 0.0
  f 1 2 3
  ```

### 2. FBX (.fbx)
- **开发公司**：Autodesk
- **特点**：功能最全面的商业格式
- **支持内容**：网格、骨骼、动画、材质、灯光、相机、场景树
- **版本**：ASCII和Binary两种，Binary更常用
- **适用场景**：游戏开发、影视制作、软件间复杂资产交换
- **优势**：Unity、Unreal、Maya、3ds Max原生支持

### 3. glTF/GLB (.gltf/.glb)
- **开发组织**：Khronos Group
- **定位**：3D领域的"JPEG"，Web 3D标准
- **特点**：
  - glTF：JSON描述 + 二进制资源分离
  - GLB：单文件打包，自包含
- **支持内容**：PBR材质、动画、骨骼、Morph Target
- **适用场景**：Web 3D、AR/VR、移动端、在线展示
- **优势**：加载快、体积小、GPU友好

### 4. USD/USDZ (.usd/.usdz)
- **开发公司**：Pixar
- **特点**：工业级场景描述格式
- **支持内容**：复杂场景图层、多资产组合、非破坏性编辑
- **适用场景**：影视特效、工业设计、苹果AR生态
- **优势**：Apple原生支持、大型场景管理

---

## 二、3D打印格式

### 5. STL (.stl)
- **全称**：Stereolithography
- **特点**：3D打印行业标准
- **支持内容**：仅三角网格（无颜色、无材质）
- **版本**：
  - ASCII：可读但体积大
  - Binary：体积小，更常用
- **适用场景**：3D打印、快速原型、CAD导出

### 6. 3MF (.3mf)
- **开发组织**：3MF Consortium（微软主导）
- **定位**：STL的现代替代品
- **支持内容**：网格、颜色、材质、打印参数
- **适用场景**：彩色3D打印、全彩模型

### 7. AMF (.amf)
- **全称**：Additive Manufacturing File Format
- **特点**：支持曲线（非纯三角化）
- **支持内容**：网格、颜色、材质、排列
- **适用场景**：增材制造、高精度打印

---

## 三、CAD工程格式

### 8. STEP (.stp/.step)
- **标准**：ISO 10303
- **特点**：精确NURBS曲面，无损交换
- **支持内容**：实体、曲面、装配体、PMI（产品制造信息）
- **适用场景**：机械设计、工程制造、CAD软件间交换
- **优势**：精度无损、行业标准

### 9. IGES (.igs/.iges)
- **全称**：Initial Graphics Exchange Specification
- **特点**：老牌CAD交换格式
- **支持内容**：曲线、曲面、实体
- **适用场景**：传统CAD系统间交换
- **现状**：逐渐被STEP取代

### 10. SAT (.sat)
- **开发公司**：Spatial (ACIS内核)
- **特点**：ACIS实体建模格式
- **适用场景**：使用ACIS内核的CAD软件

### 11. Parasolid (.x_t/.x_b)
- **开发公司**：Siemens
- **特点**：Parasolid内核原生格式
- **适用场景**：SolidWorks、NX等软件

---

## 四、游戏/实时渲染格式

### 12. DAE (.dae)
- **标准**：Collada (Khronos Group)
- **特点**：XML基础，跨平台通用
- **支持内容**：网格、骨骼、动画、材质、特效
- **适用场景**：游戏资产交换、Google Earth

### 13. 3DS (.3ds)
- **开发公司**：Autodesk (3ds Max老格式)
- **特点**：二进制格式，兼容性广
- **限制**：网格上限65535顶点，功能有限
- **适用场景**：老软件兼容、简单模型交换

### 14. MDL/MD2/MD3 (.mdl/.md2/.md3)
- **开发公司**：id Software
- **特点**：Quake引擎专用格式
- **支持内容**：网格、动画帧、皮肤
- **适用场景**：经典游戏mod

### 15. X (.x)
- **开发公司**：Microsoft
- **特点**：DirectX原生格式
- **支持内容**：网格、骨骼、动画
- **适用场景**：DirectX应用、老游戏

---

## 五、扫描/点云格式

### 16. PLY (.ply)
- **全称**：Polygon File Format
- **特点**：支持点云和多边形
- **支持内容**：顶点属性（颜色、法线、强度）
- **适用场景**：3D扫描、点云处理、科研

### 17. XYZ (.xyz)
- **特点**：纯点云格式
- **支持内容**：仅坐标（可扩展颜色）
- **适用场景**：激光扫描、点云数据

### 18. LAS/LAZ (.las/.laz)
- **开发组织**：ASPRS
- **特点**：LiDAR点云标准
- **支持内容**：坐标、强度、分类、GPS时间
- **适用场景**：地理测绘、林业、建筑扫描

### 19. E57 (.e57)
- **标准**：ASTM E2807
- **特点**：厂商中立的点云格式
- **支持内容**：点云、图像、扫描仪位姿
- **适用场景**：工业扫描、建筑测量

---

## 六、动画/影视格式

### 20. BVH (.bvh)
- **全称**：Biovision Hierarchy
- **特点**：动作捕捉数据标准
- **支持内容**：骨骼层级、关键帧动画
- **适用场景**：动捕数据、角色动画

### 21. ABC (.abc)
- **全称**：Alembic
- **开发公司**：Sony Pictures Imageworks + ILM
- **特点**：缓存式动画交换
- **支持内容**：网格动画、粒子、相机
- **适用场景**：影视特效、复杂动画缓存

### 22. C4D (.c4d)
- **开发公司**：Maxon
- **特点**：Cinema 4D原生格式
- **适用场景**：Motion Graphics、C4D用户

---

## 七、Web/AR/VR格式

### 23. VRML/WRL (.wrl)
- **全称**：Virtual Reality Modeling Language
- **特点**：早期Web 3D格式
- **现状**：被X3D和glTF取代

### 24. X3D (.x3d)
- **标准**：ISO/IEC 19775
- **特点**：VRML继承者，XML/Web3D标准
- **适用场景**：科学可视化、Web 3D

### 25. SCENE (.scene)
- **开发公司**：Babylon.js / Three.js
- **特点**：Web引擎场景描述
- **适用场景**：WebGL应用

---

## 八、工业/专业格式

### 26. JT (.jt)
- **开发公司**：Siemens
- **特点**：轻量化可视化格式
- **支持内容**：精确B-rep + 精简网格
- **适用场景**：PLM、产品可视化

### 27. DWG/DXF (.dwg/.dxf)
- **开发公司**：Autodesk
- **特点**：2D/3D CAD标准
- **适用场景**：建筑设计、工程制图

### 28. IFC (.ifc)
- **标准**：buildingSMART
- **特点**：BIM数据交换标准
- **支持内容**：建筑构件、属性、关系
- **适用场景**：建筑信息模型(BIM)

### 29. 3DM (.3dm)
- **开发公司**：Robert McNeel (Rhino)
- **特点**：NURBS曲面格式
- **适用场景**：Rhino、Grasshopper

---

## 九、格式选择指南

| 使用场景 | 推荐格式 | 备选格式 |
|---------|---------|---------|
| 游戏开发 | FBX, glTF | OBJ, DAE |
| Web 3D | glTF/GLB | USDZ |
| 3D打印 | STL | 3MF, OBJ |
| CAD工程 | STEP | IGES, Parasolid |
| 影视特效 | ABC, FBX | USD |
| AR/VR | USDZ, glTF | FBX |
| 扫描点云 | PLY, LAS | E57, XYZ |
| 软件间交换 | OBJ, FBX | glTF, DAE |
| 建筑BIM | IFC | DWG |

---

## 十、Blender导入/导出支持

| 格式 | 导入 | 导出 | 插件 |
|------|------|------|------|
| OBJ | ✅ | ✅ | 内置 |
| FBX | ✅ | ✅ | 内置 |
| glTF/GLB | ✅ | ✅ | 内置 |
| STL | ✅ | ✅ | 内置 |
| USD | ✅ | ✅ | 内置 |
| DAE | ✅ | ✅ | 内置 |
| PLY | ✅ | ✅ | 内置 |
| 3DS | ✅ | ✅ | 内置 |
| ABC | ✅ | ✅ | 内置 |
| BVH | ✅ | ❌ | 内置 |
| SVG | ✅ | ✅ | 内置 |

---

## 十一、Web 3D展示注意事项

### 文件大小限制

| 平台 | 单文件限制 | 说明 |
|------|-----------|------|
| GitHub Pages | ~100MB | 超大文件响应超时 |
| Three.js (STL) | ~50MB | 加载缓慢，易超时 |
| model-viewer (GLB) | ~20MB | 推荐最大尺寸 |
| 移动端 | ~10MB | 建议控制在此范围 |

### 格式选择（Web场景）

| 格式 | 文件大小 | 加载速度 | 推荐度 |
|------|---------|---------|--------|
| GLB | 最小 | 最快 | ⭐⭐⭐⭐⭐ |
| glTF | 小 | 快 | ⭐⭐⭐⭐ |
| OBJ | 中 | 中 | ⭐⭐⭐ |
| STL | 大 | 慢 | ⭐⭐ |
| STEP | 很大 | 不支持 | ❌ |

### 实际案例

本项目中遇到的问题：

| 模型 | STL大小 | GLB大小 | 结果 |
|------|---------|---------|------|
| 铁十字（基础版） | 19KB | - | ✅ Three.js可加载 |
| 铁十字（精细化） | 29MB | ~500KB | ❌ STL失败 → ✅ GLB成功 |
| 共和国勋章 | 118MB | ~2MB | ❌ STL失败 → ✅ GLB成功 |

### 最佳实践

1. **Web展示优先使用GLB格式**
   - 压缩率高（通常比STL小10-50倍）
   - 支持材质、动画
   - model-viewer原生支持

2. **STL转换为GLB**
   ```python
   # Blender Python
   bpy.ops.import_mesh.stl(filepath="model.stl")
   bpy.ops.export_scene.gltf(filepath="model.glb", export_format='GLB')
   ```

3. **减小文件体积的方法**
   - 减少多边形数量
   - 使用压缩格式（GLB自带压缩）
   - 合并重复顶点
   - 降低细节精度

4. **Web 3D组件选择**
   - **model-viewer**：最简单，支持GLB/glTF，自动处理加载
   - **Three.js**：功能强大，支持多种格式，需要手动编码
   - **Babylon.js**：完整3D引擎，适合复杂场景

---

## 参考资料

- [Khronos Group - glTF](https://www.khronos.org/gltf/)
- [Pixar - Universal Scene Description](https://openusd.org/)
- [Autodesk FBX](https://www.autodesk.com/products/fbx)
- [3MF Specification](https://3mf.io/specification/)
- [buildingSMART - IFC](https://www.buildingsmart.org/standards/technical-standards/ifc/)
- [model-viewer](https://modelviewer.dev/)
- [Three.js](https://threejs.org/)
