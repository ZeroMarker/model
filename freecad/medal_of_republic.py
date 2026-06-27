# -*- coding: utf-8 -*-
"""
共和国勋章 - FreeCAD Python脚本
中华人民共和国最高荣誉勋章复刻

历史背景：
- 2016年1月1日设立
- 授予在中国特色社会主义建设和保卫国家中作出巨大贡献、
  建立卓越功勋的杰出人士
- 勋章设计融合了中国传统文化元素
"""

import sys
import os

# FreeCAD Python环境
FREECAD_PATHS = [
    r"C:\Users\{}\AppData\Local\Programs\FreeCAD 1.1\bin".format(os.getenv('USERNAME')),
    r"C:\Users\{}\AppData\Local\Programs\FreeCAD 1.1\lib".format(os.getenv('USERNAME')),
]

for path in FREECAD_PATHS:
    if path not in sys.path:
        sys.path.append(path)

try:
    import FreeCAD
    import Part
    import math
    
    print("FreeCAD模块导入成功")
    
    # 创建新文档
    doc = FreeCAD.newDocument("MedalOfRepublic")
    print("文档创建成功")
    
    # ========== 参数定义 ==========
    # 共和国勋章尺寸（毫米）
    star_outer_radius = 35.0    # 五角星外半径
    star_inner_radius = 15.0    # 五角星内半径
    medal_thickness = 4.0       # 勋章厚度
    border_width = 3.0          # 边框宽度
    center_radius = 12.0        # 中心区域半径
    wheat_width = 4.0           # 麦穗宽度
    
    print("参数定义完成")
    
    # ========== 创建五角星 ==========
    def create_star_points(outer_r, inner_r, num_points=5):
        """创建五角星顶点"""
        points = []
        for i in range(num_points * 2):
            angle = math.pi / 2 + i * math.pi / num_points
            if i % 2 == 0:
                r = outer_r
            else:
                r = inner_r
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            points.append(FreeCAD.Vector(x, y, 0))
        return points
    
    # 创建五角星轮廓
    star_points = create_star_points(star_outer_radius, star_inner_radius)
    
    # 使用多边形拉伸创建五角星
    # 由于FreeCAD的Part::Polygon可能不直接支持，我们使用其他方法
    
    # 方法：使用五个三角形组合
    def create_triangle(name, p1, p2, p3, height):
        """创建三角形拉伸体"""
        # 计算三角形的边界框
        min_x = min(p1.x, p2.x, p3.x)
        max_x = max(p1.x, p2.x, p3.x)
        min_y = min(p1.y, p2.y, p3.y)
        max_y = max(p1.y, p2.y, p3.y)
        
        # 创建一个盒子作为基础
        box = doc.addObject("Part::Box", name)
        box.Length = max_x - min_x
        box.Width = max_y - min_y
        box.Height = height
        box.Placement = FreeCAD.Placement(
            FreeCAD.Vector(min_x, min_y, 0),
            FreeCAD.Rotation(0, 0, 0)
        )
        return box
    
    # 创建五角星的五个尖角
    star_triangles = []
    for i in range(5):
        angle1 = math.pi / 2 + i * 2 * math.pi / 5
        angle2 = math.pi / 2 + (i + 1) * 2 * math.pi / 5
        angle3 = math.pi / 2 + (i + 0.5) * 2 * math.pi / 5
        
        p1 = FreeCAD.Vector(star_outer_radius * math.cos(angle1), 
                           star_outer_radius * math.sin(angle1), 0)
        p2 = FreeCAD.Vector(star_outer_radius * math.cos(angle2), 
                           star_outer_radius * math.sin(angle2), 0)
        p3 = FreeCAD.Vector(star_inner_radius * math.cos(angle3), 
                           star_inner_radius * math.sin(angle3), 0)
        
        tri = create_triangle(f"星角_{i}", p1, p2, p3, medal_thickness)
        star_triangles.append(tri)
    
    # 创建中心五边形
    center_pentagon = doc.addObject("Part::Cylinder", "中心五边形")
    center_pentagon.Radius = star_inner_radius
    center_pentagon.Height = medal_thickness
    
    print("五角星基础形状创建完成")
    
    # 合并五角星
    star_merge1 = doc.addObject("Part::Fuse", "星合并1")
    star_merge1.Base = star_triangles[0]
    star_merge1.Tool = star_triangles[1]
    
    star_merge2 = doc.addObject("Part::Fuse", "星合并2")
    star_merge2.Base = star_merge1
    star_merge2.Tool = star_triangles[2]
    
    star_merge3 = doc.addObject("Part::Fuse", "星合并3")
    star_merge3.Base = star_merge2
    star_merge3.Tool = star_triangles[3]
    
    star_merge4 = doc.addObject("Part::Fuse", "星合并4")
    star_merge4.Base = star_merge3
    star_merge4.Tool = star_triangles[4]
    
    star_merge5 = doc.addObject("Part::Fuse", "五角星")
    star_merge5.Base = star_merge4
    star_merge5.Tool = center_pentagon
    
    print("五角星合并完成")
    
    # ========== 创建边框 ==========
    # 外边框（圆形）
    border_outer = doc.addObject("Part::Cylinder", "边框外")
    border_outer.Radius = star_outer_radius + border_width
    border_outer.Height = medal_thickness + 1.0
    
    # 内边框（用于布尔减去）
    border_inner = doc.addObject("Part::Cylinder", "边框内")
    border_inner.Radius = star_outer_radius
    border_inner.Height = medal_thickness + 1.0
    
    # 布尔减去创建边框
    border_frame = doc.addObject("Part::Cut", "边框框架")
    border_frame.Base = border_outer
    border_frame.Tool = border_inner
    
    print("边框创建完成")
    
    # ========== 合并边框和五角星 ==========
    medal_with_border = doc.addObject("Part::Fuse", "勋章主体")
    medal_with_border.Base = star_merge5
    medal_with_border.Tool = border_frame
    
    print("边框合并完成")
    
    # ========== 创建中心装饰 ==========
    # 中心圆盘（代表天安门）
    center_disc = doc.addObject("Part::Cylinder", "中心圆盘")
    center_disc.Radius = center_radius
    center_disc.Height = medal_thickness * 0.6
    
    # 中心小五角星
    small_star_points = create_star_points(8.0, 3.0)
    small_star_triangles = []
    for i in range(5):
        angle1 = math.pi / 2 + i * 2 * math.pi / 5
        angle2 = math.pi / 2 + (i + 1) * 2 * math.pi / 5
        angle3 = math.pi / 2 + (i + 0.5) * 2 * math.pi / 5
        
        p1 = FreeCAD.Vector(8.0 * math.cos(angle1), 
                           8.0 * math.sin(angle1), 0)
        p2 = FreeCAD.Vector(8.0 * math.cos(angle2), 
                           8.0 * math.sin(angle2), 0)
        p3 = FreeCAD.Vector(3.0 * math.cos(angle3), 
                           3.0 * math.sin(angle3), 0)
        
        tri = create_triangle(f"小星角_{i}", p1, p2, p3, medal_thickness * 0.8)
        small_star_triangles.append(tri)
    
    # 合并小五角星
    small_star_merge1 = doc.addObject("Part::Fuse", "小星合并1")
    small_star_merge1.Base = small_star_triangles[0]
    small_star_merge1.Tool = small_star_triangles[1]
    
    small_star_merge2 = doc.addObject("Part::Fuse", "小星合并2")
    small_star_merge2.Base = small_star_merge1
    small_star_merge2.Tool = small_star_triangles[2]
    
    small_star_merge3 = doc.addObject("Part::Fuse", "小星合并3")
    small_star_merge3.Base = small_star_merge2
    small_star_merge3.Tool = small_star_triangles[3]
    
    small_star_merge4 = doc.addObject("Part::Fuse", "小五角星")
    small_star_merge4.Base = small_star_merge3
    small_star_merge4.Tool = small_star_triangles[4]
    
    print("中心装饰创建完成")
    
    # ========== 创建麦穗装饰 ==========
    # 左侧麦穗（用椭圆体模拟）
    wheat_left = doc.addObject("Part::Cylinder", "左麦穗")
    wheat_left.Radius = wheat_width / 2
    wheat_left.Height = 30.0
    wheat_left.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-star_outer_radius - border_width - 8, -15, 0),
        FreeCAD.Rotation(0, 0, 15)
    )
    
    # 右侧麦穗
    wheat_right = doc.addObject("Part::Cylinder", "右麦穗")
    wheat_right.Radius = wheat_width / 2
    wheat_right.Height = 30.0
    wheat_right.Placement = FreeCAD.Placement(
        FreeCAD.Vector(star_outer_radius + border_width + 8, -15, 0),
        FreeCAD.Rotation(0, 0, -15)
    )
    
    # 麦穗颗粒（用球体模拟）
    wheat_grains = []
    for i in range(8):
        # 左侧颗粒
        grain_l = doc.addObject("Part::Sphere", f"左麦粒_{i}")
        grain_l.Radius = 2.5
        grain_l.Placement = FreeCAD.Placement(
            FreeCAD.Vector(-star_outer_radius - border_width - 12 + i * 2, 
                          -10 + i * 3, 0),
            FreeCAD.Rotation(0, 0, 0)
        )
        wheat_grains.append(grain_l)
        
        # 右侧颗粒
        grain_r = doc.addObject("Part::Sphere", f"右麦粒_{i}")
        grain_r.Radius = 2.5
        grain_r.Placement = FreeCAD.Placement(
            FreeCAD.Vector(star_outer_radius + border_width + 12 - i * 2, 
                          -10 + i * 3, 0),
            FreeCAD.Rotation(0, 0, 0)
        )
        wheat_grains.append(grain_r)
    
    print("麦穗装饰创建完成")
    
    # ========== 创建挂环 ==========
    # 挂环（用于佩戴）
    hanging_ring = doc.addObject("Part::Torus", "挂环")
    hanging_ring.Radius1 = 6.0
    hanging_ring.Radius2 = 2.0
    hanging_ring.Placement = FreeCAD.Placement(
        FreeCAD.Vector(0, star_outer_radius + border_width + 10, medal_thickness/2),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    # 绶带连接环
    ribbon_ring = doc.addObject("Part::Cylinder", "绶带环")
    ribbon_ring.Radius = 4.0
    ribbon_ring.Height = 8.0
    ribbon_ring.Placement = FreeCAD.Placement(
        FreeCAD.Vector(0, star_outer_radius + border_width + 18, 0),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    print("挂环创建完成")
    
    # ========== 合并所有部件 ==========
    # 合并中心装饰
    medal_with_center = doc.addObject("Part::Fuse", "勋章含中心")
    medal_with_center.Base = medal_with_border
    medal_with_center.Tool = center_disc
    
    medal_with_star = doc.addObject("Part::Fuse", "勋章含小星")
    medal_with_star.Base = medal_with_center
    medal_with_star.Tool = small_star_merge4
    
    # 合并麦穗
    medal_with_wheat1 = doc.addObject("Part::Fuse", "勋章含麦穗1")
    medal_with_wheat1.Base = medal_with_star
    medal_with_wheat1.Tool = wheat_left
    
    medal_with_wheat2 = doc.addObject("Part::Fuse", "勋章含麦穗2")
    medal_with_wheat2.Base = medal_with_wheat1
    medal_with_wheat2.Tool = wheat_right
    
    # 合并麦粒
    current_medal = medal_with_wheat2
    for i, grain in enumerate(wheat_grains):
        merged = doc.addObject("Part::Fuse", f"勋章含麦粒_{i}")
        merged.Base = current_medal
        merged.Tool = grain
        current_medal = merged
    
    # 合并挂环
    medal_with_ring1 = doc.addObject("Part::Fuse", "勋章含挂环1")
    medal_with_ring1.Base = current_medal
    medal_with_ring1.Tool = hanging_ring
    
    final_medal = doc.addObject("Part::Fuse", "共和国勋章")
    final_medal.Base = medal_with_ring1
    final_medal.Tool = ribbon_ring
    
    print("所有部件合并完成")
    
    # 重新计算
    doc.recompute()
    print("模型计算完成")
    
    # 导出文件
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    step_path = os.path.join(output_dir, "medal_of_republic.step")
    Part.export([final_medal], step_path)
    print(f"已导出STEP：{step_path}")
    
    stl_path = os.path.join(output_dir, "medal_of_republic.stl")
    Part.export([final_medal], stl_path)
    print(f"已导出STL：{stl_path}")
    
    print("=" * 60)
    print("共和国勋章模型创建完成！")
    print("=" * 60)
    print(f"\n设计元素：")
    print(f"- 五角星：代表中国共产党的领导")
    print(f"- 中心圆盘：代表天安门")
    print(f"- 小五角星：代表人民")
    print(f"- 麦穗：代表农民阶级")
    print(f"- 挂环：用于佩戴")
    print(f"\n模型参数：")
    print(f"- 五角星外半径：{star_outer_radius}mm")
    print(f"- 五角星内半径：{star_inner_radius}mm")
    print(f"- 勋章厚度：{medal_thickness}mm")
    print(f"- 边框宽度：{border_width}mm")
    print(f"- 中心区域：{center_radius}mm")
    
except Exception as e:
    print(f"错误：{e}")
    import traceback
    traceback.print_exc()
