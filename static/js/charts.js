const ctx = document.getElementById('line-chart');

const labels = JSON.parse(document.getElementById('labels-data').textContent);
const incomes = JSON.parse(document.getElementById('incomes-data').textContent);
const expenses = JSON.parse(document.getElementById('expenses-data').textContent);

new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Income',
            data: incomes,
            borderColor: 'rgb(13, 148, 136)',
            backgroundColor: 'rgba(13, 148, 136, 0.1)',
            pointBackgroundColor: 'rgb(13, 148, 136)',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 6,
            pointHoverRadius: 8,
            fill: false,
            tension: 0.1
        }, {
            label: 'Expenses',
            data: expenses,
            borderColor: 'rgb(234, 88, 12)',
            backgroundColor: 'rgba(234, 88, 12, 0.1)',
            pointBackgroundColor: 'rgb(234, 88, 12)',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 6,
            pointHoverRadius: 8,
            fill: false,
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            intersect: false,
            mode: 'index'
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: 'white',
                titleColor: '#1f2937',
                bodyColor: '#1f2937',
                borderColor: '#e5e7eb',
                borderWidth: 1,
                cornerRadius: 8,
                displayColors: false,
                padding: 12,
                titleFont: {
                    size: 16,
                    weight: 'bold'
                },
                bodyFont: {
                    size: 14
                },
                callbacks: {
                    title: function (context) {
                        return context[0].label;
                    },
                    label: function (context) {
                        const datasetLabel = context.dataset.label;
                        const value = context.parsed.y;

                        if (datasetLabel === 'Income') {
                            return `income: $${value.toFixed(2)}`;
                        } else {
                            return `expenses: $${value.toFixed(2)}`;
                        }
                    },
                    labelTextColor: function (context) {
                        if (context.dataset.label === 'Income') {
                            return 'rgb(13, 148, 136)';
                        } else {
                            return 'rgb(234, 88, 12)';
                        }
                    }
                },
            }
        },
        scales: {
            x: {
                grid: {
                    display: true,
                    color: '#f3f4f6'
                },
                ticks: {
                    color: '#6b7280'
                }
            },
            y: {
                grid: {
                    display: true,
                    color: '#f3f4f6'
                },
                ticks: {
                    color: '#6b7280'
                }
            }
        }
    }
});