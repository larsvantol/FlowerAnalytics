async function create_line_chart(id, legend_position, aspect_ratio) {
  const data = {
    datasets: [
      {
        label: "Omzet per week 2023",
        data: [],
        backgroundColor: "rgb(255, 99, 132)",
        cubicInterpolationMode: "monotone",
        tension: 0.4,
      },
    ],
  };

  const config = {
    type: "line",
    data: data,
    options: {
      responsive: true,
      aspectRatio: aspect_ratio,
      scales: {
        x: {
          type: "time",
          time: {
            displayFormats: {
              quarter: "MMM YYYY",
            },
          },
        },
      },
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

  var line_chart = new Chart(document.getElementById(id), config);
  return line_chart;
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

async function update_line_chart(api_url, line_chart, title, tooltip_text) {
  line_chart = await line_chart;
  const response = await fetch(api_url);
  const data = await response.json();

  line_chart.data.labels = [];
  line_chart.data.datasets[0].data = [];
  line_chart.data.datasets[0].backgroundColor = [];
  line_chart.options.plugins.title.text = title;

  line_chart.options.plugins.tooltip = {
    callbacks: {
      label: function (context) {
        console.log(context);
        var label =
          new Date(context.parsed.x).toLocaleString("nl-NL", {
            year: "numeric",
            month: "numeric",
            day: "numeric",
          }) + ": ";
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

  var minimum_date = new Date(data.result[0].week);
  var maximum_date = new Date(data.result[0].week);

  data.result.forEach((element, index) => {
    line_chart.data.labels.push(element.label);
    line_chart.data.datasets[0].data.push({
      x: element.week,
      y: element.turnover,
      amount: element.amount,
    });
    line_chart.data.datasets[0].backgroundColor.push(COLORS[0]);
    if (new Date(element.week) < minimum_date) {
      minimum_date = new Date(element.week);
    }
    if (new Date(element.week) > maximum_date) {
      maximum_date = new Date(element.week);
    }
  });

  //   update scales
  line_chart.options.scales.x.min = minimum_date;
  line_chart.options.scales.x.max = maximum_date;

  line_chart.update();
}
