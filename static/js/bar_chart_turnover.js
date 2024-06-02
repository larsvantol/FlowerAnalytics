async function create_bar_chart_producten(id, legend_position, aspect_ratio) {
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
    type: "bar",
    data: data,
    options: {
      responsive: true,
      aspectRatio: aspect_ratio,
      plugins: {
        legend: {
          position: legend_position,
          display: false,
        },
        title: {
          display: true,
          text: " ",
        },
      },
    },
  };

  var bar_chart = new Chart(document.getElementById(id), config);
  return bar_chart;
}

async function update_bar_chart_producten(
  api_url,
  bar_chart,
  title,
  tooltip_text
) {
  bar_chart = await bar_chart;
  const response = await fetch(api_url);
  const data = await response.json();

  bar_chart.data.labels = [];
  bar_chart.data.datasets[0].data = [];
  bar_chart.data.datasets[0].backgroundColor = [];
  bar_chart.options.plugins.title.text = title;

  bar_chart.options.plugins.tooltip = {
    callbacks: {
      label: function (context) {
        var label = "";
        if (context.parsed.y !== null) {
          if (tooltip_text == "€") {
            let currency = Intl.NumberFormat("en-US", {
              style: "currency",
              currency: "EUR",
            }).format(context.parsed.y);
            label += currency;
          } else {
            label += " " + context.parsed.y + " " + tooltip_text;
          }
        }
        return label;
      },
    },
  };

  data.result.forEach((element, index) => {
    if (!(element.amount == 0)) {
      bar_chart.data.labels.push(element.label);
      bar_chart.data.datasets[0].data.push(element.amount);
      bar_chart.data.datasets[0].backgroundColor.push(
        COLORS[index % COLORS.length]
      );
    }
  });

  bar_chart.update();
}
