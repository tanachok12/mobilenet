document.addEventListener("DOMContentLoaded", function () {
  var fileInput = document.getElementById("image-upload");
  var uploadButton = document.getElementById("upload-button");
  var captureButton = document.getElementById("capture");
  var predictionElement = document.getElementById("predictionText");

  // Function to handle image upload
  function uploadImage(imageData) {
    console.log("Uploading image data:", imageData);

    var formData = new FormData();
    formData.append('image', imageData);
    var threshold = document.getElementById('thresholdRange').value;
    formData.append('threshold', threshold);  // เพิ่ม threshold ใน formData
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Server returned an error');
        }
        return response.json();
    })
    .then(data => {
        if (data.image_data) {
            var image = new Image();
            image.src = 'data:image/jpeg;base64,' + data.image_data;
            showPredictionPopup(`Prediction: ${data.prediction}`, image.src);
        } else {
            console.error('No image data received');
        }
    })
    
    .catch(error => {
        console.error('Error:', error);
        displayPredictionAndClear(predictionElement, `Error: ${error.message}`);
    });
}



  // Function to convert dataURL to Blob
  function dataURLtoBlob(dataURL) {
    var byteString = atob(dataURL.split(",")[1]);
    var mimeString = dataURL.split(",")[0].split(":")[1].split(";")[0];
    var arrayBuffer = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(arrayBuffer);
    for (var i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([arrayBuffer], { type: mimeString });
  }

  // Function to show the prediction popup
  function showPredictionPopup(prediction, imageUrl) {
    var modal = document.getElementById("predictionModal");
    var span = document.getElementsByClassName("close")[0];
    var predictionText = document.getElementById("predictionText");
    var predictionImage = document.getElementById("predictionImage");
    var modal = document.getElementById("predictionModal");

    span.onclick = function () {
      modal.style.display = "none";
    };

    window.onclick = function (event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    };

    predictionText.textContent = prediction;
    predictionImage.src = imageUrl;  // ตั้งค่า src ของรูปภาพเป็น Base64 string
    modal.style.display = "block";
    console.log("img:", imageUrl);
    console.log("img:", prediction);
  }

  // Upload button event
  uploadButton.addEventListener("click", function (e) {
    e.preventDefault();
    var file = fileInput.files[0];
    if (file) {
      uploadImage(file);
    } else {
      alert("Please select an image file first.");
    }
  });

  // Capture button event
  if (captureButton) {
    captureButton.addEventListener("click", async () => {
      const video = document.getElementById("video");
      const canvas = document.getElementById("canvas");
      if (!video.srcObject) {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
        });
        video.srcObject = stream;
        captureButton.textContent = "Take Picture";
      } else {
        canvas.getContext("2d").drawImage(video, 0, 0);
        video.srcObject.getTracks().forEach((track) => track.stop());
        video.srcObject = null;
        captureButton.textContent = "Capture";
        const dataURL = canvas.toDataURL("image/png");
        uploadImage(dataURLtoBlob(dataURL));
      }
    });
  }
});

function displayPredictionAndClear(predictionElement, message) {
  predictionElement.textContent = message;
  setTimeout(() => {
    predictionElement.textContent = "";
  }, 5000);
}
