#!/usr/bin/python3

import sys
import os
import pyperclip
import emoji
import re
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer, Qt

# Precompile emoji pattern
EMOJI_PATTERN = re.compile(r':[a-zA-Z0-9_\-]+:')

# Custom emoji mappings
CUSTOM_EMOJIS = {
    ":rain_cloud:": "🌧️",
    ":partly_sunny_rain:": "🌦️",  # Add this custom mapping
    # Add more custom mappings here
}

def flag_shortcode_to_emoji(shortcode):
    country_code = shortcode[6:-1]
    if len(country_code) == 2:
        country_code = country_code.upper()
        return chr(0x1F1E6 + ord(country_code[0]) - ord('A')) + \
               chr(0x1F1E6 + ord(country_code[1]) - ord('A'))
    else:
        return shortcode

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
    
    # Handle newlines by respecting them and adding an extra newline after existing ones
    # But make sure there's no additional space between emojis and text
    text = text.replace('\n', '\n\n')  # Add a newline after each existing newline
    
    # Replace emojis and ensure no spaces are left between emoji and surrounding text
    text = EMOJI_PATTERN.sub(replace_match, text)
    
    # Remove any spaces that may have been left between text and emojis
    text = re.sub(r'\s+([^\s\w])', r'\1', text)  # Remove spaces before emojis
    
    return text

class ClipboardWatcher(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.setToolTip("Slack Emoji Fixer")
        self.last_clipboard = ""

        # Create the context menu
        self.menu = QMenu(parent)
        
        # Add "Exit" action to the menu
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.quit_application)
        self.menu.addAction(exit_action)

        # Set the context menu for the tray icon
        self.setContextMenu(self.menu)

        # Set up the timer to check clipboard every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(1000)

        # Connect the right-click event to show the context menu
        self.activated.connect(self.on_tray_icon_activated)

    def check_clipboard(self):
        current_clipboard = pyperclip.paste()
        if current_clipboard != self.last_clipboard and isinstance(current_clipboard, str):
            converted = replace_emoji_codes(current_clipboard)
            if converted != current_clipboard:
                pyperclip.copy(converted)
                self.last_clipboard = converted

    def quit_application(self):
        print("Exiting the application.")
        QApplication.quit()

    def on_tray_icon_activated(self, reason):
        # If the user right-clicks, we show the menu
        if reason == QSystemTrayIcon.ActivationReason.Context:
            self.menu.exec()  # Display the context menu

def main():
    app = QApplication(sys.argv)

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the icon in the same directory as the script
    icon_path = os.path.join(script_dir, "smiley.png")  # Replace with your icon filename
    
    # Check if the icon exists
    icon = QIcon(icon_path)
    
    if icon.isNull():
        print(f"Icon not found at {icon_path}. Check the file path.")
        icon = QIcon.fromTheme("application-default-icon")  # Fallback to default icon

    # Set the tray icon
    tray_icon = ClipboardWatcher(icon)
    tray_icon.show()

    print("🚀 Slack Emoji Fixer is running")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
