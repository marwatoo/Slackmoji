#!/usr/bin/python3

import time
import pyperclip
import os

from custom_emojis import CUSTOM_EMOJIS, EMOJI_PATTERN
from util_emojis import replace_emoji_codes

# Main function to monitor clipboard and convert emoji codes
def main():
    last_clipboard = ""
    print("🚀 Slack Emoji Fixer is running. Press Ctrl+C to stop.")
    if os.environ.get("XDG_SESSION_TYPE") == "wayland":
        pyperclip.set_clipboard("wl-clipboard")
    while True:
        try:
            current_clipboard = pyperclip.paste()
            # Only process if clipboard changed and is a small enough string
            if current_clipboard != last_clipboard and isinstance(current_clipboard, str) and len(current_clipboard) < 500_000:
                if ':' in current_clipboard:
                    # Replace emoji codes with actual emojis
                    converted = replace_emoji_codes(current_clipboard)
                    # Update the clipboard only if changed
                    if converted != current_clipboard:
                        print(f"\n[Clipboard Updated]")
                        pyperclip.copy(converted)
                        last_clipboard = converted
                    else:
                        last_clipboard = current_clipboard
                else:
                    last_clipboard = current_clipboard
            time.sleep(1.0)  # <- Slightly slower check, less CPU usage
        except KeyboardInterrupt:
            print("\n🛑 Slack Emoji Fixer stopped.")
            break

if __name__ == "__main__":
    main()
