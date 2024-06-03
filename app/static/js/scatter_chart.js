async function create_scatter_chart(id, legend_position, aspect_ratio) {
  const data = {
    datasets: [
      {
        label: "Orders",
        data: [],
        backgroundColor: "rgb(255, 99, 132)",
      },
    ],
  };

  const config = {
    type: "scatter",
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
              hour: "dd-MM HH:mm",
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

  var scatter_chart = new Chart(document.getElementById(id), config);
  return scatter_chart;
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

async function update_scatter_chart(
  api_url,
  scatter_chart,
  title,
  tooltip_text
) {
  scatter_chart = await scatter_chart;
  const response = await fetch(api_url);
  const data = await response.json();

  scatter_chart.data.labels = [];
  scatter_chart.data.datasets[0].data = [];
  scatter_chart.data.datasets[0].backgroundColor = [];
  scatter_chart.options.plugins.title.text = title;

  scatter_chart.options.plugins.tooltip = {
    callbacks: {
      label: function (context) {
        console.log(context);
        var label =
          new Date(context.parsed.x).toLocaleString("nl-NL", {
            year: "numeric",
            month: "numeric",
            day: "numeric",
            hour: "numeric",
            minute: "numeric",
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
          label += " " + context.raw.amount + " stuk(s)";
        }
        return label;
      },
    },
  };

  var minimum_date = new Date(data.result[0].date);
  var maximum_date = new Date(data.result[0].date);

  data.result.forEach((element, index) => {
    scatter_chart.data.labels.push(element.label);
    scatter_chart.data.datasets[0].data.push({
      x: element.date,
      y: element.price,
      amount: element.amount,
    });
    scatter_chart.data.datasets[0].backgroundColor.push(
      COLORS[index % COLORS.length]
    );
    if (new Date(element.date) < minimum_date) {
      minimum_date = new Date(element.date);
    }
    if (new Date(element.date) > maximum_date) {
      maximum_date = new Date(element.date);
    }
  });

  //   update scales
  scatter_chart.options.scales.x.min = new Date(
    minimum_date.getFullYear(),
    minimum_date.getMonth(),
    minimum_date.getDate() - 1,
    0,
    0,
    0,
    0
  );
  scatter_chart.options.scales.x.max = new Date(
    maximum_date.getFullYear(),
    maximum_date.getMonth(),
    maximum_date.getDate() + 1,
    23,
    59,
    59,
    999
  );

  scatter_chart.update();
}
