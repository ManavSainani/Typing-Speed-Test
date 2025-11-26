import tkinter as tk
from tkinter import messagebox
import time
import random

# -------------------------
# Sample Text Passages
# -------------------------
passages = [
    "Typing fast requires practice and patience.",
    "Python is a versatile language used for many applications.",
    "The quick brown fox jumps over the lazy dog.",
    "Artificial intelligence is transforming the world rapidly.",
    "Consistency is the key to improving your typing speed."
]


class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x500")

        self.start_time = None
        self.sample_text = random.choice(passages)

        # -------- Display Sample Text --------
        self.text_label = tk.Label(
            root,
            text=self.sample_text,
            font=("Arial", 16),
            wraplength=760,
            justify="center"
        )
        self.text_label.pack(pady=20)

        # -------- Input Box --------
        self.input_box = tk.Text(root, height=8, font=("Arial", 14))
        self.input_box.pack(pady=20)
        self.input_box.bind("<KeyPress>", self.start_timer)

        # -------- Submit Button --------
        self.submit_btn = tk.Button(root, text="Finish", font=("Arial", 14), command=self.finish_test)
        self.submit_btn.pack()

        # Results Frame
        self.results_frame = tk.Frame(root)

    # -------------------------
    # Start timer on first key press
    # -------------------------
    def start_timer(self, event):
        if self.start_time is None:
            self.start_time = time.time()

    # -------------------------
    # WPM Calculation
    # -------------------------
    def calculate_wpm(self, typed_text, elapsed_time):
        words_typed = len(typed_text) / 5  # standard WPM formula
        minutes = elapsed_time / 60
        if minutes == 0:
            return 0
        return round(words_typed / minutes)

    # -------------------------
    # Accuracy + Errors
    # -------------------------
    def calculate_accuracy(self, typed_text):
        reference = self.sample_text
        total_chars = len(reference)

        correct = 0
        errors = 0

        for i, char in enumerate(typed_text):
            if i < len(reference) and char == reference[i]:
                correct += 1
            else:
                errors += 1

        # remaining characters missed entirely
        if len(typed_text) < len(reference):
            errors += (len(reference) - len(typed_text))

        accuracy = (correct / total_chars) * 100
        return round(accuracy, 2), errors

    # -------------------------
    # Finish Test + Show Results
    # -------------------------
    def finish_test(self):
        if self.start_time is None:
            messagebox.showinfo("Error", "You haven't typed anything yet!")
            return

        typed_text = self.input_box.get("1.0", tk.END).strip()
        elapsed = time.time() - self.start_time

        wpm = self.calculate_wpm(typed_text, elapsed)
        accuracy, errors = self.calculate_accuracy(typed_text)

        # Hide main widgets
        self.text_label.pack_forget()
        self.input_box.pack_forget()
        self.submit_btn.pack_forget()

        # Show results
        tk.Label(self.results_frame, text=f"WPM: {wpm}", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.results_frame, text=f"Accuracy: {accuracy}%", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.results_frame, text=f"Errors: {errors}", font=("Arial", 18)).pack(pady=10)

        retry_btn = tk.Button(self.results_frame, text="Retry", font=("Arial", 16), command=self.retry)
        retry_btn.pack(pady=20)

        self.results_frame.pack()

    # -------------------------
    # Retry Test
    # -------------------------
    def retry(self):
        # reset everything
        self.results_frame.pack_forget()
        self.start_time = None
        self.sample_text = random.choice(passages)

        self.text_label.config(text=self.sample_text)
        self.text_label.pack(pady=20)

        self.input_box.delete("1.0", tk.END)
        self.input_box.pack(pady=20)

        self.submit_btn.pack()


# Run the app
root = tk.Tk()
TypingTestApp(root)
root.mainloop()