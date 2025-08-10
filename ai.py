import pyttsx3
import speech_recognition as sr
from llama_cpp import Llama

# === INITIALIZATION ===
engine = pyttsx3.init()
engine.setProperty('rate', 180)
recognizer = sr.Recognizer()

# === LOAD MODEL (OPTIMIZED THREADS AND SETTINGS) ===
print("🔄 Loading your AI model...")
llm = Llama(
    model_path="model.gguf",  # Update this to your correct model path
    n_ctx=1024,
    n_threads=8,
    n_gpu_layers=20,
    f16_kv=True,
    verbose=False
)
print("✅ Model loaded successfully!")

# === CHARACTER STYLES ===
characters = {
    "parent": "You are a caring parent explaining this in a simple and emotional way.",
    "sibling": "You are a funny, helpful sibling who explains in a friendly tone.",
    "teacher": "You are a strict but helpful school teacher giving a detailed explanation.",
    "scientist": "You are a logical scientist providing precise and technical answers.",
    "friend": "You are a supportive best friend who explains casually and nicely.",
    "normal": "You are a helpful assistant answering questions clearly and neutrally."
}
current_role = "normal"
input_mode = "text"  # default mode

# === SPEAK FUNCTION ===
def speak(text):
    print(f"\n🤖: {text}")
    engine.say(text)
    engine.runAndWait()

# === GET TEXT INPUT ===
def get_text_input():
    return input("\nYou: ").strip()

# === GET VOICE INPUT ===
def get_voice_input():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        speak("Sorry, speech service is down.")
        return ""

# === GENERATE RESPONSE ===
def generate_response(question):
    try:
        style = characters.get(current_role, characters["normal"])
        prompt = f"{style}\nQ: {question}\nA:"
        response = llm(
            prompt,
            max_tokens=150,
            temperature=0.6,
            stop=["\n", "Q:"],
            echo=False
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        print(f"❌ Error: {e}")
        return "Sorry, I had trouble answering that."

# === ROLE SELECT ===
def choose_role():
    global current_role
    print("\n🎭 Choose a character (parent, sibling, teacher, scientist, friend, normal):")
    selected = input("Your choice: ").strip().lower()
    if selected in characters:
        current_role = selected
        speak(f"Okay, I will now answer as a {selected}.")
    else:
        speak("Character not recognized. Using normal mode.")
        current_role = "normal"

# === INPUT MODE SELECT ===
def choose_input_mode():
    global input_mode
    print("\n🧠 Choose input mode (voice / text):")
    selected = input("Your choice: ").strip().lower()
    if selected in ["voice", "text"]:
        input_mode = selected
        speak(f"Input mode set to {input_mode}.")
    else:
        speak("Invalid mode. Sticking with text.")

# === MAIN LOOP ===
print("\n🧠 Welcome! You can ask questions and change roles or input modes anytime.")
choose_input_mode()
speak("Hello! Ask anything or type 'role' to change character, 'mode' to change input type, or 'quit' to exit.")

while True:
    try:
        if input_mode == "voice":
            question = get_voice_input()
        else:
            question = get_text_input()

        if not question:
            continue

        if question.lower() == "quit":
            speak("Goodbye! Take care.")
            break
        elif question.lower() == "role":
            choose_role()
            continue
        elif question.lower() == "mode":
            choose_input_mode()
            continue

        print("⚡ Generating answer...")
        answer = generate_response(question)
        speak(answer)
        print("\n💬 Ask another question or say 'role' or 'mode' or 'quit'.")

    except KeyboardInterrupt:
        print("\n🛑 Exiting...")
        speak("See you soon!")
        break
    except Exception as e:
        print(f"⚠️ Error: {e}")
        speak("Oops, something went wrong.")
