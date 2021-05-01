var chartLeftData = [];
var chartRightData = [];
var timeLabels = [];
var ctxLeft = $('#chartLeft');
var ctxRight = $('#chartRight');
var chartOptions = {
    responsive: true,
    legend: {
        display: false
    },
    tooltips: {
        mode: "index",
        intersect: false,
    },
    hover: {
        mode: "nearest",
        intersect: true
    },
    scales: {
        x: {
            type: 'time',
            time: {
                parser: moment,
                tooltipFormat: 'YYYY-MM-DD HH:mm',
                displayFormats: {
                    millisecond: 'YYYY-MM-DD HH:mm:ss.SSS',
                    second: 'YYYY-MM-DD HH:mm:ss',
                    minute: 'YYYY-MM-DD HH:mm',
                    hour: 'YYYY-MM-DD HH',
                    day: 'YYYY-MM-DD',
                    month: 'YYYY-MM',
                    year: 'YYYY'
                }
            },
            title: {
                display: true,
                text: 'Date'
            }
        },
        y: {
            title: {
                display: true,
                text: 'value'
            }
        }
    },
    pan: {enabled: false,mode: 'xy',rangeMin: {x: null,y: null},rangeMax: {x: null,y: null}},
    zoom: {enabled: true,drag: true,mode: 'xy',rangeMin: {x: null,y: null},rangeMax: {x: null,y: null}},
    animation: {
        duration: 0
    }
}

var myLeftChart = new Chart(ctxLeft, {
    type: 'line',
    data: {
        labels: timeLabels,
        datasets: [
            {
                label: "power delta [W]",
                data: chartLeftData,
                fill: false,
                borderColor:"blue",
                backgroundColor:"transparent",
                borderWidth: 1,
                spanGaps: false,
                tooltips: {
                    enabled: false
                }

            }
        ]
    },
    options: chartOptions
});

var myRightChart = new Chart(ctxRight, {
    type: 'line',
    data: {
        labels: timeLabels,
        datasets: [
            {
                label: "power setpoint [W]",
                data: chartLeftData,
                fill: false,
                borderColor:"red",
                backgroundColor:"transparent",
                borderWidth: 1,
                spanGaps: false,
                tooltips: {
                    enabled: false
                }

            }
        ]
    },
    options: chartOptions
});

$("#chartLeftPan").click(() => {
    myLeftChart.options.zoom.enabled = false;
    myLeftChart.options.zoom.pan = true;
});

$("#chartLeftZoom").click(() => {
    myLeftChart.options.zoom.enabled = true;
    myLeftChart.options.zoom.pan = false;
});

$("#chartLeftReset").click(() => {
    myLeftChart.resetZoom()
});

$("#chartRightPan").click(() => {
    myRightChart.options.zoom.enabled = false;
    myRightChart.options.zoom.pan = true;
});

$("#chartRightZoom").click(() => {
    myRightChart.options.zoom.enabled = true;
    myRightChart.options.zoom.pan = false;
});

$("#chartRightReset").click(() => {
    myRightChart.resetZoom()
});

function readDataFromDB() {
    get_data("power-delta", data => {
        myLeftChart.data.datasets[0].data = [];
        myLeftChart.data.labels = [];
        data.forEach((item,index) => {
            myLeftChart.data.labels.push(new Date(item.time));
            myLeftChart.data.datasets[0].data.push(item.value);
        });
    });
    get_data("power-setpoint", data => {
        myRightChart.data.datasets[0].data = [];
        myRightChart.data.labels = [];
        data.forEach((item,index) => {
            myRightChart.data.labels.push(new Date(item.time));
            myRightChart.data.datasets[0].data.push(item.value);
        });
    });
}

function updateChart() {
    readDataFromDB();
    myLeftChart.update();
    myRightChart.update();
}

function get_data(variable, callback){
    url = window.location.href.split("/");
    url[url.length-2] = url[url.length-2]+"log";
    if(variable){
        url[5] = variable;
    }
    url.splice(url.length-1,0,charger_name);
    url = url.join("/");
    $.getJSON(url, data => {
        callback(data);
    });
}

$(document).ready(() => {
    updateChart();
    setInterval(() => {
        updateChart();
    }, 5000)
});
