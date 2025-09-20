let chart;

async function fetchStats() {
  try {
    // Fetch stats (total + unique)
    let res = await fetch("http://127.0.0.1:8000/stats");
    let data = await res.json();

    // Fill values
    document.getElementById("productive-total").textContent =
      data.total?.productive || 0;
    document.getElementById("distracting-total").textContent =
      data.total?.distracting || 0;
    document.getElementById("productive-unique").textContent =
      data.unique?.productive || 0;
    document.getElementById("distracting-unique").textContent =
      data.unique?.distracting || 0;

    // Fetch analytics
    let trendRes = await fetch("http://127.0.0.1:8000/analytics");
    let trendData = await trendRes.json();

    let labels = Object.keys(trendData);
    let productive = labels.map((day) => trendData[day].productive);
    let distracting = labels.map((day) => trendData[day].distracting);

    if (chart) chart.destroy();
    let ctx = document.getElementById("trendChart").getContext("2d");
    chart = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Productive",
            data: productive,
            borderColor: "#22c55e",
            backgroundColor: "rgba(34,197,94,0.2)",
            fill: true,
            tension: 0.3
          },
          {
            label: "Distracting",
            data: distracting,
            borderColor: "#ef4444",
            backgroundColor: "rgba(239,68,68,0.2)",
            fill: true,
            tension: 0.3
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "bottom" }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  } catch (err) {
    console.error("Failed to fetch stats:", err);
  }
}

document.getElementById("refresh").addEventListener("click", fetchStats);
fetchStats();
