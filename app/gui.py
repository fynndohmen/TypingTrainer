import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
from app import logic
from PIL import ImageFont  # Für manuelles Laden von .ttf-Schriften

class TypingTrainerGUI:
    def __init__(self, master, width=1000, height=500):
        self.master = master
        self.master.title("TypingTrainer")
        self.master.configure(bg="#222222")
        self.master.geometry(f"{width}x{height}")

        # 📌 Schriftart laden
        font_path = os.path.join(os.path.dirname(__file__), "../resources/fonts/Rubik-Regular.ttf")

        if os.path.exists(font_path):
            print(f"✅ Schriftart gefunden: {font_path}")
            try:
                font = ImageFont.truetype(font_path, 36)  # Teste, ob die Datei gültig ist
                tkFont.nametofont("TkDefaultFont").configure(family="Rubik", size=36)
                self.font_family = "Rubik"
            except Exception as e:
                print(f"⚠️ Fehler beim Laden der Schriftart: {e} - Fallback auf Arial.")
                self.font_family = "Arial"
        else:
            print("❌ Fehler: Schriftart nicht gefunden! Fallback auf Arial.")
            self.font_family = "Arial"

        # Schriftart setzen
        self.font_main = tkFont.Font(family=self.font_family, size=36)
        self.font_status = tkFont.Font(family=self.font_family, size=14)

        # GUI States
        self.state = "idle"

        # Hauptframe
        main_frame = ttk.Frame(self.master, padding="10", style="Main.TFrame")
        main_frame.grid(sticky=(tk.W, tk.E, tk.N, tk.S))

        # Anzeige-Textfeld
        self.display_text = tk.Text(main_frame, wrap="word", bg="#2A2A2A", fg="#AAAAAA",
                                    state="disabled", font=self.font_main)
        self.display_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Statusleiste mit weißem Hintergrund und schwarzem Text
        status_frame = ttk.Frame(main_frame, padding="5", style="Status.TFrame")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.status_var = tk.StringVar(value="Willkommen! Drücke Enter, um einen neuen Text zu laden.")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, foreground="black",
                                      background="white", font=self.font_status)
        self.status_label.grid(sticky=(tk.W, tk.E))

        # Skalierung ermöglichen
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Interner Index für das nächste zu tippende Zeichen
        self.current_index = 0
        self.current_text = ""

        # Tastatureingaben binden
        self.master.bind("<Key>", self.on_key_press)

        # Text-Tags für Farbe und Unterstreichung
        self.display_text.tag_configure("typed", foreground="#FFFFFF")  # Getippte Zeichen = Weiß
        self.display_text.tag_configure("untouched", foreground="#AAAAAA")  # Noch nicht getippte Zeichen = Hellgrau
        self.display_text.tag_configure("underline", underline=True, foreground="yellow")  # 🔥 Gelbe Unterstreichung

    def load_new_text(self):
        """Neuen Text laden und anzeigen."""
        self.current_text = logic.get_new_text()
        self.current_index = 0

        self.display_text.config(state="normal")
        self.display_text.delete("1.0", tk.END)
        self.display_text.insert("1.0", self.current_text)
        self.display_text.tag_add("untouched", "1.0", tk.END)
        self.display_text.config(state="disabled")

        self.status_var.set("Text geladen. Drücke Enter, um das Tippen zu starten.")
        self.state = "text_loaded_not_started"

        self.update_underline()  # 🆕 Unterstreichung setzen

    def start_typing(self):
        """Startet die Tipp-Zeitmessung und setzt Fehlerzählung zurück."""
        logic.reset_stats()
        logic.start_timing()
        self.state = "typing_in_progress"
        self.status_var.set("Tippe den angezeigten Text ab...")

    def complete_text(self):
        """Wird aufgerufen, wenn der Nutzer den gesamten Text fertig getippt hat."""
        logic.stop_timing()
        self.status_var.set("Super! Drücke Enter, um einen neuen Text zu laden.")
        self.state = "text_completed"

    def on_key_press(self, event):
        """Verarbeitet jeden Tastendruck."""
        if event.keysym == "Return":
            if self.state == "idle":
                self.load_new_text()
            elif self.state == "text_loaded_not_started":
                self.start_typing()
            elif self.state == "text_completed":
                self.load_new_text()
            return

        if self.state == "typing_in_progress":
            typed_char = event.char
            if typed_char and len(typed_char) == 1:
                expected_char = self.current_text[self.current_index] if self.current_index < len(self.current_text) else ""
                if typed_char == expected_char:
                    logic.record_keystroke(correct=True)
                    self.display_text.config(state="normal")

                    start_idx = f"1.0 + {self.current_index} chars"
                    end_idx = f"1.0 + {self.current_index+1} chars"

                    self.display_text.tag_remove("untouched", start_idx, end_idx)
                    self.display_text.tag_add("typed", start_idx, end_idx)

                    self.display_text.config(state="disabled")
                    self.current_index += 1

                    if self.current_index >= len(self.current_text):
                        self.complete_text()
                    else:
                        self.update_underline()  # 🆕 Nach jeder Eingabe aktualisieren
                else:
                    logic.record_keystroke(correct=False)

    def update_underline(self):
        """Setzt die Unterstreichung unter das aktuelle Zeichen."""
        self.display_text.tag_remove("underline", "1.0", tk.END)  # Entfernt vorherige Unterstreichung
        if self.current_index < len(self.current_text):  # Falls noch Zeichen übrig sind
            start_idx = f"1.0 + {self.current_index} chars"
            end_idx = f"1.0 + {self.current_index + 1} chars"
            self.display_text.tag_add("underline", start_idx, end_idx)  # Setzt die gelbe Unterstreichung

def start_gui(width=1300, height=700):
    root = tk.Tk()
    app = TypingTrainerGUI(root, width, height)
    root.mainloop()
