import os
import logging
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random

logger = logging.getLogger(__name__)

def generate_cover(topic, age_group):
    """
    Genera una imagen de portada simple para el libro.
    
    Args:
        topic (str): Tema del libro
        age_group (str): Grupo de edad del público objetivo
        
    Returns:
        bytes: Datos binarios de la imagen generada
    """
    try:
        return create_simple_cover(topic, age_group)
    except Exception as e:
        logger.error(f"Error en la generación de portada: {e}")
        print(f"Error general de portada: {e}")
        return None

def create_simple_cover(topic, age_group):
    """
    Crea una portada simple con texto.
    
    Args:
        topic (str): Tema del libro
        age_group (str): Grupo de edad del público objetivo
        
    Returns:
        bytes: Datos binarios de la imagen generada
    """
    try:
        # Crear una imagen con dimensiones de portada
        width, height = 1000, 1400
        
        # Usar un color aleatorio para el fondo
        background_colors = [
            (135, 206, 235),  # Azul cielo
            (144, 238, 144),  # Verde claro
            (255, 182, 193),  # Rosa claro
            (255, 218, 185),  # Melocotón
            (230, 230, 250)   # Lavanda
        ]
        bg_color = random.choice(background_colors)
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Añadir un borde decorativo
        border_width = 30
        border_color = (bg_color[0]-30, bg_color[1]-30, bg_color[2]-30)
        draw.rectangle([(border_width, border_width), 
                        (width-border_width, height-border_width)], 
                        outline=border_color, width=border_width//2)
        
        # Añadir formas decorativas
        for _ in range(20):
            shape_color = (
                random.randint(100, 250),
                random.randint(100, 250),
                random.randint(100, 250)
            )
            
            # Posición y tamaño aleatorios
            x = random.randint(border_width*2, width-border_width*3)
            y = random.randint(border_width*2, height-border_width*3)
            size = random.randint(30, 100)
            
            # Alternar entre círculos y rectángulos
            if random.choice([True, False]):
                draw.ellipse([x, y, x+size, y+size], fill=shape_color)
            else:
                draw.rectangle([x, y, x+size, y+size], fill=shape_color)
        
        # Área para el título
        title_bg = (255, 255, 255, 200)  # Blanco semi-transparente
        title_box = [(100, height//3-100), (width-100, height//3+200)]
        draw.rectangle(title_box, fill=title_bg)
        
        # Fuente para el texto
        try:
            # Intentar usar fuentes del sistema
            title_font = ImageFont.truetype("arial.ttf", 72)
            subtitle_font = ImageFont.truetype("arial.ttf", 36)
        except Exception:
            # Si falla, usar la fuente por defecto
            title_font = ImageFont.load_default()
            subtitle_font = title_font
        
        # Textos
        title_text = topic
        subtitle_text = f"Para niños de {age_group}"
        author_text = "Un libro educativo ilustrado"
        
        # Dibujar textos centrados
        # Título
        w_title = title_font.getbbox(title_text)[2]
        x_title = (width - w_title) // 2
        draw.text((x_title, height//3-50), title_text, fill=(0, 0, 0), font=title_font)
        
        # Subtítulo
        w_subtitle = subtitle_font.getbbox(subtitle_text)[2]
        x_subtitle = (width - w_subtitle) // 2
        draw.text((x_subtitle, height//3+80), subtitle_text, fill=(0, 0, 0), font=subtitle_font)
        
        # Autor/descripción
        w_author = subtitle_font.getbbox(author_text)[2]
        x_author = (width - w_author) // 2
        draw.text((x_author, height//3+140), author_text, fill=(0, 0, 0), font=subtitle_font)
        
        # Guardar la imagen
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        return img_byte_arr.getvalue()
        
    except Exception as e:
        logger.error(f"Error al crear portada simple: {e}")
        print(f"Error al crear portada simple: {e}")
        
        # Último recurso: crear una portada extremadamente básica
        try:
            solid_img = Image.new('RGB', (1000, 1400), color=(240, 240, 240))
            solid_draw = ImageDraw.Draw(solid_img)
            solid_draw.rectangle([(50, 50), (950, 1350)], outline=(0, 0, 0), width=10)
            
            font = ImageFont.load_default()
            solid_draw.text((500, 700), f"Libro sobre {topic}", fill=(0, 0, 0), anchor="mm")
            
            solid_byte_arr = BytesIO()
            solid_img.save(solid_byte_arr, format='JPEG')
            solid_byte_arr.seek(0)
            return solid_byte_arr.getvalue()
        except:
            return None