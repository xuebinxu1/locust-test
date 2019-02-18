from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
from io import BytesIO
import base64


# 随机字母:
def rndChar():
    str = ''
    for i in range(8):
        str += chr(random.randint(65, 90))
    return str


# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def get_image(text):
    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('Songti.ttc', 22)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=(0, 0, 0))

        draw.text((20, 10), str(text), font=font, fill=(255, 255, 255))
    # 模糊:
    # image = image.filter(ImageFilter.BLUR)
    return image


def get_image_base64(text):
    image = get_image(text)
    output_buffer = BytesIO()
    image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str.decode()


def get_image_bytes(text):
    image = get_image(text)
    output_buffer = BytesIO()
    image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    return byte_data
