# -*- coding: utf-8 -*-
"""
共和国勋章（简化版） - FreeCAD Python脚本
适用于Web展示的轻量级版本
"""

import sys
import os

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
    
    doc = FreeCAD.newDocument("MedalOfRepublicSimple")
    print("文档创建成功")
    
    # ========== 参数定义 ==========
    star_outer_radius = 35.0
    star_inner_radius = 15.0
    medal_thickness = 4.0
    border_width = 3.0
    center_radius = 12.0
    
    print("参数定义完成")
    
    # ========== 创建五角星（简化版） ==========
    # 使用更少的多边形
    def create_star_points(outer_r, inner_r, num_points=5):
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
    
    # 创建五角星的五个尖角（使用更简单的几何体）
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
        
        # 计算三角形的边界框
        min_x = min(p1.x, p2.x, p3.x)
        max_x = max(p1.x, p2.x, p3.x)
        min_y = min(p1.y, p2.y, p3.y)
        max_y = max(p1.y, p2.y, p3.y)
        
        # 创建一个盒子作为基础
        box = doc.addObject("Part::Box", f"星角_{i}")
        box.Length = max_x - min_x
        box.Width = max_y - min_y
        box.Height = medal_thickness
        box.Placement = FreeCAD.Placement(
            FreeCAD.Vector(min_x, min_y, 0),
            FreeCAD.Rotation(0, 0, 0)
        )
        star_triangles.append(box)
    
    # 创建中心五边形（使用更少的多边形）
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
    # 中心圆盘
    center_disc = doc.addObject("Part::Cylinder", "中心圆盘")
    center_disc.Radius = center_radius
    center_disc.Height = medal_thickness * 0.6
    
    # 中心小五角星（简化版）
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
        
        min_x = min(p1.x, p2.x, p3.x)
        max_x = max(p1.x, p2.x, p3.x)
        min_y = min(p1.y, p2.y, p3.y)
        max_y = max(p1.y, p2.y, p3.y)
        
        box = doc.addObject("Part::Box", f"小星角_{i}")
        box.Length = max_x - min_x
        box.Width = max_y - min_y
        box.Height = medal_thickness * 0.8
        box.Placement = FreeCAD.Placement(
            FreeCAD.Vector(min_x, min_y, 0),
            FreeCAD.Rotation(0, 0, 0)
        )
        small_star_triangles.append(box)
    
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
    
    # ========== 创建麦穗装饰（简化版） ==========
    # 左侧麦穗（用单个圆柱体）
    wheat_left = doc.addObject("Part::Cylinder", "左麦穗")
    wheat_left.Radius = 4.0
    wheat_left.Height = 30.0
    wheat_left.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-star_outer_radius - border_width - 8, -15, 0),
        FreeCAD.Rotation(0, 0, 15)
    )
    
    # 右侧麦穗
    wheat_right = doc.addObject("Part::Cylinder", "右麦穗")
    wheat_right.Radius = 4.0
    wheat_right.Height = 30.0
    wheat_right.Placement = FreeCAD.Placement(
        FreeCAD.Vector(star_outer_radius + border_width + 8, -15, 0),
        FreeCAD.Rotation(0, 0, -15)
    )
    
    print("麦穗装饰创建完成")
    
    # ========== 创建挂环（简化版） ==========
    # 挂环
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
    
    # 合并挂环
    medal_with_ring1 = doc.addObject("Part::Fuse", "勋章含挂环1")
    medal_with_ring1.Base = medal_with_wheat2
    medal_with_ring1.Tool = hanging_ring
    
    final_medal = doc.addObject("Part::Fuse", "共和国勋章_简化版")
    final_medal.Base = medal_with_ring1
    final_medal.Tool = ribbon_ring
    
    print("所有部件合并完成")
    
    # 重新计算
    doc.recompute()
    print("模型计算完成")
    
    # 导出文件
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    stl_path = os.path.join(output_dir, "medal_of_republic_simple.stl")
    Part.export([final_medal], stl_path)
    print(f"已导出STL：{stl_path}")
    
    print("=" * 60)
    print("共和国勋章（简化版）模型创建完成！")
    print("=" * 60)
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
