from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import string
import random
from random import choice
from string import ascii_lowercase as abc

author = 'Sean Hofland'

doc = """
oTree experiment playing hangman
"""
LTR_ERR = 'SOMETHING IS WRONG WITH LETTERS!'


class Constants(BaseConstants):
    name_in_url = 'hangman52'
    players_per_group = None
    mywords = ['cat', 'bat', 'crazy']
    num_rounds = len(mywords)
    num_attempts = 10
    max_num_attempts = 15
    assert num_attempts <= max_num_attempts, 'TOO MANY ATTEMPTS'


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.session.get_participants():
                words = Constants.mywords
                random.shuffle(words)
                p.vars['words'] = words
        for p in self.get_players():
            p.word_to_guess = p.participant.vars['words'][p.round_number - 1]
            p.len_word = len(p.word_to_guess)
            p.to_choose = abc
            p.chosen = ''
            p.correct = '_' * len(p.word_to_guess)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    win = models.BooleanField(default=False)
    lost = models.BooleanField(default=False)
    game_array = models.CharField()
    correct = models.CharField()
    wrong = models.CharField(initial='')
    to_choose = models.CharField()
    chosen = models.CharField(initial='')
    word_to_guess = models.CharField()
    len_word = models.IntegerField()
    last_letter = models.CharField()
    last_letter_correct = models.CharField()

    def update_word_sets(self, letter):
        p = self
        if not (p.win or p.lost):
            assert letter in p.to_choose, LTR_ERR
            assert letter not in p.chosen, LTR_ERR
            assert letter not in p.correct, LTR_ERR
            p.last_letter = letter
            p.to_choose = p.to_choose.replace(letter, "")
            p.chosen += letter
            if letter in p.word_to_guess:
                p.last_letter_correct = True
                indices = [i for i, x in enumerate(p.word_to_guess) if x == letter]
                correct = list(p.correct)
                for i in indices:
                    correct[i] = letter
                p.correct = ''.join(correct)
            else:
                p.last_letter_correct = False
                p.wrong += letter

            if p.correct == p.word_to_guess:
                p.win = True
            else:
                p.win = False
            if p.correct != p.word_to_guess and len(p.wrong) >= Constants.num_attempts:
                p.lost = True
            p.save()
            return True
        return False
