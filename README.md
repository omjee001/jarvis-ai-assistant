# 🎙️ Jarvis — Custom macOS Siri Replacement

Jarvis is a local, AI-powered desktop voice assistant for macOS. It replaces standard Siri with deeper web integration, automatic YouTube first-video playback, Spotify app/browser routing, custom terminal execution, and multi-turn conversational reasoning.

---

## ⚡ Features

- 🧠 **Local LLM Intelligence (Ollama + Llama 3.2)**: Fast, private, offline conversational reasoning and tool calling.
- 🎵 **Smart Music Player**:
  - **YouTube**: Searches and autoplays the **first top video** directly in Brave Browser.
  - **Spotify**: Detects if the native macOS Spotify app is installed; if not, falls back seamlessly to Brave web player.
  - **Multi-turn Dialog**: Asks *"Where would you like to listen to that? YouTube or Spotify?"* if you don't specify a platform.
- 🌐 **Dynamic Web Search & Navigation**: Direct navigation, domain handling, and Google search in Brave Browser.
- 💻 **Native macOS Controls**: Open applications, navigate folders, search and open files, lock screen, sleep Mac, empty trash.
- 🗣️ **Local Voice Pipeline**: Whisper STT (`faster-whisper` + INT8 VAD) + Native macOS Text-to-Speech (`say`).
- 📈 **Work-progress reports**: Ask what you are working on to hear the active app/window, explicitly tracked tasks, and Git changes in a project folder.
- 👁️ **On-demand screen understanding**: Ask Jarvis to look at your screen for a concise, local vision-model progress summary.

---

## 🚀 Setup & Installation

### 1. System Requirements
- macOS (Apple Silicon or Intel)
- [Ollama](https://ollama.ai) installed and running:
  ```bash
  ollama pull llama3.2
  ```
- PortAudio (for microphone streaming):
  ```bash
  brew install portaudio
  ```
- [Brave Browser](https://brave.com) (set as default assistant browser in `config.py`)

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## 🎯 Usage

Start Jarvis by running:
```bash
python3 main.py
```

### Example Commands:
- **Music**:
  - *"Play Starboy"* $\rightarrow$ Jarvis asks *"Where would you like to listen to that? YouTube or Spotify?"* $\rightarrow$ Say *"YouTube"*
  - *"Play Bohemian Rhapsody on YouTube"* $\rightarrow$ Opens and autoplays top YouTube video directly.
  - *"Play Jazz on Spotify"* $\rightarrow$ Opens Spotify and plays.
- **Web & Search**:
  - *"Search the latest SpaceX launch on Google"*
  - *"Open github.com"*
- **macOS System**:
  - *"Open Calculator"* / *"Open WhatsApp"*
  - *"Open Downloads folder"*
  - *"Lock my screen"* / *"Empty the trash"*
- **Conversational Q&A**:
  - *"What is the distance between Earth and Mars?"*
  - *"Tell me a fun fact about space."*
- **Work progress**:
  - *"What is my work progress?"* → reports the foreground app and any tracked tasks.
  - *"Track fixing the login bug"* / *"I completed the login bug"* → starts or completes a local task.
  - *"What is the progress in ~/Projects/my-app?"* → also reports branch, uncommitted changes, and latest commit.
  - *"Look at my screen and tell me my work progress"* → takes a one-time screenshot and gives a two-sentence summary.

## Privacy and macOS permissions

Normal progress reporting only reads the foreground application name, its window title, task data stored in `~/.jarvis_work_progress.json`, and Git metadata from a folder you name. It does **not** capture or upload your screen.

If macOS does not return a window title, grant your terminal or Python interpreter **Accessibility** permission in **System Settings → Privacy & Security → Accessibility**, then restart Jarvis.

Screen analysis runs only when you explicitly ask for it. First install the local model with `ollama pull llama3.2-vision`, and grant your terminal or Python interpreter **Screen Recording** permission in **System Settings → Privacy & Security → Screen Recording**. The screenshot is sent only to the local Ollama service and deleted immediately after analysis.
