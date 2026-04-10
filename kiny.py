import tkinter as tk
from tkinter import messagebox
import pygame
import os
import time

# Initialize Pygame mixer
pygame.mixer.init()

# Path to your audio folder
AUDIO_FOLDER = "kinyarwanda_audio"

def play_audio_sequence():
    sentence = entry.get().strip().lower()
    words = sentence.split()

    for word in words:
        audio_path = os.path.join(AUDIO_FOLDER, f"{word}.wav")
        
        if os.path.exists(audio_path):
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)  # Wait for current word to finish playing
        else:
            print(f"[⚠] No audio found for: {word}")
            continue

# GUI setup
root = tk.Tk()
root.title("Kinyarwanda Text to Audio")

label = tk.Label(root, text="Andika amagambo (e.g. 'muraho neza'):")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

play_button = tk.Button(root, text="Vuga", command=play_audio_sequence)
play_button.pack(pady=20)

root.mainloop()