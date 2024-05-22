from tkinter import ttk

class DraggableTreeview(ttk.Treeview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Button-1>', self._select)
        self.bind('<B1-Motion>', self._move)
        self.bind('<ButtonRelease-1>', self._stop_dragging)
        self.bind('<<TreeviewSelect>>', self._on_select)
        self.curIndex = None
        self.scroll_speed = 1  # Default scroll speed
        self.scroll_delay = 200  # Delay in milliseconds between scroll steps
        self.scroll_timer = None
        self.dragging = False

    def _select(self, event):
        item = self.identify_row(event.y)
        if item:
            self.curIndex = item
            self.dragging = True

    def _move(self, event):
        if not self.dragging:
            return

        item = self.identify_row(event.y)
        if item and self.curIndex:
            index = self.index(item)
            curIndex = self.index(self.curIndex)
            if index < curIndex:
                self.move(self.curIndex, '', index)
                self.curIndex = self.get_children('')[index]
            elif index > curIndex and index < len(self.get_children('')) - 1:
                self.move(self.curIndex, '', index + 1)
                self.curIndex = self.get_children('')[index + 1]
            elif index == len(self.get_children('')) - 1:
                self.move(self.curIndex, '', index)
                self.curIndex = self.get_children('')[index]
            self._update_striping()

        # Scroll if the mouse is near the top or bottom edge
        scroll_boundary = 40  # Increase the boundary area
        if event.y < scroll_boundary:
            self._start_scrolling(-self.scroll_speed)
        elif event.y > self.winfo_height() - scroll_boundary:
            self._start_scrolling(self.scroll_speed)
        else:
            self._stop_scrolling()

        self._update_buttons_state()

    def _stop_dragging(self, event=None):
        self.dragging = False
        self._stop_scrolling()

    def _start_scrolling(self, direction):
        if self.scroll_timer is None:
            self._scroll(direction)

    def _scroll(self, direction):
        if self.dragging:  # Only scroll if dragging
            self.yview_scroll(direction, "units")
            self.scroll_timer = self.after(self.scroll_delay, self._scroll, direction)

    def _stop_scrolling(self):
        if self.scroll_timer is not None:
            self.after_cancel(self.scroll_timer)
            self.scroll_timer = None

    def _update_striping(self):
        for index, item in enumerate(self.get_children()):
            tags = ('even',) if index % 2 == 0 else ('odd',)
            self.item(item, tags=tags)

    def _on_select(self, event):
        self._update_buttons_state()

    def _update_buttons_state(self):
        if hasattr(self.master.master, 'update_buttons_state'):
            self.master.master.update_buttons_state()
