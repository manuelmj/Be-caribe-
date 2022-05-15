var ctx_temp = document.getElementById("temperature_gauge");
var ctx_hum = document.getElementById("humidity_gauge");
var ctx_temp_hum = document.getElementById("humidity_temperature")

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

const plugin = {
    id: 'custom_canvas_background_color',
    beforeDraw: (chart) => {
      const ctx = chart.canvas.getContext('2d');
      ctx.save();
      ctx.globalCompositeOperation = 'destination-over';
      ctx.fillStyle = 'rgb(239,239,239)';
      ctx.fillRect(0, 0, chart.width, chart.height);
      ctx.restore();  }
  };

const config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: "Numero 1",
            backgroundColor: "rgb(132,186,91,0.2)",
            borderColor: "rgb(62,150,81,1)",
            data: [],
            fill: false,
        }],
    },
    plugins: [plugin],
    options: {
        responsive: true,
        title: {
            display: true,
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Fecha y Hora'
                },
                ticks: {
                    display: false
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Flujo de agua (L/min)'
                }
            }]
        }
    }
};

const lineChart = new Chart(ctx_temp_hum , config);
