import tkinter as tk
import unittest
from unittest.mock import patch, MagicMock

import pytest

from src import M3U8DownloaderUI


class TestM3U8DownloaderUI(unittest.TestCase):
    """Unit test cases for M3U8DownloaderUI"""

    def setUp(self):
        self.root = tk.Tk()
        self.source = M3U8DownloaderUI(self.root)
        self.input_url = 'https://raw.githubusercontent.com/coldsofttech/pym3u8downloader/main/tests/files/index.m3u8'
        self.output_file = 'video.mp4'

    def tearDown(self) -> None:
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    @pytest.mark.sequential_order
    def test__select_output_button_callback(self):
        """Test if select output button callback works as expected"""
        with patch('tkinter.filedialog.asksaveasfilename') as mock_file_dialog:
            mock_file_dialog.return_value = self.output_file
            self.source._select_output_button_callback()
            self.assertEqual(self.source.selected_file_path.get(), self.output_file)

    @pytest.mark.sequential_order
    def test__new_callback(self):
        """Test if new callback works as expected"""
        self.source.input_entry.insert(0, self.input_url)
        self.source.selected_file_path.set(self.output_file)
        self.source._new_callback()
        self.assertEqual(self.source.input_entry.get(), '')
        self.assertEqual(self.source.selected_file_path, '')

    @pytest.mark.sequential_order
    def test__exit_callback_download_thread_running(self):
        """Test if exit callback displays warning when download is running"""
        self.source.download_thread = MagicMock()
        self.source.download_thread.is_alive.return_value = True

        with patch('tkinter.messagebox.showwarning') as mock_showwarning:
            self.source._exit_callback()
            mock_showwarning.assert_called_once()

    @pytest.mark.sequential_order
    def test__exit_callback_download_thread_not_running(self):
        """Test if exit callback works as expected"""
        self.source.download_thread = MagicMock()
        self.source.download_thread.is_alive.return_value = False
        self.source._exit_callback()
        try:
            master_title = self.source.master.title()
        except tk.TclError:
            master_title = None
        self.assertIsNone(master_title)

    @pytest.mark.sequential_order
    @patch('webbrowser.open')
    def test__help_callback(self, mock_open):
        """Test if help callback works as expected"""
        self.assertTrue(self.source.help_link.endswith('README.md'))
        self.source._help_callback()
        mock_open.assert_called_once_with(self.source.help_link)

    @pytest.mark.sequential_order
    def test_disable_controls(self):
        """Test if disable controls works as expected"""
        self.source.disable_controls()
        self.assertEqual(str(self.source.input_entry.cget('state')), 'disabled')
        self.assertEqual(str(self.source.output_entry.cget('state')), 'disabled')
        self.assertEqual(str(self.source.select_output_button.cget('state')), 'disabled')
        self.assertEqual(str(self.source.download_button.cget('state')), 'disabled')
        self.assertEqual(str(self.source.file_menu.entrycget(0, 'state')), 'disabled')

    @pytest.mark.sequential_order
    def test_enable_controls(self):
        """Test if enable controls works as expected"""
        self.source.enable_controls()
        self.assertEqual(str(self.source.input_entry.cget('state')), 'normal')
        self.assertEqual(str(self.source.output_entry.cget('state')), 'readonly')
        self.assertEqual(str(self.source.select_output_button.cget('state')), 'normal')
        self.assertEqual(str(self.source.download_button.cget('state')), 'normal')
        self.assertEqual(str(self.source.file_menu.entrycget(0, 'state')), 'normal')


if __name__ == "__main__":
    unittest.main()
