document.addEventListener('DOMContentLoaded', function() {
  const ctx = document.getElementById('expenseChart').getContext('2d');
  const labels = JSON.parse(document.getElementById('chartLabels').textContent);
  const data = JSON.parse(document.getElementById('chartData').textContent);
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: [
          '#6366f1', '#f59e42', '#10b981', '#ef4444', '#fbbf24', '#3b82f6', '#a78bfa', '#f472b6'
        ],
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        title: { display: true, text: 'Expense Distribution by Category' }
      }
    }
  });
});
