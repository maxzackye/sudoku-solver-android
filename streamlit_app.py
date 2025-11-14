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

# 默认数独题目
default_puzzle = [
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

# 应用标题
st.title("🔢 数独求解器")

# 应用说明
st.markdown("""
这是一个交互式数独求解器。您可以：
- 在网格中输入数字（1-9）
- 点击"求解数独"按钮获得解答
- 点击"清除"清空整个网格
- 点击"加载示例"加载默认题目
""")

# 初始化会话状态
if 'puzzle' not in st.session_state:
    st.session_state.puzzle = copy.deepcopy(default_puzzle)

# 创建网格输入
st.subheader("数独网格")
cols = st.columns(9)

# 创建输入网格
new_puzzle = []
for i in range(9):
    row = []
    for j in range(9):
        with cols[j]:
            # 添加边框样式
            cell_style = ""
            if i % 3 == 2 and i != 8:
                cell_style += "border-bottom: 2px solid black; "
            if j % 3 == 2 and j != 8:
                cell_style += "border-right: 2px solid black; "
            
            value = st.number_input(
                f"({i+1},{j+1})", 
                min_value=0, 
                max_value=9, 
                value=st.session_state.puzzle[i][j],
                key=f"cell_{i}_{j}",
                label_visibility="collapsed",
                format="%d"
            )
            row.append(value)
    new_puzzle.append(row)

# 更新会话状态
st.session_state.puzzle = new_puzzle

# 添加按钮
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("求解数独", use_container_width=True):
        # 复制数独题目以保留原始题目
        solution = copy.deepcopy(st.session_state.puzzle)
        
        # 求解数独
        solver = SudokuSolver()
        if solver.solve_sudoku(solution):
            st.session_state.puzzle = solution
            st.success("数独已解决！")
        else:
            st.error("该数独无解")

with col2:
    if st.button("清除", use_container_width=True):
        # 清空网格
        st.session_state.puzzle = [[0 for _ in range(9)] for _ in range(9)]
        st.success("网格已清空")

with col3:
    if st.button("加载示例", use_container_width=True):
        # 加载示例题目
        st.session_state.puzzle = copy.deepcopy(default_puzzle)
        st.success("已加载示例题目")

# 显示解决方案说明
st.info("💡 **使用说明**：在上方网格中输入数独题目（空格用0表示），然后点击'求解数独'按钮。")

# 添加关于信息
st.markdown("---")
st.markdown("_created with ❤️ using Streamlit_")