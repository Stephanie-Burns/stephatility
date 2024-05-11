
import tkinter as tk

from containers.directory_cleaner import DirectoryCleaner
from containers.tempfile_generator import TempFileGenerator

class UtilApp(tk.Frame):
    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)

        self.current_ip = '192.168.1.100'  # This would ideally come from a configuration or external source

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        # Initialize Containers
        self.x = DirectoryCleaner(self,"C:/Viper")
        self.y = DirectoryCleaner(self,"C:/ViperConfigData")
        self.z = TempFileGenerator(self)
        self.x.grid(row=0, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
        self.y.grid(row=1, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
        self.z.grid(row=2, column=0, columnspan=4, sticky='ew', padx=5, pady=5)





def main():
    root = tk.Tk()
    root.title('ViperTility')
    app = UtilApp(root)
    app.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
