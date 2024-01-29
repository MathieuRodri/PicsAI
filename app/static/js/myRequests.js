document.getElementById("btn-option-1").addEventListener("click", function() {
    sendRequestToProcess(1)
});
document.getElementById("btn-option-2").addEventListener("click", function() {
    sendRequestToProcess(2)
});
document.getElementById("btn-option-3").addEventListener("click", function() {
    sendRequestToProcess(3)
});
document.getElementById("btn-option-4").addEventListener("click", function() {
    sendRequestToProcess(4)
});
document.getElementById("btn-option-5").addEventListener("click", function() {
    sendRequestToProcess(5)
});
document.getElementById("btn-option-6").addEventListener("click", function() {
    sendRequestToProcess(6)
});
document.getElementById("btn-option-7").addEventListener("click", function() {
    sendRequestToProcess(7)
});

function sendRequestToProcess(id_operation) {
    const canvas = document.getElementById("imageCanvas");
    const image = canvas.toDataURL("image/jpeg"); // Convertir le canvas en base64
    const loading_gif = document.getElementById('loading-gif');

    fadeIn(loading_gif);

    // Récupérez le jeton CSRF depuis les cookies Django
    const csrftoken = getCookie('csrftoken');

    // Envoie de la requête AJAX avec le jeton CSRF inclus dans l'en-tête
    $.ajax({
        type: "POST",
        url: `/execute_background_script/${id_operation}/`,
        data: { image_data: image }, // Envoyez les données de l'image dans le corps de la requête POST
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken); // Inclure le jeton CSRF dans l'en-tête
        },
        success: function (response) {
            // Mettez à jour le canvas avec l'image reçue
            const img = new Image();
            img.onload = function () {
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext("2d");
                ctx.drawImage(img, 0, 0);
            };
            console.log(response)
            img.src = `data:image/jpeg;base64,${response.image_data}`;
            loading_gif.style.display = 'none';

            fadeOut(loading_gif);
        },
        error: function (error) {
            // Gérez les erreurs ici si nécessaire.
            console.error("Erreur lors de la requête AJAX : " + error);

            fadeOut(loading_gif);
        },
    });
}

function fadeIn(element, duration = 500) {
    let opacity = 0;
    element.style.opacity = opacity;
    element.style.display = 'block';
    const interval = 10; // Durée d'un pas en millisecondes
    const step = interval / duration; // Augmentation de l'opacité par pas

    const fading = setInterval(function() {
        opacity += step;
        element.style.opacity = opacity;
        if(opacity >= 0.6) clearInterval(fading);
    }, interval);
}

function fadeOut(element, duration = 500) {
    let opacity = 0.6;
    element.style.opacity = opacity;
    const interval = 10; // Durée d'un pas en millisecondes
    const step = interval / duration; // Diminution de l'opacité par pas

    const fading = setInterval(function() {
        opacity -= step;
        element.style.opacity = opacity;
        if(opacity <= 0) {
            clearInterval(fading);
            element.style.display = 'none';
        }
    }, interval);
}

// Fonction pour récupérer le jeton CSRF depuis les cookies Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}