import sys
import os

from app.data import initialize_database
from app.gui import start_gui

def main():
    # Stelle sicher, dass die Datenbank initialisiert ist
    initialize_database()

    # Starte die GUI
    start_gui()

if __name__ == "__main__":
    main()
