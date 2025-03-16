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

import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()
available_fonts = tkFont.families()
root.destroy()

if "Rubik" in available_fonts:
    print("✅ Rubik ist in Tkinter verfügbar!")
else:
    print("❌ Rubik wurde nicht von Tkinter erkannt.")
