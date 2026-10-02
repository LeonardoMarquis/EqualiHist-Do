# necessita pip install pillow numpy matplotlib
# use pip install -r requirements.txt
import tkinter as tk
from interface import ImageEqualizerApp
import ctypes

myappid = 'dokizax.equalihistdo.tkinter.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("assets/grace_s_icon.ico")  
    app = ImageEqualizerApp(root)
    root.mainloop()