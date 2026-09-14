# ToDo 管理系统（Django）

要求：
- Python 3.8+
- 推荐虚拟环境

安装依赖：
pip install -r requirements.txt

初始化并运行：
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

访问：
http://127.0.0.1:8000/ 

功能：
- 新建/编辑/删除任务
- 筛选（状态/优先级/关键词）
- 分页（每页 8 条）
- 显示统计（总数/已完成/未完成）
- 导出当前筛选结果为 Excel（xlsx）
- 表单验证（标题必填、截止日期不能早于今天）

提交要求说明：
- 将此目录完整提交为源码。
- 运行截图：在浏览器打开后用系统截图工具截取页面并保存为 PNG/JPG。
- 设计说明 PPT：将 README 中的设计说明文本复制到 PPT 幻灯片中（后面提供了示例段落）。
