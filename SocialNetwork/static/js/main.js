function showFileName(input) {
    // Get the name of the first selected file or show "No file" if none selected
    const fileName = input.files.length > 0 ? input.files[0].name : "Žiadny súbor";
    // Display the file name in the element with id "file-name"
    document.getElementById("file-name").textContent = fileName;
}

document.addEventListener('DOMContentLoaded', function () {
    // Attach submit event listener to all comment forms on the page
    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', async function (e) {
            e.preventDefault(); // Prevent default form submission

            const postId = form.dataset.postId; // Get post ID from data attribute
            const textInput = form.querySelector('input[name="text"]'); // Get comment text input
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value; // Get CSRF token

            // Prepare URL encoded form data with comment text
            const bodyData = new URLSearchParams({ text: textInput.value });

            // Send POST request to submit comment asynchronously
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // Include CSRF token header for security
                    'X-Requested-With': 'XMLHttpRequest', // Identify AJAX request
                    'Content-Type': 'application/x-www-form-urlencoded' // Specify content type
                },
                body: bodyData
            });

            // Parse JSON response
            const data = await response.json();

            // If server returned HTML snippet for new comment, append it to the comment list
            if (data.html) {
                const commentList = document.getElementById(`comments-${postId}`);
                commentList.insertAdjacentHTML('beforeend', data.html);
                textInput.value = ''; // Clear comment input field
            }
        });
    });

    // Attach submit event listener to all like forms on the page
    document.querySelectorAll('.like-form').forEach(form => {
        form.addEventListener('submit', async function (e) {
            e.preventDefault(); // Prevent default form submission

            const postId = form.dataset.postId; // Get post ID from data attribute
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value; // Get CSRF token

            // Send POST request to toggle like asynchronously
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // CSRF token for security
                    'X-Requested-With': 'XMLHttpRequest' // Identify AJAX request
                }
            });

            // Parse JSON response
            const data = await response.json();

            // If server returned updated like count, update it in the UI
            if (data.total_likes !== undefined) {
                const likeCountSpan = form.querySelector('.like-count');
                likeCountSpan.textContent = `(${data.total_likes})`;
            }
        });
    });
});

// Attach submit event listener to the post creation form
document.getElementById('post-form').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent default form submission

    const form = e.target;
    const formData = new FormData(form); // Collect all form data including files

    try {
        // Send POST request to create a new post asynchronously
        const response = await fetch("{% url 'ajax-create-post' %}", {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Identify AJAX request
                'X-CSRFToken': '{{ csrf_token }}' // CSRF token for security
            }
        });

        // Parse JSON response
        const data = await response.json();

        // If response is not OK, alert the error message
        if (!response.ok) {
            alert(data.error || 'Chyba pri vytváraní príspevku');
            return;
        }

        // Create a new post element to display the submitted post
        const newPost = document.createElement('div');
        newPost.classList.add('post');
        newPost.innerHTML = `
            <div class="post-header">
                <img src="{{ user.profile.image.url }}" alt="profil">
                <div class="username">
                    <a href="/profile/{{ user.username }}">{{ user.username }}</a>
                </div>
            </div>
            <div class="post-content">
                <p>${data.content}</p>
                ${data.image_url ? `<img src="${data.image_url}" alt="príspevok">` : ''}
                ${data.video_url ? `<video controls style="max-width: 100%; margin-top: 1rem; border-radius: 8px;">
                    <source src="${data.video_url}" type="video/mp4">
                </video>` : ''}
                <div style="margin-top: 0.5rem;">
                    ${data.tags.map(tag => `<a href="/tag/${tag.slice(1)}" style="color: #1877f2; font-weight: bold; text-decoration: none;">${tag}</a>`).join(' ')}
                </div>
            </div>
        `;

        // Insert the new post right below the first post-box element in the container
        const container = document.querySelector('.container');
        container.insertBefore(newPost, container.children[1]);

        // Reset the post creation form and file name display
        form.reset();
        document.getElementById('file-name').innerText = 'Žiadny súbor';

    } catch (error) {
        // Show error alert if fetch fails
        alert('Chyba pri odoslaní požiadavky');
    }
});
