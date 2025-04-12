import os
from fpdf import FPDF
from book.cover_generator import generate_cover
from book.image_generator import generate_image
import logging
import textwrap

logger = logging.getLogger(__name__)

class BookPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.chapter_title = ""
        self.page_count = 0
        
    def header(self):
        if self.page_no() > 1:  # No mostrar encabezado en la primera página
            self.set_font('Arial', 'I', 8)
            if self.chapter_title:
                self.cell(0, 10, self.chapter_title, 0, 0, 'L')
            self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'R')
            self.ln(10)
            
    def footer(self):
        if self.page_no() > 1:  # No mostrar pie de página en la primera página
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            
    def chapter_title_page(self, title):
        self.add_page()
        self.chapter_title = title
        self.set_font('Arial', 'B', 20)
        self.ln(60)
        self.cell(0, 10, title, ln=True, align='C')
        self.ln(10)
        
    def chapter_body(self, content):
        # Dividir el contenido en bloques más pequeños para que ocupe más páginas
        self.set_font('Arial', '', 12)
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs:
            # Dividir párrafos largos en partes más pequeñas
            if len(paragraph) > 300:
                parts = textwrap.wrap(paragraph, width=80)
                for part in parts:
                    # Espaciar más el contenido para ocupar más páginas
                    self.multi_cell(0, 8, part)
                    self.ln(5)
            else:
                self.multi_cell(0, 8, paragraph)
                self.ln(5)
            
            # Añadir espacio adicional entre párrafos
            self.ln(5)
        
        # Asegurar suficiente espacio para las imágenes
        self.ln(10)

    def fun_fact_box(self, fun_fact):
        # Guardar posición actual
        x = self.get_x()
        y = self.get_y()
        
        # Verificar si hay suficiente espacio en la página
        if y > 230:  # Si estamos cerca del final de la página
            self.add_page()
            y = self.get_y()
        
        # Dibujar un cuadro para el dato curioso
        self.set_fill_color(240, 240, 200)  # Color amarillo claro
        self.set_draw_color(200, 200, 150)  # Borde más oscuro
        
        # Calcular altura necesaria para el texto
        self.set_font('Arial', 'I', 10)
        lines = self.get_multi_cell_lines(180, 6, fun_fact)
        height = len(lines) * 6 + 10  # Altura calculada + margen
        
        # Dibujar el rectángulo
        self.rect(15, y, 180, height, 'DF')
        
        # Añadir texto del dato curioso
        self.set_xy(20, y + 5)
        self.set_text_color(0, 0, 0)
        self.multi_cell(170, 6, fun_fact)
        
        # Restaurar posición después del cuadro
        self.set_xy(x, y + height + 5)
        self.set_text_color(0, 0, 0)
        
    def get_multi_cell_lines(self, w, h, txt):
        # Función auxiliar para calcular cuántas líneas ocupará un multi_cell
        cw = self.current_font['cw']
        if w == 0:
            w = self.w - self.r_margin - self.x
        wmax = (w - 2 * self.c_margin) * 1000 / self.font_size
        s = txt.replace('\r', '')
        nb = len(s)
        if nb > 0 and s[nb-1] == '\n':
            nb -= 1
        lines = []
        sep = -1
        i = 0
        j = 0
        l = 0
        while i < nb:
            c = s[i]
            if c == '\n':
                lines.append(s[j:i])
                i += 1
                sep = -1
                j = i
                l = 0
                continue
            if c == ' ':
                sep = i
            if ord(c) >= 128:
                l += 1
            else:
                l += cw.get(c, 0) / 1000.0 * self.font_size
            if l > wmax:
                if sep == -1:
                    if i == j:
                        i += 1
                    lines.append(s[j:i])
                else:
                    lines.append(s[j:sep])
                    i = sep + 1
                sep = -1
                j = i
                l = 0
            else:
                i += 1
        if i != j:
            lines.append(s[j:i])
        return lines

def create_pdf(book_data, output_path="output/book.pdf"):
    """
    Genera un PDF educativo extenso usando los datos proporcionados.
    
    Args:
        book_data (dict): Diccionario con el contenido del libro
        output_path (str): Ruta donde se guardará el PDF
        
    Returns:
        str or None: Ruta del PDF generado o None si hubo un error
    """
    try:
        # Extraer información del diccionario
        topic = book_data["topic"]
        age_group = book_data["age_group"]
        book_title = book_data.get("title", f"Libro sobre {topic}")
        introduction = book_data.get("introduction", "")
        chapters = book_data.get("chapters", [])
        exercises = book_data.get("exercises", "")
        glossary = book_data.get("glossary", [])
        conclusion = book_data.get("conclusion", "")
        
        # Crear el PDF con el contenido generado
        pdf = BookPDF()
        pdf.set_title(book_title)
        pdf.set_author("Sistema de Generación de Libros Educativos")
        
        # Asegurar que la ruta output_path sea absoluta o relativa a la ubicación actual
        output_path = os.path.abspath(output_path)
        output_dir = os.path.dirname(output_path)
        
        # Crear el directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Crear un directorio temporal para las imágenes si no existe
        temp_image_dir = os.path.join(output_dir, "temp_images")
        os.makedirs(temp_image_dir, exist_ok=True)

        # Generar la portada y agregarla al PDF
        print("Generando portada...")
        cover_image = generate_cover(topic, age_group)
        
        # Página de portada
        pdf.add_page()
        pdf.set_font("Arial", "B", 24)
        pdf.ln(40)
        pdf.cell(0, 20, book_title, ln=True, align="C")
        pdf.set_font("Arial", "", 14)
        pdf.cell(0, 10, f"Un libro educativo para niños de {age_group}", ln=True, align="C")
        pdf.ln(20)

        if cover_image:
            cover_path = os.path.join(temp_image_dir, "cover.jpg")
            try:
                with open(cover_path, "wb") as f:
                    f.write(cover_image)
                pdf.image(cover_path, x=30, y=100, w=150)
            except Exception as e:
                logger.warning(f"No se pudo agregar la imagen de portada: {e}")
                print(f"Error con la imagen de portada: {e}")
        else:
            logger.warning("No se generó imagen de portada.")
            print("No se generó imagen de portada.")
            
        # Páginas iniciales: índice
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Índice", ln=True)
        pdf.ln(5)
        
        page_counter = 4  # Empezamos en la página 4 (1-portada, 2-índice, 3-introducción)
        pdf.set_font("Arial", "", 12)
        
        # Introducción en el índice
        pdf.cell(0, 8, f"Introducción..................................{page_counter}", ln=True)
        page_counter += 2  # Estimamos 2 páginas para la introducción
        
        # Capítulos en el índice
        for i, chapter in enumerate(chapters):
            chapter_title = chapter.get("title", f"Capítulo {i+1}")
            pdf.cell(0, 8, f"{chapter_title}..................................{page_counter}", ln=True)
            page_counter += 5  # Estimamos 5 páginas por capítulo en promedio
        
        # Secciones finales en el índice
        pdf.cell(0, 8, f"Ejercicios y Actividades..........................{page_counter}", ln=True)
        page_counter += 3
        
        pdf.cell(0, 8, f"Glosario..................................{page_counter}", ln=True)
        page_counter += 2
        
        pdf.cell(0, 8, f"Conclusión..................................{page_counter}", ln=True)
        
        # Página de introducción
        pdf.chapter_title_page("Introducción")
        pdf.chapter_body(introduction)
        
        # Páginas para cada capítulo
        print("Añadiendo capítulos con imágenes...")
        for i, chapter in enumerate(chapters):
            chapter_title = chapter.get("title", f"Capítulo {i+1}")
            chapter_content = chapter.get("content", "")
            fun_fact = chapter.get("fun_fact", "")
            
            # Título del capítulo en página nueva
            pdf.chapter_title_page(chapter_title)
            
            # Contenido del capítulo
            pdf.chapter_body(chapter_content)
            
            # Generar imagen para el capítulo
            print(f"Generando imagen para el capítulo: {chapter_title}...")
            image_prompt = f"Ilustración educativa para niños sobre '{chapter_title}' relacionado con {topic}"
            image = generate_image(image_prompt)
            
            if image:
                image_path = os.path.join(temp_image_dir, f"chapter_{i+1}.jpg")
                try:
                    with open(image_path, "wb") as f:
                        f.write(image)
                    # Verificar si hay suficiente espacio en la página actual
                    if pdf.get_y() > 180:
                        pdf.add_page()
                    # Centrar la imagen
                    pdf.image(image_path, x=(210-150)/2, y=pdf.get_y(), w=150)
                except Exception as e:
                    logger.warning(f"No se pudo agregar imagen para el capítulo {i+1}: {e}")
                    print(f"Error con la imagen del capítulo {i+1}: {e}")
            
            # Añadir dato curioso si existe
            if fun_fact:
                pdf.ln(10)
                pdf.fun_fact_box(fun_fact)
            
            pdf.ln(10)
        
        # Sección de ejercicios
        pdf.chapter_title_page("Ejercicios y Actividades")
        pdf.chapter_body(exercises)
        
        # Generar imagen para los ejercicios
        print("Generando imagen para los ejercicios...")
        exercises_image = generate_image(f"Ilustración para ejercicios y actividades sobre {topic} para niños")
        if exercises_image:
            exercises_image_path = os.path.join(temp_image_dir, "exercises.jpg")
            try:
                with open(exercises_image_path, "wb") as f:
                    f.write(exercises_image)
                pdf.image(exercises_image_path, x=(210-150)/2, y=pdf.get_y(), w=150)
            except Exception as e:
                logger.warning(f"No se pudo agregar imagen para ejercicios: {e}")
                print(f"Error con la imagen de ejercicios: {e}")
        
        # Glosario
        pdf.chapter_title_page("Glosario")
        pdf.set_font("Arial", "", 12)
        for term_def in glossary:
            term = term_def.get("term", "")
            definition = term_def.get("definition", "")
            if term and definition:
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, term, ln=True)
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 8, definition)
                pdf.ln(5)
        
        # Conclusión
        pdf.chapter_title_page("Conclusión")
        pdf.chapter_body(conclusion)
        
        # Verificar que tengamos al menos 50 páginas
        if pdf.page_no() < 50:
            print(f"Añadiendo páginas adicionales para alcanzar el objetivo de 50 páginas (actual: {pdf.page_no()})...")
            
            # Añadir páginas de notas al final
            pages_needed = 50 - pdf.page_no()
            
            if pages_needed > 0:
                pdf.chapter_title_page("Mis Notas")
                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 10, "Usa estas páginas para tomar notas sobre lo que has aprendido:", ln=True)
                pdf.ln(5)
                
                # Añadir páginas de líneas para notas
                for _ in range(pages_needed - 1):  # -1 porque ya añadimos la página de título
                    pdf.add_page()
                    # Dibujar líneas horizontales para notas
                    y = 30
                    while y < 270:
                        pdf.line(20, y, 190, y)
                        y += 12
        
        # Guardar el archivo PDF
        print(f"Guardando PDF en {output_path}...")
        pdf.output(output_path)
        print(f"PDF generado con {pdf.page_no()} páginas.")
        return output_path

    except Exception as e:
        print(f"\n❌ Error al generar el PDF: {e}")
        return None