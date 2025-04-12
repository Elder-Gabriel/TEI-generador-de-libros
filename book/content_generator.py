import os
import json
import logging
from openai import OpenAI  # Importación actualizada para OpenAI v1.0+

logger = logging.getLogger(__name__)

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_book_content(topic, age_group):
    """
    Genera el contenido de un libro educativo sobre un tema específico para un grupo de edad.
    
    Args:
        topic (str): El tema del libro
        age_group (str): El grupo de edad del público objetivo
        
    Returns:
        dict: Un diccionario con el contenido del libro
    """
    try:
        print(f"Generando contenido para un libro sobre {topic} para niños de {age_group}...")
        
        # Crear el prompt para la generación del contenido
        prompt = f"""
        Crea un libro educativo extenso sobre "{topic}" para niños de {age_group}. 
        El libro debe tener aproximadamente 50 páginas de contenido y estar organizado de la siguiente manera:
        
        1. Una introducción atractiva que despierte el interés.
        2. De 8 a 10 capítulos principales, cada uno con:
           - Un título atractivo
           - Contenido educativo extenso y detallado (aproximadamente 3-4 páginas por capítulo)
           - Datos curiosos o "¿Sabías que...?" en cada capítulo
        3. Una sección de ejercicios y actividades para reforzar el aprendizaje.
        4. Un glosario con términos importantes.
        5. Una conclusión que resuma los puntos principales.
        
        Asegúrate de que el contenido sea:
        - Apropiado para la edad indicada ({age_group})
        - Educativo pero entretenido
        - Detallado y con explicaciones claras
        - Con suficiente texto para cubrir aproximadamente 50 páginas
        - Con lenguaje sencillo pero preciso
        
        Formatea tu respuesta como un JSON con la siguiente estructura:
        {{
            "title": "Título principal del libro",
            "introduction": "Texto de introducción",
            "chapters": [
                {{
                    "title": "Título del capítulo 1", 
                    "content": "Texto extenso del capítulo 1",
                    "fun_fact": "Dato curioso relacionado con este capítulo"
                }},
                {{
                    "title": "Título del capítulo 2", 
                    "content": "Texto extenso del capítulo 2",
                    "fun_fact": "Dato curioso relacionado con este capítulo"
                }},
                // Más capítulos aquí...
            ],
            "exercises": "Ejercicios y actividades detalladas",
            "glossary": [
                {{"term": "Término 1", "definition": "Definición 1"}},
                {{"term": "Término 2", "definition": "Definición 2"}},
                // Más términos del glosario...
            ],
            "conclusion": "Texto de conclusión"
        }}
        """
        
        # Llamada a la API de OpenAI con la nueva sintaxis
        response = client.chat.completions.create(
            model="gpt-4",  # O el modelo que prefieras usar
            messages=[
                {"role": "system", "content": "Eres un experto en crear contenido educativo extenso y detallado para niños."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000  # Aumentado para permitir más contenido
        )
        
        # Extraer el contenido generado y parsearlo como JSON
        content_json = response.choices[0].message.content.strip()
        
        # Eliminar cualquier línea de código markdown si existe
        if "```json" in content_json:
            content_json = content_json.split("```json")[1].split("```")[0].strip()
        elif "```" in content_json:
            content_json = content_json.split("```")[1].split("```")[0].strip()
            
        # Parsear el JSON
        book_data = json.loads(content_json)
        
        # Verificar que el JSON tenga la estructura esperada
        required_keys = ["title", "introduction", "chapters", "exercises", "conclusion"]
        for key in required_keys:
            if key not in book_data:
                raise ValueError(f"El contenido generado no tiene la clave '{key}' esperada")
            
        # Agregar topic y age_group al diccionario para uso posterior
        book_data["topic"] = topic
        book_data["age_group"] = age_group
        
        return book_data
        
    except Exception as e:
        logger.error(f"Error al generar el contenido del libro: {e}")
        print(f"Error al generar el contenido del libro: {e}")
        # Devolver un contenido de respaldo en caso de error
        return {
            "topic": topic,
            "age_group": age_group,
            "title": f"Todo sobre {topic}",
            "introduction": f"Bienvenidos a este fascinante viaje por el mundo de {topic}. En este libro exploraremos todos los aspectos interesantes de este tema, adaptados especialmente para niños de {age_group}.",
            "chapters": [
                {
                    "title": f"Introducción a {topic}", 
                    "content": f"Este capítulo presenta una introducción básica sobre {topic} para niños de {age_group}. Explica los conceptos principales de manera sencilla y amigable.\n\nContinúa con más detalles sobre la importancia de {topic} en nuestra vida diaria y por qué es un tema tan fascinante de estudiar. Los niños aprenderán las bases fundamentales que les ayudarán a entender los siguientes capítulos.",
                    "fun_fact": f"¿Sabías que...? Un dato muy interesante sobre {topic} es que tiene una historia que se remonta a muchos años atrás."
                },
                {
                    "title": "Conceptos importantes", 
                    "content": f"Aquí explicamos los conceptos más importantes sobre {topic} de forma sencilla pero detallada. Cada concepto viene con ejemplos prácticos y explicaciones adaptadas para niños de {age_group}.\n\nAdemás, se incluyen ilustraciones conceptuales que ayudarán a los niños a visualizar estos conceptos abstractos de manera concreta y comprensible.",
                    "fun_fact": f"¿Sabías que...? Hay más de 1000 formas diferentes de aplicar lo que aprendemos sobre {topic} en nuestra vida diaria."
                },
                {
                    "title": "Historia y evolución", 
                    "content": f"Este capítulo narra la fascinante historia y evolución de {topic} a lo largo del tiempo. Los niños aprenderán cómo ha cambiado y desarrollado, desde sus orígenes hasta la actualidad.\n\nSe presentan las figuras históricas más relevantes que contribuyeron al desarrollo de {topic} y cómo sus descubrimientos o invenciones impactaron al mundo.",
                    "fun_fact": f"¿Sabías que...? El primer descubrimiento relacionado con {topic} ocurrió por accidente cuando un científico estaba buscando algo completamente diferente."
                },
                {
                    "title": "Aplicaciones prácticas", 
                    "content": f"Descubre las múltiples aplicaciones prácticas de {topic} en el mundo real. Este capítulo explora cómo se utiliza {topic} en diferentes campos y situaciones cotidianas.\n\nLos niños aprenderán a identificar ejemplos de {topic} en su entorno y comprenderán su importancia práctica a través de ejemplos concretos y relevantes para su edad.",
                    "fun_fact": f"¿Sabías que...? Todos los días utilizamos al menos 5 cosas que están relacionadas con {topic} sin darnos cuenta."
                },
                {
                    "title": "Experimentos y actividades", 
                    "content": f"Este emocionante capítulo presenta experimentos y actividades prácticas relacionadas con {topic} que los niños pueden realizar con supervisión adulta. Cada experimento viene con instrucciones paso a paso y explicaciones sobre los principios científicos involucrados.\n\nEstas actividades prácticas refuerzan el aprendizaje teórico y permiten a los niños experimentar de primera mano los conceptos relacionados con {topic}.",
                    "fun_fact": f"¿Sabías que...? Los científicos que estudian {topic} realizan experimentos similares a los que harás en este capítulo, pero con equipos mucho más sofisticados."
                },
                {
                    "title": "Datos curiosos", 
                    "content": f"Este capítulo está repleto de datos curiosos y sorprendentes sobre {topic} que fascinarán a los niños. Cada dato viene con una explicación detallada para satisfacer su curiosidad y ampliar su conocimiento.\n\nEstos datos están seleccionados específicamente para captar la atención de niños de {age_group} y despertar su interés por aprender más sobre {topic}.",
                    "fun_fact": f"¿Sabías que...? El dato más sorprendente sobre {topic} fue descubierto hace apenas 10 años por un equipo internacional de investigadores."
                },
                {
                    "title": f"{topic} en el futuro", 
                    "content": f"¿Cómo será el futuro de {topic}? Este capítulo explora las tendencias actuales y las posibles evoluciones futuras relacionadas con {topic}. Los niños aprenderán sobre las investigaciones en curso y los desarrollos más prometedores.\n\nTambién se discute cómo estos avances podrían cambiar nuestra forma de vida y qué papel podrían jugar ellos mismos en ese futuro.",
                    "fun_fact": f"¿Sabías que...? Los expertos predicen que en los próximos 20 años, {topic} cambiará radicalmente gracias a nuevos descubrimientos."
                },
                {
                    "title": "Preguntas frecuentes", 
                    "content": f"Este capítulo responde a las preguntas más frecuentes que suelen tener los niños sobre {topic}. Cada pregunta tiene una respuesta clara, directa y adaptada al nivel de comprensión de niños de {age_group}.\n\nLas preguntas han sido seleccionadas basándose en la curiosidad natural de los niños y cubren aspectos que quizás no se hayan tratado en profundidad en otros capítulos.",
                    "fun_fact": f"¿Sabías que...? La pregunta más común sobre {topic} que hacen los niños de todo el mundo es '¿Por qué es importante?'"
                }
            ],
            "exercises": f"Esta sección contiene una variedad de ejercicios y actividades para reforzar lo aprendido sobre {topic}.\n\n1. Preguntas de comprensión: Responde a las siguientes preguntas sobre los capítulos anteriores.\n\n2. Actividades prácticas: Realiza estas actividades con ayuda de un adulto para aplicar lo aprendido.\n\n3. Crucigramas y sopas de letras: Encuentra las palabras clave relacionadas con {topic}.\n\n4. Experimentos sencillos: Siguiendo las instrucciones de seguridad, realiza estos experimentos para ver {topic} en acción.\n\n5. Proyectos creativos: Crea tus propios proyectos relacionados con {topic}.",
            "glossary": [
                {"term": f"{topic}", "definition": f"Definición básica de {topic} adaptada para niños de {age_group}."},
                {"term": "Concepto relacionado 1", "definition": "Definición del primer concepto importante relacionado con el tema."},
                {"term": "Concepto relacionado 2", "definition": "Definición del segundo concepto importante relacionado con el tema."},
                {"term": "Concepto relacionado 3", "definition": "Definición del tercer concepto importante relacionado con el tema."},
                {"term": "Concepto relacionado 4", "definition": "Definición del cuarto concepto importante relacionado con el tema."},
                {"term": "Concepto relacionado 5", "definition": "Definición del quinto concepto importante relacionado con el tema."},
                {"term": "Concepto relacionado 6", "definition": "Definición del sexto concepto importante relacionado con el tema."},
                {"term": "Concepto relacionado 7", "definition": "Definición del séptimo concepto importante relacionado con el tema."},
                {"term": "Concepto relacionado 8", "definition": "Definición del octavo concepto importante relacionado con el tema."},
                {"term": "Concepto relacionado 9", "definition": "Definición del noveno concepto importante relacionado con el tema."},
                {"term": "Concepto relacionado 10", "definition": "Definición del décimo concepto importante relacionado con el tema."}
            ],
            "conclusion": f"En conclusión, hemos explorado muchos aspectos fascinantes de {topic} a lo largo de este libro. Hemos aprendido sobre su historia, conceptos importantes, aplicaciones prácticas y su posible futuro. Esperamos que este viaje de conocimiento haya sido tan emocionante para ti como lo fue para nosotros al crear este libro.\n\nRecuerda que {topic} es un tema muy amplio y siempre hay más por descubrir. Te animamos a seguir explorando, preguntando y aprendiendo más sobre este fascinante tema. ¡Tu curiosidad es el motor más poderoso para el aprendizaje!"
        }