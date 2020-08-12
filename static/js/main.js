var socket;
var playername;
var ishost = 0;
var roomname;

$(document).ready(function() {
    document.getElementById("join-form").style.display = "block";
    document.getElementById("waitingroom").style.display = "none";
    document.getElementById("game").style.display = "none";
    document.getElementById("hostwait").style.display = "none";

    socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    console.log(location.protocol + '//' + document.domain + ':' + location.port)
    // Join clicked, moving to waitingroom
    document.getElementById("joinbtn").onclick = function() {
        roomname = document.getElementById("roomname").value;
        playername = document.getElementById("playername").value;
        socket.emit('join', {'roomname': roomname, 'playername': playername});

        document.getElementById("room").innerHTML = roomname;
        document.getElementById("join-form").style.display = "none"; // hide
        document.getElementById("waitingroom").style.display = "block"; // show
    }

    // Update player list
    socket.on('population', function(data){
        console.log('Change in room population: ', data)
        const players_node = document.getElementById("players");
        while(players_node.firstChild){
            players_node.removeChild(players_node.lastChild);
        }
        data.players.forEach(item => {
            let li = document.createElement('li');
            players_node.appendChild(li);
            li.innerHTML += item;
        });
    });

    // Is host
    socket.on('host', function(){
        console.log('Host');
        document.getElementById("hostwait").style.display = "block"; // show
        ishost = 1;
    });

    // Start button
    document.getElementById("startbtn").onclick = function() {
        socket.emit('startbtn', {'room': roomname});
    }

    // Move to game
    socket.on('startgame', function(data){
        console.log('Starting game', data);
        document.getElementById("rolename").innerHTML = data.role;
        document.getElementById("explanation").innerHTML = data.explanation;

        document.getElementById("waitingroom").style.display = "none"; // hide
        document.getElementById("hostwait").style.display = "none"; // hide
        document.getElementById("game").style.display = "block"; // show
    });
});