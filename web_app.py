from flask import Flask, render_template, request, jsonify
import copy
import os

# 创建Flask应用实例
app = Flask(__name__, template_folder='templates')

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

@app.route('/')
def index():
    try:
        return render_template('sudoku.html')
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        if not data or 'puzzle' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
            
        puzzle = data['puzzle']
        
        # 验证输入数据
        if not isinstance(puzzle, list) or len(puzzle) != 9:
            return jsonify({'error': 'Invalid puzzle format'}), 400
            
        # 复制数独题目以保留原始题目
        solution = copy.deepcopy(puzzle)
        
        # 求解数独
        solver = SudokuSolver()
        if solver.solve_sudoku(solution):
            return jsonify({'solution': solution, 'status': 'solved'})
        else:
            return jsonify({'solution': [], 'status': 'no_solution'})
    except Exception as e:
        return jsonify({'error': f'Error solving puzzle: {str(e)}'}), 500

# 仅在直接运行此脚本时启动应用
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port, debug=True)