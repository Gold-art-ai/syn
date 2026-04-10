import tkinter as tk
from tkinter import messagebox
from gtts import gTTS
import tempfile
import os
import threading
import uuid
import pygame

# Initialize pygame mixer
pygame.mixer.init()

def speak_kinyarwanda_gui():
    text = entry.get().strip()

    if not text:
        messagebox.showerror("Ikosa", "Injiza amagambo y'Ikinyarwanda mbere!")
        return

    def play():
        try:
            filename = f"{uuid.uuid4().hex}.mp3"
            tmp_path = os.path.join(tempfile.gettempdir(), filename)

            # Save the audio file
            tts = gTTS(text=text, lang='sw')  
            tts.save(tmp_path)

            # Play using pygame
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()

            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Unload and delete safely
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            os.remove(tmp_path)

        except Exception as e:
            messagebox.showerror("Ikosa", f"Ntibyagenze neza:\n{e}")

    threading.Thread(target=play).start()

# GUI Setup
root = tk.Tk()
root.title("Kinyarwanda TTS")
root.geometry("480x200")
root.configure(bg="white")

tk.Label(root, text="Injiza amagambo y'Ikinyarwanda:", font=("Arial", 14), bg="white").pack(pady=10)
entry = tk.Entry(root, font=("Arial", 14), width=40)
entry.pack(pady=10)

tk.Button(root, text="Vuga", font=("Arial", 14), command=speak_kinyarwanda_gui, bg="#28a745", fg="white").pack(pady=10)

root.mainloop()

