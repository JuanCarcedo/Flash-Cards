"""
Created on Mon Jul 25 15:59:11 2022
    main.py
    Main program for the "flashcards" game to learn Spanish.
    :copyright: (c) 2022-2023 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
    Updates:
    - v2 2022 Some improvements in code.
    - v3 04/2023 GUI updated using customtkinter by TomSchimansky [https://github.com/TomSchimansky/CustomTkinter]

HOW TO IMPROVE THE CODE:
    Use df.to_dict(orient='records') to gather and use the data
        note rnd.choice()
"""
from gui import App, UsernameManager

if __name__ == '__main__':
    # Get the username (program based on that)
    username_manager = UsernameManager()
    username_manager.end_screen()
    # Create the App (GUI)
    app = App(username_manager.get_username())
    app.end_screen()
