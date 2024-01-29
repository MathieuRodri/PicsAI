document.getElementById('btn-download').addEventListener('click', function() {
    const imageCanvas = document.getElementById('imageCanvas');
    if (imageCanvas) {
        const imageDataURL = imageCanvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.download = 'image.png';
        link.href = imageDataURL;
        link.click();
    }
});

document.getElementById('btn-remove').addEventListener('click', function() {
    if (imageCanvas) {
        const context = imageCanvas.getContext('2d');
        context.clearRect(0, 0, imageCanvas.width, imageCanvas.height);
        imageCanvas.style.display = "none";
        document.getElementById("drop-text").style.display = "block";
    }
});
