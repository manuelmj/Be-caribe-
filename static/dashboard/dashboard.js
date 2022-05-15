var ctx_temp = document.getElementById("temperature_gauge");
var ctx_hum = document.getElementById("humidity_gauge");

var chart_temp = new Chart(ctx_temp, {
    type:"doughnut",
    data: {
        datasets: [{
            label: "Temperatura",
            data : [1, 99],
            backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 205, 86)"
            ]
        }]
    },
    plugins: [ChartDataLabels],
    options: {
        circumference: 180,
        rotation : -90,
        cutout : '80%', // precent
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                enabled: false,
            },
            datalabels: {
                backgroundColor: 'rgba(0, 0, 0, 0.7)',
                borderColor: '#ffffff',
                color: function(context) {
                    return context.dataset.backgroundColor;
                },
                font: function(context) {
                        var w = context.chart.width;
                        return {
                            size: w < 512 ? 18 : 20,
                            weight:800,
                        }
                },  
                align: 'start',
                anchor: 'start',
                offset: 20,
                borderRadius: 4,
                borderWidth: 2,
                padding: 10,
                formatter: function(value, context) {
                    var i = context.dataIndex;
                    var len = context.dataset.data.length - 1;
                    if(i == len){
                        return null;
                    }
                    return value+' °C';
                }
            },
        },
    }
});
var chart_hum = new Chart(ctx_hum, {
    type:"doughnut",
    data: {
        datasets: [{
            label: "Temperatura",
            data : [1, 99],
            backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 205, 86)"
            ]
        }]
    },
    plugins: [ChartDataLabels],
    options: {
        circumference: 180,
        rotation : -90,
        cutout : '80%', // precent
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                enabled: false,
            },
            datalabels: {
                backgroundColor: 'rgba(0, 0, 0, 0.7)',
                borderColor: '#ffffff',
                color: function(context) {
                    return context.dataset.backgroundColor;
                },
                font: function(context) {
                        var w = context.chart.width;
                        return {
                            size: w < 512 ? 18 : 20,
                            weight:800,
                        }
                },  
                align: 'start',
                anchor: 'start',
                offset: 20,
                borderRadius: 4,
                borderWidth: 2,
                padding: 10,
                formatter: function(value, context) {
                    var i = context.dataIndex;
                    var len = context.dataset.data.length - 1;
                    if(i == len){
                        return null;
                    }
                    return value+' %';
                }
            },
        },
    }
});
