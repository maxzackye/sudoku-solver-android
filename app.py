import os
from flask import Flask, request, render_template, jsonify
import cv2
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def generate_sudoku():
    """生成示例数独题目（当前实现为随机生成）"""
    # 当前实现为随机生成示例题目，后续可以替换为实际的图像识别逻辑
    sudoku = [[0 for _ in range(9)] for _ in range(9)]
    # 添加一些预设数字作为示例
    sudoku[0][0] = 5
    sudoku[0][1] = 3
    sudoku[0][4] = 7
    sudoku[1][0] = 6
    sudoku[1][3] = 1
    sudoku[1][4] = 9
    sudoku[1][5] = 5
    sudoku[2][1] = 9
    sudoku[2][2] = 8
    sudoku[2][7] = 6
    sudoku[3][0] = 8
    sudoku[3][4] = 6
    sudoku[3][8] = 3
    sudoku[4][0] = 4
    sudoku[4][3] = 8
    sudoku[4][5] = 3
    sudoku[4][8] = 1
    sudoku[5][0] = 7
    sudoku[5][4] = 2
    sudoku[5][8] = 6
    sudoku[6][1] = 6
    sudoku[6][6] = 2
    sudoku[6][7] = 8
    sudoku[7][3] = 4
    sudoku[7][4] = 1
    sudoku[7][5] = 9
    sudoku[7][8] = 5
    sudoku[8][4] = 8
    sudoku[8][7] = 7
    sudoku[8][8] = 9
    return sudoku

def load_sample_sudoku():
    """加载示例数独数据"""
    try:
        import json
        with open('data/sample_sudoku.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # 如果找不到样本文件，则生成一个默认的数独
        return generate_sudoku()

def is_valid(board, row, col, num):
    """检查在给定位置放置数字是否有效"""
    # 检查行
    for i in range(9):
        if board[row][i] == num:
            return False
    
    # 检查列
    for i in range(9):
        if board[i][col] == num:
            return False
    
    # 检查3x3子网格
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    
    return True

def solve_sudoku(board):
    """使用回溯算法解决数独"""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku(board):
                            return True
                        board[i][j] = 0
                return False
    return True

def extract_sudoku_from_image(image_path):
    """
    从图像中提取数独题目
    当前为占位实现，返回示例数独
    """
    # 这里应该实现图像处理和数字识别逻辑
    # 目前返回示例数独作为演示
    return load_sample_sudoku()

@app.route('/')
def index():
    """主页路由"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """处理文件上传"""
    # 检查是否有文件被上传
    if 'file' not in request.files:
        # 如果没有文件上传，使用示例数独
        original_sudoku = load_sample_sudoku()
    else:
        file = request.files['file']
        if file.filename == '':
            # 如果文件名为空，使用示例数独
            original_sudoku = load_sample_sudoku()
        else:
            # 保存上传的文件
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # 从图像中提取数独（当前为模拟实现）
            original_sudoku = extract_sudoku_from_image(file_path)
    
    # 创建要解决的数独副本
    solved_sudoku = [row[:] for row in original_sudoku]
    
    # 解决数独
    solve_sudoku(solved_sudoku)
    
    # 返回JSON响应
    return jsonify({
        'original': original_sudoku,
        'solved': solved_sudoku
    })

if __name__ == '__main__':
    app.run(debug=False)
