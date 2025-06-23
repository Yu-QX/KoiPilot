import tkinter as tk
from .KOI import DesktopKOI

def main():
    root = tk.Tk()
    app = DesktopKOI(root)
    root.mainloop()

if __name__ == "__main__":
    main()