import tkinter as tk
from tkinter import ttk
from app import logic

class TypingTrainerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("TypingTrainer")

        # States:
        # "idle" – kein Text geladen
        # "text_loaded_not_started" – Text geladen, aber Tippvorgang noch nicht gestartet
        # "typing_in_progress" – Nutzer tippt gerade
        # "text_completed" – Text ist fertig getippt, warte auf Enter für neuen Text
        self.state = "idle"

        # Hauptframe
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(sticky=(tk.W, tk.E, tk.N, tk.S))

        # Anzeige-Textfeld (read-only)
        self.display_text = tk.Text(main_frame, height=10, width=80, wrap="word",
                                    bg="#333333", fg="white", state="disabled", font=("Bookerly", 36))
        self.display_text.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Statusleiste
        status_frame = ttk.Frame(main_frame, padding="5")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.status_var = tk.StringVar(value="Willkommen! Drücke Enter, um einen neuen Text zu laden.")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.grid(sticky=(tk.W, tk.E))

        # Interner Index für das nächste zu tippende Zeichen
        self.current_index = 0
        self.current_text = ""

        # Tastatureingaben binden
        # Wir fangen alle Key-Events ab, um den Tippvorgang zu überwachen.
        self.master.bind("<Key>", self.on_key_press)

        # Text-Tag für bereits getippte Zeichen (ausgegraut)
        self.display_text.tag_configure("typed", foreground="#333333")

    def load_new_text(self):
        """Neuen Text laden und anzeigen."""
        self.current_text = logic.get_new_text()  # Diese Funktion musst du in logic.py umsetzen
        self.current_index = 0

        self.display_text.config(state="normal")
        self.display_text.delete("1.0", tk.END)
        self.display_text.insert("1.0", self.current_text)
        self.display_text.config(state="disabled")

        self.status_var.set("Text geladen. Drücke Enter, um das Tippen zu starten.")
        self.state = "text_loaded_not_started"

    def start_typing(self):
        """Startet die Tipp-Zeitmessung und setzt Fehlerzählung zurück."""
        logic.reset_stats()
        logic.start_timing()
        self.state = "typing_in_progress"
        self.status_var.set("Tippe den angezeigten Text ab...")

    def complete_text(self):
        """Wird aufgerufen, wenn der Nutzer den gesamten Text fertig getippt hat."""
        logic.stop_timing()
        # Hier könnte man Statistiken ausgeben oder im Statusfeld anzeigen
        self.status_var.set("Super! Drücke Enter, um einen neuen Text zu laden.")
        self.state = "text_completed"

    def on_key_press(self, event):
        """Verarbeitet jeden Tastendruck."""
        # Enter-Taste abhängig vom Zustand behandeln
        if event.keysym == "Return":
            if self.state == "idle":
                self.load_new_text()
            elif self.state == "text_loaded_not_started":
                self.start_typing()
            elif self.state == "text_completed":
                self.load_new_text()
            return

        # Wenn wir im Tippvorgang sind, prüfen wir das eingegebene Zeichen
        if self.state == "typing_in_progress":
            typed_char = event.char
            # Nur sichtbare Zeichen prüfen (Shift, Ctrl etc. ignorieren)
            if typed_char and len(typed_char) == 1:
                expected_char = self.current_text[self.current_index] if self.current_index < len(self.current_text) else ""
                if typed_char == expected_char:
                    # Richtiger Buchstabe
                    logic.record_keystroke(correct=True)
                    # Buchstaben als getippt markieren
                    self.display_text.config(state="normal")
                    start_idx = f"1.0 + {self.current_index} chars"
                    end_idx = f"1.0 + {self.current_index+1} chars"
                    self.display_text.tag_add("typed", start_idx, end_idx)
                    self.display_text.config(state="disabled")

                    self.current_index += 1

                    if self.current_index >= len(self.current_text):
                        self.complete_text()
                else:
                    # Falscher Buchstabe
                    logic.record_keystroke(correct=False)

def start_gui():
    root = tk.Tk()
    app = TypingTrainerGUI(root)
    root.mainloop()
