from collections import Counter


def analyze_typing_errors(typing_data):
    """
    Analyzes typing data to identify average time and error count per character.

    Args:
        typing_data (list): List of dicts like:
            [{"char": "e", "time": 0.3, "correct": True}, ...]

    Returns:
        dict: A dictionary with characters as keys and statistics as values, e.g.:
            {
                "e": {"total_time": 1.2, "count": 5, "errors": 2, "average_time": 0.24},
                ...
            }
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

    for char, stats in char_stats.items():
        stats["average_time"] = stats["total_time"] / stats["count"] if stats["count"] > 0 else 0

    return char_stats


def most_problematic_chars(typing_data, top_n=10):
    """
    Returns the top `top_n` most problematic characters based on a combined score.

    The score is calculated as:
        score = average_time + (1.0 * errors)

    Each error adds the equivalent of 1 second to the average time.
    Characters are sorted in descending order of this score.

    Args:
        typing_data (list): List of typing records.
        top_n (int): Number of characters to return.

    Returns:
        list: List of tuples (char, stats), sorted by score descending.
    """
    char_stats = analyze_typing_errors(typing_data)

    for char, stats in char_stats.items():
        avg_t = stats.get("average_time", 0)
        errs = stats.get("errors", 0)
        stats["score"] = avg_t + (errs * 1.0)

    sorted_chars = sorted(
        char_stats.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    return sorted_chars[:top_n]


def letter_frequency_analysis(text):
    """
    Analyzes frequency of each alphabetical character in the given text.

    Args:
        text (str): Input text.

    Returns:
        list: List of tuples (letter, frequency), sorted descending.
    """
    text = text.lower()
    frequencies = Counter(char for char in text if char.isalpha())
    return frequencies.most_common()
