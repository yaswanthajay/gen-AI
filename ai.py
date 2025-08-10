import streamlit as st
import pyttsx3
import speech_recognition as sr
from llama_cpp import Llama

# === INITIALIZATION ===
engine = pyttsx3.init()
engine.setProperty('rate', 180)
recognizer = sr.Recognizer()

# === LOAD MODEL (OPTIMIZED THREADS AND SETTINGS) ===
@st.cache_resource
def load_model():
    st.write("🔄 Loading your AI model...")
    model = Llama(
        model_path="model.gguf",  # Update this to your correct model path
        n_ctx=1024,
        n_threads=8,
        n_gpu_layers=20,
        f16_kv=True,
        verbose=False
    )
    st.write("✅ Model loaded successfully!")
    return model

llm = load_model()

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
    st.write(f"🤖: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        st.warning("Speech synthesis may not work in this environment.")

# === GET TEXT INPUT ===
def get_text_input():
    return st.text_input("💬 You:", "").strip()

# === GET VOICE INPUT ===
def get_voice_input():
    st.warning("Voice input is not supported on Streamlit Cloud.")
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
        st.error(f"❌ Error: {e}")
        return "Sorry, I had trouble answering that."

# === ROLE SELECT ===
def choose_role():
    global current_role
    selected = st.selectbox("🎭 Choose a character:", list(characters.keys()))
    current_role = selected
    speak(f"Okay, I will now answer as a {selected}.")

# === INPUT MODE SELECT ===
def choose_input_mode():
    global input_mode
    selected = st.radio("🧠 Choose input mode:", ["text", "voice"])
    input_mode = selected
    speak(f"Input mode set to {input_mode}.")

# === STREAMLIT APP ===
st.title("🧠 AI Chat with Roles")
st.write("Ask questions, change roles, or switch input modes anytime.")

choose_input_mode()
choose_role()

if input_mode == "voice":
    question = get_voice_input()
else:
    question = get_text_input()

if st.button("⚡ Generate Answer"):
    if question:
        st.write("⚡ Generating answer...")
        answer = generate_response(question)
        speak(answer)
    else:
        st.warning("Please enter a question.")
