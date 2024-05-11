import tkinter as tk
from tkinter import ttk, filedialog
import shutil
import os
import APIAplication

# Constants for fonts and dimensions
LARGEFONT = ("Verdana", 35)
MENU_SIZE = (600, 600)  # Width and height for the menus

# Define paths for the background images
folder_path = 'userInterface'
mainMenu_background = os.path.join(folder_path, 'mainMenu.png')
gameMenu_background = os.path.join(folder_path, 'gameMenu.png')

content = ""

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Creating a container
        container = tk.Frame(self) 
        container.pack(side="top", fill="both", expand=True) 

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {} 

        # List all frames here
        for F in (StartPage, Page1, MainMenu, GameMenu):
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10) 

        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))
        button1.grid(row=1, column=1, padx=10, pady=10)

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=1, padx=10, pady=10)

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(width=MENU_SIZE[0], height=MENU_SIZE[1])
        self.bg_image = tk.PhotoImage(file=mainMenu_background)
        label = tk.Label(self, image=self.bg_image)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        button1 = ttk.Button(self, text="Play",
                             command=lambda: controller.show_frame(GameMenu))
        button1.place(x=5, y=5)

        label2 = tk.Label(self, text="This App Was Made For Comedic Purposes Only", wraplength=200,
                          justify='left', bg='white', fg='black',
                          font=('Helvetica', 12))
        label2.place(x=220, y=150)

class GameMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(width=MENU_SIZE[0], height=MENU_SIZE[1])
        self.bg_image = tk.PhotoImage(file=gameMenu_background)
        self.content = ""
        label = tk.Label(self, image=self.bg_image)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        button1 = ttk.Button(self, text="Main Menu",
                            command=lambda: controller.show_frame(MainMenu))
        button1.place(x=5, y=5)

        # Label for displaying text
        self.info_label = tk.Label(self, text=self.content, wraplength=325,  # width in pixels
                            justify='left', bg='white', fg='black',
                            font=('Helvetica', 12))
        self.info_label.place(x=150, y=100)  # Adjust placement accordingly

        # Button to trigger file selection and copying
        file_button = ttk.Button(self, text="Did you clean your room", command=self.file_button_command)
        file_button.place(x=85, y=5)


    def file_button_command(self):
        self.get_file_and_copy()
        new_content = APIAplication.CreateDescription()
        self.content = new_content
        self.info_label.config(text=self.content)  # Update info_label text

    def get_file_and_copy(self):
        # Open the file selection dialog
        file_path = filedialog.askopenfilename(title="Select an Image File",
                                               filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        
        if file_path:
            # Define the destination directory
            destination_folder = 'rooms'

            # Ensure the destination directory exists, if not, create it
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            # Define the new file path in the destination directory
            destination_path = os.path.join(destination_folder, 'photo.png')

            # Copy and rename the selected file to the destination folder
            shutil.copy(file_path, destination_path)
            

# Driver Code
app = tkinterApp()
app.mainloop()
