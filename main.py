from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import copy

class SudokuGrid(GridLayout):
    def __init__(self, grid_data, editable=False, **kwargs):
        super(SudokuGrid, self).__init__(**kwargs)
        self.cols = 9
        self.rows = 9
        self.spacing = [1, 1]
        self.size_hint_y = None
        self.height = '360dp'
        self.width = '360dp'
        self.size_hint_x = None
        
        self.cells = []
        self.editable = editable
        
        # 创建数独网格
        for i in range(9):
            row = []
            for j in range(9):
                cell_value = grid_data[i][j] if grid_data[i][j] != 0 else ""
                text_input = TextInput(
                    text=str(cell_value),
                    multiline=False,
                    readonly=not editable,
                    font_size='20sp',
                    halign='center',
                    valign='middle'
                )
                # 添加粗边框分隔3x3宫格
                if i % 3 == 0:
                    text_input.padding = [0, 2, 0, 0]  # 上边框
                if j % 3 == 0:
                    text_input.padding = [2, 0, 0, 0]  # 左边框
                    
                self.add_widget(text_input)
                row.append(text_input)
            self.cells.append(row)

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

class SudokuApp(App):
    def build(self):
        self.title = "数独求解器"
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title_label = Label(
            text="数独求解器",
            size_hint_y=None,
            height='40dp',
            font_size='24sp'
        )
        
        # 默认数独题目
        self.default_puzzle = [
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
        
        # 显示初始数独网格
        self.puzzle_grid = SudokuGrid(self.default_puzzle, editable=True)
        
        # 按钮布局
        button_layout = BoxLayout(size_hint_y=None, height='50dp', spacing=10)
        
        # 求解按钮
        solve_button = Button(text="求解数独")
        solve_button.bind(on_press=self.solve_puzzle)
        
        # 清除按钮
        clear_button = Button(text="清除")
        clear_button.bind(on_press=self.clear_puzzle)
        
        # 重置按钮
        reset_button = Button(text="重置示例")
        reset_button.bind(on_press=self.reset_puzzle)
        
        button_layout.add_widget(solve_button)
        button_layout.add_widget(clear_button)
        button_layout.add_widget(reset_button)
        
        # 添加控件到主布局
        main_layout.add_widget(title_label)
        main_layout.add_widget(self.puzzle_grid)
        main_layout.add_widget(button_layout)
        
        return main_layout
    
    def solve_puzzle(self, instance):
        # 获取当前网格数据
        puzzle = []
        for i in range(9):
            row = []
            for j in range(9):
                cell_text = self.puzzle_grid.cells[i][j].text
                if cell_text.isdigit() and 1 <= int(cell_text) <= 9:
                    row.append(int(cell_text))
                else:
                    row.append(0)
            puzzle.append(row)
        
        # 复制数独题目以保留原始题目
        solution = copy.deepcopy(puzzle)
        
        # 求解数独
        solver = SudokuSolver()
        if solver.solve_sudoku(solution):
            # 显示解决方案
            for i in range(9):
                for j in range(9):
                    # 只更新空白单元格
                    if puzzle[i][j] == 0:
                        self.puzzle_grid.cells[i][j].text = str(solution[i][j])
                        # 更改背景色以标识解答的单元格
                        self.puzzle_grid.cells[i][j].background_color = (0.7, 1, 0.7, 1)  # 浅绿色
        else:
            # 无解提示
            popup = Popup(
                title='无解',
                content=Label(text='该数独无解'),
                size_hint=(None, None),
                size=('200dp', '100dp')
            )
            popup.open()
    
    def clear_puzzle(self, instance):
        # 清除所有单元格
        for i in range(9):
            for j in range(9):
                self.puzzle_grid.cells[i][j].text = ""
                self.puzzle_grid.cells[i][j].background_color = (1, 1, 1, 1)  # 白色
    
    def reset_puzzle(self, instance):
        # 重置为示例数独
        for i in range(9):
            for j in range(9):
                value = self.default_puzzle[i][j]
                self.puzzle_grid.cells[i][j].text = str(value) if value != 0 else ""
                self.puzzle_grid.cells[i][j].background_color = (1, 1, 1, 1)  # 白色

if __name__ == '__main__':
    SudokuApp().run()