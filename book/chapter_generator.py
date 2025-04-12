from openai import OpenAI

client = OpenAI()

def generate_chapters(topic: str, age_group: str) -> list:
    """
    Genera capítulos sobre el tema dado.

    Returns:
        list of tuples: Cada uno con (título, contenido del capítulo).
    """
    prompt = (
        f"Escribe al menos 5 capítulos detallados sobre el tema '{topic}' para niños de {age_group}. "
        "Cada capítulo debe incluir un título y un desarrollo claro en párrafos."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    text = response.choices[0].message.content

    # Separar los capítulos por títulos (asume formato: Capítulo X: Título)
    import re
    matches = re.findall(r"(Capítulo\s\d+:.*?)(?=Capítulo\s\d+:|\Z)", text, re.DOTALL)

    chapters = []
    for match in matches:
        title_match = re.search(r"Capítulo\s\d+:\s*(.*)", match)
        title = title_match.group(1).strip() if title_match else "Capítulo"
        content = match.replace(title, "", 1).strip()
        chapters.append((title, content))

    return chapters
