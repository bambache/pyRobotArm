// var ws = new WebSocket("wss://pyrobotarm-c9-bambache.c9.io/echosocket?encoding=text");

// ws.onopen = function() {
//     ws.send("Hello, world");
// };

// ws.onerror = function() {
//     alert("Error");
// };

// ws.onmessage = function (evt) {
//     alert(evt.data);
// };

$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#slider").change( function() {
        updater.socket.send($(this).val());
        return false;
    });
    
    $("#slider").select();
    updater.start();
});

function newMessage(form) {
    var message = form.formToDict();
    updater.socket.send(JSON.stringify(message));
    form.find("input[type=text]").val("").select();
}

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var updater = {
    socket: null,

    start: function() {
        var url = "wss://" + location.host + "/sliderssocket";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            $("#status").append(event.data + "<br>");
        }
        updater.socket.onerror = function() {
            $("#status").append("socket error<br>");
        }
        updater.socket.onopen = function() {
            $("#status").append("socket opened<br>");
        }
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    }
};