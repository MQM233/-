from PIL import Image, ImageDraw, ImageFont
import random
import os
import sys
import argparse

# 设置控制台编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

class XiaohongshuCoverGenerator:
    def __init__(self):
        self.canvas_width = 1080
        self.canvas_height = 1440  # 3:4比例，高分辨率
        
        # 预设主题配色
        self.themes = {
            "青提甜瓜": {
                "bg_color": "#fbffe4",
                "main_color": "#000000",
                "highlight_color": "#98FB98",
                "accent_colors": ["#E8F5E8", "#90EE90", "#32CD32"],
                "description": "清新自然，治愈系"
            },
            "博朗经典": {
                "bg_color": "#F5F1EB",
                "main_color": "#000000",
                "highlight_color": "#8B4513",
                "accent_colors": ["#DEB887", "#D2B48C", "#BC8F8F"],
                "description": "温暖现代，高对比度"
            },
            "日落黄昏": {
                "bg_color": "#FFF8E1",
                "main_color": "#000000",
                "highlight_color": "#FF4500",
                "accent_colors": ["#FFE4B5", "#FFDAB9", "#F4A460"],
                "description": "温暖浪漫，高级感"
            },
            "深海蓝调": {
                "bg_color": "#F3F8FF",
                "main_color": "#000000",
                "highlight_color": "#4169E1",
                "accent_colors": ["#E0F6FF", "#87CEEB", "#87CEFA"],
                "description": "沉稳专业，商务感"
            }
        }
        
        # 预设模板样式
        self.templates = [
            "大字标题",
            "简约风格",
            "渐变背景",
            "分层布局"
        ]

    def _load_font(self, size):
        """加载字体"""
        try:
            return ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", size)
        except:
            try:
                return ImageFont.truetype("arial.ttf", size)
            except:
                return ImageFont.load_default()

    def _get_text_size(self, text, font):
        """获取文本尺寸"""
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    # 新增：加载 Emoji 字体与检测/绘制混排
    def _load_emoji_font(self, size):
        """加载Emoji字体（Windows: Segoe UI Emoji），失败则回退到主字体。"""
        try:
            return ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", size)
        except:
            return self._load_font(size)

    def _is_emoji(self, ch):
        """粗略判断字符是否为emoji（覆盖常见范围）。"""
        code = ord(ch)
        return (
            0x1F300 <= code <= 0x1FAFF or  # 大部分彩色表情与符号
            0x2600 <= code <= 0x27BF or    # 杂项符号/装饰
            0x1F1E6 <= code <= 0x1F1FF or  # 区域标识符（国旗）
            code in (0xFE0F, 0x200D)       # 变体选择符/ZWJ
        )

    def _draw_line_with_emoji(self, draw, line, x, y, font_main, color):
        """按字符绘制一行文本：普通文字用主字体，emoji用emoji字体（支持embedded_color）。"""
        current_x = x
        emoji_font = self._load_emoji_font(font_main.size if hasattr(font_main, 'size') else 48)
        skip_next_width = False
        i = 0
        while i < len(line):
            ch = line[i]
            # 处理零宽连接符/变体选择符，直接跳过宽度计算
            if ch in ('\u200d', '\ufe0f'):
                i += 1
                continue

            if self._is_emoji(ch):
                try:
                    draw.text((current_x, y), ch, font=emoji_font, embedded_color=True)
                except TypeError:
                    # 某些 Pillow 版本不支持 embedded_color 参数
                    draw.text((current_x, y), ch, font=emoji_font, fill=color)
                w, _ = self._get_text_size(ch, emoji_font)
            else:
                draw.text((current_x, y), ch, font=font_main, fill=color)
                w, _ = self._get_text_size(ch, font_main)

            current_x += w
            i += 1

    def _wrap_text(self, text, font, max_width, max_chars=8):
        """文本自动换行 - 默认8个字符换行"""
        # 支持命令行中使用"\\n"作为手动换行标记
        if "\\n" in text:
            text = text.replace("\\n", "\n")
        lines = []
        current_line = ""
        
        # 直接按字符处理，不分词
        for char in text:
            if char == '\n':
                if current_line:
                    lines.append(current_line)
                    current_line = ""
                continue
            
            # 检查字符数限制
            if len(current_line) >= max_chars:
                lines.append(current_line)
                current_line = char
            else:
                current_line += char
        
        if current_line:
            lines.append(current_line)
        
        return [line for line in lines if line.strip()]  # 过滤空行

    def _get_optimal_font_size(self, text, max_width, max_height, max_chars=8):
        """获取最佳字体大小"""
        for font_size in range(120, 20, -5):
            font = self._load_font(font_size)
            lines = self._wrap_text(text, font, max_width, max_chars)
            
            if len(lines) <= 6:  # 最多6行
                _, font_height = self._get_text_size("测试", font)
                line_spacing = max(10, int(font_height * 0.3))
                total_height = len(lines) * (font_height + line_spacing) - line_spacing
                
                if total_height <= max_height:
                    return font, lines, font_height, line_spacing
        
        # 如果都不合适，使用最小字体
        font = self._load_font(24)
        lines = self._wrap_text(text, font, max_width, max_chars)[:6]
        _, font_height = self._get_text_size("测试", font)
        line_spacing = max(10, int(font_height * 0.3))
        return font, lines, font_height, line_spacing

    def _draw_text_block(self, draw, text, x, y, max_width, max_height, color, max_chars=8, align="left"):
        """绘制文本块"""
        font, lines, font_height, line_spacing = self._get_optimal_font_size(
            text, max_width, max_height, max_chars
        )
        
        # 计算起始Y位置（垂直居中）
        total_height = len(lines) * (font_height + line_spacing) - line_spacing
        start_y = y + (max_height - total_height) // 2
        
        # 绘制每一行
        current_y = start_y
        for line in lines:
            if not line.strip():
                current_y += font_height + line_spacing
                continue
            
            # 计算X位置（注意：为兼容混排，宽度仍按主字体估算）
            if align == "center":
                text_width, _ = self._get_text_size(line, font)
                line_x = x + (max_width - text_width) // 2
            elif align == "right":
                text_width, _ = self._get_text_size(line, font)
                line_x = x + max_width - text_width
            else:  # left
                line_x = x
            
            # 使用混排绘制，emoji 自动切换到 Emoji 字体
            self._draw_line_with_emoji(draw, line, line_x, current_y, font, color)
            current_y += font_height + line_spacing
        
        return len(lines), total_height

    def _add_decorations(self, draw, theme):
        """添加装饰元素"""
        num_decorations = random.randint(3, 6)
        
        for _ in range(num_decorations):
            decoration_type = random.choice(['circle', 'rectangle', 'triangle'])
            x = random.randint(50, self.canvas_width - 100)
            y = random.randint(50, self.canvas_height - 100)
            size = random.randint(15, 40)
            color = random.choice(theme["accent_colors"])
            
            if decoration_type == 'circle':
                draw.ellipse([x, y, x + size, y + size], fill=color)
            elif decoration_type == 'rectangle':
                draw.rectangle([x, y, x + size, y + size], fill=color)
            else:  # triangle
                points = [(x, y + size), (x + size, y + size), (x + size//2, y)]
                draw.polygon(points, fill=color)
    
    def _add_emoji(self, draw):
        """添加emoji"""
        emojis = ['👍', '✨', '🔥', '💪', '💡', '❤️', '🎯', '🌟']
        emoji = random.choice(emojis)
        
        # emoji大小设置 - 可以修改这里的数值来调整emoji大小
        emoji_size = 240  # 主要emoji大小
        backup_size = 240  # 备用字体大小
        circle_size = 240
         # 备用圆点大小
        
        try:
            emoji_font = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", emoji_size)
        except:
            emoji_font = self._load_font(backup_size)
        
        # 右下角位置 - 向左移动50，向上移动20
        x = self.canvas_width - 280  # 原来是200，现在向左移动50
        y = self.canvas_height - 260  # 原来是200，现在向上移动20
        
        try:
            draw.text((x, y), emoji, font=emoji_font, embedded_color=True)
        except:
            # 备用方案：绘制彩色圆点
            draw.ellipse([x, y, x + circle_size, y + circle_size], fill="#FFD700")
    
    def _draw_big_title(self, draw, text, theme):
        """大字标题模板"""
        max_width = self.canvas_width - 80
        max_height = 500
        x = 40
        y = 200
        
        self._draw_text_block(draw, text, x, y, max_width, max_height, 
                             theme["main_color"], max_chars=8, align="left")
    
    def _draw_simple_style(self, draw, text, theme):
        """简约风格模板"""
        max_width = self.canvas_width - 80
        max_height = 400
        x = 40
        y = 300
        
        line_count, text_height = self._draw_text_block(
            draw, text, x, y, max_width, max_height, 
            theme["main_color"], max_chars=8, align="left"
        )
        
        # 添加装饰线
        if line_count > 0:
            line_y = y + max_height + 30
            draw.rectangle([x, line_y, x + 200, line_y + 8], fill=theme["highlight_color"])
    
    def _draw_gradient_background(self, draw, theme):
        """绘制渐变背景"""
        colors = theme["accent_colors"]
        step = self.canvas_height // len(colors)
        
        for i, color in enumerate(colors):
            y_start = i * step
            y_end = min((i + 1) * step + 20, self.canvas_height)  # 重叠一点避免缝隙
            draw.rectangle([0, y_start, self.canvas_width, y_end], fill=color)
    
    def _draw_gradient_style(self, draw, text, theme):
        """渐变背景模板"""
        self._draw_gradient_background(draw, theme)
        
        max_width = self.canvas_width - 80
        max_height = 400
        x = 40
        y = 400
        
        self._draw_text_block(draw, text, x, y, max_width, max_height, 
                             theme["main_color"], max_chars=8, align="left")
    
    # 几何装饰模板已删除
    
    def _draw_layered_style(self, draw, text, theme):
        """分层布局模板"""
        # 底层背景
        draw.rectangle([0, 0, self.canvas_width, 600], fill=theme["accent_colors"][0])
        
        # 白色背景层（全宽度）
        draw.rectangle([0, 120, self.canvas_width, 480], fill="white")
        
        # 在白色背景上绘制文字（不受边框限制）
        max_width = self.canvas_width - 80  # 左右各留40px边距
        max_height = 480 - 120 - 80  # 减去背景高度和上下边距
        x = 40  # 左边距
        y = 120 + 40  # 白色背景顶部 + 上边距
        
        self._draw_text_block(draw, text, x, y, max_width, max_height, 
                             theme["main_color"], max_chars=8, align="left")
        
        # 添加小标签
        tag_font = self._load_font(28)
        draw.rectangle([40, 105, 160, 145], fill=theme["highlight_color"])
        draw.text((50, 115), "❤", font=tag_font, fill="white")
    
    def generate_cover(self, theme_text, output_path=None, theme_name=None, template_name=None):
        """生成封面"""
        # 选择主题
        if theme_name and theme_name in self.themes:
            selected_theme_name = theme_name
        else:
            selected_theme_name = random.choice(list(self.themes.keys()))
        
        theme = self.themes[selected_theme_name]
        
        # 选择模板
        if template_name and template_name in self.templates:
            template = template_name
        else:
            template = random.choice(self.templates)
        
        # 创建画布
        img = Image.new('RGB', (self.canvas_width, self.canvas_height), theme["bg_color"])
        draw = ImageDraw.Draw(img)
        
        # 先添加装饰（底层）
        self._add_decorations(draw, theme)
        
        # 根据模板绘制（中层）
        if template == "大字标题":
            self._draw_big_title(draw, theme_text, theme)
        elif template == "简约风格":
            self._draw_simple_style(draw, theme_text, theme)
        elif template == "渐变背景":
            self._draw_gradient_style(draw, theme_text, theme)
        # 几何装饰模板已删除
        elif template == "分层布局":
            self._draw_layered_style(draw, theme_text, theme)
        
        # 最后添加emoji（顶层）
        self._add_emoji(draw)
        
        # 保存图片
        if not output_path:
            safe_text = "".join(c for c in theme_text if c.isalnum() or c in (' ', '-', '_')).strip()[:10]
            output_path = f"{safe_text}_{selected_theme_name}.png"
        
        img.save(output_path, "PNG", quality=95)
        
        return {
            "path": output_path,
            "theme": selected_theme_name,
            "template": template,
            "size": f"{self.canvas_width}x{self.canvas_height}"
        }
    
    def list_themes(self):
        """列出所有主题"""
        return list(self.themes.keys())
    
    def list_templates(self):
        """列出所有模板"""
        return self.templates

def interactive_mode():
    """交互式模式"""
    generator = XiaohongshuCoverGenerator()
    
    print("🎨 小红书封面生成器")
    print("=" * 30)
    print("可用主题:")
    for i, theme in enumerate(generator.list_themes(), 1):
        theme_info = generator.themes[theme]
        print(f"  {i}. {theme} - {theme_info['description']}")
    
    print("\n可用模板:")
    for i, template in enumerate(generator.list_templates(), 1):
        print(f"  {i}. {template}")
    
    print("\n使用说明:")
    print("  - 直接输入文字生成封面 (支持多行，空行结束)")
    print("  - 'themes' - 查看主题列表")
    print("  - 'templates' - 查看模板列表")
    print("  - 'quit' - 退出程序")
    print("=" * 30)
    
    while True:
        try:
            print("\n请输入主题内容 (输入空行结束):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            
            if not lines:
                continue
            
            user_input = "\n".join(lines).strip()
            
            if user_input.lower() == 'quit':
                print("👋 再见！")
                break
            elif user_input.lower() == 'themes':
                print("\n可用主题:")
                for i, theme in enumerate(generator.list_themes(), 1):
                    theme_info = generator.themes[theme]
                    print(f"  {i}. {theme} - {theme_info['description']}")
                continue
            elif user_input.lower() == 'templates':
                print("\n可用模板:")
                for i, template in enumerate(generator.list_templates(), 1):
                    print(f"  {i}. {template}")
                continue
            
            print("🎨 正在生成封面...")
            result = generator.generate_cover(user_input)
            
            print(f"✅ 生成成功!")
            print(f"   文件: {result['path']}")
            print(f"   主题: {result['theme']}")
            print(f"   模板: {result['template']}")
            print(f"   尺寸: {result['size']}")
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 生成失败: {e}")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 命令行模式
        parser = argparse.ArgumentParser(description='小红书封面生成器')
        parser.add_argument('text', help='封面文字内容')
        parser.add_argument('-o', '--output', help='输出文件名')
        parser.add_argument('-t', '--theme', help='指定主题名称')
        parser.add_argument('-m', '--template', help='指定模板名称')
        parser.add_argument('--list-themes', action='store_true', help='列出所有主题')
        parser.add_argument('--list-templates', action='store_true', help='列出所有模板')
        
        args = parser.parse_args()
        generator = XiaohongshuCoverGenerator()
        
        if args.list_themes:
            print("可用主题:")
            for theme in generator.list_themes():
                theme_info = generator.themes[theme]
                print(f"  - {theme}: {theme_info['description']}")
            return
        
        if args.list_templates:
            print("可用模板:")
            for template in generator.list_templates():
                print(f"  - {template}")
            return
        
        try:
            result = generator.generate_cover(args.text, args.output, args.theme, args.template)
            print(f"✅ 生成成功: {result['path']}")
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            sys.exit(1)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()