async function create_histogram_chart(id, legend_position, aspect_ratio) {
  const data = {
    datasets: [
      {
        label: "Prijzen",
        data: [],
        backgroundColor: "rgb(255, 99, 132)",
      },
    ],
  };

  const config = {
    type: "bar",
    data: data,
    options: {
      responsive: true,
      aspectRatio: aspect_ratio,
      plugins: {
        legend: {
          position: legend_position,
        },
        title: {
          display: true,
          text: " ",
        },
      },
    },
  };

  var histogram_chart = new Chart(document.getElementById(id), config);
  return histogram_chart;
}

// if not defined, define COLORS
// if (typeof COLORS === "undefined") {
//   var COLORS = [
//     "rgb(255, 99, 132)",
//     "rgb(54, 162, 235)",
//     "rgb(255, 205, 86)",
//     "rgb(75, 192, 192)",
//     "rgb(153, 102, 255)",
//     "rgb(255, 159, 64)",
//   ];
// }

async function update_histogram_chart(
  api_url,
  histogram_chart,
  title,
  tooltip_text
) {
  histogram_chart = await histogram_chart;
  const response = await fetch(api_url);
  const data = await response.json();

  histogram_chart.data.labels = [];
  histogram_chart.data.datasets[0].data = [];
  histogram_chart.data.datasets[0].backgroundColor = [];
  histogram_chart.options.plugins.title.text = title;

  data.result.bin_edges.forEach((element) => {
    histogram_chart.data.labels.push(parseFloat(element).toFixed(3));
  });
  histogram_chart.data.datasets[0].data = data.result.hist;
  histogram_chart.data.datasets[0].backgroundColor = COLORS[1];

  histogram_chart.options.plugins.annotation = {
    annotations: [
      {
        type: "line",
        scaleID: "x",
        borderWidth: 3,
        borderColor: "black",
        value:
          (data.result.hist.length *
            (data.result.average - Math.min(...data.result.bin_edges))) /
          (Math.max(...data.result.bin_edges) -
            Math.min(...data.result.bin_edges)),
        label: {
          content: "Average (€" + data.result.average.toFixed(4) + ")",
          enabled: true,
          display: true,
          position: "start",
        },
      },
      {
        type: "line",
        scaleID: "x",
        borderWidth: 3,
        borderColor: "grey",
        value:
          (data.result.hist.length *
            (data.result.quarter_1 - Math.min(...data.result.bin_edges))) /
          (Math.max(...data.result.bin_edges) -
            Math.min(...data.result.bin_edges)),
        label: {
          content: "50% (€" + data.result.quarter_1.toFixed(2) + ")",
          enabled: true,
          display: true,
          position: "20%",
        },
      },
      {
        type: "line",
        scaleID: "x",
        borderWidth: 3,
        borderColor: "grey",
        value:
          (data.result.hist.length *
            (data.result.quarter_3 - Math.min(...data.result.bin_edges))) /
          (Math.max(...data.result.bin_edges) -
            Math.min(...data.result.bin_edges)),
        label: {
          content: "50% (€" + data.result.quarter_3.toFixed(2) + ")",
          enabled: true,
          display: true,
          position: "20%",
        },
      },
      {
        type: "line",
        scaleID: "x",
        borderWidth: 3,
        borderColor: "grey",
        value:
          (data.result.hist.length *
            (data.result.eigth_1 - Math.min(...data.result.bin_edges))) /
          (Math.max(...data.result.bin_edges) -
            Math.min(...data.result.bin_edges)),
        label: {
          content: "75% (€" + data.result.eigth_1.toFixed(2) + ")",
          enabled: true,
          display: true,
          position: "30%",
        },
      },
      {
        type: "line",
        scaleID: "x",
        borderWidth: 3,
        borderColor: "grey",
        value:
          (data.result.hist.length *
            (data.result.eigth_7 - Math.min(...data.result.bin_edges))) /
          (Math.max(...data.result.bin_edges) -
            Math.min(...data.result.bin_edges)),
        label: {
          content: "75% (€" + data.result.eigth_7.toFixed(2) + ")",
          enabled: true,
          display: true,
          position: "30%",
        },
      },
    ],
  };

  histogram_chart.update();
}
