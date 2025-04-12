def generate_introduction(topic: str, age_group: str) -> str:
    """
    Genera la introducción del libro.

    Args:
        topic (str): Tema del libro.
        age_group (str): Rango de edad del público objetivo.

    Returns:
        str: Texto de la introducción.
    """
    return f"""
    ¡Hola! Bienvenido a este libro sobre {topic}.

    Este libro ha sido pensado especialmente para niños y niñas de {age_group}. Aquí aprenderás cosas muy interesantes
    sobre {topic}, con explicaciones fáciles de entender, ejemplos divertidos, ilustraciones y actividades para practicar.

    Esperamos que disfrutes cada página y que al final te conviertas en un experto en el tema.
    ¡Comencemos esta aventura juntos!
    """
