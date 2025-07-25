function showFileName(input) {
    // Get the file name from the input, or show "No file" if none selected
    const fileName = input.files.length > 0 ? input.files[0].name : "Žiadny súbor";
    // Set the text content of the element with id "file-name" to the file name
    document.getElementById("file-name").textContent = fileName;
}

document.addEventListener('DOMContentLoaded', function () {

    // Add submit event logic to comment forms
    function addCommentFormLogic(form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();  // Prevent default form submission
            // Get URL for the request from data attribute or form action attribute
            const url = form.dataset.url || form.action;
            const textInput = form.querySelector('input[name="text"]');
            const text = textInput.value.trim();  // Trim whitespace from input

            if (!text) return;  // If text is empty, do nothing

            // Create FormData with the comment text and CSRF token
            const formData = new FormData();
            formData.append('text', text);
            formData.append('csrfmiddlewaretoken', form.querySelector('[name=csrfmiddlewaretoken]').value);

            // Send POST request with the form data
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'  // Indicate AJAX request
                }
            });

            const data = await response.json();

            if (!response.ok) {
                // Show error alert if response is not ok
                alert(data.error || 'Chyba pri odoslaní komentára');
                return;
            }

            // Find the comment list container near the form
            const commentList = form.closest('.comments').querySelector('.comment-list');
            // Create new comment element and populate it with data from server
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.innerHTML = `
                <img src="${data.profile_image_url}" alt="profil" class="comment-avatar">
                <div class="comment-body">
                    <div class="comment-header">
                        <strong>${data.username}</strong>
                        <span class="comment-time">${data.created_at}</span>
                    </div>
                    <div class="comment-text">${data.text}</div>
                </div>`;
            // Append the new comment to the list
            commentList.appendChild(newComment);
            // Clear the input field
            textInput.value = '';
        });
    }

    // Add submit event logic to like forms
    function addLikeFormLogic(form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();  // Prevent default form submission
            const postId = form.dataset.postId;  // Get post ID (not used here but available)
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value; // Get CSRF token

            // Send POST request to like/unlike endpoint
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,  // CSRF token header for security
                    'X-Requested-With': 'XMLHttpRequest'  // Indicate AJAX request
                }
            });

            const data = await response.json();
            if (data.total_likes !== undefined) {
                // Update the like count displayed in the form
                const likeCountSpan = form.querySelector('.like-count');
                likeCountSpan.textContent = `(${data.total_likes})`;
            }
        });
    }

    // Attach comment and like logic to existing forms on the page
    document.querySelectorAll('.comment-form').forEach(addCommentFormLogic);
    document.querySelectorAll('.like-form').forEach(addLikeFormLogic);

    // Handle submission of the new post form
    const postForm = document.getElementById('post-form');
    if (postForm) {
        postForm.addEventListener('submit', async function (e) {
            e.preventDefault();  // Prevent default form submission

            const form = e.target;
            const formData = new FormData(form);
            const url = form.dataset.url;  // URL to send the request to

            try {
                // Send POST request with form data to create new post
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });

                const data = await response.json();

                if (!response.ok) {
                    // Show alert if error returned from server
                    alert(data.error || 'Chyba pri vytváraní príspevku');
                    return;
                }

                // Create new post element with returned data
                const newPost = document.createElement('div');
                newPost.classList.add('post-box', 'post');
                newPost.innerHTML = `
                    <div class="post-header">
                        <img src="${data.profile_image_url}" alt="profil">
                        <div class="username">
                            <a href="${data.profile_url}">${data.username}</a>
                        </div>
                    </div>
                    <div class="post-content">
                        <p>${data.content}</p>
                        ${data.image_url ? `<img src="${data.image_url}" alt="príspevok">` : ''}
                        ${data.video_url ? `<video controls><source src="${data.video_url}" type="video/mp4"></video>` : ''}
                        <div style="margin-top: 0.5rem;">
                            ${data.tags.map(tag => `<a href="/posts/by-tag/${tag.replace('#', '')}" style="color: #1877f2; font-weight: bold; text-decoration: none;">${tag}</a>`).join(' ')}
                        </div>
                    </div>

                    <!-- Like button form -->
                    <form method="POST" action="/like/${data.post_id}/" class="like-form" data-post-id="${data.post_id}">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">
                        <button type="submit" class="like-button">
                            👍 <span class="like-text">Lajk</span>
                            <span class="like-count">(0)</span>
                        </button>
                    </form>

                    <div class="comments">
                        <h4>Komentáre</h4>
                        <div class="comment-list" id="comments-${data.post_id}">
                            <p>Žiadne komentáre.</p>
                        </div>

                        <!-- Comment form -->
                        <form method="POST" action="/comment/add/${data.post_id}/" class="comment-form" data-post-id="${data.post_id}" data-url="/comment/add/${data.post_id}/">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">
                            <input type="text" name="text" placeholder="Napíš komentár..." required>
                            <button type="submit">Pridať</button>
                        </form>
                    </div>
                `;

                // Insert the new post element into the page right after the first post-box element
                const container = document.querySelector('.container');
                container.insertBefore(newPost, container.querySelector('.post-box').nextSibling);

                // Reset the post form inputs
                form.reset();
                // Reset file name display
                document.getElementById('file-name').innerText = 'Žiadny súbor';

                // Attach comment and like form logic to the new post's forms
                newPost.querySelectorAll('.comment-form').forEach(addCommentFormLogic);
                newPost.querySelectorAll('.like-form').forEach(addLikeFormLogic);

            } catch (error) {
                // Show alert if the request fails
                alert('Chyba pri odoslaní požiadavky.');
            }
        });
    }
});
