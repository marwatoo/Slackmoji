#!/usr/bin/python3

#This script uses PyQt5 to adapt systrtray menu to default theme, for some reason, pyqt6 doesn't follow the theme

import sys
import os
import pyperclip


from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

from custom_emojis import CUSTOM_EMOJIS, EMOJI_PATTERN
from util_emojis import replace_emoji_codes


# Class to handle the system tray icon and clipboard monitoring
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
            self.menu.exec_()  # Display the context menu

# Main function to set up the application
def main():
    app = QApplication(sys.argv)

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the icon in the same directory as the script
    icon_path = os.path.join(script_dir, "smile.png")  # Replace with your icon filename
    
    # Check if the icon exists
    icon = QIcon(icon_path)
    
    if icon.isNull():
        print(f"Icon not found at {icon_path}. Check the file path.")
        icon = QIcon.fromTheme("application-default-icon")  # Fallback to default icon

    # Set the tray icon
    tray_icon = ClipboardWatcher(icon)
    tray_icon.show()

    print("🚀 Slack Emoji Fixer is running")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
