window.onload = function() {
    const ctx = document.getElementById('myChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'People Count',
                borderColor: 'rgb(75, 192, 192)',
                data: []
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Frame'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'People Count'
                    },
                    min: 0,
                    max: 50
                }
            }
        }
    });

    const source = new EventSource('/graph_data');
    source.onmessage = function(event) {
        const data = JSON.parse(event.data);
        chart.data.labels = data.labels;
        chart.data.datasets[0].data = data.data;
        chart.update();
    };
};
