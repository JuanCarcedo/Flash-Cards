"""
    gui.py
    Control the gui and other methods.
    :copyright: (c) 2022-2023 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
    - v3 02/2023:
        GUI: Updated using customtkinter by TomSchimansky [https://github.com/TomSchimansky/CustomTkinter]
        Code: Some enhancements to structure.
"""

import tkinter as tk
import customtkinter as ctk
from datamanager import DataManager

# Config of customtkinter
ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')  # Available: Blue, dark-blue, green

# CONSTANTS ============
INIT_TEXT = '''Welcome to the self study method with flashcards.
This program will store your right answers and your wrong answers separately.
Note "nn" equals "ñ". Example castanna is castaña.
Exit button will exit the application and save data.
'''
M_SECONDS_WAIT = 3000


class UsernameManager(ctk.CTk):
    """Manage the user's login (gather the username)"""

    def __init__(self):
        super().__init__()
        self.config(padx=10, pady=10)
        self.title('Log in')
        self.__basic_structure()

    def __basic_structure(self):
        ctk.CTkLabel(self, text="Please, enter your username:", font=('Arial', 15)).pack()
        self.input_username = tk.StringVar()
        entry_username = ctk.CTkEntry(self, textvariable=self.input_username)
        entry_username.pack(padx=10, pady=10)
        entry_username.focus()
        ctk.CTkButton(self, text='Ok', command=lambda: self.destroy()).pack()

    def end_screen(self) -> None:
        """End program."""
        self.mainloop()

    def get_username(self):
        return self.input_username.get()


class App(ctk.CTk):
    TITLE_APP = 'Flashcard learning'
    __username = 'New'

    def __init__(self, username: str = ''):
        super().__init__()

        # Set the username (program based on that)
        self.set_username(username)

        # Get the data
        self.data = DataManager(self.get_username())

        # GUI
        self.eval('tk::PlaceWindow . center')  # Set the window to the middle of screen
        self.title(self.TITLE_APP)
        self.geometry('500x300')
        # Create welcome pop-up
        self.welcome_screen()

        # Building
        self.grid_columnconfigure(1, weight=1)
        self.__build_welcome()
        self.__build_words()
        self.__build_option_menus()
        self.__build_bottom()

    def welcome_screen(self):
        """Create a welcome screen."""
        window = ctk.CTkToplevel(self)
        window.title('Welcome!')
        window.geometry('500x150')
        label = ctk.CTkLabel(window, text=INIT_TEXT)
        label.pack(side='top', fill='both', expand=True, padx=20, pady=(10, 0))
        button_exit = ctk.CTkButton(window, text='Continue', command=lambda: window.destroy())
        button_exit.pack(fill='both', padx=20, pady=20)

    def end_screen(self) -> None:
        """End program."""
        self.mainloop()

    # Building the GUI ===================================================================
    def __build_welcome(self):
        self.legend_label = ctk.CTkLabel(self, text=f'Player: {self.get_username()}',
                                         font=ctk.CTkFont(size=25, weight='bold'))
        self.legend_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 10))

    def __build_words(self):
        """Flashcard building. """
        self.__label_learning_word = ctk.CTkLabel(self, text=self.data.get_word_to_guess(), font=ctk.CTkFont(size=20))
        self.__label_learning_word.grid(row=1, column=0, columnspan=3, padx=10, pady=(15, 15))

    def __build_option_menus(self):
        """Create menus/options available"""
        # Options menus -----
        self.frame_user = ctk.CTkFrame(self, width=300, fg_color='transparent')
        self.frame_user.grid(row=2, column=0, columnspan=2)

        # Refresh/new word or Exit
        self.frame_options = ctk.CTkFrame(self.frame_user, width=125)
        self.frame_options.grid(row=0, column=0, rowspan=3, columnspan=1, padx=(15, 5))
        self.btn_new_word = ctk.CTkButton(self.frame_options, command=self.new_word, text='New Word')
        self.btn_new_word.grid(row=0, column=0, padx=10, pady=10)
        self.btn_exit_save = ctk.CTkButton(self.frame_options, command=self.exit_program,
                                           text='Save & Exit',
                                           fg_color='transparent',
                                           border_width=1)
        self.btn_exit_save.grid(row=2, column=0, padx=10, pady=(40, 10))

        # Check answers
        self.frame_selection = ctk.CTkFrame(self.frame_user, width=100)
        self.frame_selection.grid(row=0, column=1, rowspan=3, columnspan=1, padx=(15, 5), pady=10)
        self.__radio_btn_check = tk.IntVar(value=0)  # Default value set to 0
        self.radio_btn_dont_know = ctk.CTkRadioButton(master=self.frame_selection,
                                                      variable=self.__radio_btn_check,
                                                      value=0,
                                                      text='I don\'t know')
        self.radio_btn_dont_know.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.radio_btn_i_know = ctk.CTkRadioButton(master=self.frame_selection,
                                                   variable=self.__radio_btn_check,
                                                   value=1,
                                                   text='I know! :)')
        self.radio_btn_i_know.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.btn_check_answer = ctk.CTkButton(self.frame_selection, command=self.check_answer, text='Check answer')
        self.btn_check_answer.grid(row=2, column=0, padx=(10, 10), pady=(5, 10))

    def __build_bottom(self):
        """Create the bottom layer of the app"""
        self.label_bottom = ctk.CTkLabel(self, text='Juan Carcedo © 2022-2023', font=ctk.CTkFont(size=10))
        self.label_bottom.grid(row=3, column=0, columnspan=3, padx=10, pady=(10, 10))

    # Logics / buttons ===================================================================
    def check_answer(self) -> None:
        """Show the correct answer. . """
        if self.get_radio_button_status() == 1:  # User knows the word
            # Save the word as user knows it
            self.data.correct_answer()

        # Show correct answer
        self.set_label_learning_word(self.data.get_word_translated())
        # Wait 3 seconds and create a new word.
        # self.wait_time()
        # # New Word
        # self.new_word()

    def new_word(self) -> None:
        """ Create a new word """
        # Retrieve a new word in the data class
        self.data.new_word()
        # Set in the screen the new word
        self.set_label_learning_word(self.data.get_word_to_guess())

    def wait_time(self, time_to_wait: int = M_SECONDS_WAIT):
        """
        Create idle time to wait.
        :param time_to_wait: int; if nothing is used, then use the default constant.
        """
        self.after(time_to_wait)

    def exit_program(self) -> None:
        """ Save and Exit """
        self.data.save_data(self.get_username())
        self.destroy()

    # Setters and getters ===========================================================
    def set_username(self, user: str = '') -> None:
        """Set the current username.
        :param user: Current user.
        """
        self.__username = user

    def get_username(self):
        """Get the value of the username."""
        return self.__username

    def set_label_learning_word(self, value: str = '') -> None:
        """
        Set the user entry field.
        :param value: string to set.
        :return:
        """
        self.__label_learning_word.configure(text=value)

    def get_label_learning_word(self):
        """Get the value of the word to guess"""
        return self.__label_learning_word.cget('text')

    def get_radio_button_status(self):
        """Get the selected radio button"""
        return self.__radio_btn_check.get()


if __name__ == '__main__':
    print('I am not meant to be executed as a main...')
