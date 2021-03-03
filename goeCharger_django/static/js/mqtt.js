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
// var host = "broker.hivemq.com";
// var port = 8000;
// var path = "/mqtt";
var host = "192.168.178.107";
var port = 9002
var path = ""
var clientID = "server_mqtt_client";
var topic = "/home_test_server/goe_charger";
var mqttClient = new Paho.MQTT.Client(host,port,path,clientID);

var Messages = new messagesHandle(5);

// set callback handlers
mqttClient.onConnectionLost = onConnectionLost;
mqttClient.onMessageArrived = onMessageArrived;

// connect the client
mqttClient.connect({
    onSuccess:onConnect
});

// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
    mqttClient.subscribe(topic+"/#");
    payload = "First message";
    mqttClient.send(topic, payload, qos=0, retained=true);
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
    var receivedData = ""
    try{
        receivedData = JSON.parse(message.payloadString);}
    catch(e){}
    console.log("receivedData: "+receivedData);
};

$(document).ready(() => {
    var counter = 0;
    setInterval(() => {
        if(mqttClient.isConnected()){
            // mqttClient.send(topic+"/subtopic", String(counter), qos=0, retained=true);
            // counter++;
        }
    }, 10000)
});

$('#test-form').on('submit', event => {
    event.preventDefault();
    input_text = $('#test-text').val();
    console.log("text ("+input_text+") submitted!");
    $("#return-text").html(input_text);
});

$('#toggle-charging-form').on('submit', event => {
    event.preventDefault();
    var args = undefined;
    if(charging_state){
        args = 0;
    }
    else{
        args = 1;
    }
    var payload = {command:"alw","args":args}
    payload = JSON.stringify(payload)
    if(charging_state){
        $("#btn-toggle-charging").html("Stop charging");
    }
    else{
        $("#btn-toggle-charging").html("Charge");
    }
    if(mqttClient.isConnected()){
        mqttClient.send(topic+"/"+charger_name, payload, qos=0, retained=true)
    }
});
