function showFileName(input) {
    // Show the selected file name or "No file" if none selected
    const fileName = input.files.length > 0 ? input.files[0].name : "Žiadny súbor";
    document.getElementById("file-name").textContent = fileName;
}

document.addEventListener('DOMContentLoaded', function () {

    // Function to add logic to comment forms
    function addCommentFormLogic(form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault(); // Prevent default form submission

            // Use data-url attribute or form action for request URL
            const url = form.dataset.url || form.action;
            const textInput = form.querySelector('input[name="text"]');
            const text = textInput.value.trim();

            if (!text) return; // Do nothing if text is empty

            // Prepare form data for POST request
            const formData = new FormData();
            formData.append('text', text);
            formData.append('csrfmiddlewaretoken', form.querySelector('[name=csrfmiddlewaretoken]').value);

            // Send POST request with AJAX
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Identify AJAX request
                }
            });

            const data = await response.json();

            if (!response.ok) {
                // Show error alert if request failed
                alert(data.error || 'Chyba pri odoslaní komentára');
                return;
            }

            // Find the comment list container closest to this form
            const commentList = form.closest('.comments').querySelector('.comment-list');

            // Create new comment HTML block and add to comment list
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
            commentList.appendChild(newComment);

            textInput.value = ''; // Clear comment input after successful submission
        });
    }

    // Function to add logic to like forms
    function addLikeFormLogic(form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault(); // Prevent default form submission

            // Get CSRF token value from hidden input
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

            // Send POST request for like/unlike with AJAX
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // CSRF token for security
                    'X-Requested-With': 'XMLHttpRequest' // Identify AJAX request
                }
            });

            const data = await response.json();

            if (data.total_likes !== undefined) {
                // Update like count text if returned by server
                const likeCountSpan = form.querySelector('.like-count');
                likeCountSpan.textContent = `(${data.total_likes})`;
            }
        });
    }

    // Initialize comment and like form handlers on existing forms
    document.querySelectorAll('.comment-form').forEach(addCommentFormLogic);
    document.querySelectorAll('.like-form').forEach(addLikeFormLogic);

    // Handle new post submission
    const postForm = document.getElementById('post-form');
    if (postForm) {
        postForm.addEventListener('submit', async function (e) {
            e.preventDefault(); // Prevent default form submission

            const form = e.target;
            const formData = new FormData(form);
            const url = form.dataset.url;

            try {
                // Send AJAX POST request to create new post
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
                    // Show error alert if server returns an error
                    alert(data.error || 'Chyba pri vytváraní príspevku');
                    return;
                }

                // Create new post HTML element with received data
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
                        <form method="POST"
                              action="/comment/add/${data.post_id}/"
                              class="comment-form"
                              data-post-id="${data.post_id}"
                              data-url="/comment/add/${data.post_id}/">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">
                            <input type="text" name="text" placeholder="Napíš komentár..." required>
                            <button type="submit">Pridať</button>
                        </form>
                    </div>
                `;

                // Insert the new post right after the first post in the container
                const container = document.querySelector('.container');
                container.insertBefore(newPost, container.querySelector('.post-box').nextSibling);

                form.reset(); // Reset the post form inputs
                document.getElementById('file-name').innerText = 'Žiadny súbor'; // Reset file name display

                // Attach comment and like handlers to the newly created forms inside the new post
                newPost.querySelectorAll('.comment-form').forEach(addCommentFormLogic);
                newPost.querySelectorAll('.like-form').forEach(addLikeFormLogic);

            } catch (error) {
                // Handle network or other unexpected errors
                alert('Chyba pri odoslaní požiadavky.');
            }
        });
    }
});
