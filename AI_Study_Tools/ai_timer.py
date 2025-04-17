import time
import threading
import tkinter as tk
import random
import ollama
import sv_ttk  # Import sv_ttk for theming
from tkinter import ttk  # Import ttk for themed widgets

# Fallback quotes list (optimized to be small and efficient)
fallback_quotes = [
    "You're making steady progress. Keep pushing.",
    "Every second counts! Stay focused.",
    "You're doing great! Stay on track.",
    "Keep going. You're building momentum.",
    "You're one step closer to your goal.",
    "Stay strong. You’ve got this.",
    "Small steps lead to big wins.",
    "What you're doing now matters.",
    "One second at a time. Keep moving.",
    "Progress is happening right now.",
    "Keep grinding. It’s working.",
    "This moment is a part of the story.",
    "Real work happens when no one's watching.",
    "Keep your head down. Keep building.",
    "Greatness comes from repetition.",
    "You’re in the zone. Stay there.",
    "Trust the process. You’re on track.",
    "Success is forged in silence.",
    "Focus now, shine later.",
    "You are becoming unstoppable."
]

# Function to create buttons with ttk
def create_button(parent, text, command):
    button = ttk.Button(parent, text=text, command=command, width=30, padding=(5, 10), style="Custom.TButton")
    button.pack(pady=30, padx=15)
    return button

# Function to get a fallback quote
def get_fallback_quote():
    return random.choice(fallback_quotes)

# Function to get a motivational quote from the AI
def get_motivational_quote(total_seconds, total_minutes):
    prompt = (
        f"There are {total_seconds} seconds left in a {total_minutes}-minute study session. "
        f"Give ONE short, motivating sentence that makes me feel progress is being made. "
        f"No math, no quotes, no extra things. Just one direct, motivating sentence. "
    )

    result = {"quote": None}

    def fetch_quote():
        try:
            response = ollama.chat(model='phi', messages=[
                {'role': 'user', 'content': prompt}
            ])
            quote = response['message']['content'].strip()

        except Exception:
            result["quote"] = get_fallback_quote()

    quote_thread = threading.Thread(target=fetch_quote)
    quote_thread.start()
    quote_thread.join(timeout=15)

    if result["quote"] is None:
        result["quote"] = get_fallback_quote()

    return result["quote"]

# Main function to launch the timer
def launch_ai_timer():
    def show_timer_input_screen():
        timer_input_frame = tk.Toplevel()
        timer_input_frame.title("AI Timer")
        sv_ttk.set_theme('dark')  # Apply dark theme

        label = tk.Label(timer_input_frame, text="Enter study timer duration (minutes):", font=("Segoe UI", 28))
        label.pack(pady=25)

        timer_input = tk.Entry(timer_input_frame, width=20, font=("Segoe UI", 28), bg="#D3D3D3", fg="black")
        timer_input.pack(pady=25)

        def get_duration():
            try:
                mins = int(timer_input.get())
                start_ai_timer(mins)
                timer_input_frame.destroy()
            except ValueError:
                error_label.config(text="Please enter a valid number.")

        error_label = tk.Label(timer_input_frame, text="", fg="red", font=("Segoe UI", 16))
        error_label.pack(pady=10)

        create_button(timer_input_frame, "Start Timer", get_duration)

    def start_ai_timer(duration_minutes):
        timer_frame = tk.Toplevel()
        timer_frame.title("AI Timer")

        # Make timer window big and centered
        timer_frame.geometry("800x600")
        timer_frame.update_idletasks()
        screen_width = timer_frame.winfo_screenwidth()
        screen_height = timer_frame.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (600 // 2)
        timer_frame.geometry(f"+{x}+{y}")

        countdown_label = tk.Label(timer_frame, text="Time left: 00:00", font=("Segoe UI", 35),
                                   anchor="center", justify="center")
        countdown_label.pack(pady=25, fill=tk.BOTH, expand=True)

        quote_label = tk.Label(timer_frame, text="", wraplength=700, font=("Segoe UI", 25),
                               anchor="center", justify="center")
        quote_label.pack(pady=30, fill=tk.BOTH, expand=True)

        state = {'running': False, 'paused': False, 'time_left': duration_minutes * 60}

        def schedule_quote():
            if state['running']:
                threading.Thread(target=generate_quote, daemon=True).start()
                delay = random.randint(10000, 30000)  # 20–30 seconds
                timer_frame.after(delay, schedule_quote)

        def update_timer():
            while state['time_left'] > 0 and state['running']:
                if not state['paused']:
                    minutes, seconds = divmod(state['time_left'], 60)
                    time_str = f"{minutes:02}:{seconds:02}"
                    countdown_label.config(text=f"Time left: {time_str}")
                    state['time_left'] -= 1
                time.sleep(1)

            if state['running']:
                countdown_label.config(text="✅ Time’s up!")
                state['running'] = False

        def generate_quote():
            quote = get_motivational_quote(state['time_left'], duration_minutes)
            quote_label.config(text=quote)

        def start_timer():
            state['running'] = True
            threading.Thread(target=update_timer, daemon=True).start()
            threading.Thread(target=generate_quote, daemon=True).start()  # Initial quote
            schedule_quote()

        def toggle_pause():
            state['paused'] = not state['paused']
            pause_button.config(text="Resume Timer" if state['paused'] else "Pause Timer")

        def reset_timer():
            state['running'] = False
            state['time_left'] = duration_minutes * 60
            timer_frame.destroy()
            start_ai_timer(duration_minutes)

        start_timer()
        pause_button = create_button(timer_frame, "Pause Timer", toggle_pause)
        create_button(timer_frame, "Reset Timer", reset_timer)

    show_timer_input_screen()
