function calculateHistogramFromCanvas(canvas) {
    const ctx = canvas.getContext("2d");

    // S'assure que le canvas contient bien une image
    if (canvas.width === 0 || canvas.height === 0) {
      console.error("Le canvas est vide.");
      return [];
    }

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    // Création d'un tableau pour les valeurs de l'histogramme
    let histogram = new Array(256).fill(0);

    for (let i = 0; i < data.length; i += 4) {
      // Utilisation de la luminance pour un histogramme en niveaux de gris
      const brightness = Math.floor(
        0.34 * data[i] + 0.5 * data[i + 1] + 0.16 * data[i + 2]
      );
      histogram[brightness]++;
    }

    return histogram;
  }
  function calculateRGBHistogramsFromCanvas(canvas) {
    const ctx = canvas.getContext("2d");
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    // Créer trois tableaux pour les histogrammes RGB
    let histograms = {
      red: new Array(256).fill(0),
      green: new Array(256).fill(0),
      blue: new Array(256).fill(0),
    };

    for (let i = 0; i < data.length; i += 4) {
      histograms.red[data[i]]++;
      histograms.green[data[i + 1]]++;
      histograms.blue[data[i + 2]]++;
    }

    return histograms;
  }

  function displayHistogram(histogramData, canvasId) {
    const ctx = document.getElementById(canvasId).getContext("2d");

    if (histogramChart_L) {
      histogramChart_L.destroy();
    }

    const labels = Array.from({ length: 256 }, (_, i) => i.toString());
    histogramChart_L = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Histogram",
            data: histogramData,
            backgroundColor: "rgba(255, 255, 255, 1)",
            borderColor: "rgba(255, 255, 255, 1)",
            borderWidth: 0,
            //barThickness: 0.25,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        plugins: {
          legend: {
            display: false, // Cela masquera la légende du graphique
          },
        },
        responsive: true,
        maintainAspectRatio: false,
      },
    });
  }

  function displayRGBHistograms(histograms, canvasId) {
    const ctx = document.getElementById(canvasId).getContext("2d");

    // Détruire l'ancien graphique s'il existe
    if (histogramChart_RGB) {
      histogramChart_RGB.destroy();
    }

    const labels = Array.from({ length: 256 }, (_, i) => i.toString());
    histogramChart_RGB = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Red",
            data: histograms.red,
            backgroundColor: "rgba(255, 0, 0, 1)",
            borderColor: "rgba(255, 0, 0, 1)",
            borderWidth: 0,
          },
          {
            label: "Green",
            data: histograms.green,
            backgroundColor: "rgba(0, 255, 0, 1)",
            borderColor: "rgba(0, 255, 0, 1)",
            borderWidth: 0,
          },
          {
            label: "Blue",
            data: histograms.blue,
            backgroundColor: "rgba(0, 0, 255, 1)",
            borderColor: "rgba(0, 0, 255, 1)",
            borderWidth: 0,
          },
        ],
      },
      options: {
        scales: {
          x: {
            stacked: false,
          },
          y: {
            beginAtZero: true,
            stacked: false,
          },
        },
        plugins: {
          legend: {
            display: false, // Cela masquera la légende du graphique
          },
        },
        responsive: true,
        maintainAspectRatio: false,
      },
    });
  }