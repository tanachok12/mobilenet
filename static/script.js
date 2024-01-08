document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData();
    formData.append('image', e.target.image.files[0]);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('prediction').textContent = `Prediction: ${data.prediction}`;
    })
    .catch(error => console.error('Error:', error));
});
