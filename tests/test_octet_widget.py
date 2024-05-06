import unittest
import tkinter as tk
from containers.widgets.octet_widget import OctetWidget


class TestOctetWidget(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.octet_widget = OctetWidget(self.root, self.advance_focus, 0, "192")
        self.octet_widget.pack()

    def advance_focus(self, index):
        # Dummy function to simulate focus advancement
        pass

    def test_initial_state(self):
        self.assertEqual(self.octet_widget.get(), "192")

    def test_valid_input(self):
        self.octet_widget.delete(0, tk.END)
        self.octet_widget.insert(0, "123")
        self.assertEqual(self.octet_widget.get(), "123")

    def test_invalid_input(self):
        self.octet_widget.delete(0, tk.END)
        self.octet_widget.insert(0, "256")
        self.octet_widget.on_focus_out(None)
        self.assertNotEqual(self.octet_widget.get(), "256")  # Assuming you reset it on invalid

    def test_arrow_navigation(self):
        # Assuming initial focus and cursor at the end
        self.octet_widget.focus_set()
        self.octet_widget.on_key_press(self.create_event('Left', 0x0000))
        self.assertEqual(self.octet_widget.index(tk.INSERT), 0)

    def create_event(self, keysym, state):
        return type('TestEvent', (object,), {'keysym': keysym, 'state': state})()

    def test_shift_enter_does_not_leave_first_octet(self):
        self.octet_widget.position = 0  # First octet
        self.octet_widget.on_key_press(self.create_event('Return', 0x0001))
        self.assertTrue(self.octet_widget.focus_get() is self.octet_widget)

    def tearDown(self):
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()
