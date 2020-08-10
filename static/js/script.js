var socket;
var playername;
var ishost = 0;
var roomname;

$(document).ready(function() {
    // The http vs. https is important. Use http for localhost!
    document.getElementById("join-form").style.display = "block";
    document.getElementById("waitingroom").style.display = "none";
    document.getElementById("game").style.display = "none";
    document.getElementById("hostwait").style.display = "none";

    socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('joinaff', function (data) {
        console.log('joinaff', data)
        if(data.ishost == 'T'){
            ishost = 1
            document.getElementById("hostwait").style.display = "block";
        }
        else{
            ishost = 0
        }
    });

    document.getElementById("joinbtn").onclick = function() {
        roomname = document.getElementById("roomname").value;
        playername = document.getElementById("playername").value;
        console.log('join game')
        socket.emit('join', {'roomname': roomname, 'playername': playername});
        // socket.on('redirect', function (data) {
        //     window.location = data.url + '?room=' + data.room;
        // });

        document.getElementById("join-form").style.display = "none";
        document.getElementById("waitingroom").style.display = "block";
    }

    document.getElementById("startbtn").onclick = function() {
        console.log('start game')
        socket.emit('start', {'roomname': roomname});
        
    }

    socket.on('startgame', function (data) {
        console.log('starting', data)
        document.getElementById("rolename").innerHTML = data.role;
        document.getElementById("waitingroom").style.display = "none";
        document.getElementById("game").style.display = "block";
    });
});