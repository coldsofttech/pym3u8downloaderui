import tkinter as tk
import unittest
from unittest.mock import patch

import pytest

from src import AboutUI


class TestAboutUI(unittest.TestCase):
    """Unit test cases for AboutUI"""

    def setUp(self):
        self.root = tk.Tk()

    def tearDown(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    @pytest.mark.sequential_order
    @patch('webbrowser.open')
    def test__open_license_link(self, mock_open):
        about_ui = AboutUI(self.root)
        try:
            self.assertTrue(about_ui.license_link.endswith('LICENSE'))

            about_ui.license_label.event_generate('<Button-1>')
            mock_open.assert_called_once_with(about_ui.license_link)
        finally:
            about_ui.window.destroy()


if __name__ == "__main__":
    unittest.main()
