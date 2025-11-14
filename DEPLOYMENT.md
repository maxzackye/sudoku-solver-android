# 数独求解器 Web 应用部署指南

本文档介绍了如何将数独求解器部署为Web应用程序。

## 项目结构

```
数独/
├── web_app.py          # Flask Web 应用主文件
├── requirements.txt    # 项目依赖
├── templates/
│   └── sudoku.html     # Web 界面模板
├── data/
│   └── sample_sudoku.json  # 示例数据
├── README.md
└── DEPLOYMENT.md       # 本部署指南
```

## 本地运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python web_app.py
```

应用将在 `http://127.0.0.1:5000` 启动。

## 部署到云平台

### 部署到 Heroku

1. 安装 [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

2. 登录 Heroku：
   ```bash
   heroku login
   ```

3. 在项目根目录创建 `Procfile` 文件：
   ```
   web: python web_app.py
   ```

4. 创建 `runtime.txt` 文件指定 Python 版本：
   ```
   python-3.8.10
   ```

5. 初始化 Git 仓库（如果尚未初始化）：
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

6. 创建 Heroku 应用：
   ```bash
   heroku create your-app-name
   ```

7. 部署应用：
   ```bash
   git push heroku main
   ```

8. 打开应用：
   ```bash
   heroku open
   ```

### 部署到 PythonAnywhere

1. 注册 [PythonAnywhere](https://www.pythonanywhere.com/) 账户

2. 上传项目文件到 PythonAnywhere

3. 在 PythonAnywhere 控制台中安装依赖：
   ```bash
   pip install --user -r requirements.txt
   ```

4. 配置 Web 应用：
   - 进入 "Web" 选项卡
   - 创建新 Web 应用
   - 选择 "Manual configuration"
   - 设置代码路径指向项目目录
   - 设置 WSGI 配置文件，示例如下：
     ```python
     import sys
     path = '/home/yourusername/sudoku/'
     if path not in sys.path:
         sys.path.append(path)
     
     from web_app import app as application
     ```

5. 重新加载应用

### 部署到 VPS (如 Ubuntu)

1. 确保服务器上安装了 Python 和 pip

2. 克隆或上传项目文件到服务器

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 安装并配置 Nginx：
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

5. 安装并配置 Gunicorn：
   ```bash
   pip install gunicorn
   ```

6. 创建 systemd 服务文件 `/etc/systemd/system/sudoku.service`：
   ```ini
   [Unit]
   Description=Gunicorn instance to serve sudoku
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/sudoku
   ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind unix:sudoku.sock -m 007 web_app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. 启动并启用服务：
   ```bash
   sudo systemctl start sudoku
   sudo systemctl enable sudoku
   ```

8. 配置 Nginx，创建 `/etc/nginx/sites-available/sudoku`：
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://unix:/path/to/sudoku/sudoku.sock;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

9. 启用 Nginx 配置：
   ```bash
   sudo ln -s /etc/nginx/sites-available/sudoku /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## 使用说明

1. 访问部署的网站 URL
2. 点击数独网格中的空格可以输入数字（1-9）
3. 点击已有数字的格子可以清除该格子
4. 点击"求解数独"按钮自动填充剩余的空格
5. 点击"清除"清空整个网格
6. 点击"示例"加载示例数独题目

## 注意事项

1. Web 版本使用 Flask 框架，与 Android 版本使用不同的技术栈
2. Web 版本支持在任何现代浏览器中运行
3. 应用不依赖数据库，所有数据都存储在内存中
4. 如果需要持久化存储，可以考虑添加数据库支持