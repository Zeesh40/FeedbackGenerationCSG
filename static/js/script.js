let criteriaCount = 1; // Default criteria already present
const maxCriteria = 10; // Limit of 10

function addCriteria() {
    if (criteriaCount >= maxCriteria) {
        swal.fire({
            title: "Oh No!",
            text: "You have reached the maximum number of criterias that can be added.",
            icon: "warning"
        });
        return; // Stop execution if the limit is reached
    }

    var criteriaContainer = document.getElementById("criteriaInputs");

    var newInputGroup = document.createElement("div");
    newInputGroup.classList.add("input-group");

    // Create the number label
    var numberLabel = document.createElement("span");
    numberLabel.textContent = (criteriaCount + 1) + "."; // Incremented number
    numberLabel.classList.add("criteria-number");

    // Create the new input fields  
    var newCriteriaInput = document.createElement("input");
    newCriteriaInput.type = "text";
    newCriteriaInput.name = "criteria[]";
    newCriteriaInput.placeholder = "Insert Criteria Name";
    newCriteriaInput.required = true;

    var newScoreInput = document.createElement("input");
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

    // Move buttons below the last added input fields each time
    var form = document.getElementById("feedbackForm");
    form.appendChild(document.querySelector(".add-btn"));
    form.appendChild(document.querySelector(".generate-btn"));

    // Update counter display
    criteriaCount++;
    updateCounter();
}

function updateCounter() {
    document.getElementById("criteriaCounter").textContent = `${criteriaCount}/10`;
}


