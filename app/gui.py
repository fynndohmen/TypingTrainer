import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os

from app import logic
from app import analysis
from app import text_generator

class TypingTrainerGUI:
    def __init__(self, master, width=1000, height=500):
        self.master = master
        self.master.title("TypingTrainer")
        self.master.configure(bg="#222222")
        self.master.geometry(f"{width}x{height}")

        font_path = os.path.join(os.path.dirname(__file__), "../resources/fonts/Rubik-Regular.ttf")
        self.font_family = "Arial"

        self.font_main = tkFont.Font(family=self.font_family, size=36)
        self.font_status = tkFont.Font(family=self.font_family, size=14)

        self.state = "idle"

        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(sticky=(tk.W, tk.E, tk.N, tk.S))

        self.display_text = tk.Text(main_frame, wrap="word", bg="#2A2A2A", fg="#AAAAAA",
                                    state="disabled", font=self.font_main)
        self.display_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        status_frame = ttk.Frame(main_frame, padding="5")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.status_var = tk.StringVar(value="Welcome! Press Enter to load a new text.")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, foreground="#808080",
                                      background="white", font=self.font_status)
        self.status_label.grid(sticky=(tk.W, tk.E))

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.current_index = 0
        self.current_text = ""
        self.error_flags = {}

        self.master.bind("<Key>", self.on_key_press)

        # Text tags
        self.display_text.tag_configure("typed", foreground="#FFFFFF")
        self.display_text.tag_configure("untouched", foreground="#AAAAAA")
        self.display_text.tag_configure("underline", underline=True, foreground="yellow")
        self.display_text.tag_configure("incorrect", foreground="#FF0000")
        self.display_text.tag_configure("weak_incorrect", foreground="#FF8888")

        self.problem_chars_for_next = None

    def load_new_text(self, problem_chars=None):
        self.current_index = 0
        self.error_flags = {}
        if problem_chars:
            self.current_text = text_generator.get_new_text(problem_chars=problem_chars)
        else:
            self.current_text = text_generator.get_new_text()

        self.display_text.config(state="normal")
        self.display_text.delete("1.0", tk.END)
        self.display_text.insert("1.0", self.current_text)
        self.display_text.tag_add("untouched", "1.0", tk.END)
        self.display_text.config(state="disabled")

        self.status_var.set("Text loaded. Press Enter to start typing.")
        self.state = "text_loaded_not_started"
        self.update_underline()

    def start_typing(self):
        logic.reset_stats()
        logic.start_timing()
        self.state = "typing_in_progress"
        self.status_var.set("Type the text...")

    def complete_text(self):
        logic.stop_timing()
        self.show_mistake_stats()
        top_problems = analysis.most_problematic_chars(logic.typed_data)
        self.problem_chars_for_next = [p[0] for p in top_problems]
        logic.clear_typed_data()
        self.state = "showing_stats"
        self.status_var.set("Mistakes shown - Press Enter to load new text.")

    def show_mistake_stats(self):
        self.display_text.config(state="normal")
        self.display_text.delete("1.0", tk.END)

        char_stats = analysis.analyze_typing_errors(logic.typed_data)
        lines = ["Mistakes:"]
        any_mistakes = False
        for ch, stats in char_stats.items():
            if stats["errors"] > 0:
                lines.append(f"{ch}: {stats['errors']}")
                any_mistakes = True
        if not any_mistakes:
            lines.append("No mistakes made! Great job!")

        stats_text = "\n".join(lines)
        self.display_text.insert("1.0", stats_text)
        self.display_text.config(state="disabled")

    def on_key_press(self, event):
        if event.keysym == "Return":
            if self.state == "idle":
                self.load_new_text()
            elif self.state == "text_loaded_not_started":
                self.start_typing()
            elif self.state == "text_completed":
                self.load_new_text()
            elif self.state == "showing_stats":
                if self.problem_chars_for_next:
                    self.load_new_text(problem_chars=self.problem_chars_for_next)
                else:
                    self.load_new_text()
            return

        if self.state == "typing_in_progress":
            typed_char = event.char
            if typed_char and len(typed_char) == 1:
                if self.current_index < len(self.current_text):
                    expected_char = self.current_text[self.current_index]
                else:
                    expected_char = ""

                if typed_char == expected_char:
                    logic.record_keystroke(expected_char, correct=True)
                    typed_time = 0.0
                    if logic.typed_data:
                        typed_time = logic.typed_data[-1]["time"]

                    self.display_text.config(state="normal")
                    start_idx = f"1.0 + {self.current_index} chars"
                    end_idx = f"1.0 + {self.current_index+1} chars"
                    self.display_text.tag_remove("untouched", start_idx, end_idx)

                    if typed_time > 1.0:
                        self.display_text.tag_add("weak_incorrect", start_idx, end_idx)
                    else:
                        self.display_text.tag_add("typed", start_idx, end_idx)

                    self.display_text.config(state="disabled")

                    self.current_index += 1
                    if self.current_index >= len(self.current_text):
                        self.state = "text_completed"
                        self.complete_text()
                    else:
                        self.update_underline()
                else:
                    logic.record_keystroke(expected_char, correct=False)
                    self.display_text.config(state="normal")
                    start_idx = f"1.0 + {self.current_index} chars"
                    end_idx = f"1.0 + {self.current_index+1} chars"
                    self.display_text.tag_remove("untouched", start_idx, end_idx)
                    self.display_text.tag_add("incorrect", start_idx, end_idx)
                    self.display_text.config(state="disabled")

    def update_underline(self):
        self.display_text.config(state="normal")
        self.display_text.tag_remove("underline", "1.0", tk.END)
        if self.current_index < len(self.current_text):
            start_idx = f"1.0 + {self.current_index} chars"
            end_idx = f"1.0 + {self.current_index + 1} chars"
            self.display_text.tag_add("underline", start_idx, end_idx)
        self.display_text.config(state="disabled")

def start_gui(width=1300, height=700):
    root = tk.Tk()
    app = TypingTrainerGUI(root, width, height)
    root.mainloop()
