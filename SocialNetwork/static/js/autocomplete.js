document.addEventListener('DOMContentLoaded', function () {
    // Wait until the DOM is fully loaded before executing this code
    const input = document.getElementById('searchInput'); // Get the search input field
    const suggestions = document.getElementById('suggestionsList'); // Get the container for displaying suggestions

    if (input && suggestions) {
        input.addEventListener('input', function () {
            const query = this.value; // Get the current input value

            if (query.length > 1) {
                // Only send request if the input is longer than 1 character
                fetch(`/search/suggestions/?q=${encodeURIComponent(query)}`) // Send GET request to the server
                    .then(response => response.json()) // Parse the JSON response
                    .then(data => {
                        suggestions.innerHTML = ''; // Clear previous suggestions

                        // Display matching users
                        data.users.forEach(user => {
                            const li = document.createElement('li'); // Create a list item
                            li.innerHTML = `<span class="icon">👤</span> ${user.username}`; // Show user with icon
                            li.style.padding = '10px 15px'; // Style for padding
                            li.style.cursor = 'pointer'; // Make it look clickable
                            li.onclick = () => {
                                window.location.href = `/profile/${user.username}/`; // Redirect to user's profile
                            };
                            suggestions.appendChild(li); // Add to suggestions list
                        });

                        // Display matching posts
                        data.posts.forEach(post => {
                            const li = document.createElement('li'); // Create a list item
                            li.innerHTML = `<span class="icon">📝</span> ${post.content.slice(0, 50)}...`; // Show post snippet with icon
                            li.style.padding = '10px 15px'; // Style for padding
                            li.style.cursor = 'pointer'; // Make it look clickable
                            li.onclick = () => {
                                window.location.href = `/profile/${post.user__username}/`; 
                                // Or use `/post/${post.id}/` if you want to redirect to post details
                            };
                            suggestions.appendChild(li); // Add to suggestions list
                        });
                    });
            } else {
                // Clear suggestions if input is too short
                suggestions.innerHTML = '';
            }
        });

        // Hide suggestions when clicking outside the autocomplete area
        document.addEventListener('click', function (e) {
            if (!e.target.closest('.autocomplete-wrapper')) {
                suggestions.innerHTML = '';
            }
        });
    }
});
