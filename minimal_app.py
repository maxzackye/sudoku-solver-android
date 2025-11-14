import streamlit as st
import copy

# 设置页面配置
st.set_page_config(
    page_title="数独求解器",
    page_icon="🔢",
    layout="centered"
)

# 数独求解器类
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

# 显示数独网格的函数
def display_sudoku_grid(grid_data, title):
    st.subheader(title)
    
    # 创建HTML表格来显示数独网格
    table_html = "<table style='border-collapse: collapse; margin: 10px auto;'>"
    
    for i in range(9):
        table_html += "<tr>"
        for j in range(9):
            # 添加边框样式
            border_style = "border: 1px solid #999; width: 40px; height: 40px; text-align: center; vertical-align: middle;"
            
            # 添加粗边框分隔3x3宫格
            if i % 3 == 0 and i != 0:
                border_style += " border-top: 3px solid #000;"
            if j % 3 == 0 and j != 0:
                border_style += " border-left: 3px solid #000;"
            if i == 8:
                border_style += " border-bottom: 3px solid #000;"
            if j == 8:
                border_style += " border-right: 3px solid #000;"
            
            # 添加背景色
            bg_color = ""
            if grid_data[i][j] != 0:
                bg_color = "background-color: #e0e0e0;"  # 原始数字背景色
            
            cell_value = grid_data[i][j] if grid_data[i][j] != 0 else ""
            table_html += f"<td style='{border_style} {bg_color} font-weight: bold; font-size: 20px;'>{cell_value}</td>"
        table_html += "</tr>"
    
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)

# 应用标题
st.title("🔢 数独求解器")

# 应用说明
st.markdown("""
这是一个简单的数独求解器，可以直接输入数独题目并求解。
""")

# 创建示例数独
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

# 显示示例数独
st.subheader("示例数独")
display_sudoku_grid(sample_sudoku, "示例题目")

# 求解示例数独
if st.button("求解示例数独"):
    with st.spinner("正在求解数独..."):
        # 创建要解决的数独副本
        solved_sudoku = copy.deepcopy(sample_sudoku)
        
        # 解决数独
        solver = SudokuSolver()
        if solver.solve_sudoku(solved_sudoku):
            st.success("数独已成功求解！")
            display_sudoku_grid(solved_sudoku, "求解结果")
        else:
            st.error("该数独无解")

# 技术说明
st.markdown("---")
st.markdown("### 技术说明")
st.markdown("""
- 使用回溯算法求解数独
- 使用Streamlit构建用户界面
""")

# 添加关于信息
st.markdown("_created with ❤️ using Streamlit_")