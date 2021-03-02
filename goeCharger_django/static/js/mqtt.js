class messagesHandle{
    constructor(n_messages){
        this.n_messages = n_messages;
        this.messages = new Array(n_messages);
    };

    get getMessages(){
        return this.messages;
    };

    addMessage(message){
        if(this.messages.length >= this.n_messages){
            this.messages.shift();}
        this.messages.push(message);
    };
};

// Create a client instance
var host = "broker.hivemq.com";
var port = 8000;
var path = "/mqtt";
var clientID = "server_mqtt_client";
var topic = "/home_test_server/goe_charger";
var client = new Paho.MQTT.Client(host,port,path,clientID);

var Messages = new messagesHandle(5);

console.log(Messages);

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({
    onSuccess:onConnect
});

// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
    client.subscribe(topic+"/#");
    payload = "First message";
    client.send(topic, payload, qos=0, retained=true);
};

// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost: "+responseObject.errorMessage);
    };
};

// called when a message arrives
function onMessageArrived(message) {
    console.log("onMessageArrived: "+message.payloadString);
    Messages.addMessage(message);
    $("#messages-table").html("")
    Messages.messages.forEach( element => {
        $("#messages-table").prepend("<tr><th>"+element.destinationName+"</th><th>"+element.payloadString+"</th></tr>");
    });
};

$(document).ready(function() {
    var counter = 0;
    setInterval(function() {
        client.send(topic+"/subtopic", String(counter), qos=0, retained=true);
        counter++;
    }, 2000)
});

$('#test-form').on('submit', (event) => {
    event.preventDefault();
    input_text = $('#test-text').val();
    console.log("text ("+input_text+") submitted!");
    $("#return-text").html(input_text);
});

$('#toggle-charging-form').on('submit', (event) => {
    event.preventDefault();
    if(charging_state){
        $("#btn-toggle-charging").html("Stop charging");
    }
    else{
        $("#btn-toggle-charging").html("Charge");
    }
});
