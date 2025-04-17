import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ollama
import re
import sv_ttk

# Generate flashcards using Ollama + phi
def generate_flashcards(text):
    prompt = f"""
Create exactly 5 study flashcards from the article below.

Each flashcard should be formatted as:
1. Question
- Answer

Be concise but informative.

Do not include any sentences that are not included in the format provided. Do not make answers too long, more than 5 sentences is too much.
Only include information from the article. No math problems, no word problems, nothing extra. Only things from the article provided.
Do not include any greetings or things like Here are the study flashcards. Only include the question and answer in the format above.
After the 5 questions, stop writing. Do not write anything before or after the five questions.
Make sure the questions and answers are complete.
Article:
{text}
"""
    try:
        response = ollama.chat(model='phi', messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"ERROR: {e}"

def parse_flashcards(raw_text):
    lines = raw_text.strip().splitlines()
    flashcards = []
    current_q = None
    current_a = []

    for line in lines:
        line = line.strip()

        match = re.match(r"^\d+\.\s*(.*)\?", line)
        if match:
            if current_q and current_a:
                flashcards.append({
                    'question': current_q,
                    'answer': ' '.join(current_a).strip()
                })
            current_q = match.group(1)
            current_a = []
            continue

        if line.startswith("Answer:"):
            current_a = [line.replace("Answer:", "").strip()]
            continue

        if line.startswith("-"):
            cleaned_line = line.lstrip("-").strip()
            if cleaned_line:
                current_a.append(cleaned_line)

    if current_q and current_a:
        flashcards.append({
            'question': current_q,
            'answer': ' '.join(current_a).strip()
        })

    return flashcards

def show_flashcards(flashcard_data):
    flashcard_window = tk.Toplevel()
    flashcard_window.title("Flashcards Viewer")
    flashcard_window.geometry("800x600")  # Ensures window has a size
    sv_ttk.set_theme("dark")

    flashcard_window.columnconfigure(0, weight=1)
    flashcard_window.rowconfigure(0, weight=1)
    flashcard_window.rowconfigure(1, weight=0)

    current_index = [0]
    showing_question = [True]
    content_var = tk.StringVar()
    font_size = 28

    label = ttk.Label(
        flashcard_window,
        textvariable=content_var,
        font=("Segoe UI", font_size),
        anchor="center",
        wraplength=1200,
        justify="center"
    )
    label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=40, pady=40)

    def update_card():
        card = flashcard_data[current_index[0]]
        text = card['question'] if showing_question[0] else card['answer']
        content_var.set(f"Q: {text}" if showing_question[0] else f"A: {text}")

    def flip():
        showing_question[0] = not showing_question[0]
        update_card()

    def next_card():
        if current_index[0] < len(flashcard_data) - 1:
            current_index[0] += 1
            showing_question[0] = True
            update_card()

    def prev_card():
        if current_index[0] > 0:
            current_index[0] -= 1
            showing_question[0] = True
            update_card()

    ttk.Button(flashcard_window, text="Previous", command=prev_card).grid(row=1, column=0, sticky="ew", padx=10, pady=20)
    ttk.Button(flashcard_window, text="Flip", command=flip).grid(row=1, column=1, sticky="ew", padx=10, pady=20)
    ttk.Button(flashcard_window, text="Next", command=next_card).grid(row=1, column=2, sticky="ew", padx=10, pady=20)

    for i in range(3):
        flashcard_window.columnconfigure(i, weight=1)

    flashcard_window.bind("<Escape>", lambda e: flashcard_window.attributes("-fullscreen", False))

    # Call update_card to show the first flashcard
    update_card()

def run_flashcard_generator():
    root = tk.Tk()
    root.title("Flashcard Generator")
    root.geometry("800x600")
    sv_ttk.set_theme("dark")

    ttk.Label(root, text="Paste Article Text:").pack(anchor="w", padx=10, pady=(10, 5))

    text_input = tk.Text(root, height=15, wrap="word", font=("Segoe UI", 12))
    text_input.pack(fill="both", expand=True, padx=10)

    def browse_file():
        file_path = filedialog.askopenfilename(title="Select an Article File", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                text_input.delete("1.0", tk.END)
                text_input.insert(tk.END, content)

    def generate():
        content = text_input.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Missing Text", "Please paste or load article content first.")
            return
        raw = generate_flashcards(content)
        if raw.startswith("ERROR"):
            messagebox.showerror("AI Error", raw)
            return
        data = parse_flashcards(raw)
        if not data:
            messagebox.showwarning("No Flashcards", "Flashcard generation failed.")
            return
        show_flashcards(data)

    frame = ttk.Frame(root)
    frame.pack(fill="x", padx=10, pady=10)

    ttk.Button(frame, text="Browse File", command=browse_file).pack(side="left", padx=5)
    ttk.Button(frame, text="Generate Flashcards", command=generate).pack(side="right", padx=5)

    root.mainloop()
