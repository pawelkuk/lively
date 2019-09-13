var myChart = document.getElementById("myChart").getContext('2d');
var tmp_label = null;
var tmp_data = null;
var chart_labels = [];
var chart_data = [];
var chart_label = document.getElementById('label').innerText;
var i = 0;
while (true) {
    try {
        tmp_label = document.getElementById('label-'+i).innerText;
        tmp_data = document.getElementById('data-'+i).innerText;
    }
    catch (e)
    {
        break;
    }
    chart_labels.push(tmp_label);
    chart_data.push(tmp_data);
    i = i + 1;
}

var lineChart = new Chart(myChart, {
    type: 'line',
    data: {
        labels: chart_labels,
        datasets: [{
            label: chart_label,
            data: chart_data
        }]
    },
    options: {}
});