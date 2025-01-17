// Add a new criteria input group dynamically
function addCriteria() {
    const container = document.getElementById('criteriaInputs');
    const inputGroups = container.querySelectorAll('.input-group');

    // Limit to 6 criteria
    if (inputGroups.length >= 6) {
        alert('You can only add up to 6 criteria.');
        return;
    }

    const div = document.createElement('div');
    div.classList.add('input-group');
    div.innerHTML = `
        <input type="text" name="criteria[]" placeholder="Insert Criteria Name" required>
        <input type="number" name="scores[]" placeholder="Insert %" min="0" max="100" required>
    `;
    container.appendChild(div);
}

// Handle "Generate" button click
document.getElementById('generateFeedback').addEventListener('click', function () {
    const feedbackOutput = document.getElementById('feedbackOutput');
    feedbackOutput.textContent = "This is a placeholder for feedback generation.";
});
