import tkinter as tk
from tkinter import messagebox
import asyncio
import edge_tts
import tempfile
import os
import ctypes # Built-in: talks to Windows system files

# Function to play sound using Windows MCI (Media Control Interface)
def play_native_windows(file_path):
    # This sends a direct command to the Windows Sound Driver
    # It does NOT open VLC or any other player
    mci = ctypes.windll.winmm
    mci.mciSendStringW(f'open "{file_path}" type mpegvideo alias my_audio', None, 0, 0)
    mci.mciSendStringW('play my_audio wait', None, 0, 0)
    mci.mciSendStringW('close my_audio', None, 0, 0)

async def speak_sw(text):
    communicate = edge_tts.Communicate(text, voice="sw-KE-RafikiNeural")
    
    # Create a hidden temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        temp_path = tmp.name
        
    await communicate.save(temp_path)

    try:
        # Play it using the internal Windows driver
        play_native_windows(temp_path)
    finally:
        # Clean up the file after playing
        if os.path.exists(temp_path):
            os.remove(temp_path)

def speak_kiswahili(text):
    if not text.strip():
        messagebox.showerror("Error", "Injiza amagambo mbere!")
        return
    try:
        asyncio.run(speak_sw(text))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Native System Reader")

tk.Label(root, text="Injiza amagambo y'ikinyarwanda:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 14), width=35)
entry.pack(padx=10, pady=10)

btn = tk.Button(root, text="Vuga", command=lambda: speak_kiswahili(entry.get()), bg="#0078d4", fg="white")
btn.pack(pady=10)

root.mainloop()