import os
import requests
import logging
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random

logger = logging.getLogger(__name__)

def generate_image(prompt):
    """
    Genera una imagen simple basada en un prompt.
    
    Args:
        prompt (str): Descripción de la imagen a generar
        
    Returns:
        bytes: Datos binarios de la imagen generada
    """
    try:
        # Método simple: crear una imagen con texto
        return create_simple_image(prompt)
    except Exception as e:
        logger.error(f"Error en la generación de imagen: {e}")
        print(f"Error general de imagen: {e}")
        return None

def create_simple_image(text):
    """
    Crea una imagen simple con texto.
    
    Args:
        text (str): Texto para mostrar en la imagen
        
    Returns:
        bytes: Datos binarios de la imagen generada
    """
    try:
        # Crear una imagen con colores aleatorios
        width, height = 800, 600
        
        # Usar colores pastel aleatorios
        r = random.randint(180, 240)
        g = random.randint(180, 240)
        b = random.randint(180, 240)
        img = Image.new('RGB', (width, height), color=(r, g, b))
        
        # Preparar para dibujar
        draw = ImageDraw.Draw(img)
        
        # Añadir un borde
        border_color = (r-40, g-40, b-40)
        draw.rectangle([(20, 20), (width-20, height-20)], outline=border_color, width=10)
        
        # Añadir algunas formas decorativas
        for _ in range(5):
            shape_r = random.randint(100, 200)
            shape_g = random.randint(100, 200)
            shape_b = random.randint(100, 200)
            shape_color = (shape_r, shape_g, shape_b)
            
            # Dibujar círculos aleatorios
            x = random.randint(50, width-100)
            y = random.randint(50, height-100)
            size = random.randint(30, 100)
            draw.ellipse([x, y, x+size, y+size], fill=shape_color)
        
        # Preparar el texto
        # El texto será una versión resumida del prompt
        if len(text) > 100:
            display_text = text[:97] + "..."
        else:
            display_text = text
            
        # Dibujar un rectángulo para el texto
        text_bg = (255, 255, 255, 180)  # Blanco semi-transparente
        text_box = [(50, height//2-50), (width-50, height//2+50)]
        draw.rectangle(text_box, fill=text_bg)
        
        # Añadir el texto
        try:
            # Intentar usar una fuente del sistema
            font = ImageFont.truetype("arial.ttf", 24)
        except Exception:
            # Si falla, usar la fuente por defecto
            font = ImageFont.load_default()
        
        # Centrar texto
        text_width = font.getbbox(display_text)[2]
        text_x = (width - text_width) // 2
        draw.text((text_x, height//2-10), display_text, fill=(0, 0, 0), font=font)
        
        # Guardar la imagen
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        return img_byte_arr.getvalue()
        
    except Exception as e:
        logger.error(f"Error al crear imagen simple: {e}")
        print(f"Error al crear imagen simple: {e}")
        
        # Último recurso: crear una imagen completamente básica
        try:
            solid_img = Image.new('RGB', (800, 600), color=(240, 240, 240))
            solid_byte_arr = BytesIO()
            solid_img.save(solid_byte_arr, format='JPEG')
            solid_byte_arr.seek(0)
            return solid_byte_arr.getvalue()
        except:
            return None