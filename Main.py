import sys, subprocess

required = ["customtkinter"]
for package in required:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

from UI.UIComponents import EightRooksApp

if __name__ == "__main__":
    app = EightRooksApp()
    window_width = 1300
    window_height = 650
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight() - 60
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    app.geometry(f"{window_width}x{window_height}+{x}+{y}")
    app.mainloop()