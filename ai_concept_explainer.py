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
                f"Include a real-world analogy if appropriate. If it's a problem (like a math or word problem), solve it step by step. "
                f"If not a word or math problem, then do not include any math or word problems that do not relate to the topic provided. "
                f"Do not include math problems when not asked."
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
    window.geometry("800x600")
    sv_ttk.set_theme("dark")

    # Configure grid
    for i in range(4):
        window.rowconfigure(i, weight=(1 if i == 2 else 0))
    window.columnconfigure(0, weight=1)

    # Label (on its own row)
    label = ttk.Label(window, text="Input any concept or problem below:", font=("Segoe UI", 16))
    label.grid(row=0, column=0, padx=20, pady=(30, 5), sticky="n")

    # Input Entry
    input_entry = ttk.Entry(window, font=("Segoe UI", 14))
    input_entry.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="ew")

    # Output Text Area with Scrollbar
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

    # Allow Esc to exit fullscreen
    window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))

    # Center window
    window.update_idletasks()
    width, height = window.winfo_width(), window.winfo_height()
    screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry(f'{width}x{height}+{(screen_width - width) // 2}+{(screen_height - height) // 2}')

    window.mainloop()
