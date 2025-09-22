小红书封面图生成工具，专为内容创作者打造。可搭配Trae、Cursor等平台批量生成。

支持多种主题配色、模板样式，智能文本排版，完美支持 Emoji 混排渲染。

✨ 特性亮点

🎯 开箱即用：无需设计经验，一键生成专业封面

🌈 4套精美主题：青提甜瓜、博朗经典、日落黄昏、深海蓝调

📐 4种设计模板：大字标题、简约风格、渐变背景、分层布局

🤖 智能排版：自动换行、字体自适应、行间距优化

😊 Emoji 支持：完美支持 Emoji 混排渲染和装饰

⚡ 高效便捷：支持命令行批量生成和交互式创作


🚀 快速开始

#安装依赖

pip install pillow

#交互式生成

python generate.py

按提示输入多行文字（空行结束），自动生成封面

#命令行生成

python generate.py "美食探店攻略"

#指定主题和模板

python generate.py "穿搭分享" -t "青提甜瓜" -m "大字标题"

#完整示例

python generate.py "花瓶清洁小妙招\n瓶口细长\n怎么把里面的水垢刷干净🎨" -t "深海蓝调" -m "大字标题" -o "花瓶清洁-emoji封面.png"

#参数说明

python generate.py [-o OUTPUT] [-t THEME] [-m TEMPLATE] [--list-themes] [--list-templates]

📱 适用场景
小红书笔记封面制作

社交媒体内容配图

个人博客头图设计

营销素材快速产出

搭配自动发帖MCP

🎨 效果预览

生成的封面图片尺寸为 1080×1440（3:4 比例），完美适配小红书平台要求，支持高分辨率输出。

<img width="480" height="930" alt="image" src="https://github.com/user-attachments/assets/273007a7-7157-452f-af8d-4f4b384fdc7f" />


🔥 搭配Trae、Cursor等平台生成
<img width="900" height="500" alt="image" src="https://github.com/user-attachments/assets/673db4c2-bf6b-4305-80f9-f68aafbd1c0d" />



让创作更简单，让封面更出彩！⭐如果这个项目对您有帮助，请给个 Star 支持一下！






