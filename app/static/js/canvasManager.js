document
        .getElementById("drop-area")
        .addEventListener("click", function () {
          document.getElementById("imageInput").click();
        });

      document
        .getElementById("imageInput")
        .addEventListener("change", function (event) {
          handleFiles(event.target.files);
        });

      document
        .getElementById("drop-area")
        .addEventListener("dragover", function (event) {
          event.preventDefault();
          event.stopPropagation();
          this.style.background = "#e1e7f0";
        });

      document
        .getElementById("drop-area")
        .addEventListener("dragleave", function (event) {
          event.preventDefault();
          event.stopPropagation();
          this.style.background = "";
        });

      document
        .getElementById("drop-area")
        .addEventListener("drop", function (event) {
          event.preventDefault();
          event.stopPropagation();
          this.style.background = "";
          let dt = event.dataTransfer;
          let files = dt.files;
          handleFiles(files);
        });

      function handleFiles(files) {
        if (files.length === 0) return;
        const file = files[0];
        if (file.type.startsWith("image/")) {
          const reader = new FileReader();
          reader.onload = function (e) {
            const img = new Image();
            img.onload = function () {
              const canvas = document.getElementById("imageCanvas");
              canvas.width = img.width;
              canvas.height = img.height;
              const ctx = canvas.getContext("2d");
              ctx.drawImage(img, 0, 0);
              canvas.style.display = "block";
              document.getElementById("drop-text").style.display = "none";
              //Histogram

              const histogramData_L = calculateHistogramFromCanvas(imageCanvas);
              displayHistogram(histogramData_L, "histogram_L");

              const histogramData_RGB =
                calculateRGBHistogramsFromCanvas(imageCanvas);
              displayRGBHistograms(histogramData_RGB, "histogram_RGB");

              getImageInfoFromCanvas(imageCanvas);
            };
            img.src = e.target.result;
          };
          reader.readAsDataURL(file);
        } else {
          alert("Please drop an image file.");
        }
      }