import sys
import os

from app.gui import start_gui

def main():

    start_gui()

if __name__ == "__main__":
    main()

import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()
available_fonts = tkFont.families()
root.destroy()

if "Rubik" in available_fonts:
    print("✅ Rubik is available in Tkinter!")
else:
    print("❌ Rubik was not recognized by Tkinter.")
