import emoji
import re

from custom_emojis import CUSTOM_EMOJIS, EMOJI_PATTERN

# Function to fix Slack emoji shortcodes to emojis
def flag_shortcode_to_emoji(shortcode):
    country_code = shortcode[6:-1]
    if len(country_code) == 2:
        country_code = country_code.upper()
        return chr(0x1F1E6 + ord(country_code[0]) - ord('A')) + \
               chr(0x1F1E6 + ord(country_code[1]) - ord('A'))
    else:
        return shortcode

# Function to replace emoji text with actual emojis
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
    
    original_text = text  # Keep a copy to detect changes

    # Replace emojis first (without touching newlines)
    replaced_text = EMOJI_PATTERN.sub(replace_match, text)

    # Remove spaces inside emoji shortcodes (before and after word)
    replaced_text = re.sub(r':\s*([a-zA-Z0-9\-_]+)\s*:', r':\1:', replaced_text)

    # Check if anything changed
    if replaced_text != original_text:
        # If text changed (meaning emojis were added), handle newlines
        replaced_text = re.sub(r'(?<!\n)\n(?!\n)', '\n\n', replaced_text)
    
    return replaced_text

# Function to double newlines, needed for readability on Social Media, like X, Instagram, etc.
def double_newlines(text):
    return text.replace('\n', '\n\n')
