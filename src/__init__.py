import json
import os
import sys
import threading
import tkinter as tk
import webbrowser
from tkinter import messagebox, ttk, filedialog


class StdoutRedirector:
    """Class for redirecting standard output to a Tkinter text variable."""

    def __init__(self, text_variable) -> None:
        """
        Initialize the StdoutRedirector class.

        :param text_variable: Tkinter text variable to store the output.
        :type text_variable: tk.StringVar
        """
        self.text_variable = text_variable
        self.buffer = ''

    def write(self, message) -> None:
        """
        Write the message to the text variable.

        :param message: The message to be written.
        :type message: str
        :return: None
        """
        self.text_variable.set(message)

    def flush(self) -> None:
        """Flush the output buffer."""
        pass


class Constants:
    """This class holds all the constant values used in the application"""

    APP_TITLE = 'M3U8 Downloader'  # Title of the application
    APP_VERSION = '0.1.2'  # Version of the application
    APP_PACKAGE_NAME = 'pym3u8downloaderui'  # Package name of the application
    APP_PACKAGE_DESCRIPTION = """
    M3U8 Downloader UI is a Python-based graphical user interface (GUI) application designed 
    to simplify the process of downloading and concatenating video files using the 
    pym3u8downloader package. This application streamlines the task of downloading and 
    merging video files from M3U8 playlists.
    """  # Description of the application
    APP_WINDOW_WIDTH = 450  # Width of the application window
    APP_WINDOW_HEIGHT = 250  # Height of the application window
    APP_PALETTE_BACKGROUND = '#FFFFFF'  # Background color of the application
    APP_PALETTE_FOREGROUND = '#000000'  # Foreground color of the application
    APP_THEME = 'xpnative'  # Theme of the application
    APP_LABEL_FONT_TYPE = 'Segoe UI'  # Font type for labels
    APP_LABEL_FONT_SIZE = 8  # Font size for labels
    APP_LABEL_FONT_STYLE = 'bold'  # Font style for labels
    APP_ROW_MIN_SIZE = 10  # Minimum size for rows
    APP_PADDING = 10  # Padding for elements
    APP_ICON_IMAGE_FILE_NAME = 'icon.png'  # File name of the icon image
    APP_ICON_IMAGE_FILE_PATH = (
        f'https://raw.githubusercontent.com/coldsofttech/pym3u8downloaderui/'
        f'main/src/Resources/Images/{APP_ICON_IMAGE_FILE_NAME}'
    )  # Full URL of the icon image file
    APP_ICON_FILE_NAME = 'icon.ico'  # File name of the icon
    APP_ICON_FILE_PATH = (
        f'https://raw.githubusercontent.com/coldsofttech/pym3u8downloaderui/'
        f'main/src/Resources/Images/{APP_ICON_FILE_NAME}'
    )  # Full URL of the icon file

    MENU_FILE_TITLE = 'File'  # Title of the file menu
    MENU_FILE_NEW_TITLE = 'New'  # Tile of the 'New' option in the file menu
    MENU_FILE_EXIT_TITLE = 'Exit'  # Title of the 'Exit' option in the file menu
    MENU_HELP_TITLE = 'Help'  # Title of the help menu
    MENU_HELP_HELP_TITLE = 'Help'  # Title of the 'Help' option in the help menu
    MENU_HELP_ABOUT_TITLE = 'About'  # Title of the 'About' option in the help menu

    LABEL_INPUT_TITLE = 'Input URL (.m3u8):'  # Title for input URL label
    LABEL_OUTPUT_TITLE = 'Output File (.mp4):'  # Title for output file label

    BUTTON_BROWSE_TITLE = '...'  # Title for browse button
    BUTTON_DOWNLOAD_TITLE = 'Download'  # Title for download button

    INVALID_INPUT_TITLE = 'Warning'  # Title for invalid input warning
    INVALID_INPUT_MESSAGE = 'Please provide both input url and output file.'  # Message for invalid input warning

    BROWSE_FILE_TYPES = [('MP4 Files', '*.mp4'), ('All files', '*.*')]  # File types for browsing
    BROWSE_DEFAULT_EXTENSION = '.mp4'  # Default extension for browsing

    DOWNLOAD_IN_PROGRESS_TITLE = 'Warning'  # Title for download in progress warning
    # Message for download in progress warning
    DOWNLOAD_IN_PROGRESS_MESSAGE = 'Download is in progress and cannot be interrupted!'
    DOWNLOAD_COMPLETE_TITLE = 'Download'  # Title for download complete message
    DOWNLOAD_COMPLETE_MESSAGE = 'Download completed successfully!'  # Message for download complete message
    DOWNLOAD_ERROR_TITLE = 'Error'  # Title for download error message

    ABOUT_TITLE = 'About'  # Title for about window
    ABOUT_WINDOW_WIDTH = 300  # Width of the about window
    ABOUT_WINDOW_HEIGHT = 250  # Height of the about window

    CONFIG_FILE = 'config.json'  # File name for configuration file


class M3U8DownloaderUI:
    """
    Class for creating and managing the user interface of an M3U8 Downloader application
    """

    def __init__(self, master: tk.Tk) -> None:
        """
        Initialize the M3U8DownloaderUI class.

        :param master: The Tkinter root window.
        :type master: tk.Tk
        """
        self.master = master
        self.master.title(Constants.APP_TITLE)
        self.master.geometry(f'{Constants.APP_WINDOW_WIDTH}x{Constants.APP_WINDOW_HEIGHT}')
        self.master.resizable(False, False)
        self._set_icon()

        self._set_overrides()
        self._set_defaults()
        self._set_styles()
        self._set_fonts()
        self._set_menus()
        self._set_controls()

    def _set_icon(self) -> None:
        """Set icon for the application window."""
        import requests

        if os.path.exists(Constants.APP_ICON_FILE_NAME):
            self.master.iconbitmap(default=Constants.APP_ICON_FILE_NAME)
        else:
            try:
                response = requests.get(Constants.APP_ICON_FILE_PATH)
                if response.status_code == 200:
                    with open(Constants.APP_ICON_FILE_NAME, 'wb') as icon_file:
                        icon_file.write(response.content)
                    self.master.iconbitmap(default=Constants.APP_ICON_FILE_NAME)
            except requests.RequestException:
                pass

    def _set_overrides(self) -> None:
        """Set overrides for the application window."""
        self.master.protocol('WM_DELETE_WINDOW', self._exit_callback)

    def _set_defaults(self) -> None:
        """Set default value for various attributes."""
        self.selected_file_path = tk.StringVar()
        self.std_output = tk.StringVar()
        self.download_thread = None
        self.help_link = 'https://github.com/coldsofttech/pym3u8downloaderui/blob/main/README.md'

    def _set_styles(self) -> None:
        """Set styles for the application."""
        self.master.tk_setPalette(
            background=Constants.APP_PALETTE_BACKGROUND, foreground=Constants.APP_PALETTE_FOREGROUND
        )
        self.style = ttk.Style()
        self.style.theme_use(Constants.APP_THEME)

    def _set_fonts(self) -> None:
        """Set font styles for labels."""
        self.font_label_style = (
            Constants.APP_LABEL_FONT_TYPE, Constants.APP_LABEL_FONT_SIZE, Constants.APP_LABEL_FONT_STYLE
        )

    def _set_menus(self) -> None:
        """Set up menus for the application."""
        self.menu_bar = tk.Menu(self.master)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label=Constants.MENU_FILE_NEW_TITLE, command=self._new_callback)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=Constants.MENU_FILE_EXIT_TITLE, command=self._exit_callback)
        self.menu_bar.add_cascade(label=Constants.MENU_FILE_TITLE, menu=self.file_menu)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.help_menu.add_command(label=Constants.MENU_HELP_HELP_TITLE, command=self._help_callback)
        self.help_menu.add_separator()
        self.help_menu.add_command(label=Constants.MENU_HELP_ABOUT_TITLE, command=lambda: AboutUI(self.master))
        self.menu_bar.add_cascade(label=Constants.MENU_HELP_TITLE, menu=self.help_menu)

        self.master.config(menu=self.menu_bar)

    def _set_controls(self) -> None:
        """Set up various controls/widgets in the application window."""
        self.master.rowconfigure(0, minsize=Constants.APP_ROW_MIN_SIZE)

        self.input_label = ttk.Label(self.master, text=Constants.LABEL_INPUT_TITLE, font=self.font_label_style)
        self.input_label.grid(row=1, column=0, sticky=tk.W, padx=Constants.APP_PADDING)

        self.input_entry = ttk.Entry(self.master, textvariable=tk.StringVar(), width=65, font=self.font_label_style)
        self.input_entry.grid(row=2, column=0, columnspan=2, sticky=tk.E + tk.W, padx=Constants.APP_PADDING)

        self.master.rowconfigure(3, minsize=Constants.APP_ROW_MIN_SIZE)

        self.output_label = ttk.Label(self.master, text=Constants.LABEL_OUTPUT_TITLE, font=self.font_label_style)
        self.output_label.grid(row=4, column=0, sticky=tk.W, padx=Constants.APP_PADDING)

        self.output_entry = ttk.Entry(
            self.master, textvariable=self.selected_file_path, width=55, font=self.font_label_style, state='readonly'
        )
        self.output_entry.grid(row=5, column=0, sticky=tk.W, padx=Constants.APP_PADDING)

        self.select_output_button = ttk.Button(
            self.master, text=Constants.BUTTON_BROWSE_TITLE, command=self._select_output_button_callback, width=10
        )
        self.select_output_button.grid(row=5, column=1, sticky=tk.W, padx=(0, Constants.APP_PADDING))

        self.master.rowconfigure(6, minsize=Constants.APP_ROW_MIN_SIZE)

        self.download_button = ttk.Button(
            self.master, text=Constants.BUTTON_DOWNLOAD_TITLE, command=self._download_button_callback
        )
        self.download_button.grid(row=7, column=0, columnspan=2, sticky=tk.E, padx=Constants.APP_PADDING)

        self.master.rowconfigure(8, minsize=Constants.APP_ROW_MIN_SIZE)

        self.stdout_label = ttk.Label(self.master, textvariable=self.std_output, wraplength=430)
        self.stdout_label.grid(row=9, column=0, columnspan=2, sticky=tk.W, padx=Constants.APP_PADDING)

    def disable_controls(self) -> None:
        """Disable all user controls."""
        self.input_entry.config(state=tk.DISABLED)
        self.output_entry.config(state=tk.DISABLED)
        self.select_output_button.config(state=tk.DISABLED)
        self.download_button.config(state=tk.DISABLED)
        self.file_menu.entryconfig(Constants.MENU_FILE_NEW_TITLE, state=tk.DISABLED)

    def enable_controls(self) -> None:
        """Enable all user controls."""
        self.input_entry.config(state=tk.NORMAL)
        self.output_entry.config(state='readonly')
        self.select_output_button.config(state=tk.NORMAL)
        self.download_button.config(state=tk.NORMAL)
        self.file_menu.entryconfig(Constants.MENU_FILE_NEW_TITLE, state=tk.NORMAL)

    def _download_playlist(self, input_url: str, output_file: str) -> None:
        """
        Download the playlist from the given input URL.

        :param input_url: Input URL (.m3u8).
        :type input_url: str
        :param output_file: Output file (.mp4).
        :type output_file: str
        :return: None
        """
        self.download_thread = DownloadThread(input_url, output_file, self)
        self.download_thread.start()

    def _download_button_callback(self) -> None:
        """Callback function for the download button."""
        input_url = self.input_entry.get()
        output_file = self.output_entry.get()

        if not input_url or not output_file:
            messagebox.showwarning(Constants.INVALID_INPUT_TITLE, Constants.INVALID_INPUT_MESSAGE)
            return

        self._download_playlist(input_url, output_file)

    def _select_output_button_callback(self) -> None:
        """Callback function for the select output button."""
        file_types = Constants.BROWSE_FILE_TYPES
        selected_file_name = filedialog.asksaveasfilename(
            filetypes=file_types, defaultextension=Constants.BROWSE_DEFAULT_EXTENSION
        )
        if selected_file_name:
            self.selected_file_path.set(selected_file_name)

    def _new_callback(self) -> None:
        """Callback function for the 'New' option in the file menu."""
        self.input_entry.delete(0, tk.END)
        self.selected_file_path = ''

    def _exit_callback(self) -> None:
        """Callback function for the 'Exit' option in the file menu."""
        if self.download_thread and self.download_thread.is_alive():
            messagebox.showwarning(Constants.DOWNLOAD_IN_PROGRESS_TITLE, Constants.DOWNLOAD_IN_PROGRESS_MESSAGE)
            return

        self.master.destroy()

    def _help_callback(self) -> None:
        """Callback function for the 'Help' option in the help menu."""
        webbrowser.open(self.help_link)


class DownloadThread(threading.Thread):
    """Thread class for downloading M3U8 playlists in a separate thread."""

    def __init__(self, input_url: str, output_file: str, source: M3U8DownloaderUI) -> None:
        """
        Initialize the DownloadThread class.

        :param input_url: Input URL (.m3u8).
        :type input_url: str
        :param output_file: Output file (.mp4).
        :type output_file: str
        :param source: The source M3U8DownloaderUI instance.
        :type source: M3U8DownloaderUI
        """
        super().__init__()
        self.input_url = input_url
        self.output_file = output_file
        self.source = source
        self.skip_space_check = False
        self.debug = False

    def _load_config(self) -> None:
        """Load configuration settings from the config file (if exists)."""
        if os.path.exists(Constants.CONFIG_FILE):
            with open(Constants.CONFIG_FILE, 'r') as file:
                config = json.load(file)
                self.skip_space_check = config.get('skip_space_check', False)
                self.debug = config.get('debug', False)

    def run(self) -> None:
        """Run the download process in a separate thread."""
        from pym3u8downloader import M3U8Downloader, M3U8DownloaderError

        try:
            self._load_config()
            self.source.disable_controls()
            sys.stdout = StdoutRedirector(self.source.std_output)
            downloader = M3U8Downloader(self.input_url, self.output_file, self.skip_space_check, self.debug)
            downloader.download_playlist()
            messagebox.showinfo(Constants.DOWNLOAD_COMPLETE_TITLE, Constants.DOWNLOAD_COMPLETE_MESSAGE)
        except (OSError, ValueError, TypeError, M3U8DownloaderError) as e:
            messagebox.showerror(Constants.DOWNLOAD_ERROR_TITLE, str(e))
        finally:
            self.source.enable_controls()


class AboutUI:
    """
    Class for creating an 'About' window in the M3U8 Downloader application.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """
        Initialize the AboutUI class.

        :param parent: The parent Tkinter root window.
        :type parent: tk.Tk
        """
        self.parent = parent
        self.window = tk.Toplevel(self.parent)
        self.window.title(Constants.ABOUT_TITLE)
        self.window.resizable(False, False)
        self.window.transient(self.parent)
        self.window.grab_set()

        self._set_window_size()
        self._set_defaults()
        self._set_styles()
        self._set_fonts()
        self._set_controls()

    def _set_window_size(self) -> None:
        """Set the size and position of the about window."""
        self.window_width = Constants.ABOUT_WINDOW_WIDTH
        self.window_height = Constants.ABOUT_WINDOW_HEIGHT
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.window.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')

    def _set_defaults(self) -> None:
        """Set default values for various attributes."""
        self.header = 'About this app'
        self.app_name = 'M3U8 Downloader'
        self.app_version = Constants.APP_VERSION
        self.copyrights = '© 2024 coldsofttech'
        self.license_type = 'MIT License'
        self.license_link = 'https://raw.githubusercontent.com/coldsofttech/pym3u8downloaderui/main/LICENSE'

    def _set_styles(self) -> None:
        """Set styles for the about window."""
        self.window.tk_setPalette(
            background=Constants.APP_PALETTE_BACKGROUND, foreground=Constants.APP_PALETTE_FOREGROUND
        )
        self.style = ttk.Style()
        self.style.theme_use(Constants.APP_THEME)

        self.no_background_style = ttk.Style()
        self.no_background_style.configure('NoBackground.TLabel', background=self.window.cget('background'))

    def _set_fonts(self) -> None:
        """Set font styles for labels."""
        self.font_header_style = (Constants.APP_LABEL_FONT_TYPE, 15, Constants.APP_LABEL_FONT_STYLE)
        self.font_label_style = (Constants.APP_LABEL_FONT_TYPE, 10)

    def _set_controls(self) -> None:
        """Set up various controls/widgets in the about window."""
        self.window.rowconfigure(0, minsize=Constants.APP_ROW_MIN_SIZE)

        self.header_label = ttk.Label(
            self.window, text=self.header, font=self.font_header_style, style='NoBackground.TLabel'
        )
        self.header_label.grid(row=1, column=0, sticky=tk.W, padx=Constants.APP_PADDING)

        self.window.rowconfigure(2, minsize=Constants.APP_ROW_MIN_SIZE)

        self._show_icon()

        self.window.rowconfigure(4, minsize=Constants.APP_ROW_MIN_SIZE)

        self.app_name_label = ttk.Label(
            self.window, text=f'{self.app_name} {self.app_version}', font=self.font_label_style,
            style='NoBackground.TLabel'
        )
        self.app_name_label.grid(row=5, column=0, sticky=tk.W, padx=Constants.APP_PADDING)

        self.copyright_label = ttk.Label(
            self.window, text=self.copyrights, font=self.font_label_style, style='NoBackground.TLabel'
        )
        self.copyright_label.grid(row=6, column=0, sticky=tk.W, padx=Constants.APP_PADDING)

        self.window.rowconfigure(7, minsize=Constants.APP_ROW_MIN_SIZE)

        self.license_label = ttk.Label(
            self.window, text=self.license_type, foreground='blue', cursor='hand2', font=self.font_label_style,
            style='NoBackground.TLabel'
        )
        self.license_label.grid(row=8, column=0, sticky=tk.W, padx=Constants.APP_PADDING)
        self.license_label.bind('<Button-1>', self._open_license)

    def _show_icon(self) -> None:
        """Show icon for the application."""
        import requests

        try:
            response = requests.get(Constants.APP_ICON_IMAGE_FILE_PATH)
            if response.status_code == 200:
                image_data = response.content
                self.image = tk.PhotoImage(data=image_data)
                self.image = self.image.subsample(int(self.image.width() / 64), int(self.image.height() / 64))

                self.icon_label = ttk.Label(self.window, image=self.image)
                self.icon_label.image = self.image
                self.icon_label.grid(row=3, column=0, sticky=tk.W, padx=Constants.APP_PADDING)
        except requests.RequestException:
            pass

    def _open_license(self, event) -> None:
        """
        Open the license link in a web browser.

        :param event: Mouse click event.
        :type event: tkinter.Event
        :return: None
        """
        webbrowser.open(self.license_link)


def main():
    root = tk.Tk()
    M3U8DownloaderUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
