document.addEventListener('DOMContentLoaded', function() {
    // Initialize date pickers
    const dateInputs = document.querySelectorAll('input[type="date"]');
    for (const input of dateInputs) {
        if (!input.value) {
            input.valueAsDate = new Date();
        }
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Handle bulk price update
    const updatePricesBtn = document.getElementById('updatePricesBtn');
    if (updatePricesBtn) {
        updatePricesBtn.addEventListener('click', updatePrices);
    }
    
    // Handle security delete confirmations
    const deleteButtons = document.querySelectorAll('.delete-security-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this security?')) {
                e.preventDefault();
            }
        });
    });
    
    // Handle time period selector for performance chart
    const periodSelector = document.getElementById('periodSelector');
    if (periodSelector) {
        periodSelector.addEventListener('change', function() {
            updatePerformanceChart(this.value);
        });
    }
});

function updatePrices() {
    const securityRows = document.querySelectorAll('tr.security-row');
    const updates = [];
    
    securityRows.forEach(row => {
        const securityId = row.dataset.id;
        const priceInput = row.querySelector('.current-price-input');
        
        if (securityId && priceInput && priceInput.value) {
            updates.push({
                id: securityId,
                current_price: priceInput.value
            });
        }
    });
    
    if (updates.length === 0) {
        alert('No price updates to submit.');
        return;
    }
    
    // Show spinner
    const spinner = document.getElementById('updateSpinner');
    if (spinner) spinner.classList.remove('d-none');
    
    // Update prices via API
    fetch('/api/update_prices', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Reload the page to show updated values
            window.location.reload();
        } else {
            alert('Error updating prices: ' + (data.message || 'Unknown error'));
            if (spinner) spinner.classList.add('d-none');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating prices. See console for details.');
        if (spinner) spinner.classList.add('d-none');
    });
}

function updatePerformanceChart(days) {
    // Show loading indicator
    const chartContainer = document.getElementById('performanceChart').parentNode;
    chartContainer.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    
    // Fetch updated performance data
    fetch(`/api/portfolio_performance?days=${days}`)
        .then(response => response.json())
        .then(data => {
            // Recreate the chart with new data
            chartContainer.innerHTML = '<canvas id="performanceChart"></canvas>';
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
                            text: `Portfolio Performance (${days} days)`,
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
            chartContainer.innerHTML = '<div class="alert alert-danger">Failed to load performance data</div>';
        });
}

// Format currency values
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

// Format percentage values
function formatPercentage(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value / 100);
}

// Calculate gain/loss percentages
function calculateGainLoss(currentPrice, purchasePrice) {
    if (!purchasePrice || purchasePrice === 0) return 0;
    return ((currentPrice - purchasePrice) / purchasePrice) * 100;
}
