import customtkinter as ctk, sys, os, json, pyglet
from tkinter import *
from tkinter import filedialog



# app state manager class
class Iglens():
    def __init__(self):
        # variables and data
        self.follower_list = None
        self.following_list = None
        self.result_list = None
        self.mode = 0

        # core window
        self.root = ctk.CTk()
        
        # fonts
        self.HANDCAPS = 'Handcaps'
        self.handcaps_50_bold = ctk.CTkFont(family=self.HANDCAPS, size=50, weight='bold')
        self.handcaps_20 = ctk.CTkFont(family=self.HANDCAPS, size = 20)
        self.handcaps_25 = ctk.CTkFont(family=self.HANDCAPS, size = 25)
        self.handcaps_35_bold = ctk.CTkFont(family=self.HANDCAPS, size = 35)



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



def get_follower_list(filename_label, investigate_button):
    # ask user for file
    followers_file = filedialog.askopenfile(mode='r', title = 'Select Meta JSON file containing followers...')
    # parse file
    followers_raw_data = json.load(followers_file)
    # initialize list
    follower_list = []

    # parse list and extract usernames
    for follower in followers_raw_data:
        follower_list.append(follower['string_list_data'][0]['value'])

    # assign parsed list to global object
    iglens.follower_list = follower_list

    # change filename label in GUI
    filename_label.configure(text = os.path.basename(followers_file.name))

    # update button state
    update_button_state(investigate_button)



def get_following_list(filename_label, investigate_button):
    # ask user for file
    following_file = filedialog.askopenfile(mode = 'r', title = 'Select Meta JSON file containing following...')
    # parse file
    following_raw_data = json.load(following_file)
    # initialize list
    following_list = []

    # parse list and extract usernames
    for following in following_raw_data['relationships_following']:
        following_list.append(following['string_list_data'][0]['value'])
    
    # assign parsed list to global object
    iglens.following_list = following_list

    # change filename label in GUI
    filename_label.configure(text = os.path.basename(following_file.name))

    # update button state
    update_button_state(investigate_button)
    


def fetch_nonfollowers():
    followers_set = set(iglens.follower_list)
    following_set = set(iglens.following_list)

    nonfollowers_set = following_set.difference(followers_set)
    nonfollowers_list = list(nonfollowers_set)
    nonfollowers_list.sort()


    return nonfollowers_list



def fetch_fans():
    followers_set = set(iglens.follower_list)
    following_set = set(iglens.following_list)

    fans_set = followers_set.difference(following_set)
    fans_list = list(fans_set)
    fans_list.sort()

    return fans_list



def fetch_friends():
    followers_set = set(iglens.follower_list)
    following_set = set(iglens.following_list)

    friends_set = followers_set.intersection(following_set)
    friends_list = list(friends_set)
    friends_list.sort()

    return friends_list



def present_results():
    results_window = ctk.CTkToplevel(iglens.root)
    results_window.title('IGLens Results')
    results_window.geometry('350x600')
    results_window.wm_attributes("-type", "dialog")
    results_window.resizable(width = False, height = True)
    results_window.configure(fg_color = '#FFFBAD')

    scroll_frame = ctk.CTkScrollableFrame(results_window, label_text='Account list',
        label_font = iglens.handcaps_25, fg_color = '#FFFBAD')
    scroll_frame.pack(fill = 'both', expand = True, padx = 10, pady = 10)

    for acc in iglens.result_list:
        entry = ctk.CTkCheckBox(scroll_frame, text = acc, border_color = '#8F0024',
            text_color = '#8F0024', font=('Courier', 18, 'bold'))
        entry.pack(pady = 2, padx = 10, anchor = 'w')




def start_investigation(mode):
    match mode:
        case 1:
            iglens.result_list = fetch_nonfollowers()
        case 2:
            iglens.result_list = fetch_fans()
        case 3:
            iglens.result_list = fetch_friends()

    present_results()



def update_button_state(button):
    if iglens.follower_list is not None and iglens.following_list is not None \
        and iglens.mode != 0:
        button.configure(state='normal')
    else:
        button.configure(state='disabled')



def handle_radio_button(mode, investigate_button):
    iglens.mode = mode
    update_button_state(investigate_button)



def main():
    # constants
    VERSION_NAME = "v0.1-a"
    FONT_PATH = os.path.join(os.path.dirname(__file__), 'assets')
    FONT_NAME = "handcaps-regular.otf"
    HANDCAPS = "Handcaps"

    # add font with pyglet
    pyglet.font.add_file(os.path.join(FONT_PATH, FONT_NAME))

    # general window attributes
    root = iglens.root
    root.title('IGlens v0.1-a')
    root.geometry('400x430')
    root.resizable(width=False, height=False)
    root.configure(fg_color='#FFFBAD')

    # set up grid format
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # create wrapper frame inside main window
    frame = ctk.CTkFrame(root, fg_color='#FFFBAD')
    frame.grid(column = 0, row = 0, sticky = (N, W, E, S), padx = 15, pady = 15)

    # create layout for wrapper frame
    frame.columnconfigure(10, weight = 1)
    frame.rowconfigure(10, weight = 1)

    # define result mode variable
    mode = IntVar(value = 0)
    # link internal mode value to value in Iglens class
    iglens.mode = mode.get()

    # define UI elements
    title_label = ctk.CTkLabel(frame, text = 'IGLens', text_color='#8F0024', justify = 'left',
        padx = 0, pady = 0, font=iglens.handcaps_50_bold)
    
    version_label = ctk.CTkLabel(frame, text = VERSION_NAME, text_color = '#8F0024', 
        justify = 'left', padx = 0, pady = 0, font=iglens.handcaps_20)

    follower_filename_label = ctk.CTkLabel(frame, text = 'NO FILE SELECTED...', text_color='#8F0024',
        justify = 'right', padx = 0, pady = 0, font=iglens.handcaps_20)
    
    following_filename_label = ctk.CTkLabel(frame, text = 'NO FILE SELECTED...', text_color='#8F0024', 
        justify = 'right', padx = 0, pady = 0, font=iglens.handcaps_20)
    
    investigate_button = ctk.CTkButton(frame, text = 'Investigate!', 
        command = lambda: start_investigation(mode.get()), width = 300, fg_color = '#8F0024', hover_color = '#520014',
        corner_radius = 10, text_color = '#FFFBAD', font = iglens.handcaps_35_bold, border_spacing = 0, state = 'disabled',
        text_color_disabled = '#FF1F57')

    follower_button = ctk.CTkButton(frame, text = 'follower list...', 
        command = lambda: get_follower_list(follower_filename_label, investigate_button), width = 150, 
        fg_color = '#8F0024', hover_color = '#520014', corner_radius = 10, text_color = '#FFFBAD', 
        font = iglens.handcaps_25, border_spacing = 0)

    following_button = ctk.CTkButton(frame, text = 'following list...', 
        command = lambda: get_following_list(following_filename_label, investigate_button), width = 150, 
        fg_color = '#8F0024', hover_color = '#520014', corner_radius = 10, text_color = '#FFFBAD', 
        font = iglens.handcaps_25, border_spacing = 0)
    
    mode_select_hint_label = ctk.CTkLabel(frame, text = 'Select type of output:', text_color='#8F0024',
        justify = 'left', padx = 0, pady = 0, font= iglens.handcaps_25)
    
    nonfollowers_rdo = ctk.CTkRadioButton(frame, text='doesn\'t-follow-back', width = 100,
        corner_radius = 10, border_color='#8F0024', text_color='#8F0024', text_color_disabled='#444444',
        hover=True, state='normal', command=lambda: handle_radio_button(mode.get(), investigate_button), variable=mode, 
        value = 1, font = iglens.handcaps_20, hover_color = '#520014', fg_color='#8F0024', border_width_checked=8)
    
    fans_rdo = ctk.CTkRadioButton(frame, text='fans', width = 100,
        corner_radius = 10, border_color='#8F0024', text_color='#8F0024', text_color_disabled='#444444',
        hover=True, state='normal', command=lambda: handle_radio_button(mode.get(), investigate_button), variable=mode, 
        value = 2, font = iglens.handcaps_20, hover_color = '#520014', fg_color='#8F0024', border_width_checked=8)

    friends_rdo = ctk.CTkRadioButton(frame, text='friends', width = 100,
        corner_radius = 10, border_color='#8F0024', text_color='#8F0024', text_color_disabled='#444444',
        hover=True, state='normal', command=lambda: handle_radio_button(mode.get(), investigate_button), variable=mode, 
        value = 3, font = iglens.handcaps_20, hover_color = '#520014', fg_color='#8F0024', border_width_checked=8)




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