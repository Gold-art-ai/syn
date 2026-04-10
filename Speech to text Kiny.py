import speech_recognition as sr

recognizer = sr.Recognizer()


def speech_to_text_kinyarwanda():
    with sr.Microphone() as source:
        print("Rindira...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Vuga!!")
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing...")
            
           
            text = recognizer.recognize_google(audio, language="rw-RW")
            print(f"Uvuze: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected within timeout. Check your microphone.")
        except sr.UnknownValueError:
            print("Could not understand the audio. Is 'rw-RW' supported or is the audio clear?")
           
            try:
                print("Trying fallback to English (en-US)...")
                text = recognizer.recognize_google(audio, language="en-US")
                print(f"English fallback transcription: {text}")
            except:
                print("English fallback also failed.")
        except sr.RequestError as e:
            print(f"API request failed: {e}. Check your internet or API support for 'rw-RW'.")
        return None

# Run the function
if __name__ == "__main__":
    speech_to_text_kinyarwanda()