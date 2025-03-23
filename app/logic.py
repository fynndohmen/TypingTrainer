import time
from app import text_generator

# Global variables for typing session state
start_time = None
end_time = None
error_count = 0
total_chars_typed = 0

# In-memory keystroke storage
typed_data = []  # e.g. [{"char": "z", "correct": False, "time": 0.12}, ...]
last_keystroke_time = None

def get_new_text():
    """
    Fetches a new text from text_generator.
    Ensures it's at most 300 characters long.
    """
    text = text_generator.get_new_text()
    return text[:300]

def reset_stats():
    """
    Resets all counters and timers before a new typing session.
    """
    global start_time, end_time, error_count, total_chars_typed
    start_time = None
    end_time = None
    error_count = 0
    total_chars_typed = 0
    # typed_data is not cleared here; call clear_typed_data() after the session

def start_timing():
    """
    Records the start time of a typing session.
    """
    global start_time, last_keystroke_time
    start_time = time.time()
    last_keystroke_time = None

def stop_timing():
    """
    Records the end time of a typing session.
    No further action is needed since data is not saved to disk.
    """
    global end_time
    end_time = time.time()

def record_keystroke(expected_char, correct):
    """
    Records a single keystroke with timing and correctness.

    expected_char (str): The expected character to type.
    correct (bool): Whether the character was typed correctly.
    """
    global error_count, total_chars_typed, last_keystroke_time, typed_data

    total_chars_typed += 1
    if not correct:
        error_count += 1

    current_time = time.time()
    typed_time = 0.0
    if last_keystroke_time is not None:
        typed_time = current_time - last_keystroke_time
    last_keystroke_time = current_time

    typed_data.append({
        "char": expected_char,
        "correct": correct,
        "time": typed_time
    })

def clear_typed_data():
    """
    Clears all stored keystroke data at the end of a session.
    """
    global typed_data, last_keystroke_time
    typed_data.clear()
    last_keystroke_time = None
