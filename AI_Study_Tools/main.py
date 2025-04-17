import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from flashcards import run_flashcard_generator
from ai_timer import launch_ai_timer
from ai_concept_explainer import launch_ai_concept_explainer
import sv_ttk

class ResponsiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Study Tools")

        # Start fullscreen
        self.root.attributes("-fullscreen", True)

        self.font_size = 12
        self.button_font = tkfont.Font(family="Segoe UI", size=self.font_size)
        self.title_font = tkfont.Font(family="Segoe UI", size=self.font_size + 6, weight="bold")

        sv_ttk.set_theme("dark")

        self.style = ttk.Style()
        self.style.configure("Rounded.TButton",
                             font=self.button_font,
                             padding=(8, 6),
                             relief="solid",
                             background="#1f1f1f",
                             foreground="white",
                             bordercolor="#2a2a2a",
                             borderwidth=2)
        self.style.map("Rounded.TButton", background=[], foreground=[])

        self.create_layout()
        self.root.bind("<Configure>", self.on_resize)

        # Optional: Exit fullscreen on ESC
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

    def create_layout(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        for i in range(5):  # 4 buttons + 1 title
            self.main_frame.rowconfigure(i, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        title_label = tk.Label(self.main_frame, text="AI Study Tools", font=self.title_font, fg="white")
        title_label.grid(row=0, column=0, sticky="n", pady=(0, 20))

        self.buttons = []

        entries = [
            ("Flashcard Generator", run_flashcard_generator),
            ("AI Concept Explainer", launch_ai_concept_explainer),
            ("AI Study Timer", launch_ai_timer),
            ("Quit", self.root.quit)
        ]

        for i, (text, cmd) in enumerate(entries):
            btn = ttk.Button(self.main_frame, text=text, command=cmd, style="Rounded.TButton")
            btn.grid(row=i + 1, column=0, sticky="nsew", pady=6, padx=10)
            self.buttons.append(btn)

    def on_resize(self, event):
        width = self.root.winfo_width()
        new_size = max(10, int(width / 30))
        if new_size != self.font_size:
            self.font_size = new_size
            self.button_font.configure(size=self.font_size)
            self.title_font.configure(size=self.font_size + 6)
            self.style.configure("Rounded.TButton", font=self.button_font)


if __name__ == "__main__":
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app = ResponsiveApp(root)
    root.mainloop()
