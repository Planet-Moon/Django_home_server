function changeControlMode(){
    console.log("changeControlMode");
    var control_mode_selected = $('#control-mode-select option:selected').val();
    console.log("control mode "+control_mode_selected+" selected");
    mqttClient.send(topic+"/command/control-mode", control_mode_selected, qos=0, retained=false)
}
