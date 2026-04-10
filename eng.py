
import tkinter as tk
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)    # Speed
engine.setProperty('volume', 1.0)  # Volume

# Function to speak the entered text
def speak_text():
    text = entry.get()
    if text.strip() != "":
        engine.say(text)
        engine.runAndWait()
    else:
        engine.say("Please enter some text.")
        engine.runAndWait()

# Create the main GUI window
root = tk.Tk()
root.title("Syntok Text to Speech App")
root.geometry("400x200")
root.configure(bg="white")

# Title label
label = tk.Label(root, text="Enter text to speak", font=("Arial", 14), bg="white")
label.pack(pady=10)

# Input field
entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=20)

# Speak button
button = tk.Button(root, text="Speak", command=speak_text, font=("Arial", 12), bg="#539ADD", fg="white")
button.pack(pady=10)

# Run the GUI loop
root.mainloop()
