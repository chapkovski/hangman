from channels.routing import route
from .consumers import ws_message, ws_connect, ws_disconnect
from otree.channels.routing import channel_routing
from channels.routing import include

ending=r'^/(?P<participant_code>\w+)/(?P<player_pk>\w+)$'
hangman_routing = [route("websocket.connect",
                ws_connect,  path=ending),
                route("websocket.receive",
                ws_message,  path=ending),
                route("websocket.disconnect",
                ws_disconnect,  path=ending), ]
channel_routing += [
    include(hangman_routing, path=r"^/hangman"),
]
