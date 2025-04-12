from book.pdf_creator import create_pdf
from book.content_generator import generate_book_content
import os

def main():
    print("=== Generador de Libros con Imágenes ===")
    topic = input("Tema del libro: ").strip()
    age_group = input("Edad del público objetivo: ").strip()

    print("\nGenerando libro, por favor espere...")
    
    # Generar contenido del libro
    book_data = generate_book_content(topic, age_group)
    
    # Definir la ruta de salida para el PDF
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"libro_{topic.replace(' ', '_').lower()}.pdf")
    
    # Llamar a create_pdf con el diccionario y la ruta de salida
    generated_path = create_pdf(book_data, output_path)

    if generated_path:
        print(f"\n✅ Libro generado exitosamente: {generated_path}")
    else:
        print("\n❌ Ocurrió un error al generar el libro.")

if __name__ == "__main__":
    main()