# Streamlit 数独应用部署指南

这是一个简化版本的数独求解器，使用Streamlit构建，更容易部署和分享。

## 本地运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
streamlit run streamlit_app.py
```

应用将在 `http://localhost:8501` 启动。

## 部署到 Streamlit Community Cloud

Streamlit提供了免费的部署平台，无需复杂的配置：

### 1. 将代码推送到GitHub
确保您的代码已推送到GitHub仓库。

### 2. 访问 Streamlit Community Cloud
1. 访问 https://streamlit.io/cloud
2. 点击"Get started"或直接访问 https://share.streamlit.io/
3. 使用您的GitHub账户登录

### 3. 部署应用
1. 点击"New app"
2. 选择包含 `streamlit_app.py` 的GitHub仓库
3. 确保配置正确：
   - Branch: main
   - Main file: streamlit_app.py
4. 点击"Deploy!"

### 4. 访问应用
部署完成后，您将获得一个URL，可以通过该URL访问您的数独应用。

## 优势

使用Streamlit的优势：
- 无需复杂的WSGI配置
- 自动处理部署和托管
- 响应式设计，适配移动设备
- 免费且易于使用
- 不需要支付信息验证

## 使用说明

1. 在网格中输入数独题目（使用数字1-9，空格用0表示）
2. 点击"求解数独"按钮获得解答
3. 点击"清除"清空整个网格
4. 点击"加载示例"加载默认题目

这个简化版本保留了所有核心功能，但部署过程更加简单直接。