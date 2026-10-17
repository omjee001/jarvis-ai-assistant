import time
from config import WAKE_WORD


def wait_for_wake_word():
    """
    Waits for the wake word activation.
    Supports typing the wake word or pressing Enter to trigger Jarvis.
    """
    print(f"\n🎙️ Jarvis is listening... (Type '{WAKE_WORD}' or press Enter to activate, or 'exit' to quit)")

    while True:
        try:
            text = input("Jarvis > ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            return False

        if text in ["exit", "quit", "q"]:
            return False

        if text == WAKE_WORD or text == "" or "jarvis" in text or "hey" in text:
            print("✅ Wake word detected!")
            time.sleep(0.2)
            return True

        print("...still waiting")


if __name__ == "__main__":
    if wait_for_wake_word():
        print("Wake word module is ready to hand control to Jarvis.")