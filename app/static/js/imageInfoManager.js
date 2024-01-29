function getImageInfoFromCanvas(canvas) {
    const ctx = canvas.getContext("2d");

    // Assure-toi que quelque chose est dessiné sur le canvas
    if (ctx) {
      const width = canvas.width;
      const height = canvas.height;

      // Pour obtenir la taille du fichier, tu peux convertir le canvas en blob
      canvas.toBlob(function (blob) {
        const fileSize = blob.size; // Taille du fichier en octets
        const fileSizeInKB = (fileSize / 1024).toFixed(2); // Conversion en kilo-octets

        // Affiche les informations dans le bloc inférieur droit
        const infoBlock = document.getElementById("image-info"); // Assure-toi d'avoir un élément avec cet ID
        infoBlock.innerHTML = `<p>Largeur: ${width}px</p>
                         <p>Hauteur: ${height}px</p>
                         <p>Taille: ${fileSizeInKB}KB</p>
                         <p>Profil couleur: RGB</p>`; // Les images canvas sont toujours en RGB
      });
    }
  }