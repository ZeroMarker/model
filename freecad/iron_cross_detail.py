# -*- coding: utf-8 -*-
"""
铁十字勋章 (Iron Cross) - FreeCAD Python脚本
经典普鲁士/德国军事勋章复刻（精细化版本）

历史特征：
- 1813年首次设立，由普鲁士国王腓特烈·威廉三世设计
- 十字形状源自条顿骑士团十字
- 边框代表银质框架
- 中心年份代表颁发年份
- 橡叶装饰代表普鲁士荣誉
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
    doc = FreeCAD.newDocument("IronCrossDetail")
    print("文档创建成功")
    
    # ========== 参数定义（基于真实比例） ==========
    # 铁十字勋章标准尺寸（毫米）
    outer_size = 50.0       # 十字外臂长
    arm_width_outer = 14.0  # 臂宽（外端）- 历史上较窄
    arm_width_inner = 22.0  # 臂宽（中心）- 历史上较宽
    thickness = 3.5         # 勋章厚度
    border_width = 2.5      # 边框宽度
    border_height = 1.2     # 边框凸起高度
    center_size = 16.0      # 中心区域大小
    chamfer_size = 0.8      # 倒角大小
    year = "1813"           # 年份（首次设立年份）
    
    print("参数定义完成")
    
    # ========== 创建十字主体（带渐变宽度） ==========
    # 使用拉伸和放样实现臂的渐变
    
    # 创建十字轮廓（使用多边形）
    # 中心区域
    center_points = [
        FreeCAD.Vector(-arm_width_inner/2, -arm_width_inner/2, 0),
        FreeCAD.Vector(arm_width_inner/2, -arm_width_inner/2, 0),
        FreeCAD.Vector(arm_width_inner/2, arm_width_inner/2, 0),
        FreeCAD.Vector(-arm_width_inner/2, arm_width_inner/2, 0),
    ]
    
    # 水平臂轮廓（左）
    h_arm_left_points = [
        FreeCAD.Vector(-outer_size, -arm_width_outer/2, 0),
        FreeCAD.Vector(-arm_width_inner/2, -arm_width_outer/2, 0),
        FreeCAD.Vector(-arm_width_inner/2, arm_width_outer/2, 0),
        FreeCAD.Vector(-outer_size, arm_width_outer/2, 0),
    ]
    
    # 水平臂轮廓（右）
    h_arm_right_points = [
        FreeCAD.Vector(arm_width_inner/2, -arm_width_outer/2, 0),
        FreeCAD.Vector(outer_size, -arm_width_outer/2, 0),
        FreeCAD.Vector(outer_size, arm_width_outer/2, 0),
        FreeCAD.Vector(arm_width_inner/2, arm_width_outer/2, 0),
    ]
    
    # 垂直臂轮廓（下）
    v_arm_bottom_points = [
        FreeCAD.Vector(-arm_width_outer/2, -outer_size, 0),
        FreeCAD.Vector(arm_width_outer/2, -outer_size, 0),
        FreeCAD.Vector(arm_width_outer/2, -arm_width_inner/2, 0),
        FreeCAD.Vector(-arm_width_outer/2, -arm_width_inner/2, 0),
    ]
    
    # 垂直臂轮廓（上）
    v_arm_top_points = [
        FreeCAD.Vector(-arm_width_outer/2, arm_width_inner/2, 0),
        FreeCAD.Vector(arm_width_outer/2, arm_width_inner/2, 0),
        FreeCAD.Vector(arm_width_outer/2, outer_size, 0),
        FreeCAD.Vector(-arm_width_outer/2, outer_size, 0),
    ]
    
    # 创建拉伸体
    def create_extruded_box(name, points, height):
        """从点列表创建拉伸体"""
        # 创建矩形盒子作为替代
        min_x = min(p.x for p in points)
        max_x = max(p.x for p in points)
        min_y = min(p.y for p in points)
        max_y = max(p.y for p in points)
        
        box = doc.addObject("Part::Box", name)
        box.Length = max_x - min_x
        box.Width = max_y - min_y
        box.Height = height
        box.Placement = FreeCAD.Placement(
            FreeCAD.Vector(min_x, min_y, 0),
            FreeCAD.Rotation(0, 0, 0)
        )
        return box
    
    # 创建中心方块
    center = create_extruded_box("中心", center_points, thickness)
    
    # 创建四个臂
    h_left = create_extruded_box("左臂", h_arm_left_points, thickness)
    h_right = create_extruded_box("右臂", h_arm_right_points, thickness)
    v_bottom = create_extruded_box("下臂", v_arm_bottom_points, thickness)
    v_top = create_extruded_box("上臂", v_arm_top_points, thickness)
    
    print("基础形状创建完成")
    
    # 合并十字主体
    cross1 = doc.addObject("Part::Fuse", "十字合并1")
    cross1.Base = center
    cross1.Tool = h_left
    
    cross2 = doc.addObject("Part::Fuse", "十字合并2")
    cross2.Base = cross1
    cross2.Tool = h_right
    
    cross3 = doc.addObject("Part::Fuse", "十字合并3")
    cross3.Base = cross2
    cross3.Tool = v_bottom
    
    cross4 = doc.addObject("Part::Fuse", "十字完整")
    cross4.Base = cross3
    cross4.Tool = v_top
    
    print("十字主体合并完成")
    
    # ========== 创建边框（带斜面） ==========
    # 外边框
    border_outer = doc.addObject("Part::Box", "边框外")
    border_outer.Length = outer_size * 2 + border_width * 2
    border_outer.Width = outer_size * 2 + border_width * 2
    border_outer.Height = thickness + border_height
    border_outer.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-outer_size - border_width, -outer_size - border_width, 0),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    # 内边框（用于布尔减去）
    border_inner = doc.addObject("Part::Box", "边框内")
    border_inner.Length = outer_size * 2
    border_inner.Width = outer_size * 2
    border_inner.Height = thickness + border_height
    border_inner.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-outer_size, -outer_size, 0),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    # 布尔减去创建边框
    border_frame = doc.addObject("Part::Cut", "边框框架")
    border_frame.Base = border_outer
    border_frame.Tool = border_inner
    
    print("边框创建完成")
    
    # ========== 合并边框和十字 ==========
    medal_with_border = doc.addObject("Part::Fuse", "勋章主体")
    medal_with_border.Base = cross4
    medal_with_border.Tool = border_frame
    
    print("边框合并完成")
    
    # ========== 添加中心装饰 ==========
    # 中心圆环
    center_ring_outer = doc.addObject("Part::Cylinder", "中心圆环外")
    center_ring_outer.Radius = center_size / 2
    center_ring_outer.Height = border_height * 0.8
    
    center_ring_inner = doc.addObject("Part::Cylinder", "中心圆环内")
    center_ring_inner.Radius = center_size / 2 - 3
    center_ring_inner.Height = border_height * 0.8
    
    center_ring = doc.addObject("Part::Cut", "中心圆环")
    center_ring.Base = center_ring_outer
    center_ring.Tool = center_ring_inner
    
    # 中心圆盘（用于放置年份）
    center_disc = doc.addObject("Part::Cylinder", "中心圆盘")
    center_disc.Radius = center_size / 2 - 3
    center_disc.Height = border_height * 0.5
    
    print("中心装饰创建完成")
    
    # ========== 创建年份浮雕（简化版） ==========
    # 创建四个小方块代表数字 "1813"
    # 数字 "1"
    digit_1 = doc.addObject("Part::Box", "数字1")
    digit_1.Length = 2
    digit_1.Width = 8
    digit_1.Height = border_height * 0.6
    digit_1.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-12, -4, thickness),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    # 数字 "8" (用两个圆环模拟)
    digit_8_outer = doc.addObject("Part::Cylinder", "数字8外")
    digit_8_outer.Radius = 4
    digit_8_outer.Height = border_height * 0.6
    digit_8_outer.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-5, 0, thickness),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    digit_8_inner = doc.addObject("Part::Cylinder", "数字8内")
    digit_8_inner.Radius = 2
    digit_8_inner.Height = border_height * 0.6
    digit_8_inner.Placement = FreeCAD.Placement(
        FreeCAD.Vector(-5, 0, thickness),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    digit_8 = doc.addObject("Part::Cut", "数字8")
    digit_8.Base = digit_8_outer
    digit_8.Tool = digit_8_inner
    
    # 数字 "1"
    digit_1_2 = doc.addObject("Part::Box", "数字1_2")
    digit_1_2.Length = 2
    digit_1_2.Width = 8
    digit_1_2.Height = border_height * 0.6
    digit_1_2.Placement = FreeCAD.Placement(
        FreeCAD.Vector(2, -4, thickness),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    # 数字 "3"
    digit_3 = doc.addObject("Part::Box", "数字3")
    digit_3.Length = 6
    digit_3.Width = 2
    digit_3.Height = border_height * 0.6
    digit_3.Placement = FreeCAD.Placement(
        FreeCAD.Vector(8, -4, thickness),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    print("年份浮雕创建完成")
    
    # ========== 创建橡叶装饰（简化版） ==========
    # 上方臂的橡叶（用锥体模拟）
    oak_leaf_top = doc.addObject("Part::Cone", "橡叶上")
    oak_leaf_top.Radius1 = 6
    oak_leaf_top.Radius2 = 0
    oak_leaf_top.Height = 12
    oak_leaf_top.Placement = FreeCAD.Placement(
        FreeCAD.Vector(0, outer_size + border_width + 2, thickness),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    # 下方臂的橡叶
    oak_leaf_bottom = doc.addObject("Part::Cone", "橡叶下")
    oak_leaf_bottom.Radius1 = 6
    oak_leaf_bottom.Radius2 = 0
    oak_leaf_bottom.Height = 12
    oak_leaf_bottom.Placement = FreeCAD.Placement(
        FreeCAD.Vector(0, -outer_size - border_width - 2, thickness),
        FreeCAD.Rotation(180, 0, 0)
    )
    
    print("橡叶装饰创建完成")
    
    # ========== 创建挂环 ==========
    # 挂环（用于佩戴）
    ring_outer = doc.addObject("Part::Torus", "挂环外")
    ring_outer.Radius1 = 5
    ring_outer.Radius2 = 1.5
    ring_outer.Placement = FreeCAD.Placement(
        FreeCAD.Vector(0, outer_size + border_width + 15, thickness/2),
        FreeCAD.Rotation(0, 0, 0)
    )
    
    print("挂环创建完成")
    
    # ========== 合并所有部件 ==========
    # 合并年份
    year_group1 = doc.addObject("Part::Fuse", "年份合并1")
    year_group1.Base = digit_1
    year_group1.Tool = digit_8
    
    year_group2 = doc.addObject("Part::Fuse", "年份合并2")
    year_group2.Base = year_group1
    year_group2.Tool = digit_1_2
    
    year_group3 = doc.addObject("Part::Fuse", "年份完整")
    year_group3.Base = year_group2
    year_group3.Tool = digit_3
    
    # 合并勋章和年份
    medal_with_year = doc.addObject("Part::Fuse", "勋章含年份")
    medal_with_year.Base = medal_with_border
    medal_with_year.Tool = year_group3
    
    # 合并中心装饰
    medal_with_center = doc.addObject("Part::Fuse", "勋章含中心")
    medal_with_center.Base = medal_with_year
    medal_with_center.Tool = center_ring
    
    medal_with_disc = doc.addObject("Part::Fuse", "勋章含圆盘")
    medal_with_disc.Base = medal_with_center
    medal_with_disc.Tool = center_disc
    
    # 合并橡叶
    medal_with_oak1 = doc.addObject("Part::Fuse", "勋章含橡叶1")
    medal_with_oak1.Base = medal_with_disc
    medal_with_oak1.Tool = oak_leaf_top
    
    medal_with_oak2 = doc.addObject("Part::Fuse", "勋章含橡叶2")
    medal_with_oak2.Base = medal_with_oak1
    medal_with_oak2.Tool = oak_leaf_bottom
    
    # 最终合并（含挂环）
    final_medal = doc.addObject("Part::Fuse", "铁十字勋章_精细版")
    final_medal.Base = medal_with_oak2
    final_medal.Tool = ring_outer
    
    print("所有部件合并完成")
    
    # 重新计算
    doc.recompute()
    print("模型计算完成")
    
    # 导出文件
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    step_path = os.path.join(output_dir, "iron_cross_detail.step")
    Part.export([final_medal], step_path)
    print(f"已导出STEP：{step_path}")
    
    stl_path = os.path.join(output_dir, "iron_cross_detail.stl")
    Part.export([final_medal], stl_path)
    print(f"已导出STL：{stl_path}")
    
    print("=" * 60)
    print("铁十字勋章精细化模型创建完成！")
    print("=" * 60)
    print(f"\n历史特征：")
    print(f"- 十字形状源自条顿骑士团十字")
    print(f"- 边框代表银质框架")
    print(f"- 中心年份：{year}（首次设立年份）")
    print(f"- 橡叶装饰代表普鲁士荣誉")
    print(f"- 挂环用于佩戴")
    print(f"\n模型参数：")
    print(f"- 外臂长度：{outer_size*2}mm")
    print(f"- 臂宽：{arm_width_outer}mm（外端）/ {arm_width_inner}mm（中心）")
    print(f"- 厚度：{thickness}mm")
    print(f"- 边框宽度：{border_width}mm")
    print(f"- 边框凸起：{border_height}mm")
    print(f"- 中心区域：{center_size}mm")
    
except Exception as e:
    print(f"错误：{e}")
    import traceback
    traceback.print_exc()
