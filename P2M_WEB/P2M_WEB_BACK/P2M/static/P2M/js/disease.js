function getCsrfToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
}



document.getElementById('crop').addEventListener('change', function (event) {
    var file = event.target.files[0];
    if (file) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var imgElement = document.getElementById('uploadedImage');
            imgElement.src = e.target.result;
            imgElement.style.display = 'block'; // Make the image visible
        };

        reader.readAsDataURL(file); // Read the file as a Data URL.
    }

    const csrfToken = getCsrfToken(); // Get CSRF token from cookies

    var formData = new FormData();
    formData.append("image", file); // Use the same name for the field as expected on the server side

    fetch(predictEndpoint, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            } else if (!response.headers.get("content-type").includes("application/json")) {
                console.error("Received non-JSON response from the server.");
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data) console.log(data);
            document.getElementById('predictionResult').textContent = 'Disease: ' + data.prediction; // Adjust 'data.prediction' as needed based on your response structure
        })
        .catch(error => console.error("Error:", error));

});

// Close functionality for the modal
document.querySelector('.close').onclick = function () {
    this.parentElement.style.display = 'none'; // Assuming '.close' is a direct child of the modal content
};


const csrfToken = getCsrfToken(); // Get CSRF token from cookies

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function () {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

