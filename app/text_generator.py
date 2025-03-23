import os
import random

# Path to the base corpus file
BASE_CORPUS_PATH = os.path.join(os.path.dirname(__file__), '../resources/base_corpus.txt')


def load_corpus_words():
    """
    Loads the content of BASE_CORPUS_PATH and splits it into words.
    Returns a list of words.
    """
    if not os.path.exists(BASE_CORPUS_PATH):
        raise FileNotFoundError(f"Corpus file not found: {BASE_CORPUS_PATH}")

    with open(BASE_CORPUS_PATH, 'r', encoding='utf-8') as file:
        content = file.read().strip()

    if not content:
        raise ValueError("ERROR: The corpus file is empty. Please fill `base_corpus.txt` with text.")

    return content.split()


def get_new_text(problem_chars=None, max_length=300):
    """
    Generates a random text (without Markovify) using whole words.
    - Considers up to 10 problematic characters.
    - Selects up to 3 words per problematic character.
    - Ensures the text doesn't exceed max_length.

    Args:
        problem_chars (list, optional): List of characters to emphasize.
        max_length (int, optional): Max length of the generated text in characters.

    Returns:
        str: A generated text with at least (3 * num_problem_chars) words
             if space allows, plus filler words, up to max_length.
    """
    words = load_corpus_words()
    if not words:
        return ""

    if not problem_chars:
        return build_random_text(words, max_length)

    filtered_chars = [c for c in problem_chars if c != ' ']
    limited_chars = filtered_chars[:10]

    mandatory_words = []
    current_text_len = 0
    for pc in limited_chars:
        pc_words = [w for w in words if pc in w]
        if pc_words:
            needed = min(3, len(pc_words))
            selected = random.sample(pc_words, needed)
            for w in selected:
                add_len = len(w) + 1
                if current_text_len + add_len <= max_length:
                    mandatory_words.append(w)
                    current_text_len += add_len

    def is_problem_word(w):
        return any(pc in w for pc in limited_chars)

    normal_words = [w for w in words if not is_problem_word(w)]

    final_words = list(mandatory_words)
    while current_text_len < max_length:
        if normal_words:
            w = random.choice(normal_words)
        else:
            w = random.choice(words)

        add_len = len(w) + 1
        if current_text_len + add_len <= max_length:
            final_words.append(w)
            current_text_len += add_len
        else:
            break

    random.shuffle(final_words)
    final_text = " ".join(final_words)
    return final_text[:max_length]


def build_random_text(words, max_length):
    """
    Builds a completely random text without mandatory words (no problem chars).
    """
    final_words = []
    current_len = 0
    while current_len < max_length:
        w = random.choice(words)
        add_len = len(w) + 1
        if current_len + add_len <= max_length:
            final_words.append(w)
            current_len += add_len
        else:
            break

    random.shuffle(final_words)
    return " ".join(final_words)
