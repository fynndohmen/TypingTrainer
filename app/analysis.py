import nltk
from collections import Counter
import spacy

# Lade das spaCy-Modell für Deutsch (falls verwendet)
try:
    nlp = spacy.load("en_core_news_sm")
except:
    nlp = None
    print("Hinweis: Das spaCy-Modell 'de_core_news_sm' wurde nicht geladen. Installiere es mit 'python -m spacy download de_core_news_sm'.")

def analyze_typing_errors(typing_data):
    """
    Analysiert Tippdaten, um problematische Zeichen zu identifizieren.

    Args:
        typing_data (list): Liste von Dictionaries mit Tippdaten,
            z.B. [{"char": "e", "time": 0.3, "correct": True}, ...]

    Returns:
        dict: Problematische Zeichen mit durchschnittlicher Tippzeit und Fehleranzahl.
    """
    char_stats = {}

    for entry in typing_data:
        char = entry["char"]
        time = entry["time"]
        correct = entry["correct"]

        if char not in char_stats:
            char_stats[char] = {"total_time": 0, "count": 0, "errors": 0}

        char_stats[char]["total_time"] += time
        char_stats[char]["count"] += 1
        if not correct:
            char_stats[char]["errors"] += 1

    # Berechne die durchschnittliche Tippzeit für jedes Zeichen
    for char in char_stats:
        stats = char_stats[char]
        stats["average_time"] = stats["total_time"] / stats["count"] if stats["count"] > 0 else 0

    return char_stats

def most_problematic_chars(typing_data, top_n=5):
    """
    Gibt die problematischsten Zeichen basierend auf Tippfehlern und Tippzeit zurück.

    Args:
        typing_data (list): Liste von Dictionaries mit Tippdaten.
        top_n (int): Anzahl der problematischsten Zeichen, die zurückgegeben werden.

    Returns:
        list: Die problematischsten Zeichen sortiert nach Fehlern und Zeit.
    """
    char_stats = analyze_typing_errors(typing_data)
    # Sortiere nach Tippfehlern, dann nach durchschnittlicher Tippzeit
    sorted_chars = sorted(char_stats.items(), key=lambda x: (-x[1]["errors"], x[1]["average_time"]))
    return sorted_chars[:top_n]

def letter_frequency_analysis(text):
    """
    Analysiert die Häufigkeit von Buchstaben in einem Text.

    Args:
        text (str): Eingabetext.

    Returns:
        list: Liste von Tupeln mit Buchstaben und deren Häufigkeiten, sortiert nach Häufigkeit.
    """
    text = text.lower()  # Kleinbuchstaben vereinheitlichen
    frequencies = Counter(char for char in text if char.isalpha())  # Nur Buchstaben zählen
    return frequencies.most_common()

def analyze_with_spacy(text):
    """
    Führt eine spaCy-Analyse durch (z. B. Tokenisierung, Wortartenanalyse).

    Args:
        text (str): Eingabetext.

    Returns:
        list: Liste von Tokens und deren Wortarten (falls spaCy verfügbar ist).
    """
    if not nlp:
        raise RuntimeError("spaCy-Modell ist nicht geladen. Installiere es mit 'python -m spacy download de_core_news_sm'.")

    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]

