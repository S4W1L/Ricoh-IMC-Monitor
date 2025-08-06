import tkinter as tk
from printer_monitor import PrinterMonitorApp
import os
import sys

def resource_path(relative_path):
    """Usado para aceder a recursos quando empacotado com PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    root = tk.Tk()

    icon_path = resource_path("ricoh.ico")

    # Verifica se o ficheiro existe antes de aplicar
    if os.path.exists(icon_path):
        root.iconbitmap(default=icon_path)
    else:
        print("Icon file not found:", icon_path)

    app = PrinterMonitorApp(root)
    root.mainloop()
