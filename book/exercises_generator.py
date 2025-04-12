def generate_exercises(topic: str, age_group: str, num_sets: int = 5) -> list[str]:
    """
    Genera una lista de ejercicios relacionados con el tema y edad.

    Args:
        topic (str): Tema central del libro.
        age_group (str): Grupo de edad objetivo.
        num_sets (int): Cantidad de bloques de ejercicios a generar.

    Returns:
        list[str]: Lista de secciones con ejercicios.
    """

    exercises = []

    for i in range(1, num_sets + 1):
        section = f"""
        Actividades - Sección {i}

        1. Explica con tus propias palabras qué entiendes por "{topic}".
        2. Dibuja algo relacionado con "{topic}" y compártelo con tus compañeros.
        3. ¿Qué fue lo más interesante que aprendiste sobre "{topic}"?
        4. Escribe tres cosas que no sabías sobre "{topic}" y que ahora conoces.
        5. Elige un personaje o evento relacionado con "{topic}" e investiga más sobre él/ella.

        Esta sección está pensada para estimular tu creatividad y comprensión.
        """

        exercises.append(section)

    return exercises
