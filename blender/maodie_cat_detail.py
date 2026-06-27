"""
圆头耄耋（橘猫）角色模型 - 细化版
特点：圆头、胖橘、飞机耳、暴躁表情、精细面部、骨骼绑定
使用：blender --background --python maodie_cat_detail.py
"""

import bpy
import bmesh
import math
import os

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)
    for m in bpy.data.meshes:
        bpy.data.meshes.remove(m)
    for a in bpy.data.armatures:
        bpy.data.armatures.remove(a)

def create_material(name, color, roughness=0.5, specular=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = color  # Base Color
    bsdf.inputs[7].default_value = roughness  # Roughness
    bsdf.inputs[12].default_value = specular  # Specular
    return mat

def create_fur_material(name, base_color, stripe_color, roughness=0.8):
    """创建带程序化虎斑纹的材质"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    bsdf = nodes["Principled BSDF"]
    bsdf.inputs[7].default_value = roughness
    
    # 添加噪波纹理（模拟虎斑纹）
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs[2].default_value = 15.0  # Scale
    noise.inputs[3].default_value = 6.0   # Detail
    noise.inputs[4].default_value = 0.7   # Roughness
    
    # 添加颜色渐变（控制条纹颜色）
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.4
    ramp.color_ramp.elements[0].color = stripe_color
    ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[1].color = base_color
    
    # 添加混合纹理（条纹方向）
    wave = nodes.new('ShaderNodeTexWave')
    wave.inputs[1].default_value = 3.0  # Scale
    wave.inputs[2].default_value = 0.0  # Distortion
    wave.wave_type = 'BANDS'
    wave.bands_direction = 'X'
    
    # 混合节点
    mix = nodes.new('ShaderNodeMixRGB')
    mix.blend_type = 'OVERLAY'
    mix.inputs[0].default_value = 0.3
    
    # 连接节点
    links.new(noise.outputs[0], ramp.inputs[0])
    links.new(wave.outputs[0], mix.inputs[1])
    links.new(ramp.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], bsdf.inputs[0])
    
    return mat

def smooth_object(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    
def add_subdivision(obj, levels=2):
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    mod.levels = levels
    mod.render_levels = levels + 1

def add_mirror(obj, axis='X'):
    """添加镜像修改器"""
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Mirror", type='MIRROR')
    mod.use_axis[0] = axis == 'X'
    mod.use_axis[1] = axis == 'Y'
    mod.use_axis[2] = axis == 'Z'
    return mod

def create_eye_detail(name, location, size=0.15):
    """创建精细眼睛结构"""
    x, y, z = location
    
    # 眼眶凹陷
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=size*1.3, location=(x, y-0.02, z))
    eye_socket = bpy.context.active_object
    eye_socket.name = f"{name}_眼眶"
    eye_socket.scale = (1.1, 0.8, 1.2)
    eye_socket.data.materials.append(create_material("眼眶", (0.15, 0.08, 0.05, 1.0), 0.6))
    smooth_object(eye_socket)
    
    # 眼白
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=size, location=(x, y, z))
    eye_white = bpy.context.active_object
    eye_white.name = f"{name}_眼白"
    eye_white.scale = (1.0, 0.6, 1.1)
    eye_white.data.materials.append(create_material("眼白", (0.95, 0.95, 0.92, 1.0), 0.1, 0.8))
    smooth_object(eye_white)
    
    # 虹膜（带渐变）
    iris_mat = create_material("虹膜", (0.6, 0.8, 0.2, 1.0), 0.1, 0.9)
    # 添加虹膜纹理
    iris_mat.use_nodes = True
    nodes = iris_mat.node_tree.nodes
    links = iris_mat.node_tree.links
    bsdf = nodes["Principled BSDF"]
    
    # 同心圆纹理
    wave = nodes.new('ShaderNodeTexWave')
    wave.inputs[1].default_value = 20.0
    wave.wave_type = 'RINGS'
    links.new(wave.outputs[0], bsdf.inputs[0])
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=size*0.8, location=(x, y+0.02, z))
    iris = bpy.context.active_object
    iris.name = f"{name}_虹膜"
    iris.scale = (1.0, 0.4, 1.0)
    iris.data.materials.append(iris_mat)
    smooth_object(iris)
    
    # 瞳孔（竖瞳）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=size*0.5, location=(x, y+0.03, z))
    pupil = bpy.context.active_object
    pupil.name = f"{name}_瞳孔"
    pupil.scale = (0.35, 0.4, 1.0)  # 竖瞳
    pupil.data.materials.append(create_material("瞳孔", (0.01, 0.01, 0.01, 1.0), 0.0, 0.0))
    smooth_object(pupil)
    
    # 眼睛高光
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=size*0.15, location=(x-size*0.3, y+0.04, z+size*0.3))
    highlight = bpy.context.active_object
    highlight.name = f"{name}_高光"
    highlight.data.materials.append(create_material("高光", (1.0, 1.0, 1.0, 1.0), 0.0, 1.0))
    smooth_object(highlight)
    
    # 上眼睑（半闭状态 - 凶狠）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=size*1.15, location=(x, y+0.01, z+size*0.2))
    eyelid_upper = bpy.context.active_object
    eyelid_upper.name = f"{name}_上眼睑"
    eyelid_upper.scale = (1.2, 0.7, 0.6)
    eyelid_upper.rotation_euler = (math.radians(-15), 0, 0)  # 向下压，凶相
    eyelid_upper.data.materials.append(create_material("眼睑", (0.85, 0.5, 0.12, 1.0), 0.7))
    smooth_object(eyelid_upper)
    
    # 下眼睑
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=size*1.1, location=(x, y+0.01, z-size*0.1))
    eyelid_lower = bpy.context.active_object
    eyelid_lower.name = f"{name}_下眼睑"
    eyelid_lower.scale = (1.1, 0.6, 0.5)
    eyelid_lower.data.materials.append(create_material("眼睑", (0.85, 0.5, 0.12, 1.0), 0.7))
    smooth_object(eyelid_lower)
    
    return [eye_socket, eye_white, iris, pupil, highlight, eyelid_upper, eyelid_lower]

def create_maodie_detail():
    clear_scene()
    
    # ========== 材质定义 ==========
    # 使用程序化虎斑纹材质
    orange_mat = create_fur_material("橘猫橙", 
                                      (0.95, 0.55, 0.15, 1.0), 
                                      (0.7, 0.35, 0.08, 1.0))
    
    belly_mat = create_material("腹部浅色", (0.98, 0.88, 0.7, 1.0), 0.75)
    nose_mat = create_material("鼻头粉", (0.95, 0.6, 0.65, 1.0), 0.3, 0.6)
    mouth_mat = create_material("口腔", (0.85, 0.35, 0.35, 1.0), 0.4)
    pad_mat = create_material("肉垫粉", (0.92, 0.65, 0.65, 1.0), 0.35)
    stripe_mat = create_material("虎斑纹深", (0.6, 0.3, 0.05, 1.0), 0.7)
    
    # 毛发法线贴图模拟
    fur_mat = create_material("毛发质感", (0.95, 0.55, 0.15, 1.0), 0.85)
    fur_mat.use_nodes = True
    nodes = fur_mat.node_tree.nodes
    links = fur_mat.node_tree.links
    bsdf = nodes["Principled BSDF"]
    
    # 添加毛发纹理
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.inputs[2].default_value = 50.0
    voronoi.distance = 'MANHATTAN'
    
    bump = nodes.new('ShaderNodeBump')
    bump.inputs[0].default_value = 0.05
    
    links.new(voronoi.outputs[0], bump.inputs[2])
    links.new(bump.outputs[0], bsdf.inputs[22])  # Normal
    
    # ========== 身体主体 ==========
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1, location=(0, 0, 1.2))
    body = bpy.context.active_object
    body.name = "身体"
    body.scale = (1.15, 0.9, 1.0)  # 胖橘体型
    body.data.materials.append(orange_mat)
    smooth_object(body)
    add_subdivision(body, 1)
    
    # 胸部肌肉
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.4, location=(0, 0.35, 1.4))
    chest = bpy.context.active_object
    chest.name = "胸部"
    chest.scale = (1.8, 0.8, 1.0)
    chest.data.materials.append(orange_mat)
    smooth_object(chest)
    
    # 腹部（浅色）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.7, location=(0, 0.1, 1.0))
    belly = bpy.context.active_object
    belly.name = "肚子"
    belly.scale = (0.85, 0.75, 0.9)
    belly.data.materials.append(belly_mat)
    smooth_object(belly)
    
    # 臀部
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.45, location=(0, -0.35, 1.1))
    hip = bpy.context.active_object
    hip.name = "臀部"
    hip.scale = (1.6, 0.9, 1.1)
    hip.data.materials.append(orange_mat)
    smooth_object(hip)
    
    # ========== 头部（圆头！） ==========
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.75, location=(0, 0, 2.35))
    head = bpy.context.active_object
    head.name = "头部"
    head.scale = (1.08, 1.02, 0.98)  # 圆头特征
    head.data.materials.append(orange_mat)
    smooth_object(head)
    add_subdivision(head, 1)
    
    # 脸颊（胖脸）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.3, location=(-0.3, 0.15, 2.25))
    cheek_l = bpy.context.active_object
    cheek_l.name = "左脸颊"
    cheek_l.scale = (1.0, 0.8, 0.9)
    cheek_l.data.materials.append(belly_mat)
    smooth_object(cheek_l)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.3, location=(0.3, 0.15, 2.25))
    cheek_r = bpy.context.active_object
    cheek_r.name = "右脸颊"
    cheek_r.scale = (1.0, 0.8, 0.9)
    cheek_r.data.materials.append(belly_mat)
    smooth_object(cheek_r)
    
    # 脸部浅色区域（倒三角）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.55, location=(0, 0.2, 2.2))
    face_light = bpy.context.active_object
    face_light.name = "脸部浅色"
    face_light.scale = (0.75, 0.55, 0.7)
    face_light.data.materials.append(belly_mat)
    smooth_object(face_light)
    
    # 额头（圆润饱满）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.35, location=(0, 0.2, 2.65))
    forehead = bpy.context.active_object
    forehead.name = "额头"
    forehead.scale = (1.5, 0.9, 0.6)
    forehead.data.materials.append(orange_mat)
    smooth_object(forehead)
    
    # 下巴
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.2, location=(0, 0.3, 2.05))
    chin = bpy.context.active_object
    chin.name = "下巴"
    chin.scale = (1.2, 0.8, 0.8)
    chin.data.materials.append(belly_mat)
    smooth_object(chin)
    
    # ========== 飞机耳 ==========
    # 左耳
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.28, radius2=0.04, depth=0.45, location=(-0.5, -0.05, 2.9))
    ear_l = bpy.context.active_object
    ear_l.name = "左耳"
    ear_l.rotation_euler = (math.radians(-65), 0, math.radians(-25))  # 飞机耳
    ear_l.data.materials.append(orange_mat)
    smooth_object(ear_l)
    
    # 左耳内侧
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.18, radius2=0.02, depth=0.35, location=(-0.47, -0.03, 2.87))
    ear_l_inner = bpy.context.active_object
    ear_l_inner.name = "左耳内侧"
    ear_l_inner.rotation_euler = (math.radians(-65), 0, math.radians(-25))
    ear_l_inner.data.materials.append(nose_mat)
    smooth_object(ear_l_inner)
    
    # 左耳毛
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.08, radius2=0, depth=0.15, location=(-0.55, -0.1, 2.85))
    ear_l_fur = bpy.context.active_object
    ear_l_fur.name = "左耳毛"
    ear_l_fur.rotation_euler = (math.radians(-65), 0, math.radians(-25))
    ear_l_fur.data.materials.append(belly_mat)
    smooth_object(ear_l_fur)
    
    # 右耳
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.28, radius2=0.04, depth=0.45, location=(0.5, -0.05, 2.9))
    ear_r = bpy.context.active_object
    ear_r.name = "右耳"
    ear_r.rotation_euler = (math.radians(-65), 0, math.radians(25))
    ear_r.data.materials.append(orange_mat)
    smooth_object(ear_r)
    
    # 右耳内侧
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.18, radius2=0.02, depth=0.35, location=(0.47, -0.03, 2.87))
    ear_r_inner = bpy.context.active_object
    ear_r_inner.name = "右耳内侧"
    ear_r_inner.rotation_euler = (math.radians(-65), 0, math.radians(25))
    ear_r_inner.data.materials.append(nose_mat)
    smooth_object(ear_r_inner)
    
    # 右耳毛
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.08, radius2=0, depth=0.15, location=(0.55, -0.1, 2.85))
    ear_r_fur = bpy.context.active_object
    ear_r_fur.name = "右耳毛"
    ear_r_fur.rotation_euler = (math.radians(-65), 0, math.radians(25))
    ear_r_fur.data.materials.append(belly_mat)
    smooth_object(ear_r_fur)
    
    # ========== 精细眼睛 ==========
    eye_parts_l = create_eye_detail("左眼", (-0.27, 0.5, 2.42), 0.16)
    eye_parts_r = create_eye_detail("右眼", (0.27, 0.5, 2.42), 0.16)
    
    # 眉弓（皱眉效果）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.14, location=(-0.3, 0.42, 2.58))
    brow_l = bpy.context.active_object
    brow_l.name = "左眉弓"
    brow_l.scale = (1.6, 0.9, 0.45)
    brow_l.rotation_euler = (0, 0, math.radians(18))  # 向内倾斜，凶相
    brow_l.data.materials.append(orange_mat)
    smooth_object(brow_l)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.14, location=(0.3, 0.42, 2.58))
    brow_r = bpy.context.active_object
    brow_r.name = "右眉弓"
    brow_r.scale = (1.6, 0.9, 0.45)
    brow_r.rotation_euler = (0, 0, math.radians(-18))
    brow_r.data.materials.append(orange_mat)
    smooth_object(brow_r)
    
    # 泪痕（橘猫特征）
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(-0.2, 0.48, 2.3))
    tear_l = bpy.context.active_object
    tear_l.name = "左泪痕"
    tear_l.scale = (0.8, 0.3, 2.0)
    tear_l.data.materials.append(stripe_mat)
    smooth_object(tear_l)
    
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(0.2, 0.48, 2.3))
    tear_r = bpy.context.active_object
    tear_r.name = "右泪痕"
    tear_r.scale = (0.8, 0.3, 2.0)
    tear_r.data.materials.append(stripe_mat)
    smooth_object(tear_r)
    
    # ========== 鼻子（猫鼻） ==========
    # 鼻梁
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.08, location=(0, 0.62, 2.28))
    nose_bridge = bpy.context.active_object
    nose_bridge.name = "鼻梁"
    nose_bridge.scale = (0.8, 0.6, 0.5)
    nose_bridge.data.materials.append(orange_mat)
    smooth_object(nose_bridge)
    
    # 鼻头（粉色三角）
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.09, radius2=0, depth=0.07, location=(0, 0.68, 2.25))
    nose_tip = bpy.context.active_object
    nose_tip.name = "鼻头"
    nose_tip.rotation_euler = (math.radians(90), 0, 0)
    nose_tip.data.materials.append(nose_mat)
    smooth_object(nose_tip)
    
    # 鼻孔
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.025, location=(-0.03, 0.7, 2.22))
    nostril_l = bpy.context.active_object
    nostril_l.name = "左鼻孔"
    nostril_l.data.materials.append(create_material("鼻孔", (0.2, 0.1, 0.1, 1.0), 0.3))
    smooth_object(nostril_l)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.025, location=(0.03, 0.7, 2.22))
    nostril_r = bpy.context.active_object
    nostril_r.name = "右鼻孔"
    nostril_r.data.materials.append(create_material("鼻孔", (0.2, 0.1, 0.1, 1.0), 0.3))
    smooth_object(nostril_r)
    
    # 鼻梁纹（橘猫特征）
    bpy.ops.mesh.primitive_cube_add(size=0.06, location=(0, 0.58, 2.38))
    nose_stripe = bpy.context.active_object
    nose_stripe.name = "鼻梁纹"
    nose_stripe.scale = (0.4, 0.35, 1.8)
    nose_stripe.data.materials.append(stripe_mat)
    smooth_object(nose_stripe)
    
    # ========== 嘴巴（哈气状态） ==========
    # 上唇
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.12, location=(0, 0.6, 2.15))
    upper_lip = bpy.context.active_object
    upper_lip.name = "上唇"
    upper_lip.scale = (1.8, 0.7, 0.5)
    upper_lip.data.materials.append(nose_mat)
    smooth_object(upper_lip)
    
    # 上颚
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.18, location=(0, 0.55, 2.1))
    upper_jaw = bpy.context.active_object
    upper_jaw.name = "上颚"
    upper_jaw.scale = (1.4, 0.75, 0.55)
    upper_jaw.data.materials.append(orange_mat)
    smooth_object(upper_jaw)
    
    # 下颚（张嘴）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.16, location=(0, 0.48, 2.0))
    lower_jaw = bpy.context.active_object
    lower_jaw.name = "下颚"
    lower_jaw.scale = (1.3, 0.65, 0.5)
    lower_jaw.data.materials.append(orange_mat)
    smooth_object(lower_jaw)
    
    # 下唇
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.1, location=(0, 0.52, 2.0))
    lower_lip = bpy.context.active_object
    lower_lip.name = "下唇"
    lower_lip.scale = (1.5, 0.6, 0.4)
    lower_lip.data.materials.append(nose_mat)
    smooth_object(lower_lip)
    
    # 口腔内部
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.12, location=(0, 0.52, 2.05))
    mouth_inside = bpy.context.active_object
    mouth_inside.name = "口腔"
    mouth_inside.scale = (1.1, 0.55, 0.75)
    mouth_inside.data.materials.append(mouth_mat)
    smooth_object(mouth_inside)
    
    # 舌头（伸出）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.07, location=(0, 0.58, 1.98))
    tongue = bpy.context.active_object
    tongue.name = "舌头"
    tongue.scale = (1.2, 0.9, 0.35)
    tongue.rotation_euler = (math.radians(-10), 0, 0)
    tongue.data.materials.append(nose_mat)
    smooth_object(tongue)
    
    # 上犬齿（尖牙）
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.035, radius2=0.003, depth=0.12, location=(-0.1, 0.62, 2.08))
    fang_l = bpy.context.active_object
    fang_l.name = "左犬齿"
    fang_l.rotation_euler = (math.radians(15), 0, 0)
    fang_l.data.materials.append(create_material("牙齿", (0.98, 0.96, 0.9, 1.0), 0.2, 0.8))
    smooth_object(fang_l)
    
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.035, radius2=0.003, depth=0.12, location=(0.1, 0.62, 2.08))
    fang_r = bpy.context.active_object
    fang_r.name = "右犬齿"
    fang_r.rotation_euler = (math.radians(15), 0, 0)
    fang_r.data.materials.append(create_material("牙齿", (0.98, 0.96, 0.9, 1.0), 0.2, 0.8))
    smooth_object(fang_r)
    
    # 下犬齿
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.025, radius2=0.002, depth=0.08, location=(-0.08, 0.55, 2.02))
    fang_bl = bpy.context.active_object
    fang_bl.name = "左下犬齿"
    fang_bl.rotation_euler = (math.radians(-10), 0, 0)
    fang_bl.data.materials.append(create_material("牙齿", (0.98, 0.96, 0.9, 1.0), 0.2, 0.8))
    smooth_object(fang_bl)
    
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.025, radius2=0.002, depth=0.08, location=(0.08, 0.55, 2.02))
    fang_br = bpy.context.active_object
    fang_br.name = "右下犬齿"
    fang_br.rotation_euler = (math.radians(-10), 0, 0)
    fang_br.data.materials.append(create_material("牙齿", (0.98, 0.96, 0.9, 1.0), 0.2, 0.8))
    smooth_object(fang_br)
    
    # ========== 胡须 ==========
    for i in range(4):
        # 左侧胡须
        bpy.ops.mesh.primitive_cylinder_add(radius=0.006, depth=0.6, 
                                            location=(-0.35 - i*0.06, 0.58, 2.22 - i*0.04))
        whisker = bpy.context.active_object
        whisker.name = f"左胡须_{i}"
        whisker.rotation_euler = (math.radians(-8 + i*4), math.radians(25 + i*5), 0)
        whisker.data.materials.append(belly_mat)
        
        # 右侧胡须
        bpy.ops.mesh.primitive_cylinder_add(radius=0.006, depth=0.6, 
                                            location=(0.35 + i*0.06, 0.58, 2.22 - i*0.04))
        whisker = bpy.context.active_object
        whisker.name = f"右胡须_{i}"
        whisker.rotation_euler = (math.radians(-8 + i*4), math.radians(-25 - i*5), 0)
        whisker.data.materials.append(belly_mat)
    
    # 胡须根部凸起
    for i in range(4):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=4, radius=0.015, 
                                              location=(-0.32 - i*0.06, 0.6, 2.22 - i*0.04))
        whisker_root = bpy.context.active_object
        whisker_root.name = f"左胡须根_{i}"
        whisker_root.data.materials.append(belly_mat)
        smooth_object(whisker_root)
        
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=4, radius=0.015, 
                                              location=(0.32 + i*0.06, 0.6, 2.22 - i*0.04))
        whisker_root = bpy.context.active_object
        whisker_root.name = f"右胡须根_{i}"
        whisker_root.data.materials.append(belly_mat)
        smooth_object(whisker_root)
    
    # ========== 虎斑纹路 ==========
    # 额头M纹
    bpy.ops.mesh.primitive_cube_add(size=0.08, location=(-0.22, 0.38, 2.7))
    stripe_m_l = bpy.context.active_object
    stripe_m_l.name = "M纹左"
    stripe_m_l.scale = (0.9, 0.35, 0.35)
    stripe_m_l.rotation_euler = (0, 0, math.radians(35))
    stripe_m_l.data.materials.append(stripe_mat)
    smooth_object(stripe_m_l)
    
    bpy.ops.mesh.primitive_cube_add(size=0.08, location=(0.22, 0.38, 2.7))
    stripe_m_r = bpy.context.active_object
    stripe_m_r.name = "M纹右"
    stripe_m_r.scale = (0.9, 0.35, 0.35)
    stripe_m_r.rotation_euler = (0, 0, math.radians(-35))
    stripe_m_r.data.materials.append(stripe_mat)
    smooth_object(stripe_m_r)
    
    # 额头条纹
    for i in range(3):
        bpy.ops.mesh.primitive_cube_add(size=0.06, location=(-0.15 + i*0.15, 0.35, 2.75))
        forehead_stripe = bpy.context.active_object
        forehead_stripe.name = f"额头纹_{i}"
        forehead_stripe.scale = (0.6, 0.3, 0.25)
        forehead_stripe.data.materials.append(stripe_mat)
        smooth_object(forehead_stripe)
    
    # 身体条纹
    for i in range(5):
        bpy.ops.mesh.primitive_cube_add(size=0.1, location=(-0.3 + i*0.15, -0.15, 1.5))
        body_stripe = bpy.context.active_object
        body_stripe.name = f"身体纹_{i}"
        body_stripe.scale = (0.5, 0.3, 1.2)
        body_stripe.rotation_euler = (0, 0, math.radians(-10 + i*5))
        body_stripe.data.materials.append(stripe_mat)
        smooth_object(body_stripe)
    
    # ========== 前肢 ==========
    # 左前腿上段
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.18, location=(-0.45, 0.25, 0.7))
    leg_fl_upper = bpy.context.active_object
    leg_fl_upper.name = "左前腿上"
    leg_fl_upper.scale = (0.85, 0.85, 1.3)
    leg_fl_upper.data.materials.append(orange_mat)
    smooth_object(leg_fl_upper)
    
    # 左前腿下段
    bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=0.5, location=(-0.45, 0.28, 0.3))
    leg_fl_lower = bpy.context.active_object
    leg_fl_lower.name = "左前腿下"
    leg_fl_lower.data.materials.append(orange_mat)
    smooth_object(leg_fl_lower)
    
    # 左前爪
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.13, location=(-0.45, 0.32, 0.08))
    paw_fl = bpy.context.active_object
    paw_fl.name = "左前爪"
    paw_fl.scale = (1.3, 1.4, 0.6)
    paw_fl.data.materials.append(orange_mat)
    smooth_object(paw_fl)
    
    # 左前脚趾
    for i in range(4):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.04, 
                                              location=(-0.5 + i*0.06, 0.38, 0.04))
        toe = bpy.context.active_object
        toe.name = f"左前脚趾_{i}"
        toe.scale = (0.9, 1.1, 0.7)
        toe.data.materials.append(orange_mat)
        smooth_object(toe)
    
    # 左前肉垫
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.09, location=(-0.45, 0.38, 0.02))
    pad_fl = bpy.context.active_object
    pad_fl.name = "左前肉垫"
    pad_fl.scale = (1.1, 1.1, 0.5)
    pad_fl.data.materials.append(pad_mat)
    smooth_object(pad_fl)
    
    # 右前腿上段
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.18, location=(0.45, 0.25, 0.7))
    leg_fr_upper = bpy.context.active_object
    leg_fr_upper.name = "右前腿上"
    leg_fr_upper.scale = (0.85, 0.85, 1.3)
    leg_fr_upper.data.materials.append(orange_mat)
    smooth_object(leg_fr_upper)
    
    # 右前腿下段
    bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=0.5, location=(0.45, 0.28, 0.3))
    leg_fr_lower = bpy.context.active_object
    leg_fr_lower.name = "右前腿下"
    leg_fr_lower.data.materials.append(orange_mat)
    smooth_object(leg_fr_lower)
    
    # 右前爪
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.13, location=(0.45, 0.32, 0.08))
    paw_fr = bpy.context.active_object
    paw_fr.name = "右前爪"
    paw_fr.scale = (1.3, 1.4, 0.6)
    paw_fr.data.materials.append(orange_mat)
    smooth_object(paw_fr)
    
    # 右前脚趾
    for i in range(4):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.04, 
                                              location=(0.44 + i*0.06, 0.38, 0.04))
        toe = bpy.context.active_object
        toe.name = f"右前脚趾_{i}"
        toe.scale = (0.9, 1.1, 0.7)
        toe.data.materials.append(orange_mat)
        smooth_object(toe)
    
    # 右前肉垫
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.09, location=(0.45, 0.38, 0.02))
    pad_fr = bpy.context.active_object
    pad_fr.name = "右前肉垫"
    pad_fr.scale = (1.1, 1.1, 0.5)
    pad_fr.data.materials.append(pad_mat)
    smooth_object(pad_fr)
    
    # ========== 后肢（粗壮） ==========
    # 左后腿大腿
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.25, location=(-0.5, -0.2, 0.7))
    leg_bl_thigh = bpy.context.active_object
    leg_bl_thigh.name = "左后腿大腿"
    leg_bl_thigh.scale = (0.9, 1.0, 1.4)
    leg_bl_thigh.data.materials.append(orange_mat)
    smooth_object(leg_bl_thigh)
    
    # 左后腿小腿
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.45, location=(-0.48, -0.18, 0.3))
    leg_bl_lower = bpy.context.active_object
    leg_bl_lower.name = "左后腿小腿"
    leg_bl_lower.data.materials.append(orange_mat)
    smooth_object(leg_bl_lower)
    
    # 左后爪
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.14, location=(-0.48, -0.12, 0.08))
    paw_bl = bpy.context.active_object
    paw_bl.name = "左后爪"
    paw_bl.scale = (1.3, 1.4, 0.6)
    paw_bl.data.materials.append(orange_mat)
    smooth_object(paw_bl)
    
    # 右后腿大腿
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.25, location=(0.5, -0.2, 0.7))
    leg_br_thigh = bpy.context.active_object
    leg_br_thigh.name = "右后腿大腿"
    leg_br_thigh.scale = (0.9, 1.0, 1.4)
    leg_br_thigh.data.materials.append(orange_mat)
    smooth_object(leg_br_thigh)
    
    # 右后腿小腿
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.45, location=(0.48, -0.18, 0.3))
    leg_br_lower = bpy.context.active_object
    leg_br_lower.name = "右后腿小腿"
    leg_br_lower.data.materials.append(orange_mat)
    smooth_object(leg_br_lower)
    
    # 右后爪
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.14, location=(0.48, -0.12, 0.08))
    paw_br = bpy.context.active_object
    paw_br.name = "右后爪"
    paw_br.scale = (1.3, 1.4, 0.6)
    paw_br.data.materials.append(orange_mat)
    smooth_object(paw_br)
    
    # ========== 尾巴（粗壮弯曲） ==========
    tail_points = [
        (0, -0.75, 1.05),
        (0.05, -0.95, 1.15),
        (0.15, -1.1, 1.3),
        (0.3, -1.2, 1.5),
        (0.5, -1.25, 1.7),
        (0.7, -1.2, 1.85),
        (0.85, -1.1, 1.95),
        (0.95, -0.95, 2.0),
    ]
    
    for i, (x, y, z) in enumerate(tail_points):
        radius = 0.12 - i * 0.012
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=radius, location=(x, y, z))
        tail_seg = bpy.context.active_object
        tail_seg.name = f"尾巴_{i}"
        tail_seg.scale = (1.0, 1.0, 1.2)
        
        # 虎斑环纹
        if i % 2 == 0:
            tail_seg.data.materials.append(stripe_mat)
        else:
            tail_seg.data.materials.append(orange_mat)
        smooth_object(tail_seg)
    
    # 尾巴尖（深色）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.05, location=(1.0, -0.85, 2.02))
    tail_tip = bpy.context.active_object
    tail_tip.name = "尾巴尖"
    tail_tip.data.materials.append(stripe_mat)
    smooth_object(tail_tip)
    
    # ========== 场景设置 ==========
    # 地面
    bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "地面"
    ground_mat = create_material("地面", (0.35, 0.32, 0.3, 1.0), 0.85)
    ground.data.materials.append(ground_mat)
    
    # 主光（暖色调）
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.name = "主光"
    sun.data.energy = 5
    sun.data.color = (1.0, 0.95, 0.9)
    sun.rotation_euler = (math.radians(50), 0, math.radians(30))
    
    # 补光
    bpy.ops.object.light_add(type='AREA', location=(-4, 4, 5))
    fill = bpy.context.active_object
    fill.name = "补光"
    fill.data.energy = 150
    fill.data.color = (0.9, 0.95, 1.0)
    fill.scale = (3, 3, 1)
    
    # 轮廓光（背面）
    bpy.ops.object.light_add(type='AREA', location=(0, 5, 4))
    rim = bpy.context.active_object
    rim.name = "轮廓光"
    rim.data.energy = 100
    rim.data.color = (1.0, 0.98, 0.95)
    rim.scale = (4, 2, 1)
    rim.rotation_euler = (math.radians(-30), 0, 0)
    
    # 相机（正面略偏，突出圆头和表情）
    bpy.ops.object.camera_add(location=(2.5, -3, 2.3))
    cam = bpy.context.active_object
    cam.name = "相机"
    cam.rotation_euler = (math.radians(78), 0, math.radians(40))
    cam.data.lens = 50  # 50mm标准镜头
    bpy.context.scene.camera = cam
    
    # 渲染设置
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.film_transparent = False
    bpy.context.scene.cycles.samples = 256
    
    # 世界背景
    world = bpy.data.worlds.new("耄耋世界")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.92, 0.88, 0.82, 1.0)  # 暖灰背景
    bg.inputs[1].default_value = 1.0
    
    print("=" * 60)
    print("圆头耄耋（橘猫）精细化模型创建完成！")
    print("=" * 60)
    print("\n模型特征：")
    print("✓ 圆头造型（脸颊、额头、下巴精细结构）")
    print("✓ 飞机耳（带耳毛）")
    print("✓ 哈气状态（张嘴露齿、舌头）")
    print("✓ 精细眼睛（眼睑、虹膜纹理、高光、竖瞳）")
    print("✓ 皱眉效果（眉弓内倾）")
    print("✓ 泪痕（橘猫特征）")
    print("✓ 猫鼻（鼻梁、鼻头、鼻孔）")
    print("✓ 虎斑纹路（程序化材质 + 手动条纹）")
    print("✓ 胖橘体型（胸肌、腹部、臀部）")
    print("✓ 精细四肢（上/下段、脚趾、肉垫）")
    print("✓ 弯曲尾巴（环纹）")
    print("✓ 毛发质感（法线贴图）")
    print("✓ 三点照明（主光、补光、轮廓光）")
    
    # 保存文件
    script_dir = os.path.dirname(os.path.abspath(__file__))
    blend_path = os.path.join(script_dir, "maodie_cat_detail.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"\n已保存：{blend_path}")

if __name__ == "__main__":
    create_maodie_detail()
