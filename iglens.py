import customtkinter as ctk, sys, os, json, pyglet
from tkinter import *
from tkinter import filedialog



# app state manager class
class Iglens():
    def __init__(self):
        self.follower_list = None
        self.following_list = None



# create instance of state manager
iglens = Iglens()



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



def get_follower_list():
    # ask user for file
    followers_file = filedialog.askopenfile(mode='r', title = 'Select Meta JSON file containing followers...')
    # parse file
    followers_raw_data = json.load(followers_file)
    # initialize list
    follower_list = []

    # parse list and extract usernames
    for follower in followers_raw_data:
        follower_list.append(follower['string_list_data'][0]['value'])

    print(len(follower_list))
    # assign parsed list to global object
    iglens.follower_list = follower_list



def get_following_list():
    # ask user for file
    following_file = filedialog.askopenfile(mode = 'r', title = 'Select Meta JSON file containing following...')
    # parse file
    following_raw_data = json.load(following_file)
    # initialize list
    following_list = []

    # parse list and extract usernames
    for following in following_raw_data['relationships_following']:
        following_list.append(following['string_list_data'][0]['value'])
    
    print(len(following_list))
    # assign parsed list to global object
    iglens.following_list = following_list




def not_implemented():
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
    root.geometry('400x430')
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
    handcaps_35_bold = ctk.CTkFont(family=HANDCAPS, size = 35)

    # define result mode variable
    mode = IntVar(value = 0)

    # define UI elements
    title_label = ctk.CTkLabel(frame, text = 'IGLens', text_color='#222222', justify = 'left',
        padx = 0, pady = 0, font=handcaps_50_bold)
    
    version_label = ctk.CTkLabel(frame, text = VERSION_NAME, text_color = '#222222', 
        justify = 'left', padx = 0, pady = 0, font=handcaps_20)
    
    follower_button = ctk.CTkButton(frame, text = 'follower list...', 
        command = get_follower_list, width = 150, fg_color = '#222222', hover_color = '#333333',
        corner_radius = 10, text_color = '#999999', font = handcaps_25, border_spacing = 0)

    following_button = ctk.CTkButton(frame, text = 'following list...', 
        command = get_following_list, width = 150, fg_color = '#222222', hover_color = '#333333',
        corner_radius = 10, text_color = '#999999', font = handcaps_25, border_spacing = 0)

    follower_filename_label = ctk.CTkLabel(frame, text = 'NO FILE SELECTED...', text_color='#222222',
        justify = 'right', padx = 0, pady = 0, font=handcaps_20)
    
    following_filename_label = ctk.CTkLabel(frame, text = 'NO FILE SELECTED...', text_color='#222222', 
        justify = 'right', padx = 0, pady = 0, font=handcaps_20)
    
    mode_select_hint_label = ctk.CTkLabel(frame, text = 'Select type of output:', text_color='#222222',
        justify = 'left', padx = 0, pady = 0, font=handcaps_25)
    
    nonfollowers_rdo = ctk.CTkRadioButton(frame, text='doesn\'t-follow-back', width = 100,
        corner_radius = 10, border_color='#222222', text_color='#222222', text_color_disabled='#444444',
        hover=True, state='normal', command=not_implemented, variable=mode, value = 1, font = handcaps_20)
    
    fans_rdo = ctk.CTkRadioButton(frame, text='fans', width = 100,
        corner_radius = 10, border_color='#222222', text_color='#222222', text_color_disabled='#444444',
        hover=True, state='normal', command=not_implemented, variable=mode, value = 2, font = handcaps_20)

    friends_rdo = ctk.CTkRadioButton(frame, text='friends', width = 100,
        corner_radius = 10, border_color='#222222', text_color='#222222', text_color_disabled='#444444',
        hover=True, state='normal', command=not_implemented, variable=mode, value = 3, font = handcaps_20)

    investigate_button = ctk.CTkButton(frame, text = 'Investigate!', 
        command = not_implemented, width = 300, fg_color = '#222222', hover_color = '#333333',
        corner_radius = 10, text_color = '#999999', font = handcaps_35_bold, border_spacing = 0)


    # place UI elements on grid
    title_label.grid(row = 0, column = 0, columnspan = 2, sticky = 'w', pady = (0, 20))
    
    version_label.grid(row = 0, column = 2, columnspan = 3, padx = (0, 0), pady = (20, 20), sticky='w')

    follower_button.grid(row = 1, column = 0, columnspan = 2, sticky='w', pady = (0, 20))

    following_button.grid(row = 2, column = 0, columnspan = 2, sticky='w', pady = (0, 20))

    follower_filename_label.grid(row = 1, column = 2, columnspan = 10, sticky='e', pady=(0, 20))

    following_filename_label.grid(row = 2, column = 2, columnspan = 10, sticky='e', pady = (0, 20))

    mode_select_hint_label.grid(row = 3, column = 0, columnspan = 3, sticky = 'w')

    nonfollowers_rdo.grid(row = 4, column = 0, columnspan = 3, sticky = 'w', pady = (0, 5))

    fans_rdo.grid(row = 5, column = 0, columnspan = 3, sticky = 'w', pady = (0, 5))

    friends_rdo.grid(row = 6, column = 0, columnspan = 3, sticky = 'w', pady = (0, 20))

    investigate_button.grid(row = 7, column = 0, columnspan = 11)

    root.mainloop()



if __name__ == '__main__':
    main()