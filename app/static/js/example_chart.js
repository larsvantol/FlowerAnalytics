async function create_example_chart(datapoints) {
  const DATA_COUNT = 12;
  const labels = [];
  for (let i = 0; i < DATA_COUNT; ++i) {
    labels.push(i.toString());
  }
  const data = {
    labels: labels,
    datasets: [
      {
        label: "Cubic interpolation (monotone)",
        data: datapoints,
        borderColor: "rgb(75, 192, 192)",
        fill: false,
        cubicInterpolationMode: "monotone",
        tension: 0.4,
      },
      // {
      //   label: "Cubic interpolation",
      //   data: datapoints,
      //   borderColor: "rgb(54, 162, 235)",
      //   fill: false,
      //   tension: 0.4,
      // },
      // {
      //   label: "Linear interpolation (default)",
      //   data: datapoints,
      //   borderColor: "rgb(255, 99, 132)",
      //   fill: false,
      // },
    ],
  };
  const config = {
    type: "line",
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: "Chart.js Line Chart - Cubic interpolation mode",
        },
      },
      interaction: {
        intersect: false,
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
          },
        },
        y: {
          display: true,
          title: {
            display: true,
            text: "Value",
          },
          suggestedMin: -10,
          suggestedMax: 200,
        },
      },
    },
  };

  new Chart(document.getElementById("example_chart"), config);
}
