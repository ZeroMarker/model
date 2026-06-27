# -*- coding: utf-8 -*-
"""
铁十字勋章 (Iron Cross) - FreeCAD Python脚本
经典普鲁士/德国军事勋章复刻
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
    doc = FreeCAD.newDocument("IronCross")
    print("文档创建成功")
    
    # ========== 参数定义 ==========
    outer_size = 50.0       # 十字外臂长
    arm_width_outer = 16.0  # 臂宽（外端）
    arm_width_inner = 20.0  # 臂宽（中心）
    thickness = 3.0         # 勋章厚度
    border_width = 2.0      # 边框宽度
    border_height = 1.0     # 边框凸起高度
    center_size = 14.0      # 中心区域大小
    
    print("参数定义完成")
    
    # ========== 创建十字主体 ==========
    # 水平臂
    h_arm = doc.addObject("Part::Box", "水平臂")
    h_arm.Length = outer_size * 2
    h_arm.Width = arm_width_outer
    h_arm.Height = thickness
    h_arm.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-outer_size, -arm_width_outer/2, 0),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    # 垂直臂
    v_arm = doc.addObject("Part::Box", "垂直臂")
    v_arm.Length = arm_width_outer
    v_arm.Width = outer_size * 2
    v_arm.Height = thickness
    v_arm.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-arm_width_outer/2, -outer_size, 0),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    # 中心方块
    center = doc.addObject("Part::Box", "中心")
    center.Length = arm_width_inner
    center.Width = arm_width_inner
    center.Height = thickness
    center.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-arm_width_inner/2, -arm_width_inner/2, 0),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    print("基础形状创建完成")
    
    # 合并十字主体
    cross = doc.addObject("Part::Fuse", "十字主体")
    cross.Base = h_arm
    cross.Tool = v_arm
    
    cross2 = doc.addObject("Part::Fuse", "十字完整")
    cross2.Base = cross
    cross2.Tool = center
    
    print("十字主体合并完成")
    
    # ========== 创建边框 ==========
    border_h = doc.addObject("Part::Box", "边框水平")
    border_h.Length = outer_size * 2
    border_h.Width = arm_width_outer + border_width * 2
    border_h.Height = thickness + border_height
    border_h.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-outer_size, -(arm_width_outer + border_width * 2)/2, 0),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    border_v = doc.addObject("Part::Box", "边框垂直")
    border_v.Length = arm_width_outer + border_width * 2
    border_v.Width = outer_size * 2
    border_v.Height = thickness + border_height
    border_v.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-(arm_width_outer + border_width * 2)/2, -outer_size, 0),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    border_c = doc.addObject("Part::Box", "边框中心")
    border_c.Length = arm_width_inner + border_width * 2
    border_c.Width = arm_width_inner + border_width * 2
    border_c.Height = thickness + border_height
    border_c.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-(arm_width_inner + border_width * 2)/2, -(arm_width_inner + border_width * 2)/2, 0),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    print("边框创建完成")
    
    # 合并边框
    border1 = doc.addObject("Part::Fuse", "边框合并1")
    border1.Base = border_h
    border1.Tool = border_v
    
    border2 = doc.addObject("Part::Fuse", "边框完整")
    border2.Base = border1
    border2.Tool = border_c
    
    # 最终合并
    medal = doc.addObject("Part::Fuse", "铁十字勋章")
    medal.Base = cross2
    medal.Tool = border2
    
    print("边框合并完成")
    
    # ========== 添加中心装饰 ==========
    center_ring = doc.addObject("Part::Cylinder", "中心圆环外")
    center_ring.Radius = center_size / 2
    center_ring.Height = border_height * 0.5
    
    center_ring_inner = doc.addObject("Part::Cylinder", "中心圆环内")
    center_ring_inner.Radius = center_size / 2 - 2
    center_ring_inner.Height = border_height * 0.5
    
    ring = doc.addObject("Part::Cut", "中心圆环")
    ring.Base = center_ring
    ring.Tool = center_ring_inner
    
    # 最终勋章
    final_medal = doc.addObject("Part::Fuse", "最终勋章")
    final_medal.Base = medal
    final_medal.Tool = ring
    
    print("中心装饰完成")
    
    # 重新计算
    doc.recompute()
    print("模型计算完成")
    
    # 导出文件
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    step_path = os.path.join(output_dir, "iron_cross.step")
    Part.export([final_medal], step_path)
    print(f"已导出STEP：{step_path}")
    
    stl_path = os.path.join(output_dir, "iron_cross.stl")
    Part.export([final_medal], stl_path)
    print(f"已导出STL：{stl_path}")
    
    print("=" * 50)
    print("铁十字勋章模型创建完成！")
    print("=" * 50)
    print(f"\n模型参数：")
    print(f"- 外臂长度：{outer_size*2}mm")
    print(f"- 臂宽：{arm_width_outer}mm（外端）/ {arm_width_inner}mm（中心）")
    print(f"- 厚度：{thickness}mm")
    print(f"- 边框宽度：{border_width}mm")
    print(f"- 边框凸起：{border_height}mm")
    
except Exception as e:
    print(f"错误：{e}")
    import traceback
    traceback.print_exc()
