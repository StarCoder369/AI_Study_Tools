import tkinter as tk
from tkinter import ttk
import ollama
import threading
import sv_ttk

def get_concept_explanation(prompt, display_widget):
    display_widget.config(state="normal")
    display_widget.delete("1.0", tk.END)
    display_widget.insert(tk.END, "Thinking...\n")
    display_widget.config(state="disabled")

    def fetch():
        try:
            query = (
                f"Explain the following in a simple, clear way, as if to a student: {prompt}.\n"
                f"Include a real-world analogy if appropriate. If it's a problem (like a math or word problem), solve it step by step."
                "If not a word or math problem, then do not include any math or word problems that do not relate to the topic provided."
                "Do no include math problems when not asked"
            )
            response = ollama.chat(model="phi", messages=[
                {"role": "user", "content": query}
            ])
            answer = response['message']['content'].strip()
        except Exception:
            answer = "Something went wrong. Please try again or check your connection."

        display_widget.config(state="normal")
        display_widget.delete("1.0", tk.END)
        display_widget.insert(tk.END, answer)
        display_widget.tag_add("error", "1.0", "end")
        display_widget.config(state="disabled")

    threading.Thread(target=fetch).start()

def launch_ai_concept_explainer():
    window = tk.Tk()
    window.title("AI Concept Explainer")
    window.geometry("800x600")  # Ensures window has a size
    sv_ttk.set_theme("dark")

    # Configure grid for centering and responsive resizing
    window.rowconfigure(0, weight=0)
    window.rowconfigure(1, weight=0)  # for the entry field
    window.rowconfigure(2, weight=1)  # for the text output area
    window.rowconfigure(3, weight=0)  # for the button
    window.columnconfigure(0, weight=1)

    # Input Entry (Expanded vertically)
    input_entry = ttk.Entry(window, font=("Segoe UI", 14))
    input_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
    input_entry.configure(background="light gray")

    # Output Text Area (inside a Frame with Scrollbar)
    text_frame = ttk.Frame(window)
    text_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
    text_frame.rowconfigure(0, weight=1)
    text_frame.columnconfigure(0, weight=1)

    output_text = tk.Text(text_frame, wrap=tk.WORD, relief="flat", font=("Segoe UI", 12))
    output_text.grid(row=0, column=0, sticky="nsew")

    output_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=output_text.yview)
    output_scrollbar.grid(row=0, column=1, sticky="ns")
    output_text.configure(yscrollcommand=output_scrollbar.set, state="disabled")

    output_text.tag_config("error", foreground="white")

    # Explain Button
    explain_button = ttk.Button(window, text="Explain It", command=lambda: get_concept_explanation(input_entry.get(), output_text), style="Rounded.TButton")
    explain_button.grid(row=3, column=0, pady=15, padx=20, sticky="ew")

    # Optional: Exit fullscreen with Escape
    window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))

    # Center the window on the screen
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int((screen_height - height) / 2)
    position_right = int((screen_width - width) / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

    window.mainloop()
