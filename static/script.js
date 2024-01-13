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
    // Use AJAX to send a request to mark the checklist as completed
    // Replace 'your_flask_app_url' with the actual URL of your Flask app
    fetch(`/mark_completed/${checklistId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Marked checklist as completed with ID: ${checklistId}`);
                // You can also update the UI here if needed
            } else {
                alert('Failed to mark checklist as completed.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

    window.location.reload();
}