import tkinter as tk
from tkinter import messagebox
import time
import random

# ----------------------------------------
# Sample passages
# ----------------------------------------
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
        self.root.title("Typing Speed Test (Monkeytype Style)")
        self.root.geometry("850x520")

        self.start_time = None
        self.sample_text = random.choice(passages)

        # -------- Reference text display --------
        self.text_label = tk.Label(
            root,
            text=self.sample_text,
            font=("Arial", 18),
            wraplength=820,
            justify="center"
        )
        self.text_label.pack(pady=20)

        # -------- Typing Box --------
        self.input_box = tk.Text(root, height=6, font=("Consolas", 18), undo=False)
        self.input_box.pack(pady=20)
        self.input_box.bind("<KeyRelease>", self.on_key_release)
        self.input_box.bind("<KeyPress>", self.start_timer)

        # Highlight tags
        self.input_box.tag_configure("correct", foreground="white", background="#2c2c2c")
        self.input_box.tag_configure("incorrect", foreground="white", background="#c62828")  # red
        self.input_box.config(bg="#1e1e1e", fg="white", insertbackground="white")  # Monkeytype theme

        # -------- Submit Button --------
        self.submit_btn = tk.Button(root, text="Finish", font=("Arial", 16), command=self.finish_test)
        self.submit_btn.pack()

        # Results area
        self.results_frame = tk.Frame(root)

    # -----------------------------------------------------
    # Start the timer on first key press
    # -----------------------------------------------------
    def start_timer(self, event):
        if self.start_time is None:
            self.start_time = time.time()

    # -----------------------------------------------------
    # Real-time highlighting (Monkeytype-style)
    # -----------------------------------------------------
    def on_key_release(self, event):
        typed = self.input_box.get("1.0", tk.END).rstrip("\n")
        ref = self.sample_text

        # Clear old highlights
        self.input_box.tag_remove("correct", "1.0", tk.END)
        self.input_box.tag_remove("incorrect", "1.0", tk.END)

        for i, char in enumerate(typed):
            pos = f"1.0+{i}c"

            # Correct character
            if i < len(ref) and char == ref[i]:
                self.input_box.tag_add("correct", pos, f"{pos}+1c")
            else:
                # Incorrect OR extra character
                self.input_box.tag_add("incorrect", pos, f"{pos}+1c")

    # -----------------------------------------------------
    # WPM Calculation
    # -----------------------------------------------------
    def calculate_wpm(self, typed_text, elapsed_time):
        words = len(typed_text) / 5
        minutes = elapsed_time / 60
        if minutes == 0:
            return 0
        return round(words / minutes)

    # -----------------------------------------------------
    # Accuracy Calculation
    # -----------------------------------------------------
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

        # Missing characters are errors too
        if len(typed_text) < len(reference):
            errors += (len(reference) - len(typed_text))

        accuracy = (correct / total_chars) * 100
        return round(accuracy, 2), errors

    # -----------------------------------------------------
    # Finish Test
    # -----------------------------------------------------
    def finish_test(self):
        if self.start_time is None:
            messagebox.showinfo("Error", "You haven't typed anything yet!")
            return

        typed = self.input_box.get("1.0", tk.END).strip()
        elapsed = time.time() - self.start_time

        wpm = self.calculate_wpm(typed, elapsed)
        accuracy, errors = self.calculate_accuracy(typed)

        # Remove typing UI
        self.text_label.pack_forget()
        self.input_box.pack_forget()
        self.submit_btn.pack_forget()

        # Display results
        tk.Label(self.results_frame, text=f"WPM: {wpm}", font=("Arial", 20)).pack(pady=10)
        tk.Label(self.results_frame, text=f"Accuracy: {accuracy}%", font=("Arial", 20)).pack(pady=10)
        tk.Label(self.results_frame, text=f"Errors: {errors}", font=("Arial", 20)).pack(pady=10)

        retry_btn = tk.Button(self.results_frame, text="Retry", font=("Arial", 16), command=self.retry)
        retry_btn.pack(pady=20)

        self.results_frame.pack()

    # -----------------------------------------------------
    # Retry Test
    # -----------------------------------------------------
    def retry(self):
        self.results_frame.pack_forget()

        self.start_time = None
        self.sample_text = random.choice(passages)

        self.text_label.config(text=self.sample_text)
        self.text_label.pack(pady=20)

        self.input_box.delete("1.0", tk.END)
        self.input_box.pack(pady=20)

        self.submit_btn.pack()


root = tk.Tk()
TypingTestApp(root)
root.mainloop()