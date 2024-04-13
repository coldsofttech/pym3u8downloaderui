import json
import os
import tkinter as tk
import unittest

import pytest

from src import M3U8DownloaderUI, DownloadThread


class TestDownloadThread(unittest.TestCase):
    """Unit test cases for DownloadThread class."""

    def setUp(self):
        self.root = tk.Tk()
        self.input_url = 'https://raw.githubusercontent.com/coldsofttech/pym3u8downloader/main/tests/files/index.m3u8'
        self.output_file = 'video.mp4'
        self.source = M3U8DownloaderUI(self.root)
        self.config_file = 'config.json'

    def tearDown(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    @pytest.mark.sequential_order
    def test__load_config_no_file(self):
        """Test if load config works as expected when configuration file do not exist"""
        thread = DownloadThread(self.input_url, self.output_file, self.source)
        thread._load_config()
        self.assertFalse(os.path.exists(self.config_file))
        self.assertFalse(thread.skip_space_check)
        self.assertFalse(thread.debug)

    @pytest.mark.sequential_order
    def test__load_config_skip_space_check(self):
        """Test if load config works as expected when skip space check is provided"""
        config = {
            'skip_space_check': True
        }
        try:
            with open(self.config_file, 'w') as file:
                file.write(json.dumps(config))

            thread = DownloadThread(self.input_url, self.output_file, self.source)
            thread._load_config()
            self.assertTrue(os.path.exists(self.config_file))
            self.assertTrue(thread.skip_space_check)
            self.assertFalse(thread.debug)
        finally:
            os.remove(self.config_file)

    @pytest.mark.sequential_order
    def test__load_config_debug(self):
        """Test if load config works as expected when debug is provided"""
        config = {
            'debug': True
        }
        try:
            with open(self.config_file, 'w') as file:
                file.write(json.dumps(config))

            thread = DownloadThread(self.input_url, self.output_file, self.source)
            thread._load_config()
            self.assertTrue(os.path.exists(self.config_file))
            self.assertFalse(thread.skip_space_check)
            self.assertTrue(thread.debug)
        finally:
            os.remove(self.config_file)

    @pytest.mark.sequential_order
    def test__load_config_invalid(self):
        """Test if load config raises json.JSONDecodeError"""
        config = ['Test']
        try:
            with open(self.config_file, 'w') as file:
                file.write(str(config))

            thread = DownloadThread(self.input_url, self.output_file, self.source)
            with self.assertRaises(json.JSONDecodeError):
                thread._load_config()
        finally:
            os.remove(self.config_file)


if __name__ == "__main__":
    unittest.main()
