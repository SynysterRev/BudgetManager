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
                display: true
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
                    color: '#6b7280',
                    callback: function (value, index, ticks) {
                        return '$' + value;
                    }
                }
            }
        }
    }
});

const categoriesData = JSON.parse(document.getElementById('categories-data').textContent);
const pieChartLabels = categoriesData.map(item => item.name);
const data = categoriesData.map(item => parseFloat(item.amount));
const colors = categoriesData.map(item => item.color);

const total = data.reduce((sum, value) => sum + value, 0);
const percentages = data.map(value => ((value / total) * 100).toFixed(0));

const pieChartCanvas = document.getElementById('pie-chart');
const pieChart = new Chart(pieChartCanvas, {
    type: 'pie',
    data: {
        labels: pieChartLabels,
        datasets: [{
            data: data,
            backgroundColor: colors,
            borderColor: '#ffffff',
            borderWidth: 2,
            hoverBorderWidth: 3
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
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
                padding: 12,
                displayColors: true,
                callbacks: {
                    label: function (context) {
                        const percentage = percentages[context.dataIndex];
                        const value = context.parsed;
                        return `${context.label}: $${value.toFixed(2)} (${percentage}%)`;
                    }
                }
            }
        },

        animation: {
            animateRotate: true,
            animateScale: false
        },
        onHover: (event, activeElements) => {
            event.native.target.style.cursor = activeElements.length > 0 ? 'pointer' : 'default';
        }
    },
    plugins: [{
        afterDatasetsDraw: function (chart) {
            const ctx = chart.ctx;
            chart.data.datasets.forEach((dataset, i) => {
                const meta = chart.getDatasetMeta(i);
                meta.data.forEach((element, index) => {
                    const percentage = percentages[index];
                    if (percentage >= 5) {
                        const centerX = element.x;
                        const centerY = element.y;

                        ctx.fillStyle = 'white';
                        ctx.font = 'bold 14px Arial';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';

                        const angle = element.startAngle + (element.endAngle - element.startAngle) / 2;
                        const radius = element.outerRadius * 0.7;
                        const x = centerX + Math.cos(angle) * radius;
                        const y = centerY + Math.sin(angle) * radius;

                        ctx.fillText(`${percentage}%`, x, y);
                    }
                });
            });
        }
    }]
});

function createCustomLegend() {
    const legendContainer = document.getElementById('pie-legend');
    legendContainer.innerHTML = '';

    categoriesData.forEach((item, index) => {
        const legendItem = document.createElement('div');

        legendItem.className = 'flex items-center';
        legendItem.innerHTML = `
            <div class="w-4 h-4 rounded mr-2" style="background-color: ${item.color}"></div>
            <span class="text-sm text-gray-700">${item.name}</span>
        `;
        legendContainer.appendChild(legendItem);
    });
}

createCustomLegend();