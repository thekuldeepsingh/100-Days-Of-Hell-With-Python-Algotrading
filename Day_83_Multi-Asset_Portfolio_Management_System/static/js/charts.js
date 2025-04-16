document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts if the container elements exist
    if (document.getElementById('performanceChart')) {
        initPerformanceChart();
    }
    
    if (document.getElementById('assetAllocationChart')) {
        initAssetAllocationChart();
    }
    
    if (document.getElementById('sectorAllocationChart')) {
        initSectorAllocationChart();
    }
    
    if (document.getElementById('riskBreakdownChart')) {
        initRiskBreakdownChart();
    }
});

function initPerformanceChart() {
    // Fetch performance data
    fetch('/api/portfolio_performance')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('performanceChart').getContext('2d');
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: 'Portfolio Value ($)',
                        data: data.values,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        pointBackgroundColor: 'rgba(54, 162, 235, 1)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Portfolio Performance Over Time',
                            font: {
                                size: 16
                            }
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            callbacks: {
                                label: function(context) {
                                    return 'Value: $' + context.raw.toFixed(2);
                                }
                            }
                        },
                        legend: {
                            position: 'bottom'
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                display: false
                            }
                        },
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return '$' + value.toLocaleString();
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching performance data:', error);
            document.getElementById('performanceChart').innerHTML = '<div class="alert alert-danger">Failed to load performance data</div>';
        });
}

function initAssetAllocationChart() {
    // Fetch asset allocation data
    fetch('/api/asset_allocation')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('assetAllocationChart').getContext('2d');
            
            // Define a set of vibrant colors
            const colors = [
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 99, 132, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(201, 203, 207, 0.8)',
                'rgba(255, 99, 71, 0.8)',
                'rgba(46, 204, 113, 0.8)',
                'rgba(142, 68, 173, 0.8)'
            ];
            
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: colors.slice(0, data.labels.length),
                        borderColor: 'rgba(255, 255, 255, 0.5)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Asset Allocation',
                            font: {
                                size: 16
                            }
                        },
                        legend: {
                            position: 'right',
                            labels: {
                                boxWidth: 15
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw || 0;
                                    return label + ': ' + value.toFixed(2) + '%';
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching asset allocation data:', error);
            document.getElementById('assetAllocationChart').innerHTML = '<div class="alert alert-danger">Failed to load asset allocation data</div>';
        });
}

function initSectorAllocationChart() {
    // Fetch sector allocation data
    fetch('/api/sector_allocation')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('sectorAllocationChart').getContext('2d');
            
            // Define a set of vibrant colors
            const colors = [
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 99, 132, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(201, 203, 207, 0.8)',
                'rgba(255, 99, 71, 0.8)',
                'rgba(46, 204, 113, 0.8)',
                'rgba(142, 68, 173, 0.8)',
                'rgba(241, 196, 15, 0.8)',
                'rgba(231, 76, 60, 0.8)',
                'rgba(26, 188, 156, 0.8)'
            ];
            
            // Filter out empty sectors
            const filteredLabels = [];
            const filteredData = [];
            
            for (let i = 0; i < data.labels.length; i++) {
                if (data.data[i] > 0) {
                    filteredLabels.push(data.labels[i]);
                    filteredData.push(data.data[i]);
                }
            }
            
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: filteredLabels,
                    datasets: [{
                        label: 'Allocation (%)',
                        data: filteredData,
                        backgroundColor: colors.slice(0, filteredLabels.length),
                        borderColor: 'rgba(255, 255, 255, 0.5)',
                        borderWidth: 1
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Sector Allocation',
                            font: {
                                size: 16
                            }
                        },
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.raw || 0;
                                    return 'Allocation: ' + value.toFixed(2) + '%';
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            }
                        },
                        y: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching sector allocation data:', error);
            document.getElementById('sectorAllocationChart').innerHTML = '<div class="alert alert-danger">Failed to load sector allocation data</div>';
        });
}

function initRiskBreakdownChart() {
    // Get risk data from the page
    const riskBreakdownElement = document.getElementById('riskBreakdownData');
    
    if (!riskBreakdownElement) {
        console.error('Risk breakdown data not found');
        return;
    }
    
    try {
        const riskData = JSON.parse(riskBreakdownElement.textContent);
        const ctx = document.getElementById('riskBreakdownChart').getContext('2d');
        
        const labels = [];
        const weights = [];
        const riskScores = [];
        
        // Extract data from the risk breakdown
        for (const assetClass in riskData) {
            labels.push(assetClass);
            weights.push(riskData[assetClass].weight * 100);
            riskScores.push(riskData[assetClass].risk_score);
        }
        
        // Define a color scale for risk scores
        const getColorForRiskScore = (score) => {
            if (score <= 2) return 'rgba(46, 204, 113, 0.8)'; // Low risk - green
            if (score <= 4) return 'rgba(241, 196, 15, 0.8)'; // Medium risk - yellow
            if (score <= 6) return 'rgba(230, 126, 34, 0.8)'; // High risk - orange
            return 'rgba(231, 76, 60, 0.8)'; // Very high risk - red
        };
        
        const backgroundColors = riskScores.map(getColorForRiskScore);
        
        new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Asset Class Weight (%)',
                    data: weights,
                    backgroundColor: backgroundColors,
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        display: false
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Risk Breakdown by Asset Class',
                        font: {
                            size: 16
                        }
                    },
                    legend: {
                        position: 'bottom',
                        labels: {
                            boxWidth: 15
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const index = context.dataIndex;
                                const riskScore = riskScores[index];
                                return [
                                    'Weight: ' + value.toFixed(2) + '%',
                                    'Risk Score: ' + riskScore
                                ];
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error parsing risk breakdown data:', error);
        document.getElementById('riskBreakdownChart').innerHTML = '<div class="alert alert-danger">Failed to load risk breakdown data</div>';
    }
}
