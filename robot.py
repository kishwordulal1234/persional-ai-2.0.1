import google.generativeai as genai
import os
import pyttsx3
import speech_recognition as sr
import re  # Import the regex module to handle asterisk removal

# Set up the API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBUY4zB9JTSNlMMpMEfftfKXwwTKkk25CQ'  # Replace with your actual API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Set up the model
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Set female voice and adjust speech rate
def setup_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower():  # Choose female voice
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 150)  # Set speech rate (adjust as needed)

# Function to make the AI speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture voice input and convert it to text
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

# Main chatbot function
def chat_with_gemini(input_mode):
    print("AI: Hello! I'm an AI created by Kishwor Dulal. What would you like to chat about?")
    speak("Hello! I'm an AI created by Kishwor Dulal. What would you like to chat about?")
    
    # Start a new conversation
    chat = model.start_chat(history=[])

    while True:
        # Get input from the user based on selected mode
        if input_mode == 't':
            user_input = input("You: ").strip().lower()
        else:  # input_mode == 'v'
            user_input = get_voice_input()

        if user_input in ['quit', 'exit']:
            print("AI: Goodbye! It was nice chatting with you!")
            speak("Goodbye! It was nice chatting with you!")
            break
        
        # Custom responses for specific questions
        if "who are you" in user_input:
            response = "I am a small AI created by Kishwor Dulal."
            print("AI:", response)
            speak(response)
            continue
        elif "who created you" in user_input or "who built you" in user_input:
            response = "I was created and built by Kishwor Dulal."
            print("AI:", response)
            speak(response)
            continue
        elif "how are you" in user_input:
            response = "As an AI, I don't have personal feelings, but I'm here to help you!"
            print("AI:", response)
            speak(response)
            continue
        elif "how are you powered" in user_input or "how are you built" in user_input or "how are you trained" in user_input:
            response = "I am powered by Google Gemini and built by Kishwor Dulal."
            print("AI:", response)
            speak(response)
            continue
        elif "what is your name" in user_input:
            response = "I don’t have a specific name, but you can call me an AI assistant."
            print("AI:", response)
            speak(response)
            continue

        # Generate a response for general conversation
        response = chat.send_message(user_input)

        # Clean the response text by removing asterisks
        cleaned_response = re.sub(r'\*', '', response.text)

        print("AI:", cleaned_response)
        speak(cleaned_response)

if __name__ == "__main__":
    setup_voice()  # Setup female voice and fluent speech
    
    # Ask the user to choose input method: 't' for typing, 'v' for voice
    input_mode = input("Choose input method - 't' for typing, 'v' for voice: ").strip().lower()
    if input_mode not in ['t', 'v']:
        print("Invalid input. Defaulting to typing.")
        input_mode = 't'
    
    chat_with_gemini(input_mode)
