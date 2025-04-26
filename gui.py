#!/usr/bin/python3

import sys
import pyperclip
import emoji
import re

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer, Qt

# Precompile emoji pattern
EMOJI_PATTERN = re.compile(r':[a-zA-Z0-9_\-]+:')

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
        if code.startswith(":flag-") and code.endswith(":"):
            return flag_shortcode_to_emoji(code)
        else:
            return emoji.emojize(code, language='alias')
    
    # Handle newlines by respecting them and adding an extra newline after existing ones
    text = text.replace('\n', '\n\n')  # Add a newline after each existing newline
    return EMOJI_PATTERN.sub(replace_match, text)

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

    # Check if the icon exists and is valid
    icon_path = "smiley.png"  # Replace with the path to your icon
    icon = QIcon(icon_path)
    
    if icon.isNull():
        print("Icon is null. Check the file path.")
        icon = QIcon.fromTheme("application-default-icon")  # Fallback to default icon

    # Set the tray icon
    tray_icon = ClipboardWatcher(icon)
    tray_icon.show()

    print("Tray icon should now be visible.")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
