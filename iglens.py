import customtkinter as ctk, sys, os, json, pyglet

from tkinter import *

# ts actually puts the window off center.
# NOT using it puts the window in the center.
# wtf
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")



def get_follower_list_dir():
    pass


def get_following_list_dir():
    pass



def main():
    # constants
    VERSION_NAME = "v0.1-a"
    FONT_PATH = os.path.join(os.path.dirname(__file__), 'assets')
    FONT_NAME = "handcaps-regular.otf"
    HANDCAPS = "Handcaps"

    # add font with pyglet
    pyglet.font.add_file(os.path.join(FONT_PATH, FONT_NAME))

    # general window attributes
    root = ctk.CTk()
    root.title('IGlens v0.1-a')
    root.geometry('400x400')
    root.resizable(width=False, height=False)
    root.configure(fg_color='#999999')

    # set up grid format
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # create wrapper frame inside main window
    frame = ctk.CTkFrame(root, fg_color='#999999')
    frame.grid(column = 0, row = 0, sticky = (N, W, E, S), padx = 15, pady = 15)

    # create layout for wrapper frame
    frame.columnconfigure(10, weight = 1)
    frame.rowconfigure(10, weight = 1)

    # create custom Ctk font
    handcaps_50_bold = ctk.CTkFont(family=HANDCAPS, size=50, weight='bold')
    handcaps_20 = ctk.CTkFont(family=HANDCAPS, size = 20)
    handcaps_25 = ctk.CTkFont(family=HANDCAPS, size = 25)

    # define UI elements
    title_label = ctk.CTkLabel(frame, text = 'IGLens', text_color='#222222', justify = 'left',
        padx = 0, pady = 0, font=handcaps_50_bold)
    
    version_label = ctk.CTkLabel(frame, text = VERSION_NAME, text_color = '#222222', 
        padx = 0, pady = 0, justify = 'left', font=handcaps_20)
    
    follower_button = ctk.CTkButton(frame, text = 'follower list...', 
        command = get_follower_list_dir, width = 150, fg_color = '#222222', hover_color = '#333333',
        corner_radius = 10, text_color = '#999999', font = handcaps_25, border_spacing = 0)

    following_button = ctk.CTkButton(frame, text = 'following list...', 
    command = get_following_list_dir, width = 150, fg_color = '#222222', hover_color = '#333333',
    corner_radius = 10, text_color = '#999999', font = handcaps_25, border_spacing = 0)

    # place UI elements on grid
    title_label.grid(row = 0, column = 0, columnspan = 3)
    
    version_label.grid(row = 0, column = 3, columnspan = 1, padx = (15, 0), pady = (20, 0))

    follower_button.grid(row = 1, column = 0, columnspan = 2)

    following_button.grid(row = 2, column = 0, columnspan = 2) 


    root.mainloop()



if __name__ == '__main__':
    main()