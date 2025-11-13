#!/usr/bin/env python3
"""
生成数独示例数据的脚本
"""

import os
import json

def generate_sample_sudoku_data():
    """
    生成示例数独数据
    """
    # 示例数独题目（0表示空白格子）
    sample_sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    # 保存为JSON文件
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    with open(os.path.join(data_dir, "sample_sudoku.json"), "w") as f:
        json.dump(sample_sudoku, f)
    
    print("示例数独数据已生成并保存到 data/sample_sudoku.json")

if __name__ == "__main__":
    generate_sample_sudoku_data()