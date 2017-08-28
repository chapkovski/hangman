var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var wpsocket = new WebSocket(ws_scheme + '://' + window.location.host + "/hangman/{{player.participant.code}}/{{player.pk}}");


// Handle any errors that occur.
wpsocket.onerror = function (error) {
    console.log('WebSocket Error: ' + error);
};

// Show a connected message when the WebSocket is opened.
wpsocket.onopen = function (event) {
    console.log('connected to oTree');
};

var data;
// Handle messages sent by the server.
wpsocket.onmessage = function (e) {
    data = JSON.parse(e.data);
    if (data.correct == true) {
        for (i = 0; i < len_word; i++) {
            var curletter = data.guessed_word[i];
            $('p#correct' + i).html(curletter);
        }
    }
    ;


    $('span#attempts').html(data.attempts);
    for (var i = 1, len = data.parts_to_show; i <= len; i++) {
        $('div#hang' + i).css("visibility", "visible");
    }
    if (data.win == true | data.lost == true) {
        $('div#image').css("visibility", "visible");
        $('#winbutton').show();
        $('#overlay').show();
        // var endofgamemessage=
        $('p.endofgamemessage').html( data.win==true? ' Congratulations! You won!':  'Sorry! You lost!');
         $('#myModal').modal('toggle');
    }
    ;

};


// Show a disconnected message when the WebSocket is closed.
wpsocket.onclose = function (event) {
    console.log('disconnected from oTree');
};



