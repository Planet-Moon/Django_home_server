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
var clientID = "browser_client_"+makeid(5);
var topic = "home_test_server/goe_charger/"+charger_name;
var mqttClient = new Paho.MQTT.Client(host,port,path,clientID);

var Messages = new messagesHandle(20);
var charger_http_connected = true;
var charging_state = undefined;

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
    //console.log("onConnect");
    mqttClient.subscribe(topic+"/#");
    payload = "Client connected successfully";
    mqttClient.send(topic, payload, qos=0, retained=false);
};

// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost: "+responseObject.errorMessage);
    };
};

// called when a message arrives
function onMessageArrived(message) {
    //console.log("onMessageArrived: "+message.destinationName+" "+message.payloadString+" "+message.qos+" "+message.retained);
    Messages.addMessage(message);
    $("#messages-table").html("")
    Messages.messages.forEach( element => {
        $("#messages-table").prepend(
            "<tr><th>"+element.destinationName+
            "</th><th>"+element.payloadString+
            "</th><th>"+element.qos+
            "</th><th>"+element.retained+
            "</th></tr>");
    });
    var receivedData = ""
    try{
        receivedData = JSON.parse(message.payloadString);}
    catch(e){}
    var topic = message.destinationName;
    var topics = topic.split("/");
    var messageType = topics[3];
    if(messageType == "status"){
        var p_Name = topics[4];
        var p_Value = message.payloadString;
        if(p_Name == "httpc"){
            if(p_Value == "True"){
                charger_http_connected = true;
                $("#httpc").html("Charger connected");
                $("#btn-toggle-charging").prop("disabled", false);
                $("#btn-test-text").prop("disabled", false);
            }
            else{
                charger_http_connected = false;
                $("#http-error-alert").show()
                $("#httpc").html("Charger disconnected");
                $("#car").html("");
                $("#amp").html("");
                $("#nrg").html("");
                $("#alw").html("");
                $("#min-amp").html("");
                $("#control-mode").html("");
                $("#power-factor").html("");
                $("#control-status").html("");
                $("#solar-ratio-status").html("");
                $("#btn-toggle-charging").prop("disabled", true);
                $("#btn-test-text").prop("disabled", true);
            }
        }
        else if (p_Name == "http-error"){
            $("#http-error-description").html(p_Value);
        }
        else if(charger_http_connected){
            if(p_Name == "car_selected"){
                $("#car_selected").html("Selected car: <a href=\"../car/"+p_Value+"\">"+p_Value+"</a>");
                return
            }
            else if(p_Name == "car"){
                p_Value = parseInt(p_Value);
                function Car_status(args_){
                    if(args_ > 1){
                        return "connected";
                    }
                    else{
                        return "not connected";
                    }
                }
                car_status = Car_status(p_Value);
                $("#car").html("Car status: " + car_status);
                return
            }
            else if(p_Name == "amp"){
                $("#amp").html("I: " + p_Value + " <i>A</i>");
                return
            }
            else if(p_Name == "nrg"){
                $("#nrg").html("P: " + p_Value + " <i>W</i>");
                return
            }
            else if(p_Name == "alw"){
                $("#alw").html("Charging status: " + p_Value);
                if(p_Value==="True"){
                    charging_state = true;
                    $("#btn-toggle-charging").html("Stop charging");
                }
                else{
                    charging_state = false;
                    $("#btn-toggle-charging").html("Charge");
                }
                return
            }
            else if(p_Name == "min-amp"){
                $("#min-amp").html("I<sub>min</sub>: " + p_Value + " <i>A</i>");
                return
            }
            else if(p_Name == "power-factor"){
                $("#power-factor").html("Power factor: " + p_Value + " <i>%</i>")
            }
            else if (p_Name == "control-mode"){
                $("#control-mode").html("Control Mode: " + p_Value);
                if(p_Value==="solar"){
                    $("#control-status").removeClass("text-muted")
                    $("#solar-ratio-status").removeClass("text-muted")
                }
                else{
                    $("#control-status").addClass("text-muted")
                    $("#solar-ratio-status").addClass("text-muted")
                }
                return
            }
            else if (p_Name == "control-status"){
                $("#control-status").html("Control state: " + p_Value);
                return
            }
            else if (p_Name == "update-time"){
                $("#update-time").html(p_Value);
                return
            }
            else if (p_Name == "solar-ratio"){
                $("#solar-ratio-status").html("Solar ratio: "+p_Value+" %");
                return
            }
            else{
                console.log("unknown property "+p_Name+"with value "+p_Value);
            }
        }
    }
    return
};

$(document).ready(() => {
    $("#http-error-alert").hide();
    /*var counter = 0;
    setInterval(() => {
        if(mqttClient.isConnected()){
            // mqttClient.send(topic+"/subtopic", String(counter), qos=0, retained=true);
            // counter++;
        }
    }, 10000)
    */
});

$('#custom-publish-form').on('submit', event => {
    event.preventDefault();
    input_text = $('#test-text').val();
    //console.log("text ("+input_text+") submitted!");
    text = input_text.split(" ");
    payloadString = text.slice(1).join(" ")
    if(text.length > 1){
        mqttClient.send(topic+"/command/"+text[0], payloadString, qos=0, retained=false)}
});

$('#toggle-charging-form').on('submit', event => {
    event.preventDefault();
    var args = undefined;
    if(charging_state){
        args = "False";
    }
    else{
        args = "True";
    }
    if(mqttClient.isConnected()){
        mqttClient.send(topic+"/command/alw", args, qos=0, retained=false)
    }
});

$('#solar-ratio-form').on('submit', event => {
    event.preventDefault();
    solarRatio = $('#solar-ratio-input').val();
    //console.log("solar-ratio "+solarRatio+" submitted!")
    mqttClient.send(topic+"/command/solar-ratio", solarRatio, qos=0, retained=false)
});
