from brain import think
from assistant import execute
from voice.speak import speak
from voice.wakeword import wait_for_wake_word
from voice.whisper_listen import listen

print("Jarvis is online.")


def run_jarvis():
    while True:
        # 🔹 Wait for wake word
        if not wait_for_wake_word():
            print("Shutting down Jarvis...")
            speak("Goodbye")
            break

        print("🎤 Listening for commands...")
        speak("I'm listening")

        current_context = None

        # 🔹 Active session loop
        while True:
            command = listen()

            # ⚠️ No input case
            if not command:
                print("No input detected...")
                continue

            print(f"You: {command}")

            # 🔹 Exit / sleep commands
            if command in ["exit", "stop", "sleep", "goodbye", "bye"]:
                print("Going back to sleep...")
                speak("Going back to sleep")
                break

            # 🔹 Brain processing with multi-turn context
            try:
                result = think(command, context=current_context)
                print("Brain:", result)
            except Exception as e:
                print("❌ Brain error:", e)
                speak("Something went wrong in my brain")
                current_context = None
                continue

            result_type = result.get("type")

            # 🔹 Handle clarification follow-up (e.g., asking YouTube vs Spotify)
            if result_type == "ask_clarification":
                question = result.get("question", "Could you clarify that?")
                current_context = result.get("context", {})
                print(f"Jarvis (Clarification): {question}")
                speak(question)
                # Keep current_context active for the next turn
                continue

            # 🔹 Handle conversational chat / Q&A
            elif result_type == "chat":
                chat_response = result.get("response", "I understand.")
                print(f"Jarvis: {chat_response}")
                speak(chat_response)
                current_context = None

            # 🔹 Handle tool execution
            else:
                try:
                    response = execute(result)
                except Exception as e:
                    print("❌ Execution error:", e)
                    response = "I couldn't execute that command."

                if not response:
                    response = "Done."

                print("Jarvis:", response)
                speak(response)
                current_context = None


if __name__ == "__main__":
    run_jarvis()