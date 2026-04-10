import tkinter as tk
from tkinter import messagebox
import asyncio
import edge_tts
import tempfile
import os

# Function to run the async TTS
def speak_kiswahili(text):
    if not text.strip():
        messagebox.showerror("Error", "Injiza amagambo y'ikinyarwanda mbere!")
        return

    try:
        asyncio.run(speak_sw(text))
    except Exception as e:
        messagebox.showerror("Ntibyagenze neza", str(e))

# Async function to handle the voice generation
async def speak_sw(text):
    communicate = edge_tts.Communicate(text, voice="sw-KE-RafikiNeural")

    # Generate a temporary file path (without locking it)
    temp_path = tempfile.mktemp(suffix=".mp3")

    # Save the voice to the temp file
    await communicate.save(temp_path)

    # Safely play the file (Windows only)
    os.system(f'start "" "{temp_path}"')

# GUI setup
root = tk.Tk()
root.title("Ikinyarwanda Text-to-Speech (Simulated)")

tk.Label(root, text="Injiza amagambo y'ikinyarwanda:", font=("Arial", 14)).pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), width=40)
entry.pack(padx=10, pady=10)

btn = tk.Button(root, text="Vuga", font=("Arial", 14), command=lambda: speak_kiswahili(entry.get()), bg="#5cb85c", fg="white")
btn.pack(pady=10)

root.mainloop()
