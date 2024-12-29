import time
from app import data
from app import text_generator

# Globale Variablen für den Tippstatus
start_time = None
end_time = None
error_count = 0
total_chars_typed = 0

def get_new_text():
    """
    Holt einen neuen Text von der Textgenerierung.
    Erwartet einen ca. 300 Zeichen langen Text.
    """
    text = text_generator.get_new_text()
    # Optional: Stelle sicher, dass der Text max. 300 Zeichen hat
    text = text[:300]
    return text

def reset_stats():
    """Setzt alle Zähler und Zeiten zurück, bevor eine neue Tippübung beginnt."""
    global start_time, end_time, error_count, total_chars_typed
    start_time = None
    end_time = None
    error_count = 0
    total_chars_typed = 0

def start_timing():
    """Setzt den Startzeitpunkt, um die Tippdauer zu messen."""
    global start_time
    start_time = time.time()

def stop_timing():
    """Setzt den Endzeitpunkt, berechnet die Dauer und speichert die Session-Statistiken."""
    global end_time
    end_time = time.time()

    # Dauer der Tippübung ermitteln
    duration = 0
    if start_time is not None:
        duration = end_time - start_time

    # Speichere die Session-Daten in der Datenbank
    data.save_session_stats(duration, error_count, total_chars_typed)

def record_keystroke(correct):
    """
    Erfasst einen einzelnen Tastendruck.
    correct: Bool, True wenn richtig getippt, False wenn falsch
    """
    global error_count, total_chars_typed
    total_chars_typed += 1
    if not correct:
        error_count += 1
