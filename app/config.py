import os

# Pfad zur SQLite-Datenbank
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/database.db')

# Pfad zum Basiskorpus für die Textgenerierung
BASE_CORPUS_PATH = os.path.join(os.path.dirname(__file__), '../resources/base_corpus.txt')

# Maximale Länge der generierten Texte
MAX_TEXT_LENGTH = 300

# Standardsprachmodell für spaCy
SPACY_LANGUAGE_MODEL = "de_core_news_sm"

# Anzahl der problematischsten Zeichen, die analysiert werden sollen
TOP_PROBLEMATIC_CHARS = 5

# Standard-Parameter für Markovify
MARKOVIFY_TRIES = 100  # Anzahl der Versuche, um gültige Sätze zu generieren
MARKOVIFY_STATE_SIZE = 2  # Zustand für die Markov-Kette (je höher, desto kontextbewusster)
