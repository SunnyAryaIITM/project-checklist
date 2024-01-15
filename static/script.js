function toggleNavbar() {
    var navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

document.querySelectorAll('.nav-links a').forEach(function (link) {
    link.addEventListener('click', function () {
        var navLinks = document.querySelector('.nav-links');
        navLinks.classList.remove('active');
    });
});

function animateDynamicText() {
    const dynamicText = document.getElementById('dynamic-text');
    const cursor = document.getElementById('cursor');
    const textContent = dynamicText.textContent;

    function typeWriter(index) {
        if (index <= textContent.length) {
            dynamicText.textContent = textContent.slice(0, index);
            setTimeout(() => {
                typeWriter(index + 1);
            }, 150);
        } else {
            blinkCursor();
        }
    }

    function blinkCursor() {
        cursor.style.display = 'inline';
        setTimeout(() => {
            eraseText(textContent.length);
        }, 1500); // Adjust the delay before erasing
    }

    function eraseText(index) {
        if (index >= 0) {
            dynamicText.textContent = textContent.slice(0, index);
            setTimeout(() => {
                eraseText(index - 1);
            }, 150);
        } else {
            setTimeout(() => {
                typeWriter(0);
            }, 1500); // Adjust the delay before typing again
        }
    }

    typeWriter(0);
}

function redirectToYouTube() {
    window.open('https://www.youtube.com/@bytebuddyofficial', '_blank');
}

animateDynamicText();

// Open the Add Course Form Modal
function openAddCourseForm() {
    var modal = document.getElementById('addCourseModal');
    modal.style.display = 'block';
}

// Close the Add Course Form Modal
function closeAddCourseForm() {
    var modal = document.getElementById('addCourseModal');
    modal.style.display = 'none';
}

// Close the Add Course Form Modal if the user clicks outside of it
window.onclick = function(event) {
    var modal = document.getElementById('addCourseModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};

function markCompleted(checklistId) {
    fetch(`/mark_completed/${checklistId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log(response);
            window.location.reload()
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function markIncompleted(checklistId) {
    fetch(`/mark_incompleted/${checklistId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            window.location.reload()
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Open the Edit Checklist Form Modal
function openEditChecklistForm() {
    var modal = document.getElementById('editChecklistModal');
    modal.style.display = 'block';
}

// Close the Edit Checklist Form Modal
function closeEditChecklistForm() {
    var modal = document.getElementById('editChecklistModal');
    modal.style.display = 'none';
}

// Rename a checklist
function renameChecklist(checklistId) {
    // Implement renaming logic here
    console.log('Rename checklist with ID:', checklistId);
}

// Delete selected checklists
// Add this function to your existing JavaScript file

function deleteSelectedChecklists() {
    var checkboxes = document.querySelectorAll('input[name="checklists[]"]:checked');
    var checklistIds = Array.from(checkboxes).map(checkbox => checkbox.value);

    if (checklistIds.length === 0) {
        alert('Please select at least one checklist to delete.');
        return;
    }

    fetch('/delete_checklists', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ checklistIds: checklistIds }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Optional: Display a success message or update UI
                window.location.reload();
            } else {
                console.error('Failed to delete checklists:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Add these functions to your existing JavaScript file

function renameChecklist(checklistId) {
    // Hide the label and show the rename input field
    document.getElementById(`renameContainer_${checklistId}`).style.display = 'flex';
    document.querySelector(`label[for="checklist_${checklistId}"]`).style.display = 'none';
}

function confirmRename(checklistId) {
    var newName = document.getElementById(`renameInput_${checklistId}`).value;

    // Use fetch to send the updated name to the server
    fetch(`/rename_checklist/${checklistId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            new_name: newName,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the label and hide the rename input field
            document.querySelector(`label[for="checklist_${checklistId}"]`).textContent = newName;
            document.getElementById(`renameContainer_${checklistId}`).style.display = 'none';
            document.querySelector(`label[for="checklist_${checklistId}"]`).style.display = 'flex';
        } else {
            console.error('Failed to rename checklist:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Other functions (renameChecklist, cancelRename) remain unchanged


