from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO

def draw_rounded_rectangle_with_shadow(image, xy, radius, fill, shadow_color, shadow_offset, shadow_blur):
    """
    绘制带有阴影的圆角矩形。
    """
    try:
        x1, y1, x2, y2 = xy
        shadow_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))  # 创建一个透明图层
        shadow_draw = ImageDraw.Draw(shadow_layer)

        # 计算阴影位置
        shadow_xy = (
            x1 - shadow_offset[0],
            y1 + shadow_offset[1],
            x2 + shadow_offset[0],
            y2 + shadow_offset[1],
        )

        # 绘制阴影
        shadow_draw.rounded_rectangle(shadow_xy, radius, fill=shadow_color)
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur))

        # 粘贴阴影层
        shadow_mask = shadow_layer.split()[3]
        image.paste(shadow_layer, (0, 0), mask=shadow_mask)

        # 绘制实际的圆角矩形
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(xy, radius, fill=fill)
    except Exception as e:
        print(f"Error drawing rounded rectangle with shadow: {e}")

def add_avatar(image, avatar_url, position, size, radius):
    """
    添加带圆角的头像。
    """
    try:
        response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(response.content)).resize(size)
    except Exception as e:
        print(f"Error loading avatar: {e}")
        avatar = Image.new("RGB", size, (200, 200, 200))  # 使用灰色占位符

    try:
        # 创建一个圆角蒙版
        mask = Image.new("L", size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, size[0], size[1]), radius, fill=255)

        # 粘贴头像
        image.paste(avatar, position, mask)
    except Exception as e:
        print(f"Error adding avatar: {e}")

level_color = {
  'Tourist': ['#7F0000', (0xbf, 0, 0, 255)],
  'LGM': ['#7F0000', (0xbf, 0, 0, 255)],
  'GM': ['#AF3333', (255, 51, 51, 255)],
  'IM': ['#DFBF33', (255, 187, 85, 255)],
  "Master": ['#E7B371', (255, 204, 136, 255)],
  'CM': ['#7F8BFF', (91, 94, 231, 255)],
  'Expert': ['#3B82F6', (0x60, 0xa5, 0xfa, 255)],
  'Spelist': ['#06b6d4', (0x22, 0xd3, 0xee, 255)],
  'Pupil': ['#1D9C2B', (119, 255, 119, 255)],
  'Newbie': ['#7C7C7C', (204, 204, 204, 255)],
  'Unrated': ['#7C7C7C', (204, 204, 204, 255)],
}

def generate_codeforces_card(username, rating, max_rating, level, stars, avatar_url, output_path):
    """
    生成带有阴影和层次感的个人名片。
    """
    try:
        # 名片尺寸和颜色
        # width, height = 600, 800
        # background_color = (240, 240, 240, 255)  # 浅灰背景
        rectangle_color = level_color[level][0]  # 蓝色矩形
        shadow_color = (0, 0, 0, 40)  # 半透明黑色阴影
        text_color = "white"

        bg_color = level_color[level][1]  # 淡蓝色背景
        bg_size = (600, 800)  # 背景尺寸
        img = Image.new("RGBA", bg_size, bg_color)
        draw = ImageDraw.Draw(img)

        # 绘制 Codeforces Logo
        logo_width, logo_height = 230, 100  # Logo 尺寸
        logo_position = (bg_size[0] - logo_width, 10)  # 右上角位置，留 10px 边距

        # 绘制彩色条
        bar_x = logo_position[0] - 10
        bar_y = logo_position[1] + 15
        tx, dx = 9, 5
        draw.rounded_rectangle((bar_x + 0, bar_y, bar_x + tx, bar_y + 25), radius=3, fill="#FFD700")  # 黄色
        draw.rounded_rectangle((bar_x + tx + dx, bar_y - 8, bar_x + 2 * tx + dx, bar_y + 25), radius=3, fill="#50B3FF")  # 蓝色条
        draw.rounded_rectangle((bar_x + 2 * (tx + dx), bar_y + 8, bar_x + 3 * tx + 2 * dx, bar_y + 25), radius=3, fill="#FF5E66")  # 红色条

        # 添加文本部分
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf", 30)  # 尝试加载 Arial 字体
        except Exception as e:
            print(f"Error loading font: {e}")
            font = ImageFont.load_default(30)  # 如果 Arial 不可用，使用默认字体

        # 绘制 "Code" 文本 (白色)
        draw.text((bar_x + 50, bar_y - 6), "Code", font=font, fill="#FFFFFF")

        # 绘制 "Forces" 文本 (蓝色)
        draw.text((bar_x + 130, bar_y - 6), "Forces", font=font, fill="#0078FF")

        # 添加带阴影的圆角矩形背景
        draw_rounded_rectangle_with_shadow(
            image=img,
            xy=(50, 200, 550, 750),  # 大背景区域
            radius=40,
            fill=rectangle_color,
            shadow_color=shadow_color,
            shadow_offset=(3, 5),
            shadow_blur=4
        )

        basex = 50; basey = 200
        # 添加头像
        add_avatar(img, avatar_url, position=(225, basey - 115), size=(150, 150), radius=75)

        # 绘制文本信息
        draw = ImageDraw.Draw(img)
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf", 40)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf", 30)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf", 20)

        # 用户名
        draw.text((300, basey + 70), username, fill=text_color, font=font_large, anchor="mm")

        # Max Rating 和 Stars
        draw.text((100, basey + 150), f"MaxRating", fill=text_color, font=font_medium)
        draw.text((400, basey + 150), f"stars", fill=text_color, font=font_medium)

        draw.text((100, basey + 190), f"{max_rating}", fill=text_color, font=font_large)
        draw.text((400, basey + 190), f"{stars}", fill=text_color, font=font_large)

        # Rating 和 Level
        draw.text((100, basey + 250), "Rating", fill=text_color, font=font_medium)
        draw.text((100, basey + 300), str(rating), fill=text_color, font=font_large)
        draw.text((400, basey + 250), "Level", fill=text_color, font=font_medium)
        draw.text((400, basey + 300), level, fill=text_color, font=font_large)

        # # 解决问题统计
        # draw.text((300, basey + 400), f"Solved {problems_solved} problems", fill=text_color, font=font_small, anchor="mm")

        # 保存结果
        img.save(output_path)
        print(f"Codeforces card saved to {output_path}")
    except Exception as e:
        print(f"Error generating Codeforces card: {e}")