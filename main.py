import tkinter as tk
from tkinter import ttk


DARK_BG = "#1e1e1e"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech To Latex Converter")
        self.root.geometry("900x600")
        self.root.configure(bg=DARK_BG)

        self.setup_style()
        self.create_widgets()
        self.configure_grid()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("TFrame", background=DARK_BG)
        style.configure("TLabel", background=DARK_BG, foreground="white")
        style.configure("TButton", padding=10)

    def create_widgets(self):
        # Outer frame
        self.outer_frame = ttk.Frame(self.root, padding=10)
        self.outer_frame.grid(row=0, column=0, sticky="nsew")

        # Top display frames
        self.text_frame = tk.Frame(
            self.outer_frame,
            bg=DARK_BG,
            highlightbackground="white",
            highlightthickness=1
        )
        self.text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.image_frame = tk.Frame(
            self.outer_frame,
            bg=DARK_BG,
            highlightbackground="white",
            highlightthickness=1
        )
        self.image_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Labels centered inside frames
        self.text_label = ttk.Label(self.text_frame, text="Text Display")
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")

        self.image_label = ttk.Label(self.image_frame, text="Image Display")
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Buttons
        self.button_frame = ttk.Frame(self.outer_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=20)

        self.btn1 = ttk.Button(self.button_frame, text="Button", command=self.on_button1)
        self.btn1.grid(row=0, column=0, padx=20)

        self.btn2 = ttk.Button(self.button_frame, text="Button", command=self.on_button2)
        self.btn2.grid(row=0, column=1, padx=20)

    def configure_grid(self):
        # Root expands
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Outer frame expands
        self.outer_frame.grid_rowconfigure(0, weight=1)
        self.outer_frame.grid_rowconfigure(1, weight=0)

        self.outer_frame.grid_columnconfigure(0, weight=1)
        self.outer_frame.grid_columnconfigure(1, weight=1)

    def on_button1(self):
        self.text_label.config(text="Button 1 clicked")

    def on_button2(self):
        self.text_label.config(text="Button 2 clicked")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

