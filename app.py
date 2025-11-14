import os
from flask import Flask, request, render_template, jsonify
import cv2
import numpy as np
import copy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大16MB

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class SudokuSolver:
    @staticmethod
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

    @staticmethod
    def solve_sudoku(board):
        """使用回溯算法解决数独"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if SudokuSolver.is_valid(board, i, j, num):
                            board[i][j] = num
                            if SudokuSolver.solve_sudoku(board):
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
    return sample_sudoku

@app.route('/')
def index():
    """主页路由"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """处理文件上传"""
    # 检查是否有文件被上传
    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file:
        # 保存上传的文件
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # 从图像中提取数独
            original_sudoku = extract_sudoku_from_image(file_path)
            
            # 创建要解决的数独副本
            solved_sudoku = copy.deepcopy(original_sudoku)
            
            # 解决数独
            solver = SudokuSolver()
            if solver.solve_sudoku(solved_sudoku):
                # 返回JSON响应
                return jsonify({
                    'original': original_sudoku,
                    'solved': solved_sudoku,
                    'message': '数独已成功求解'
                })
            else:
                return jsonify({
                    'original': original_sudoku,
                    'solved': [],
                    'message': '该数独无解'
                })
        except Exception as e:
            return jsonify({'error': f'处理图像时出错: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)