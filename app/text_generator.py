import os
import markovify
from app.config import MAX_TEXT_LENGTH  # ✅ Korrekt importieren mit "app."

# Pfad zur Datei mit dem Basiskorpus
BASE_CORPUS_PATH = os.path.join(os.path.dirname(__file__), '../resources/base_corpus.txt')

def load_corpus():
    if not os.path.exists(BASE_CORPUS_PATH):
        raise FileNotFoundError(f"Korpusdatei nicht gefunden: {BASE_CORPUS_PATH}")

    with open(BASE_CORPUS_PATH, 'r', encoding='utf-8') as file:
        corpus = file.read().strip()

    print(f"DEBUG: Corpus geladen, Länge: {len(corpus)} Zeichen")  # Debugging-Ausgabe

    if not corpus:
        raise ValueError("ERROR: Die Korpusdatei ist leer! Bitte fülle `base_corpus.txt` mit Text.")

    return corpus

def get_new_text(max_length=MAX_TEXT_LENGTH):  # ✅ MAX_TEXT_LENGTH ist jetzt richtig definiert
    corpus = load_corpus()
    print(f"Corpus loaded successfully. Length: {len(corpus)} characters.")  # Debugging-Ausgabe

    text_model = markovify.Text(corpus, state_size=2)
    print("Markov model created successfully.")  # Debugging-Ausgabe

    generated_text = ""

    while len(generated_text) < max_length:
        sentence = text_model.make_sentence(tries=100)
        if sentence:
            if len(generated_text) + len(sentence) + 1 > max_length:
                break
            generated_text += " " + sentence
        else:
            break

    print(f"Generated text: {generated_text[:50]}...")  # Zeigt den ersten Teil des generierten Textes an
    return generated_text.strip()
