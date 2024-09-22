import google.generativeai as genai
import os
import pyttsx3
import speech_recognition as sr
import re
import serial
import time

os.environ['GOOGLE_API_KEY'] = 'AIzaSyBUY4zB9JTSNlMMpMEfftfKXwwTKkk25CQ'
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-1.5-flash-latest')

engine = pyttsx3.init()
recognizer = sr.Recognizer()
arduino = serial.Serial('/dev/ttyACM0', 9600)  # Change the port accordingly
time.sleep(2)

def setup_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You (voice): {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            speak("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            speak("Sorry, there was an issue with the speech recognition service.")
            return ""

def send_to_arduino(command, message):
    arduino.write(command.encode())
    print(f"AI: {message}")
    speak(message)

# Main chatbot function
def chat_with_gemini(input_mode):
    print("AI: Hello! I'm an AI created by Kishwor Dulal. What would you like to chat about?")
    speak("Hello! I'm an AI created by Kishwor Dulal. What would you like to chat about?")
    
    chat = model.start_chat(history=[])

    while True:
        if input_mode == 't':
            user_input = input("You: ").strip().lower()
        else:
            user_input = get_voice_input()

        if user_input in ['quit', 'exit']:
            print("AI: Goodbye! It was nice chatting with you!")
            speak("Goodbye! It was nice chatting with you!")
            break
        
        elif "wave" in user_input or user_input == 'h':
            response = "Let me wave for you!"
            print("AI:", response)
            speak(response)
            send_to_arduino('h', "Waving")
            continue
        elif "punch" in user_input or user_input == 'p':
            response = "Let me show you a punch!"
            print("AI:", response)
            speak(response)
            send_to_arduino('p', "Punching")
            continue
        elif "smash" in user_input or user_input == 's':
            response = "Smashing things!"
            print("AI:", response)
            speak(response)
            send_to_arduino('s', "Smashing")
            continue
        elif "uppercut" in user_input or user_input == 'u':
            response = "Let's do an uppercut!"
            print("AI:", response)
            speak(response)
            send_to_arduino('U', "Uppercutting")
            continue
        elif "look left" in user_input or user_input == 'l':
            response = "I'm looking to the left!"
            print("AI:", response)
            speak(response)
            send_to_arduino('l', "Looking left")
            continue
        elif "look right" in user_input or user_input == 'r':
            response = "I'm looking to the right!"
            print("AI:", response)
            speak(response)
            send_to_arduino('r', "Looking right")
            continue

if __name__ == "__main__":
    setup_voice()
    
    input_mode = input("Choose input method - 't' for typing, 'v' for voice: ").strip().lower()
    if input_mode not in ['t', 'v']:
        print("Invalid input. Defaulting to typing.")
        input_mode = 't'
    
    chat_with_gemini(input_mode)
