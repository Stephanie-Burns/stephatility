import unittest
from pathlib import Path
import tkinter as tk
from unittest.mock import patch, Mock

from src.gui.icon_manager import IconManager
from src.constants import ASSETS_DIR


class TestIconManager(unittest.TestCase):

    def setUp(self):
        # Create a Tkinter root window
        self.root = tk.Tk()
        # Reset IconManager instance for each test
        IconManager._instance = None
        self.icon_manager = IconManager()

    def tearDown(self):
        # Destroy the Tkinter root window
        self.root.destroy()

    def test_register_icon(self):
        icon_path = ASSETS_DIR / 'test.png'
        self.icon_manager.register_icon('test_icon', icon_path)
        self.assertIn('test_icon', self.icon_manager._icon_paths)
        self.assertEqual(self.icon_manager._icon_paths['test_icon'], icon_path)

    @patch('tkinter.PhotoImage')
    def test_get_icon(self, mock_photoimage):
        # Create a mock PhotoImage instance with width and height methods
        mock_instance = Mock()
        mock_instance.width.return_value = 32
        mock_instance.height.return_value = 32
        mock_instance.subsample.return_value = mock_instance
        mock_photoimage.return_value = mock_instance

        icon_path = ASSETS_DIR / 'test.png'
        self.icon_manager.register_icon('test_icon', icon_path)

        icon = self.icon_manager.get_icon('test_icon', (16, 16))
        mock_photoimage.assert_called_once_with(file=str(icon_path))
        self.assertIs(icon, mock_instance)

    @patch('tkinter.PhotoImage')
    def test_get_default_icon_when_icon_not_found(self, mock_photoimage):
        mock_instance = Mock()
        mock_instance.subsample.return_value = mock_instance
        mock_photoimage.return_value = mock_instance

        icon = self.icon_manager.get_icon('non_existent_icon', (16, 16))
        self.assertIs(icon, self.icon_manager.default_icon)

    @patch('tkinter.PhotoImage', side_effect=Exception('File not found'))
    def test_get_default_icon_when_icon_load_fails(self, mock_photoimage):
        icon_path = Path('path/to/invalid_icon.png')
        self.icon_manager.register_icon('invalid_icon', icon_path)

        icon = self.icon_manager.get_icon('invalid_icon', (16, 16))
        self.assertIs(icon, self.icon_manager.default_icon)

    def test_singleton(self):
        another_instance = IconManager()
        self.assertIs(another_instance, self.icon_manager)


if __name__ == '__main__':
    unittest.main()
