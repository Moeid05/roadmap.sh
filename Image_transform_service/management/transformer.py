from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os
import re
def apply_sepia(image):
    width, height = image.size
    pixels = image.load() 
    for py in range(height):
        for px in range(width):
            pixel = image.getpixel((px, py))
            if isinstance(pixel, int):
                r = g = b = pixel
            elif len(pixel) == 4:
                r, g, b, a = pixel
            elif len(pixel) == 3:
                r, g, b = pixel
            else:
                continue

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            tr = min(255, tr)
            tg = min(255, tg)
            tb = min(255, tb)

            if isinstance(pixel, int):
                pixels[px, py] = (tr + tg + tb) // 3
            elif len(pixel) == 4:
                pixels[px, py] = (tr, tg, tb, a)
            else:
                pixels[px, py] = (tr, tg, tb)

    return image


def resize(image,width,height) : 
    if width and height:
        return image.resize((width, height))
    return image

def crop (image,width,height,x,y) : 
    if width and height and x is not None and y is not None:
        return image.crop((x, y, x + width, y + height))
    return image
        

def rotate(image,angle) : 
    if angle is not None:
        return image.rotate(angle)
    return image
        
def watermark(image, text, position=(0, 0), font_size=20):
    watermark = Image.new('RGBA', image.size)
    draw = ImageDraw.Draw(watermark)
    font = ImageFont.load_default()
    draw.text(position, text, fill=(255, 255, 255, 128), font=font)
    return Image.alpha_composite(image.convert('RGBA'), watermark)

def compress(image,quality) : 
    output = io.BytesIO()
    image.save(output, format='png', quality=quality)
    return Image.open(output)

def transform_image(image, transformations):
    print('random number : 20351')
    if 'resize' in transformations:
        width = transformations['resize'].get('width')
        height = transformations['resize'].get('height')
        image = resize(image,width,height)

    if 'crop' in transformations:
        width = transformations['crop'].get('width')
        height = transformations['crop'].get('height')
        x = transformations['crop'].get('x')
        y = transformations['crop'].get('y')
        image = crop(image,width,height,x,y)

    if 'rotate' in transformations:
        angle = transformations['rotate']
        image = rotate(image,angle)

    if 'watermark' in transformations:
        text = transformations['watermark'].get('text')
        position = transformations['watermark'].get('position', (0, 0))
        if text:
            image = watermark(image, text, position)

    if 'flip' in transformations and transformations['flip']:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

    if 'mirror' in transformations and transformations['mirror']:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

    if 'compress' in transformations:
        quality = transformations['compress'].get('quality', 85)
        image = compress(image,quality)

    if 'format' in transformations:
        format_type = transformations['format'].upper()
        if format_type == 'JPEG':
            image = image.convert('RGB')
        elif format_type == 'PNG':
            image = image.convert('RGBA')

    if 'filters' in transformations:
        filters = transformations['filters']
        if filters.get('grayscale'):
            image = image.convert('L')
        if filters.get('sepia'):
            image = apply_sepia(image)
        if filters.get('blur'):
            image = image.filter(ImageFilter.GaussianBlur(radius=5))
        if filters.get('sharpen'):
            image = image.filter(ImageFilter.SHARPEN)
    
    return image

def transform_instance_image(image,transforms) :
    img = Image.open(image)
    transformed_img = transform_image(img, transforms)
    img_io = io.BytesIO()
    img_format = transforms.get('format') if transforms.get('format') else 'JPEG'
    transformed_img.save(img_io, format=img_format)
    img_io.seek(0)
    return transformed_img , img_format