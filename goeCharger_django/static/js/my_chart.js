var chartLeftData = [];
var chartLeftLabels = [];
var ctxLeft = $('#chartLeft');
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
}
var myLeftChart = new Chart(ctxLeft, {
    type: 'line',
    data: {
        labels: chartLeftLabels,
        datasets: [
            {
                label: "power delta",
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

$(document).ready(() => {
    updateChart();
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

function readDataFromDB() {
    data = get_data("power-delta", data => {
        myLeftChart.data.datasets[0].data = [];
        myLeftChart.data.labels = [];
        data.forEach((item,index) => {
            myLeftChart.data.labels.push(new Date(item.time));
            myLeftChart.data.datasets[0].data.push(item.value);
        });
    });
}

function updateChart() {
    readDataFromDB();
    myLeftChart.update();
}

function get_data(variable, callback){
    url = window.location.href.split("/");
    url[3] = url[3]+"log";
    if(variable){
        url[5] = variable;
    }
    url = url.join("/");
    $.getJSON(url, data => {
        callback(data);
    });
}

var data;
setInterval(() => {
    updateChart();
}, 10000)
