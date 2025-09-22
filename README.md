# 小红书封面生成器（Windows 版）

一个用于快速生成小红书封面图的轻量工具。内置 4 套主题与 4 种模板，支持自动/手动换行、行内 Emoji 混排渲染、随机几何装饰与右下角 Emoji 装饰，开箱即用。

## 功能特点
- 配色主题：青提甜瓜 / 博朗经典 / 日落黄昏 / 深海蓝调
- 设计模板：大字标题 / 简约风格 / 渐变背景 / 分层布局（不使用“几何装饰”模板）
- 文本智能：8 字自动换行、支持手动换行 \n、自适应字体大小与行距
- Emoji 支持：

## 安装与环境
- Windows 10/11（已内置微软雅黑、Segoe UI Emoji 字体）
- Python 3.8+
- 依赖：Pillow

安装依赖：
```bash
pip install pillow
```

## 快速开始
### 交互式模式
```bash
python generate.py
# 按提示输入多行文字（空行结束），自动生成封面
```

### 命令行模式
基本用法：
```bash
python generate.py "美食探店攻略"
```
指定输出文件名：
```bash
python generate.py "穿搭分享" -o "我的封面.png"
```
指定主题与模板：
```bash
python generate.py "护肤心得" -t "青提甜瓜" -m "大字标题"
```
手动换行（\n）：
```bash
python generate.py "窗纱脏了不用拆\n如何快速清洁" -t "深海蓝调" -m "大字标题" -o "窗纱不用拆快速清洁封面.png"
```
 Emoji 示例：
```bash
python generate.py "花瓶清洁小妙招\n瓶口细长\n怎么把里面的水垢刷干净🎨" -t "深海蓝调" -m "大字标题" -o "花瓶清洁-emoji封面.png"
```
查看可用项：
```bash
python generate.py --list-themes
python generate.py --list-templates
```

## 主题与模板
- 主题（4）：
  - 青提甜瓜：清新自然，治愈系
  - 博朗经典：温暖现代，高对比度
  - 日落黄昏：温暖浪漫，高级感
  - 深海蓝调：沉稳专业，商务感
- 模板（4）：
  - 大字标题：突出主题的大字设计
  - 简约风格：极简排版，带装饰线条
  - 渐变背景：多段渐变背景 + 文本
  - 分层布局：上色块 + 全宽白底文字区（适合短句）

## 参数说明
```text
python generate.py <text> [-o OUTPUT] [-t THEME] [-m TEMPLATE] [--list-themes] [--list-templates]
```
- text：封面文字（支持多行与 \n）
- -o/--output：输出文件名（可选）
- -t/--theme：主题名称（可选）
- -m/--template：模板名称（可选）
- --list-themes：列出主题
- --list-templates：列出模板

## 文本与 Emoji 处理
- 自动换行：每行默认 8 个字符（可在 `generate.py` 的 `_wrap_text` 中调整 `max_chars`）
- 手动换行：在命令行文本中使用 `\n`，程序会转换为实际换行
- 行内 Emoji：混排渲染，Windows 使用 `C:/Windows/Fonts/seguiemj.ttf`；不支持彩色嵌入的环境将回退为单色
- 右下角 Emoji 装饰：在 `_add_emoji` 中可调整 `emoji_size`、`x`、`y`

## 常见问题（FAQ）
- 终端里 Emoji 显示为 `?` 或方框：这是终端编码/字体显示问题，不影响生成图片；图片内会正常显示
- 指定了不存在的主题/模板：会自动随机选择一个可用项
- 字体找不到：程序会回退到 Arial 或默认字体；如需更好的中文效果，建议保留微软雅黑字体

## 目录结构
```
├── README.md
├── generate.py              # 主程序（命令行与交互式）

```

—— 欢迎在 GitHub 上提交 Issue/PR 与建议！