import os

# Path to the base corpus for text generation
BASE_CORPUS_PATH = os.path.join(os.path.dirname(__file__), '../resources/base_corpus.txt')

# Maximum length of the generated texts
MAX_TEXT_LENGTH = 300

# Number of problematic characters to analyze
TOP_PROBLEMATIC_CHARS = 15

# Default parameters for Markovify
MARKOVIFY_TRIES = 100  # Number of attempts to generate valid sentences
MARKOVIFY_STATE_SIZE = 1  # State size for the Markov chain (higher = more context-aware)
