import streamlit as st
try:
    import cv2
except ImportError:
    cv2 = None
import numpy as np
from PIL import Image
import copy
import io

# 设置页面配置
st.set_page_config(
    page_title="数独图像识别与求解",
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

# 模拟从图像中提取数独的函数
def extract_sudoku_from_image(image):
    """
    从图像中提取数独题目
    当前为占位实现，返回示例数独
    在实际应用中，这里应该实现图像处理和数字识别逻辑
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
st.title("🔢 数独图像识别与求解")

# 检查OpenCV是否可用
if cv2 is None:
    st.warning("OpenCV库不可用，图像处理功能受限。")

# 应用说明
st.markdown("""
这是一个完整的数独求解系统，包含以下功能：
- 上传包含数独题目的图片
- 从图片中识别数独题目（当前为模拟实现）
- 自动求解数独
- 显示原始题目和求解结果
""")

# 上传图片
st.subheader("上传数独图片")
uploaded_file = st.file_uploader("选择一张包含数独的图片", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 显示上传的图片
    image = Image.open(uploaded_file)
    st.image(image, caption="上传的数独图片", use_column_width=True)
    
    # 处理图片
    with st.spinner("正在处理图片并识别数独..."):
        try:
            # 将PIL图像转换为OpenCV格式（如果OpenCV可用）
            if cv2 is not None:
                opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            else:
                # 如果OpenCV不可用，则直接使用图像
                opencv_image = np.array(image)
            
            # 从图像中提取数独（当前为模拟实现）
            original_sudoku = extract_sudoku_from_image(opencv_image)
            
            # 创建要解决的数独副本
            solved_sudoku = copy.deepcopy(original_sudoku)
            
            # 解决数独
            solver = SudokuSolver()
            if solver.solve_sudoku(solved_sudoku):
                st.success("数独已成功求解！")
                
                # 显示原始题目和求解结果
                col1, col2 = st.columns(2)
                
                with col1:
                    display_sudoku_grid(original_sudoku, "原始题目")
                
                with col2:
                    display_sudoku_grid(solved_sudoku, "求解结果")
            else:
                st.error("该数独无解")
                
                # 仍显示原始题目
                display_sudoku_grid(original_sudoku, "原始题目")
        except Exception as e:
            st.error(f"处理图片时出现错误: {str(e)}")
else:
    # 显示示例和说明
    st.info("💡 请上传一张包含数独题目的图片开始使用")
    
    # 显示示例数独
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
    
    st.subheader("示例数独")
    display_sudoku_grid(sample_sudoku, "示例题目")

# 技术说明
st.markdown("---")
st.markdown("### 技术说明")
st.markdown("""
- 使用OpenCV进行图像处理（如果可用）
- 使用回溯算法求解数独
- 使用Streamlit构建用户界面
- 当前图像识别为模拟实现，实际应用中需要实现完整的OCR功能
""")

# 添加关于信息
st.markdown("_created with ❤️ using Streamlit_")