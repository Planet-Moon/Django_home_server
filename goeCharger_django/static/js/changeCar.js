/*$('#change-car-form').on('submit', event => {
    event.preventDefault();
    var car_selected = $('#car_selected').val();
    console.log("car "+car_selected+"selected");
    mqttClient.send(topic+"/command/change_car", car_selected, qos=0, retained=false)
});*/ // not working for some reason

$('#car_selected').on('change', () =>  {
    var car_selected = $('#car_selected option:selected').text();
    console.log("car "+car_selected+" selected");
    mqttClient.send(topic+"/command/change_car", car_selected, qos=0, retained=false)
});

function changeCar(){
    // gets called from change car select $("#car_selected")
}
