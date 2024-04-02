// Get CSRF token from cookie - required for POST requests in Django
function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}

// Function to send a POST request to the predict endpoint
function sendPredictionRequest(sensorId, startDate, endDate) {
    // Construct the URL endpoint for predictions
    //const predictEndpoint = `/api/predict/`;

    // Format dates to "YYYY-MM-DD" format
    const startDateFormatted = startDate.toISOString().split('T')[0];
    const endDateFormatted = endDate.toISOString().split('T')[0];

    // Prepare the data to be sent in the request
    const postData = {
        start_date: startDateFormatted,
        end_date: endDateFormatted,
        // ... include other necessary data fields
    };

    fetch(predictEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken() // get CSRF token for Django POST request
        },
        body: JSON.stringify(postData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            displayPrediction(data); // You'll need to define this function to update the UI with the prediction result
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Add a click event listener to the predict button
document.addEventListener('DOMContentLoaded', () => {
    const predictButton = document.getElementById('predictButton'); // Make sure this matches your button's ID
    if (predictButton) { // Only add listener if the button exists
        predictButton.addEventListener('click', () => {
            const sensorId = "000000000000000000000001"; // Fixed for the example
            // Dates need to be converted to ISO strings without time information
            const startDate = new Date(2023, 2, 2); // Remember, months are 0-indexed
            const endDate = new Date(2023, 2, 3);
            sendPredictionRequest(sensorId, startDate, endDate);
        });
    }
});

// Function to update the UI with the prediction result
function displayPrediction(predictionData) {
    // Assuming predictionData contains a field 'predicted_crop'
    const predictedCrop = predictionData.predicted_crop;
    // Now update the DOM with this information
    const predictionResultElement = document.getElementById('predictionResult');
    if (predictionResultElement) { // Check if the element exists
        predictionResultElement.textContent = `The suitable crop is ${predictedCrop}.`;
    }
}
