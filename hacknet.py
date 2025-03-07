import sys
import os
import requests
import socket
import psutil
from colorama import init, Back, Fore
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView


class HackNet:
    def __init__(self):
        init(autoreset=True)  # Initialize colorama
        self.app = QApplication(sys.argv)  # Create the PyQt5 application instance
        self.browser = QWebEngineView()  # Create the browser instance (but will be hidden)
        self.browser.setVisible(False)  # Set the browser window to be invisible
        self.background_color = Back.GREEN  # Default background color (green)

    def start(self):
        # Display the ASCII art with colorama (green background, white text)
        print(self.background_color + Fore.WHITE + """
          _    _               _     _   _        _   
         | |  | |             | |   | \\ | |      | |  
         | |__| |  __ _   ___ | | __|  \\| |  ___ | |_ 
         |  __  | / _ | / __|| |/ /| .  | / _ \\| __|
         | |  | || (_| || (__ |   < | |\\  ||  __/| |_ 
         |_|  |_| \\__,_| \\___||_|\\_\\|_| \\_| \\___| \\__|
        """)

        # Display the website URL after the ASCII art
        print(Fore.WHITE + "Visit us at: https://sites.google.com/view/hacknetpython/")

        # Interactive prompt for commands
        while True:
            print(Fore.WHITE)  # Set the text color to white for command input
            command = input("HackNet> ")

            if not command.strip():  # If command is empty, just continue
                continue

            if command.lower().startswith("search "):
                url = command[len("search "):]
                self.search(url)
            elif command.lower().startswith("download "):
                url = command[len("download "):]
                self.download(url)
            elif command.lower() == "webbrowser":
                print("Feature coming soon.")
            elif command.lower() == "showip":
                self.show_ip()
            elif command.lower() == "wifi":
                self.show_wifi()
            elif command.lower().startswith("color "):
                self.change_color(command)
            elif command.lower() == "help":
                self.show_help()
            elif command.lower() == "exit":
                print("Exiting HackNet...")
                break
            else:
                print("Invalid command. Try 'search <url>', 'download <url>', 'showip', 'wifi', 'color <color>', or 'help'.")

    def search(self, url):
        """Simulate a search by opening the browser with the provided URL."""
        print(f"Searching for {url}...")
        self.open_browser_window(f"http://{url}")

    def download(self, url):
        """Download a file from the provided URL."""
        print(f"Downloading from {url}...")

        # Get the file's content using the requests library
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes (e.g., 404, 500)

            # Get the filename from the URL (it will use the last part of the URL after the last slash)
            filename = url.split("/")[-1]

            # Open a file save dialog to choose the destination
            save_path, _ = QFileDialog.getSaveFileName(None, "Save File", filename, "All Files (*)")
            if save_path:
                # Save the content to the selected file
                with open(save_path, "wb") as file:
                    file.write(response.content)
                print(f"File saved as: {save_path}")
            else:
                print("Download canceled.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the file: {e}")

    def open_web_browser(self):
        """Open the web browser."""
        print("Opening the web browser...")
        self.open_browser_window("https://www.google.com")

    def open_browser_window(self, url):
        """Open the PyQt5 web browser in a separate window."""
        self.browser.setUrl(QUrl(url))
        self.browser.show()

        # Start the PyQt5 event loop for the browser
        self.app.exec_()

    def show_ip(self):
        """Show the user's current IP address."""
        ip_address = socket.gethostbyname(socket.gethostname())
        print(f"Your current IP address is: {ip_address}")

    def show_wifi(self):
        """Show the user's Wi-Fi information."""
        wifi_info = psutil.net_if_addrs()
        wifi_details = wifi_info.get('Wi-Fi', None)
        if wifi_details:
            for item in wifi_details:
                print(f"{item.family}: {item.address}")
        else:
            print("No Wi-Fi connection found.")

    def change_color(self, command):
        """Change the background color based on the command input."""
        color_mapping = {
            "grey": Back.LIGHTBLACK_EX + Fore.WHITE,
            "blue": Back.BLUE + Fore.WHITE,
            "green": Back.GREEN + Fore.WHITE,  # Default
            "black": Back.BLACK + Fore.WHITE,
        }
        
        color_choice = command.split()[1].lower()
        if color_choice in color_mapping:
            self.background_color = color_mapping[color_choice]
            print(f"Background color changed to {color_choice.capitalize()}.")
        else:
            print("Invalid color choice. Available options: grey, blue, green, black.")

    def show_help(self):
        """Display the help information for all available commands."""
        print(Fore.WHITE + """
Available commands:

1. search <url>     - Open the web browser with the given URL.
2. download <url>   - Download the file from the specified URL.
3. webbrowser       - Feature coming soon.
4. showip           - Display your current IP address.
5. wifi             - Display your Wi-Fi connection details.
6. color <color>    - Change the background color of the terminal.
   Available colors: grey, blue, green (default), black.
7. help             - Show this help information.
8. exit             - Exit the HackNet application.
""")

if __name__ == "__main__":
    hacknet = HackNet()
    hacknet.start()
