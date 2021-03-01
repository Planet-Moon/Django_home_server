
const clientId = 'mqttjs_' + Math.random().toString(16).substr(2, 8)

const host = 'ws://broker.hivemq.com:8000/mqtt'

const root_topic = "just_my_test_topic"

const options = {
    keepalive: 30,
    clientId: clientId,
    protocolId: 'MQTT',
    protocolVersion: 4,
    clean: true,
    reconnectPeriod: 1000,
    connectTimeout: 30 * 1000,
    will: {
        topic: root_topic+'WillMsg',
        payload: 'Connection Closed abnormally..!',
        qos: 0,
        retain: false
    },
    rejectUnauthorized: false
}

console.log('connecting mqtt client')
const client = mqtt.connect(host, options)

client.on('error', (err) => {
    console.log('Connection error: ', err)
    client.end()
    document.getElementById("status").innerHTML = "Status: error"
})

client.on('reconnect', () => {
console.log('Reconnecting...')
})

client.on('connect', () => {
    console.log('Client connected:' + clientId)
    client.subscribe(root_topic+"/#", { qos: 0 })
    client.publish(root_topic, 'ws connection demo...!', { qos: 0, retain: false })
    document.getElementById("status").innerHTML = "Mqtt Status: connected"
})

client.on('message', (topic, message, packet) => {
    console.log('Received Message: ' + message.toString() + '\nOn topic: ' + topic)
    document.getElementById("lrm").innerHTML = "Last received message: \""+message.toString()+"\", from topic: \""+topic+"\""
})

client.on('close', () => {
console.log(clientId + ' disconnected')
})
