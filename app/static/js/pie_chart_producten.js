async function create_pie_chart_producten(id, legend_position, aspect_ratio) {
  const data = {
    labels: [],
    datasets: [
      {
        data: [],
        backgroundColor: [],
      },
    ],
  };

  const config = {
    type: "pie",
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

  var pie_chart = new Chart(document.getElementById(id), config);
  return pie_chart;
}

const COLORS = [
  "rgb(255, 99, 132)",
  "rgb(54, 162, 235)",
  "rgb(255, 205, 86)",
  "rgb(75, 192, 192)",
  "rgb(153, 102, 255)",
  "rgb(255, 159, 64)",
];

async function update_pie_chart_producten(
  api_url,
  pie_chart,
  title,
  tooltip_text
) {
  pie_chart = await pie_chart;
  const response = await fetch(api_url);
  const data = await response.json();

  pie_chart.data.labels = [];
  pie_chart.data.datasets[0].data = [];
  pie_chart.data.datasets[0].backgroundColor = [];
  pie_chart.options.plugins.title.text = title;

  pie_chart.options.plugins.tooltip = {
    callbacks: {
      label: function (context) {
        var label = "";
        if (context.parsed.y !== null) {
          if (tooltip_text == "€") {
            let currency = Intl.NumberFormat("en-US", {
              style: "currency",
              currency: "EUR",
            }).format(context.parsed);
            label += currency;
          } else {
            label += " " + context.parsed + " " + tooltip_text;
          }
        }
        return label;
      },
    },
  };

  data.result.forEach((element, index) => {
    if (!(element.amount == 0)) {
      pie_chart.data.labels.push(element.label);
      pie_chart.data.datasets[0].data.push(element.amount);
      pie_chart.data.datasets[0].backgroundColor.push(
        COLORS[index % COLORS.length]
      );
    }
  });

  pie_chart.update();
}
