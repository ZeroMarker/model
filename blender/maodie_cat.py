"""
圆头耄耋（橘猫）角色模型 - Blender Python脚本
特点：圆头、胖橘、飞机耳、暴躁表情
使用：blender --background --python maodie_cat.py
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

def create_material(name, color, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = color
    bsdf.inputs[7].default_value = roughness
    return mat

def smooth_object(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    
def add_subdivision(obj, levels=2):
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    mod.levels = levels
    mod.render_levels = levels + 1

def create_maodie():
    clear_scene()
    
    # ========== 材质定义 ==========
    # 橘猫主色（橙色）
    orange_mat = create_material("橘猫橙", (0.95, 0.55, 0.15, 1.0), 0.7)
    # 浅色腹部
    belly_mat = create_material("腹部浅色", (0.98, 0.85, 0.65, 1.0), 0.7)
    # 鼻头粉色
    nose_mat = create_material("鼻头粉", (0.95, 0.6, 0.65, 1.0), 0.3)
    # 眼睛颜色（黄绿色）
    eye_mat = create_material("猫眼黄绿", (0.6, 0.8, 0.2, 1.0), 0.1)
    # 瞳孔
    pupil_mat = create_material("瞳孔黑", (0.02, 0.02, 0.02, 1.0), 0.0)
    # 眼白
    eye_white_mat = create_material("眼白", (0.95, 0.95, 0.92, 1.0), 0.1)
    # 嘴巴内部
    mouth_mat = create_material("口腔", (0.8, 0.3, 0.3, 1.0), 0.4)
    # 肉垫
    pad_mat = create_material("肉垫粉", (0.9, 0.6, 0.6, 1.0), 0.3)
    # 虎斑纹路
    stripe_mat = create_material("虎斑纹", (0.7, 0.35, 0.08, 1.0), 0.7)
    
    # ========== 身体（胖胖的椭圆） ==========
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=(0, 0, 1.2))
    body = bpy.context.active_object
    body.name = "身体"
    body.scale = (1.1, 0.85, 0.95)  # 胖胖的
    body.data.materials.append(orange_mat)
    smooth_object(body)
    add_subdivision(body, 1)
    
    # ========== 肚子（浅色） ==========
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.85, location=(0, 0.1, 1.1))
    belly = bpy.context.active_object
    belly.name = "肚子"
    belly.scale = (0.8, 0.7, 0.85)
    belly.data.materials.append(belly_mat)
    smooth_object(belly)
    
    # ========== 头部（圆头特征！） ==========
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.75, location=(0, 0, 2.3))
    head = bpy.context.active_object
    head.name = "头部"
    head.scale = (1.05, 1.0, 0.95)  # 圆头！横向略宽
    head.data.materials.append(orange_mat)
    smooth_object(head)
    add_subdivision(head, 1)
    
    # ========== 脸部浅色区域 ==========
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.65, location=(0, 0.15, 2.2))
    face_light = bpy.context.active_object
    face_light.name = "脸部浅色"
    face_light.scale = (0.85, 0.6, 0.75)
    face_light.data.materials.append(belly_mat)
    smooth_object(face_light)
    
    # ========== 左耳（飞机耳 - 平放状态） ==========
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.25, radius2=0.05, depth=0.4, location=(-0.45, 0, 2.85))
    ear_l = bpy.context.active_object
    ear_l.name = "左耳"
    ear_l.rotation_euler = (math.radians(-60), 0, math.radians(-20))  # 飞机耳：向外平躺
    ear_l.data.materials.append(orange_mat)
    smooth_object(ear_l)
    
    # 左耳内侧
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.15, radius2=0.03, depth=0.3, location=(-0.42, 0.02, 2.82))
    ear_l_inner = bpy.context.active_object
    ear_l_inner.name = "左耳内侧"
    ear_l_inner.rotation_euler = (math.radians(-60), 0, math.radians(-20))
    ear_l_inner.data.materials.append(nose_mat)
    smooth_object(ear_l_inner)
    
    # ========== 右耳（飞机耳） ==========
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.25, radius2=0.05, depth=0.4, location=(0.45, 0, 2.85))
    ear_r = bpy.context.active_object
    ear_r.name = "右耳"
    ear_r.rotation_euler = (math.radians(-60), 0, math.radians(20))  # 飞机耳：向外平躺
    ear_r.data.materials.append(orange_mat)
    smooth_object(ear_r)
    
    # 右耳内侧
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.15, radius2=0.03, depth=0.3, location=(0.42, 0.02, 2.82))
    ear_r_inner = bpy.context.active_object
    ear_r_inner.name = "右耳内侧"
    ear_r_inner.rotation_euler = (math.radians(-60), 0, math.radians(20))
    ear_r_inner.data.materials.append(nose_mat)
    smooth_object(ear_r_inner)
    
    # ========== 左眼 ==========
    # 眼白
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.15, location=(-0.25, 0.45, 2.4))
    eye_white_l = bpy.context.active_object
    eye_white_l.name = "左眼白"
    eye_white_l.scale = (1.0, 0.7, 1.1)
    eye_white_l.data.materials.append(eye_white_mat)
    smooth_object(eye_white_l)
    
    # 虹膜
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.12, location=(-0.25, 0.5, 2.4))
    iris_l = bpy.context.active_object
    iris_l.name = "左虹膜"
    iris_l.scale = (1.0, 0.5, 1.0)
    iris_l.data.materials.append(eye_mat)
    smooth_object(iris_l)
    
    # 瞳孔（竖瞳 - 椭圆形）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.08, location=(-0.25, 0.52, 2.4))
    pupil_l = bpy.context.active_object
    pupil_l.name = "左瞳孔"
    pupil_l.scale = (0.4, 0.5, 1.0)  # 竖瞳
    pupil_l.data.materials.append(pupil_mat)
    smooth_object(pupil_l)
    
    # ========== 右眼 ==========
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.15, location=(0.25, 0.45, 2.4))
    eye_white_r = bpy.context.active_object
    eye_white_r.name = "右眼白"
    eye_white_r.scale = (1.0, 0.7, 1.1)
    eye_white_r.data.materials.append(eye_white_mat)
    smooth_object(eye_white_r)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.12, location=(0.25, 0.5, 2.4))
    iris_r = bpy.context.active_object
    iris_r.name = "右虹膜"
    iris_r.scale = (1.0, 0.5, 1.0)
    iris_r.data.materials.append(eye_mat)
    smooth_object(iris_r)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.08, location=(0.25, 0.52, 2.4))
    pupil_r = bpy.context.active_object
    pupil_r.name = "右瞳孔"
    pupil_r.scale = (0.4, 0.5, 1.0)
    pupil_r.data.materials.append(pupil_mat)
    smooth_object(pupil_r)
    
    # ========== 眼神凶狠效果 - 眉毛上方突起（皱眉） ==========
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.12, location=(-0.28, 0.4, 2.55))
    brow_l = bpy.context.active_object
    brow_l.name = "左眉弓"
    brow_l.scale = (1.5, 0.8, 0.5)
    brow_l.rotation_euler = (0, 0, math.radians(15))  # 向内倾斜，凶相
    brow_l.data.materials.append(orange_mat)
    smooth_object(brow_l)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.12, location=(0.28, 0.4, 2.55))
    brow_r = bpy.context.active_object
    brow_r.name = "右眉弓"
    brow_r.scale = (1.5, 0.8, 0.5)
    brow_r.rotation_euler = (0, 0, math.radians(-15))
    brow_r.data.materials.append(orange_mat)
    smooth_object(brow_r)
    
    # ========== 鼻子（粉色三角） ==========
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.08, radius2=0, depth=0.06, location=(0, 0.6, 2.25))
    nose = bpy.context.active_object
    nose.name = "鼻子"
    nose.rotation_euler = (math.radians(90), 0, 0)
    nose.data.materials.append(nose_mat)
    smooth_object(nose)
    
    # 鼻梁纹（橘猫特征）
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, 0.55, 2.35))
    nose_bridge = bpy.context.active_object
    nose_bridge.name = "鼻梁纹"
    nose_bridge.scale = (0.3, 0.3, 1.5)
    nose_bridge.data.materials.append(stripe_mat)
    smooth_object(nose_bridge)
    
    # ========== 嘴巴（哈气状态 - 张嘴） ==========
    # 上颚
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.2, location=(0, 0.55, 2.1))
    upper_jaw = bpy.context.active_object
    upper_jaw.name = "上颚"
    upper_jaw.scale = (1.5, 0.8, 0.6)
    upper_jaw.data.materials.append(orange_mat)
    smooth_object(upper_jaw)
    
    # 下颚（张嘴）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.18, location=(0, 0.5, 2.0))
    lower_jaw = bpy.context.active_object
    lower_jaw.name = "下颚"
    lower_jaw.scale = (1.4, 0.7, 0.5)
    lower_jaw.data.materials.append(orange_mat)
    smooth_object(lower_jaw)
    
    # 口腔内部
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.12, location=(0, 0.52, 2.05))
    mouth_inside = bpy.context.active_object
    mouth_inside.name = "口腔"
    mouth_inside.scale = (1.2, 0.6, 0.8)
    mouth_inside.data.materials.append(mouth_mat)
    smooth_object(mouth_inside)
    
    # 舌头
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.08, location=(0, 0.58, 2.0))
    tongue = bpy.context.active_object
    tongue.name = "舌头"
    tongue.scale = (1.0, 0.8, 0.4)
    tongue.data.materials.append(nose_mat)
    smooth_object(tongue)
    
    # 上犬齿（小尖牙 - 凶相）
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.03, radius2=0.005, depth=0.1, location=(-0.1, 0.6, 2.08))
    fang_l = bpy.context.active_object
    fang_l.name = "左犬齿"
    fang_l.rotation_euler = (math.radians(20), 0, 0)
    fang_l.data.materials.append(eye_white_mat)
    smooth_object(fang_l)
    
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.03, radius2=0.005, depth=0.1, location=(0.1, 0.6, 2.08))
    fang_r = bpy.context.active_object
    fang_r.name = "右犬齿"
    fang_r.rotation_euler = (math.radians(20), 0, 0)
    fang_r.data.materials.append(eye_white_mat)
    smooth_object(fang_r)
    
    # ========== 胡须 ==========
    for i in range(3):
        # 左侧胡须
        bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=0.5, location=(-0.35 - i*0.05, 0.55, 2.2 - i*0.05))
        whisker = bpy.context.active_object
        whisker.name = f"左胡须_{i}"
        whisker.rotation_euler = (math.radians(-10 + i*5), math.radians(30), 0)
        whisker.data.materials.append(belly_mat)
        
        # 右侧胡须
        bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=0.5, location=(0.35 + i*0.05, 0.55, 2.2 - i*0.05))
        whisker = bpy.context.active_object
        whisker.name = f"右胡须_{i}"
        whisker.rotation_euler = (math.radians(-10 + i*5), math.radians(-30), 0)
        whisker.data.materials.append(belly_mat)
    
    # ========== 虎斑纹路（额头M纹） ==========
    # 额头M纹左侧
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(-0.2, 0.35, 2.6))
    stripe1 = bpy.context.active_object
    stripe1.name = "额头纹左"
    stripe1.scale = (0.8, 0.3, 0.3)
    stripe1.rotation_euler = (0, 0, math.radians(30))
    stripe1.data.materials.append(stripe_mat)
    smooth_object(stripe1)
    
    # 额头M纹右侧
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.2, 0.35, 2.6))
    stripe2 = bpy.context.active_object
    stripe2.name = "额头纹右"
    stripe2.scale = (0.8, 0.3, 0.3)
    stripe2.rotation_euler = (0, 0, math.radians(-30))
    stripe2.data.materials.append(stripe_mat)
    smooth_object(stripe2)
    
    # ========== 前腿 ==========
    # 左前腿
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.8, location=(-0.4, 0.3, 0.4))
    leg_fl = bpy.context.active_object
    leg_fl.name = "左前腿"
    leg_fl.data.materials.append(orange_mat)
    smooth_object(leg_fl)
    
    # 左前爪
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.12, location=(-0.4, 0.35, 0.05))
    paw_fl = bpy.context.active_object
    paw_fl.name = "左前爪"
    paw_fl.scale = (1.2, 1.3, 0.6)
    paw_fl.data.materials.append(orange_mat)
    smooth_object(paw_fl)
    
    # 左前肉垫
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.08, location=(-0.4, 0.4, 0.02))
    pad_fl = bpy.context.active_object
    pad_fl.name = "左前肉垫"
    pad_fl.scale = (1.0, 1.0, 0.5)
    pad_fl.data.materials.append(pad_mat)
    smooth_object(pad_fl)
    
    # 右前腿
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.8, location=(0.4, 0.3, 0.4))
    leg_fr = bpy.context.active_object
    leg_fr.name = "右前腿"
    leg_fr.data.materials.append(orange_mat)
    smooth_object(leg_fr)
    
    # 右前爪
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.12, location=(0.4, 0.35, 0.05))
    paw_fr = bpy.context.active_object
    paw_fr.name = "右前爪"
    paw_fr.scale = (1.2, 1.3, 0.6)
    paw_fr.data.materials.append(orange_mat)
    smooth_object(paw_fr)
    
    # 右前肉垫
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.08, location=(0.4, 0.4, 0.02))
    pad_fr = bpy.context.active_object
    pad_fr.name = "右前肉垫"
    pad_fr.scale = (1.0, 1.0, 0.5)
    pad_fr.data.materials.append(pad_mat)
    smooth_object(pad_fr)
    
    # ========== 后腿（粗壮） ==========
    # 左后腿
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.22, location=(-0.45, -0.2, 0.6))
    leg_bl = bpy.context.active_object
    leg_bl.name = "左后腿"
    leg_bl.scale = (0.9, 0.9, 1.5)
    leg_bl.data.materials.append(orange_mat)
    smooth_object(leg_bl)
    
    # 左后爪
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.13, location=(-0.45, -0.15, 0.05))
    paw_bl = bpy.context.active_object
    paw_bl.name = "左后爪"
    paw_bl.scale = (1.2, 1.3, 0.6)
    paw_bl.data.materials.append(orange_mat)
    smooth_object(paw_bl)
    
    # 右后腿
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.22, location=(0.45, -0.2, 0.6))
    leg_br = bpy.context.active_object
    leg_br.name = "右后腿"
    leg_br.scale = (0.9, 0.9, 1.5)
    leg_br.data.materials.append(orange_mat)
    smooth_object(leg_br)
    
    # 右后爪
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.13, location=(0.45, -0.15, 0.05))
    paw_br = bpy.context.active_object
    paw_br.name = "右后爪"
    paw_br.scale = (1.2, 1.3, 0.6)
    paw_br.data.materials.append(orange_mat)
    smooth_object(paw_br)
    
    # ========== 尾巴（粗壮橘猫尾巴） ==========
    # 尾巴分段
    tail_segments = 6
    for i in range(tail_segments):
        t = i / tail_segments
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.1 - t*0.02, 
                                              location=(0, -0.7 - i*0.15, 1.0 + i*0.12))
        tail_seg = bpy.context.active_object
        tail_seg.name = f"尾巴_{i}"
        tail_seg.scale = (1.0, 1.0, 1.2)
        if i % 3 == 0:
            tail_seg.data.materials.append(stripe_mat)
        else:
            tail_seg.data.materials.append(orange_mat)
        smooth_object(tail_seg)
    
    # 尾巴尖（深色条纹）
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.06, 
                                          location=(0, -1.6, 1.7))
    tail_tip = bpy.context.active_object
    tail_tip.name = "尾巴尖"
    tail_tip.data.materials.append(stripe_mat)
    smooth_object(tail_tip)
    
    # ========== 地面 ==========
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "地面"
    ground_mat = create_material("地面灰", (0.3, 0.3, 0.3, 1.0), 0.8)
    ground.data.materials.append(ground_mat)
    
    # ========== 场景设置 ==========
    # 阳光
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.name = "主光"
    sun.data.energy = 4
    sun.rotation_euler = (math.radians(45), 0, math.radians(30))
    
    # 补光
    bpy.ops.object.light_add(type='AREA', location=(-4, 3, 5))
    fill = bpy.context.active_object
    fill.name = "补光"
    fill.data.energy = 100
    
    # 相机（正面略偏，突出圆头）
    bpy.ops.object.camera_add(location=(3, -3, 2.5))
    cam = bpy.context.active_object
    cam.name = "相机"
    cam.rotation_euler = (math.radians(75), 0, math.radians(45))
    bpy.context.scene.camera = cam
    
    # 渲染设置
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    
    # 世界背景
    world = bpy.data.worlds.new("耄耋世界")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.95, 0.92, 0.85, 1.0)  # 暖色调背景
    bg.inputs[1].default_value = 0.8
    
    print("=" * 50)
    print("圆头耄耋（橘猫）模型创建完成！")
    print("=" * 50)
    print("\n模型特征：")
    print("- 圆头造型（横向略宽）")
    print("- 飞机耳（向外平躺）")
    print("- 哈气状态（张嘴露齿）")
    print("- 竖瞳（凶狠眼神）")
    print("- 粗壮虎斑纹路")
    print("- 胖橘体型")
    print("- 粗壮尾巴")
    
    # 保存文件
    script_dir = os.path.dirname(os.path.abspath(__file__))
    blend_path = os.path.join(script_dir, "maodie_cat.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"\n已保存：{blend_path}")

if __name__ == "__main__":
    create_maodie()
