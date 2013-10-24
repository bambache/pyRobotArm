$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    var slider_values = [90, 90, 90 ,90, 90];
    var max_status_lines = 16;
    var change_handler_enabled =true;
    
    var updater = {
        socket: null,
        
        start: function() {
            var url = "ws://" + location.host + "/sliderssocket";
            updater.socket = new WebSocket(url);
            updater.socket.onmessage = function(event) {
                logToStatus("RECV: |"+event.data + "|");
                var event_values = event.data.split(",");
                $.each(event_values, function(i, val) {
                    slider_values[i] = parseInt(val,10);
                })
                change_handler_enabled = false;
                setSliderValues();
                change_handler_enabled = true;
            }
            updater.socket.onerror = function() {
                logToStatus("socket error");
            }
            updater.socket.onopen = function() {
                logToStatus("socket opened");
            }
        },
    
    };
    
    function logToStatus(message){
        if ($("#status").contents().length > max_status_lines ) {
            $("#status :first-child").remove();
        }
        $("#status").append("<p>"+message+"</p>");
    }
    
    function sendSliderValues() {
        var allValues = slider_values.join();
        logToStatus("SEND: |" + allValues + "|");
        updater.socket.send(allValues);
    }
    
    function setSliderValues() {
        $.each(slider_values, function(i, val) {
            $("#slider" + i).empty().slider({
                value: val,
                range: "min",
                animate: true,
                orientation: "vertical",
                min: 0,
                max: 180,
                change: function(event, ui) {
                    if (!change_handler_enabled) return;
                    logToStatus(ui.value + " from: " + i);
                    slider_values[i] = ui.value;
                    sendSliderValues();
                }
            });
        });
    }
    
    setSliderValues();

    updater.start();
});


