"""
    Created on Mon Jul 25 09:45:16 2022
    v2 of code: 2023/02/04
    - Adding getters and setters
    v3 of code: 2023/06
    - Use @property

    Class DataManager to manage the data (jeje)
    :copyright: (c) 2022-2023 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""

import pandas as pd
from random import randint


class DataManager(object):
    """
    For now only spanish=english included.
    Modes: new_word, correct_answer, save_data
    """
    __word_guess_solution = ('Click en New Word', 'Click New Word')  # Word to guess, word translated

    def __init__(self, username: str = 'No_Username'):
        self.open_study_file(username)
        self.open_correct_answers_file(username)

    ## Properties =========================================
    @property
    def index(self) -> int:
        return self._index
    
    @index.setter
    def index(self, new_index:int = 0) -> None:
        self._index = new_index

    def set_word_tuple(self, word_to_guess: str = '', word_translated: str = ''):
        """Set the guess word"""
        self.__word_guess_solution = (word_to_guess, word_translated)

    def get_word_to_guess(self):
        """Retrieve the value of the word to guess."""
        return self.__word_guess_solution[0]

    def get_word_translated(self):
        """Retrieve the translated word."""
        return self.__word_guess_solution[1]
    ## ===================================================
    
    def open_study_file(self, username: str) -> None:
        """Open the current study file or create new one.
        """
        try:
            self.df = pd.read_csv(f'./data/{username}_es_en.csv',
                                  encoding_errors='replace')

        except FileNotFoundError:
            # User has no file, therefore, gather default values
            self.df = pd.read_csv('./data/languages/original_es_en.csv',
                                  encoding_errors='replace')
    
    def open_correct_answers_file(self, username: str) -> None:
        """Open the correct answers file if any, else create new one.
        """
         # Open correct answers file
        try:
            self.df_correct = pd.read_csv(f'./data/{username}_es_en_correct.csv',
                                          encoding_errors='replace')

        except FileNotFoundError:
            # User has no file, therefore, initial df (spanish english)
            self.df_correct = pd.DataFrame({'es': [], 'en': []})

    def new_word(self) -> None:
        """Select a new random word to study.
        """
        # Number of rows -- may change when correct answer
        df_rows = self.df[self.df.columns[0]].shape[0]
        # Get random item from data
        find = randint(0, df_rows)

        # Set the tuple of words (guess, solution)
        self.set_word_tuple(self.df[self.df.columns[0]][find],
                            self.df[self.df.columns[1]][find])

        # Change type of retrieving index to prevent multiple choice
        mask = (self.df[self.df.columns[0]] == self.get_word_to_guess()) &\
               (self.df[self.df.columns[1]] == self.get_word_translated())
        self.index = self.df[mask].index[0]

    def correct_answer(self) -> None:
        """Move the correct answer to correct df and drop from base"""
        try:
            self.df_correct = pd.concat([self.df_correct,
                                         self.df.iloc[[self.index]]],
                                        ignore_index=True)

        except AttributeError:
            pass

        else:  # Drop from original file
            self.df = self.df.drop(self.index)  # [0])
            # in case of same word multiple answers, drop 1 of them

    def save_data(self, username: str) -> None:
        """ Store current status.
        :param username: Username that is studying.
        """
        # a. List of correct answers
        self.df_correct.to_csv(f'./data/{username}_es_en_correct.csv',
                               index=False)
        # b. List of actual answers
        self.df.to_csv(f'./data/{username}_es_en.csv',
                       index=False)


if __name__ == '__main__':
    print('Use for tests only')
    # Get the data
    data = DataManager('UserCool')
