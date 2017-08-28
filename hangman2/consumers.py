from channels import Group
from channels.sessions import channel_session
import random
from .models import Player, Constants
import json
import time


def ws_connect(message, participant_code, player_pk):
    # message.content['text']
    message.reply_channel.send({
        "text": (json.dumps({'a': 111})),
    })


def ws_message(message, participant_code, player_pk):
    letter = message.content['text']
    print('LETTERRRR ', letter)
    player = Player.objects.get(participant__code=participant_code, pk=player_pk)
    word_to_guess = player.word_to_guess
    if player.update_word_sets(letter):
        if player.lost:
            parts_to_show = Constants.max_num_attempts
        else:
            parts_to_show = len(player.wrong)
        message.reply_channel.send({
            "text": (json.dumps({'letter': letter,
                                 'correct': player.last_letter_correct,
                                 'guessed_word': player.correct,
                                 'win': player.win,
                                 'lost': player.lost,
                                 'parts_to_show': parts_to_show,
                                 'attempts': len(player.wrong), })),
        })


def ws_disconnect(message, participant_code, player_pk):
    print('I AM DISCONNECTED')
