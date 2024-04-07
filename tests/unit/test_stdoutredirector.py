import tkinter as tk
import unittest

import pytest

from src import StdoutRedirector


class TestStdoutRedirector(unittest.TestCase):
    """Unit test cases for StdoutRedirector"""

    def setUp(self):
        self.root = tk.Tk()
        self.text_variable = tk.StringVar()
        self.stdout_redirector = StdoutRedirector(self.text_variable)

    def tearDown(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    @pytest.mark.sequential_order
    def test_write(self):
        message = 'Hello World!'
        self.stdout_redirector.write(message)
        self.assertEqual(self.text_variable.get(), message)

    @pytest.mark.sequential_order
    def test_write_multiple(self):
        messages = ['Message 1', 'Message 2', 'Message 3']
        expected_output = 'Message 3'
        for message in messages:
            self.stdout_redirector.write(message)
        self.assertEqual(self.text_variable.get(), expected_output)


if __name__ == "__main__":
    unittest.main()
