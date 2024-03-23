function generateChartData(startDate, endDate) {
  var timeDiff = endDate - startDate;
  var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24)); // Difference in days

  // Determine the period based on the difference in days
  var period;
  if (diffDays <= 21) {
    period = "daily";
  } else if (diffDays <= 93) {
    period = "weekly";
  } else if (diffDays <= 730) {
    period = "monthly";
  } else {
    period = "yearly";
  }

  // Step 1: Extract data for the specified period from the sensorsData
  var periodData = sensorsData.filter(function (measure) {
    var measureDate = new Date(measure.date);
    return measureDate >= startDate && measureDate <= endDate;
  });

  // Step 2: Group the data by period
  var groupedData = {};
  periodData.forEach(function (measure) {
    var measureDate = new Date(measure.date);
    var key;
    if (period === "daily") {
      key = measureDate.toLocaleDateString();
    } else if (period === "weekly") {
      var firstDayOfWeek = new Date(measureDate);
      firstDayOfWeek.setDate(firstDayOfWeek.getDate() - measureDate.getDay());
      key = firstDayOfWeek.toLocaleDateString();
    } else if (period === "monthly") {
      key =
        measureDate.toLocaleString("default", { month: "long" }) +
        " " +
        measureDate.getFullYear();
    } else {
      key = measureDate.getFullYear().toString();
    }
    if (!groupedData[key]) {
      groupedData[key] = [];
    }
    groupedData[key].push(measure);
  });

  // Step 3: Prepare data for Chart.js
  var labels = [];
  var phData = [];
  var temperatureData = [];
  var humidityData = [];
  var nitrogenData = [];
  var phosphorusData = [];
  var potassiumData = [];
  var rainfallData = [];

  Object.keys(groupedData).forEach(function (key) {
    var groupMeasures = groupedData[key] || [];
    var avgPH = 0;
    var avgTemperature = 0;
    var avgHumidity = 0;
    var avgNitrogen = 0;
    var avgPhosphorus = 0;
    var avgPotassium = 0;
    var avgRainfall = 0;

    groupMeasures.forEach(function (measure) {
      avgPH += measure.ph;
      avgTemperature += measure.temperature;
      avgHumidity += measure.humidity;
      avgNitrogen += measure.nitrogen;
      avgPhosphorus += measure.phosphorus;
      avgPotassium += measure.potassium;
      avgRainfall += measure.rainfall;
    });

    var count = groupMeasures.length || 1; // Ensure count is at least 1 to avoid division by zero
    avgPH /= count;
    avgTemperature /= count;
    avgHumidity /= count;
    avgNitrogen /= count;
    avgPhosphorus /= count;
    avgPotassium /= count;
    avgRainfall /= count;

    labels.push(key);
    phData.push(avgPH);
    temperatureData.push(avgTemperature);
    humidityData.push(avgHumidity);
    nitrogenData.push(avgNitrogen);
    phosphorusData.push(avgPhosphorus);
    potassiumData.push(avgPotassium);
    rainfallData.push(avgRainfall);
  });

  return {
    labels: labels,
    phData: phData,
    temperatureData: temperatureData,
    humidityData: humidityData,
    nitrogenData: nitrogenData,
    phosphorusData: phosphorusData,
    potassiumData: potassiumData,
    rainfallData: rainfallData,
  };
}

function updateCharts() {
  var startDateInput = document.getElementById("start-date");
  var endDateInput = document.getElementById("end-date");

  // Check if the input fields have values
  var startDateValue = startDateInput.value;
  var endDateValue = endDateInput.value;

  // If no value is selected, set predefined values (e.g., one year ago for start date and today for end date)
  if (!startDateValue) {
    var oneYearAgo = new Date();
    oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
    startDateInput.value = oneYearAgo.toISOString().split("T")[0]; // Format as YYYY-MM-DD
  }

  if (!endDateValue) {
    var today = new Date();
    endDateInput.value = today.toISOString().split("T")[0]; // Format as YYYY-MM-DD
  }

  // Get the selected start and end dates
  var startDate = new Date(startDateInput.value);
  var endDate = new Date(endDateInput.value);

  // Call the function to generate chart data based on the selected dates
  var chartData = generateChartData(startDate, endDate);

  [
    "phChart",
    "temperatureChart",
    "rainfallChart",
    "humidityChart",
    "npkChart",
  ].forEach((chartId) => {
    var existingChart = Chart.getChart(chartId);
    if (existingChart) {
      existingChart.destroy();
    }
  });
  // Update or recreate the charts with the new data
  // Your chart creation code goes here, using the updated chartData
  const chartConfigs = [
    {
      id: "phChart",
      label: "pH",
      data: chartData.phData,
      color: "rgba(255, 99, 132, 1)",
    },
    {
      id: "temperatureChart",
      label: "Temperature",
      data: chartData.temperatureData,
      color: "rgba(54, 162, 235, 1)",
    },
    {
      id: "rainfallChart",
      label: "Rainfall",
      data: chartData.rainfallData,
      color: "rgba(255, 99, 71, 1)",
    },
    {
      id: "humidityChart",
      label: "Humidity",
      data: chartData.humidityData,
      color: "rgba(255, 206, 86, 1)",
    },
    {
      id: "npkChart",
      label: ["Nitrogen", "Phosphorus", "Potassium"],
      data: [
        chartData.nitrogenData,
        chartData.phosphorusData,
        chartData.potassiumData,
      ],
      color: [
        "rgba(75, 192, 192, 1)",
        "rgba(153, 102, 255, 1)",
        "rgba(255, 159, 64, 1)",
      ],
    },
  ];

  chartConfigs.forEach((config) => {
    const ctx = document.getElementById(config.id).getContext("2d");

    if (config.id === "npkChart") {
      new Chart(ctx, {
        type: "line",
        data: {
          labels: chartData.labels,
          datasets: config.label.map((label, index) => ({
            label: label,
            data: config.data[index],
            borderColor: config.color[index],
            borderWidth: 1,
            fill: false,
          })),
        },
        options: {
          scales: {
            y: { beginAtZero: false },
          },
        },
      });
    } else {
      new Chart(ctx, {
        type: "line",
        data: {
          labels: chartData.labels,
          datasets: [
            {
              label: config.label,
              data: config.data,
              borderColor: config.color,
              borderWidth: 1,
              fill: false,
            },
          ],
        },
        options: {
          scales: {
            y: { beginAtZero: false },
          },
        },
      });
    }
  });
}

updateCharts();

function calculateAndDisplayLabel() {
  var startDate = new Date(document.getElementById("start-date").value);
  var endDate = new Date(document.getElementById("end-date").value);

  // Call the function to generate chart data based on the selected dates
  var chartData = generateChartData(startDate, endDate);
  // Calculate average data from chartData
  var avgData = calculateAverageData(chartData);
  console.log(avgData);

  var requestData = [
    {
      Nitrogen: avgData.avgNitrogen,
      phosphorus: avgData.avgPhosphorus,
      potassium: avgData.avgPotassium,
      temperature: avgData.avgTemperature,
      humidity: avgData.avgHumidity,
      ph: avgData.avgPH,
      rainfall: avgData.avgRainfall,
    },
  ];
  console.log(requestData);
  // Send the average data to the predict endpoint using a POST request
  fetch(predictEndpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken, // Include CSRF token in the headers
    },
    body: JSON.stringify(requestData),
  })
    .then((response) => response.json())
    .then((data) => {
      // Display the returned label on the page
      var labelResultElement = document.getElementById("labelResult");
      labelResultElement.textContent = data.predictions[0];
    })
    .catch((error) => {
      console.error("Error:", error);
      var labelResultElement = document.getElementById("labelResult");
      labelResultElement.textContent = "Error fetching label.";
    });
}

function calculateAverageData(chartData) {
  // Calculate averages of chartData
  var avgData = {
    avgPH: calculateAverage(chartData.phData),
    avgTemperature: calculateAverage(chartData.temperatureData),
    avgHumidity: calculateAverage(chartData.humidityData),
    avgNitrogen: calculateAverage(chartData.nitrogenData),
    avgPhosphorus: calculateAverage(chartData.phosphorusData),
    avgPotassium: calculateAverage(chartData.potassiumData),
    avgRainfall: calculateAverage(chartData.rainfallData),
  };
  return avgData;
}

function calculateAverage(data) {
  if (data.length === 0) return 0; // Return 0 if no data is available
  var sum = data.reduce((total, value) => total + value, 0);
  return sum / data.length;
}
