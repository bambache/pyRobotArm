$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};
    
    // setup graphic EQ
    $( "#eq > span" ).each(function(index) {
      // read initial values from markup and replace that
      var value = parseInt( $( this ).text(), 10 );
      $( this ).empty().slider({
        value: slider_values[index],
        range: "min",
        animate: true,
        orientation: "vertical",
        min: 0,
        max: 180,
        change: function( event, ui ) {
          $( "#status" ).append( ui.value + " from: " + index + "<br>");
          slider_values[index] = ui.value;
          sendSliderValues();
        }
      });
    });

    updater.start();
});

function sendSliderValues() {
    var allValues = "";
    $.each(slider_values, function(i,val) {
        allValues += val + ",";
    });
    updater.socket.send(allValues);
}

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

var slider_values = [90, 90, 90 ,90, 90];
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