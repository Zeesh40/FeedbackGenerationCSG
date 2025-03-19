let criteriaCount = 1; // Default criteria already present
const maxCriteria = 10; // Limit of 10
let criteriaData = {};  // Dictionary to store criteria name and percentage

// Function to add more criteria input fields dynamically
function addCriteria() {
    if (criteriaCount >= maxCriteria) {
        Swal.fire({
            title: "Oh No!",
            text: "You have reached the maximum number of criteria that can be added.",
            icon: "warning"
        });
        return; // Stop execution if the limit is reached
    }

    let criteriaContainer = document.getElementById("criteriaInputs");

    let newInputGroup = document.createElement("div");
    newInputGroup.classList.add("input-group");

    // Create the number label
    let numberLabel = document.createElement("span");
    numberLabel.textContent = (criteriaCount + 1) + ".";
    numberLabel.classList.add("criteria-number");

    // Create the new input fields
    let newCriteriaInput = document.createElement("input");
    newCriteriaInput.type = "text";
    newCriteriaInput.name = "criteria[]";
    newCriteriaInput.placeholder = "Insert Criteria Name";
    newCriteriaInput.required = true;

    let newScoreInput = document.createElement("input");
    newScoreInput.type = "number";
    newScoreInput.name = "scores[]";
    newScoreInput.placeholder = "Insert %";
    newScoreInput.min = "0";
    newScoreInput.max = "100";
    newScoreInput.step = "1";
    newScoreInput.required = true;

    // Append elements to the new input group
    newInputGroup.appendChild(numberLabel);
    newInputGroup.appendChild(newCriteriaInput);
    newInputGroup.appendChild(newScoreInput);

    // Append the new input group to the container
    criteriaContainer.appendChild(newInputGroup);

    // Update counter display
    criteriaCount++;
    updateCounter();
}

// Function to update the counter display
function updateCounter() {
    document.getElementById("criteriaCounter").textContent = `${criteriaCount}/10`;
}

// Function to store criteria inputs in a dictionary
function storeCriteria() {
    let inputs = document.querySelectorAll("#criteriaInputs .input-group");

    criteriaData = {}; // Reset dictionary before storing new data

    inputs.forEach(inputGroup => {
        let criteriaName = inputGroup.querySelector("input[type='text']").value.trim();
        let percentage = parseFloat(inputGroup.querySelector("input[type='number']").value);

        if (criteriaName && !isNaN(percentage)) {
            criteriaData[criteriaName] = percentage;
        }
    });

    console.log("Stored Criteria Data:", criteriaData); // Debugging output
}

// Function to validate percentage input
function validatePercentageInput(input) {
    let value = parseInt(input.value, 10);

    if (isNaN(value) || value < 0 || value > 100) {
        input.value = ""; // Clear invalid input
        Swal.fire({
            title: "Invalid Input!",
            text: "Please enter a whole number between 0 and 100.",
            icon: "error"
        });
    }
}

// Attach validation to all number inputs
document.addEventListener("input", function(event) {
    if (event.target.matches("input[type='number']")) {
        validatePercentageInput(event.target);
    }
});



// Function to send criteria data to the backend
function sendData() {
    storeCriteria(); // Collect latest input data

    if (Object.keys(criteriaData).length === 0) {
        Swal.fire({
            title: "No Data!",
            text: "Please enter at least one valid criteria before generating feedback.",
            icon: "error"
        });
        return;
    }

    fetch('/process_feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(criteriaData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("feedbackOutput").innerText = data.feedback;
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire({
            title: "Oops!",
            text: "Something went wrong while generating feedback.",
            icon: "error"
        });
    });
}

// Attach event listener to the "Generate" button
document.getElementById("generateFeedback").addEventListener("click", sendData);