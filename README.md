# 🎙️ AI agent — Real-Time Voice Agent

this is a real-time conversational AI agent that joins a LiveKit room, listens to participants, transcribes speech using Deepgram, generates responses using a Groq-powered LLM, and replies using ElevenLabs TTS.

---

## 🔥 Live Demo Pipeline

👤 You Speak →  
🎧 Deepgram (STT) →  
🧠 Groq (LLM) →  
🗣️ ElevenLabs (TTS) →  
🔁 LiveKit Room Response

---

## 🚀 Features

- 🎤 Real-time speech transcription with **Deepgram**  
- 🧠 Ultra-fast responses using **Groq API** (LLM like GPT-4 via Groq)  
- 🔊 High-quality voice synthesis using **ElevenLabs**  
- 🧵 Asynchronous architecture powered by **LiveKit Agents SDK**  
- 📈 Session metrics logged and saved as `.xlsx`

---


## 📦 Installation

```bash
git clone https://github.com/Anvit2512/LiveKIT.git
cd LiveKIT

# Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
