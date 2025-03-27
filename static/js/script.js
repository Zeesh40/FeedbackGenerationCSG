let criteriaCount = 1; // Default criteria already present
const maxCriteria = 10; // Limit of 10
let criteriaList = [];  // Array to store criteria objects
let savedJustifications = []; // Store user-added justifications


function attachJustificationEventListeners() {
    document.querySelectorAll(".add-justification").forEach((button) => {
        button.removeEventListener("click", addJustificationHandler);
        button.addEventListener("click", addJustificationHandler);
    });
}

// Justification Handler Function
// Justification Handler Function
function addJustificationHandler(event) {
    let justificationDropdown = event.target.previousElementSibling; // Get the associated dropdown

    Swal.fire({
        title: "Add a Justification",
        html: `
            <input id="justificationTitle" class="swal2-input custom-input" placeholder="Enter title e.g. 'Not Enough Work'">
            <input id="justificationText" class="swal2-input custom-input" placeholder="Enter justification e.g. 'You haven't provided enough information.'">
        `,
        showCancelButton: true,
        confirmButtonText: "Save",
        customClass: {
            popup: 'wide-popup',
        },
        preConfirm: () => {
            let title = document.getElementById("justificationTitle").value.trim();
            let text = document.getElementById("justificationText").value.trim();
    
            if (!title || !text) {
                Swal.showValidationMessage("Both fields are required!");
                return false;
            }
            return { title, text };
        }
    }).then((result) => {
        if (result.isConfirmed) {
            let { title, text } = result.value;

            // Store the justification data in the dropdown's dataset
            let newOption = document.createElement("option");
            newOption.value = text; // Store justification text as value
            newOption.textContent = title; // Display title in dropdown
            justificationDropdown.appendChild(newOption);
        }
    });
}


// Function to add more criteria input fields dynamically
function addCriteria() {
    if (criteriaCount >= maxCriteria) {
        Swal.fire({
            title: "Oh No!",
            text: "You have reached the maximum number of criteria that can be added.",
            icon: "warning"
        });
        return;
    }

    let criteriaContainer = document.getElementById("criteriaInputs");
    let newInputGroup = document.createElement("div");
    newInputGroup.classList.add("input-group");


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

    let justificationDropdown = document.createElement("select");
    justificationDropdown.classList.add("justification-dropdown");

    let defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "No Justification";
    justificationDropdown.appendChild(defaultOption);

    savedJustifications.forEach(justification => {
        let option = document.createElement("option");
        option.value = justification;
        option.textContent = justification;
        justificationDropdown.appendChild(option);
    });

    let addJustificationBtn = document.createElement("button");
    addJustificationBtn.textContent = "+";
    addJustificationBtn.type = "button";
    addJustificationBtn.classList.add("add-justification");

    // Append elements
    newInputGroup.appendChild(newCriteriaInput);
    newInputGroup.appendChild(newScoreInput);
    newInputGroup.appendChild(justificationDropdown);
    newInputGroup.appendChild(addJustificationBtn);

    criteriaContainer.appendChild(newInputGroup);

    criteriaCount++;
    updateCounter();

    // Attach Justification Event Listeners to all buttons (Including the First One)
    attachJustificationEventListeners();
}

// Function to update the counter display
function updateCounter() {
    document.getElementById("criteriaCounter").textContent = `${criteriaCount}/10`;
}

// Function to store criteria inputs in a structured way
function storeCriteria() {
    let inputs = document.querySelectorAll("#criteriaInputs .input-group");

    criteriaList = []; // Reset before storing new data

    inputs.forEach(inputGroup => {
        let criteriaName = inputGroup.querySelector("input[type='text']").value.trim();
        let percentage = parseFloat(inputGroup.querySelector("input[type='number']").value);
        let justificationDropdown = inputGroup.querySelector(".justification-dropdown");
        let justification = justificationDropdown.value; // Get selected justification text

        if (criteriaName && !isNaN(percentage)) {
            criteriaList.push({ "criterion": criteriaName, "score": percentage, "justification": justification });
        }
    });

    console.log("Stored Criteria Data:", criteriaList); // Debugging output
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

    if (criteriaList.length === 0) {
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
        body: JSON.stringify({ "criteria": criteriaList })
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
document.addEventListener("DOMContentLoaded", attachJustificationEventListeners);
