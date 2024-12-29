import os
import markovify

# Pfad zur Datei mit dem Basiskorpus
BASE_CORPUS_PATH = os.path.join(os.path.dirname(__file__), '../resources/base_corpus.txt')

def load_corpus():
    """
    Lädt den Text aus der Datei `base_corpus.txt`.

    Returns:
        str: Der gesamte Inhalt der Datei als String.
    """
    if not os.path.exists(BASE_CORPUS_PATH):
        raise FileNotFoundError(f"Korpusdatei nicht gefunden: {BASE_CORPUS_PATH}")

    with open(BASE_CORPUS_PATH, 'r', encoding='utf-8') as file:
        return file.read()

def get_new_text(max_length=300):
    """
    Generiert einen neuen Text basierend auf einem Markov-Modell.

    Args:
        max_length (int): Maximale Anzahl der Zeichen für den generierten Text.

    Returns:
        str: Ein generierter Text mit maximal `max_length` Zeichen.
    """
    corpus = load_corpus()

    # Erstelle ein Markov-Modell aus dem geladenen Korpus
    text_model = markovify.Text(corpus)

    # Generiere neuen Text bis zur gewünschten Länge
    generated_text = ""
    while len(generated_text) < max_length:
        sentence = text_model.make_sentence(tries=100)
        if sentence:
            generated_text += " " + sentence
        else:
            break  # Falls keine weiteren Sätze generiert werden können

    # Text auf die maximale Länge zuschneiden
    return generated_text.strip()[:max_length]
