def generate_conclusion(topic: str, age_group: str) -> str:
    """
    Genera la conclusión del libro basada en el tema y grupo de edad.

    Args:
        topic (str): Tema central del libro.
        age_group (str): Grupo de edad objetivo.

    Returns:
        str: Conclusión del libro.
    """

    conclusion = f"""
    Conclusión sobre {topic} para {age_group}

    En este libro, exploramos los aspectos más relevantes de "{topic}" desde una perspectiva
    que se adapta a tu edad y comprensión. Ahora sabes que:

    1. {topic} ha jugado un papel crucial en el desarrollo de nuestra sociedad y el mundo en el que vivimos.
    2. Hemos aprendido cómo las personas de diferentes épocas han interactuado con {topic}.
    3. El impacto de {topic} sigue siendo relevante hoy en día, y seguirá siéndolo en el futuro.

    Es importante que sigas investigando y aprendiendo sobre este tema, ya que puede ofrecerte
    muchas oportunidades para descubrir más sobre la historia, la ciencia o la cultura que te rodea.
    
    Recuerda que siempre puedes investigar más, y el aprendizaje nunca se detiene.

    ¡Gracias por leer y seguir aprendiendo!
    """

    return conclusion
