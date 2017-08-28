from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from string import ascii_lowercase as abc
import json


class Gamepage(Page):
    def vars_for_template(self):


        if self.player.lost or self.player.win:
            parts_to_show = Constants.max_num_attempts
        else:
            parts_to_show = Constants.num_attempts
        return {'parts_to_show': range(1, parts_to_show + 1),
                'len_parts_to_show': parts_to_show,
                'incorrect_len': len(self.player.wrong),
                'total_image': range(1, Constants.max_num_attempts + 1),
                }


class GameItself(Page):
    ...


page_sequence = [Gamepage, ]
