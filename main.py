#!/usr/bin/python3
import time
import pyperclip
import emoji
import re

from custom_emojis import CUSTOM_EMOJIS, EMOJI_PATTERN

# Function to convert Slack emoji shortcodes to emojis
def flag_shortcode_to_emoji(shortcode):
    country_code = shortcode[6:-1]
    if len(country_code) == 2:
        country_code = country_code.upper()
        return chr(0x1F1E6 + ord(country_code[0]) - ord('A')) + chr(0x1F1E6 + ord(country_code[1]) - ord('A'))
    else:
        return shortcode

# Function to replace emoji codes with actual emojis
def replace_emoji_codes(text):
    def replace_match(match):
        code = match.group(0)
        # First check for flag shortcodes
        if code.startswith(":flag-") and code.endswith(":"):
            return flag_shortcode_to_emoji(code)
        # Check if the emoji code exists in the custom mappings
        if code in CUSTOM_EMOJIS:
            return CUSTOM_EMOJIS[code]
        # Use the emoji library if the code isn't a custom one
        try:
            return emoji.emojize(code, language='alias')
        except Exception:
            # Return the code as is if no emoji is found
            return code
    # Replace emojis and ensure no spaces are left between emoji and surrounding text
    text = EMOJI_PATTERN.sub(replace_match, text)
    # Remove any spaces that may have been left between text and emojis
    text = re.sub(r'\s+([^\s\w])', r'\1', text)  # Remove spaces before emojis
    return text

# Function to double newlines, needed for readability on Social Media, like X, Instagram, etc.
def double_newlines(text):
    return text.replace('\n', '\n\n')

# Main function to monitor clipboard and convert emoji codes
def main():
    last_clipboard = ""
    print("🚀 Slack Emoji Fixer is running. Press Ctrl+C to stop.")
    while True:
        try:
            current_clipboard = pyperclip.paste()
            # Only process if clipboard changed and is a small enough string
            if current_clipboard != last_clipboard and isinstance(current_clipboard, str) and len(current_clipboard) < 500_000:
                if ':' in current_clipboard:
                    # Replace emoji codes with actual emojis
                    converted = replace_emoji_codes(current_clipboard)
                    # Double newlines for readability
                    converted = double_newlines(converted)
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
