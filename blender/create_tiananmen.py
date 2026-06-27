"""
天安门城楼Blender模型创建脚本
使用方法：
1. 打开Blender
2. 在脚本工作区中打开此文件
3. 点击"运行脚本"按钮
或者通过命令行运行：
blender --background --python create_tiananmen.py
"""

import bpy
import bmesh
import math
import os

def clear_scene():
    """清除场景中的所有对象"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # 清除所有材质
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    
    # 清除所有网格数据
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

def create_material(name, color, roughness=0.5):
    """创建材质"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = color  # Base Color
    bsdf.inputs[7].default_value = roughness  # Roughness
    return mat

def create_tiananmen():
    """创建天安门城楼模型"""
    
    # 清除场景
    clear_scene()
    
    # 创建材质
    red_mat = create_material("城墙红", (0.8, 0.1, 0.1, 1.0), 0.3)
    yellow_mat = create_material("屋顶黄", (0.9, 0.8, 0.2, 1.0), 0.2)
    gray_mat = create_material("城砖灰", (0.5, 0.5, 0.5, 1.0), 0.7)
    white_mat = create_material("汉白玉", (0.95, 0.95, 0.95, 1.0), 0.1)
    
    # 1. 创建城墙基础
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1))
    wall = bpy.context.active_object
    wall.name = "城墙基础"
    wall.scale = (12, 3, 2)  # 长12，宽3，高2
    wall.data.materials.append(red_mat)
    
    # 2. 创建城门洞
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.5))
    gate_cutout = bpy.context.active_object
    gate_cutout.name = "城门洞切割体"
    gate_cutout.scale = (2.5, 4, 2)  # 门洞宽2.5，高度2
    gate_cutout.hide_render = True
    gate_cutout.display_type = 'WIRE'
    
    # 布尔运算创建门洞
    bpy.context.view_layer.objects.active = wall
    bool_mod = wall.modifiers.new(name="城门洞", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = gate_cutout
    bpy.ops.object.modifier_apply(modifier="城门洞")
    
    # 隐藏切割体
    gate_cutout.hide_viewport = True
    gate_cutout.hide_render = True
    
    # 3. 创建城墙垛口
    merlon_height = 0.3
    merlon_width = 0.4
    for i in range(-5, 6):
        # 前排垛口
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 0.8, 1.4, 2.15))
        merlon = bpy.context.active_object
        merlon.name = f"前垛口_{i+5}"
        merlon.scale = (merlon_width, 0.2, merlon_height)
        merlon.data.materials.append(red_mat)
        
        # 后排垛口
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 0.8, -1.4, 2.15))
        merlon = bpy.context.active_object
        merlon.name = f"后垛口_{i+5}"
        merlon.scale = (merlon_width, 0.2, merlon_height)
        merlon.data.materials.append(red_mat)
    
    # 4. 创建城楼主体
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 4))
    tower_body = bpy.context.active_object
    tower_body.name = "城楼主体"
    tower_body.scale = (10, 2, 4)  # 长10，宽2，高4
    tower_body.data.materials.append(red_mat)
    
    # 5. 创建城楼柱子
    pillar_radius = 0.15
    pillar_height = 4
    for i in range(-4, 5):
        # 前排柱子
        bpy.ops.mesh.primitive_cylinder_add(
            radius=pillar_radius, 
            depth=pillar_height, 
            location=(i, 1, 4)
        )
        pillar = bpy.context.active_object
        pillar.name = f"前柱_{i+4}"
        pillar.data.materials.append(red_mat)
        
        # 后排柱子
        bpy.ops.mesh.primitive_cylinder_add(
            radius=pillar_radius, 
            depth=pillar_height, 
            location=(i, -1, 4)
        )
        pillar = bpy.context.active_object
        pillar.name = f"后柱_{i+4}"
        pillar.data.materials.append(red_mat)
    
    # 6. 创建城楼平台
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 6.1))
    platform = bpy.context.active_object
    platform.name = "城楼平台"
    platform.scale = (10.5, 2.5, 0.2)
    platform.data.materials.append(gray_mat)
    
    # 7. 创建主屋顶（重檐歇山顶）
    # 下层屋顶
    bpy.ops.mesh.primitive_cone_add(
        vertices=4, 
        radius1=3, 
        radius2=0, 
        depth=2, 
        location=(0, 0, 7.5)
    )
    roof_lower = bpy.context.active_object
    roof_lower.name = "下层屋顶"
    roof_lower.scale = (3.5, 1.2, 1)
    roof_lower.rotation_euler = (0, 0, math.radians(45))
    roof_lower.data.materials.append(yellow_mat)
    
    # 上层屋顶
    bpy.ops.mesh.primitive_cone_add(
        vertices=4, 
        radius1=2.5, 
        radius2=0, 
        depth=1.5, 
        location=(0, 0, 8.5)
    )
    roof_upper = bpy.context.active_object
    roof_upper.name = "上层屋顶"
    roof_upper.scale = (3, 1, 1)
    roof_upper.rotation_euler = (0, 0, math.radians(45))
    roof_upper.data.materials.append(yellow_mat)
    
    # 8. 创建屋脊装饰
    # 正脊
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 8.7))
    ridge = bpy.context.active_object
    ridge.name = "正脊"
    ridge.scale = (6, 0.2, 0.15)
    ridge.data.materials.append(yellow_mat)
    
    # 垂脊
    for i in range(-2, 3):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i, 0, 8.6))
        vertical_ridge = bpy.context.active_object
        vertical_ridge.name = f"垂脊_{i+2}"
        vertical_ridge.scale = (0.1, 2, 0.1)
        vertical_ridge.data.materials.append(yellow_mat)
    
    # 9. 创建城楼窗户
    window_mat = create_material("窗户", (0.2, 0.15, 0.1, 1.0), 0.1)
    for i in range(-3, 4):
        # 前窗
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 1.2, 2.05, 4.5))
        window = bpy.context.active_object
        window.name = f"前窗_{i+3}"
        window.scale = (0.6, 0.1, 1)
        window.data.materials.append(window_mat)
        
        # 后窗
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 1.2, -2.05, 4.5))
        window = bpy.context.active_object
        window.name = f"后窗_{i+3}"
        window.scale = (0.6, 0.1, 1)
        window.data.materials.append(window_mat)
    
    # 10. 创建城楼匾额
    # "中华人民共和国万岁"匾额
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 2.1, 5))
    plaque = bpy.context.active_object
    plaque.name = "中央匾额"
    plaque.scale = (3, 0.1, 0.8)
    plaque.data.materials.append(yellow_mat)
    
    # "世界人民大团结万岁"匾额
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -2.1, 5))
    plaque2 = bpy.context.active_object
    plaque2.name = "后匾额"
    plaque2.scale = (3, 0.1, 0.8)
    plaque2.data.materials.append(yellow_mat)
    
    # 11. 创建城墙标语位置
    # 左侧标语牌
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-4.5, 1.5, 1.8))
    slogan_left = bpy.context.active_object
    slogan_left.name = "左侧标语牌"
    slogan_left.scale = (2, 0.1, 0.6)
    slogan_left.data.materials.append(white_mat)
    
    # 右侧标语牌
    bpy.ops.mesh.primitive_cube_add(size=1, location=(4.5, 1.5, 1.8))
    slogan_right = bpy.context.active_object
    slogan_right.name = "右侧标语牌"
    slogan_right.scale = (2, 0.1, 0.6)
    slogan_right.data.materials.append(white_mat)
    
    # 12. 创建华表（左侧）
    # 柱身
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.15, 
        depth=6, 
        location=(-8, 2, 3)
    )
    huabiao_left = bpy.context.active_object
    huabiao_left.name = "华表_左"
    huabiao_left.data.materials.append(white_mat)
    
    # 柱头
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.3, 
        location=(-8, 2, 6.3)
    )
    huabiao_cap_left = bpy.context.active_object
    huabiao_cap_left.name = "华表柱头_左"
    huabiao_cap_left.data.materials.append(white_mat)
    
    # 柱座
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.4, 
        depth=0.5, 
        location=(-8, 2, 0.25)
    )
    huabiao_base_left = bpy.context.active_object
    huabiao_base_left.name = "华表柱座_左"
    huabiao_base_left.data.materials.append(white_mat)
    
    # 13. 创建华表（右侧）
    # 柱身
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.15, 
        depth=6, 
        location=(8, 2, 3)
    )
    huabiao_right = bpy.context.active_object
    huabiao_right.name = "华表_右"
    huabiao_right.data.materials.append(white_mat)
    
    # 柱头
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.3, 
        location=(8, 2, 6.3)
    )
    huabiao_cap_right = bpy.context.active_object
    huabiao_cap_right.name = "华表柱头_右"
    huabiao_cap_right.data.materials.append(white_mat)
    
    # 柱座
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.4, 
        depth=0.5, 
        location=(8, 2, 0.25)
    )
    huabiao_base_right = bpy.context.active_object
    huabiao_base_right.name = "华表柱座_右"
    huabiao_base_right.data.materials.append(white_mat)
    
    # 14. 创建石狮子（简化版）
    # 左侧石狮
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.5, 
        location=(-6, 2, 0.5)
    )
    lion_left = bpy.context.active_object
    lion_left.name = "石狮_左"
    lion_left.scale = (1, 1, 1.2)
    lion_left.data.materials.append(gray_mat)
    
    # 右侧石狮
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.5, 
        location=(6, 2, 0.5)
    )
    lion_right = bpy.context.active_object
    lion_right.name = "石狮_右"
    lion_right.scale = (1, 1, 1.2)
    lion_right.data.materials.append(gray_mat)
    
    # 15. 创建地面
    bpy.ops.mesh.primitive_plane_add(size=50, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "地面"
    ground_mat = create_material("地面", (0.3, 0.3, 0.3, 1.0), 0.8)
    ground.data.materials.append(ground_mat)
    
    # 16. 创建金水桥
    # 桥面
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 4, 0.2))
    bridge_deck = bpy.context.active_object
    bridge_deck.name = "金水桥_桥面"
    bridge_deck.scale = (8, 2, 0.2)
    bridge_deck.data.materials.append(white_mat)
    
    # 桥栏杆
    for i in range(-3, 4):
        # 左侧栏杆
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.05, 
            depth=0.8, 
            location=(i, 5, 0.6)
        )
        railing = bpy.context.active_object
        railing.name = f"左栏杆_{i+3}"
        railing.data.materials.append(white_mat)
        
        # 右侧栏杆
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.05, 
            depth=0.8, 
            location=(i, 3, 0.6)
        )
        railing = bpy.context.active_object
        railing.name = f"右栏杆_{i+3}"
        railing.data.materials.append(white_mat)
    
    # 17. 设置场景光照
    # 主光源（模拟太阳）
    bpy.ops.object.light_add(type='SUN', location=(20, -20, 30))
    sun = bpy.context.active_object
    sun.name = "主光源"
    sun.data.energy = 5
    sun.rotation_euler = (math.radians(45), math.radians(30), 0)
    
    # 补光
    bpy.ops.object.light_add(type='AREA', location=(-10, 10, 15))
    fill_light = bpy.context.active_object
    fill_light.name = "补光"
    fill_light.data.energy = 200
    fill_light.scale = (10, 10, 1)
    
    # 18. 设置相机
    bpy.ops.object.camera_add(location=(25, -25, 15))
    camera = bpy.context.active_object
    camera.name = "主相机"
    camera.rotation_euler = (math.radians(65), 0, math.radians(45))
    bpy.context.scene.camera = camera
    
    # 设置渲染参数
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.film_transparent = True
    
    # 设置世界背景
    world = bpy.data.worlds.new("天安门世界")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes["Background"]
    bg_node.inputs[0].default_value = (0.5, 0.7, 1.0, 1.0)  # 天蓝色背景
    bg_node.inputs[1].default_value = 0.5
    
    print("=" * 50)
    print("天安门城楼模型创建完成！")
    print("=" * 50)
    print("\n模型包含：")
    print("- 城墙基础（带城门洞）")
    print("- 城墙垛口")
    print("- 城楼主体（带柱子）")
    print("- 重檐歇山顶")
    print("- 屋脊装饰")
    print("- 窗户和匾额")
    print("- 华表（2座）")
    print("- 石狮子（2座）")
    print("- 金水桥")
    print("- 地面和场景设置")
    print("\n渲染设置：")
    print("- 分辨率：1920x1080")
    print("- 渲染引擎：Cycles")
    print("- 已设置相机和灯光")
    print("\n您可以在3D视图中旋转查看模型，或按F12渲染图像。")
    
    # 保存.blend文件
    script_dir = os.path.dirname(os.path.abspath(__file__))
    blend_file_path = os.path.join(script_dir, "tiananmen.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
    print(f"\n模型已保存到：{blend_file_path}")

if __name__ == "__main__":
    create_tiananmen()