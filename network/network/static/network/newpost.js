document.addEventListener("DOMContentLoaded", function() {
    const USER_ID = document.getElementById("user-id").value;
    const postButton = document.getElementById("new-post-button");
    const postTextarea = document.getElementById("new-content");
    const postsContainer = document.getElementById("post-container")

    // Listen for event
    postButton.addEventListener("click", (event) => {
        event.preventDefault();
        const text = postTextarea.value.trim();
        
        // Post request to add the post to the database
        fetch("/newpost", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content: text, user_id: USER_ID })
        })
        // CS50.ai generated this code because I keep getting syntax errors
        .then(response => {
            if (response.ok) {
                addPostToUI(text);
            }
            window.location.reload();
        })
        .then(content => {
            console.log("Response from server:", content);
        })
        .catch(error => console.error("Error:", error));

        // Clear the textarea after posting
        postTextarea.value = "";
    });

    // Fetch all posts when the page loads
    fetch("/allposts")
    .then(response => response.json())
    .then(data => {
      console.log(data);
      console.log(typeof data);
        // Update the page with all posts
            data.forEach(post => addPostToUI(post));

    })
    .catch(error => console.error("Error:", error));

    // Add the post to the page
    function addPostToUI(post) {
        console.log(post)
        const postElement = document.createElement("div");
        postElement.classList.add("card-body", "my-card");

        const contentElement = document.createElement("p");
        const timeElement = document.createElement("p");
        const userElement = document.createElement("p");
        // Link element
        const userLink = document.createElement("a"); 

        postElement.textContent = post.post;
        userLink.href = `/profile/${post.user_id}/`;
        userLink.textContent = post.user;
        userElement.appendChild(userLink);
        timeElement.textContent = `Posted on: ${post.time_date}`;
        
        postElement.appendChild(contentElement);
        postElement.appendChild(timeElement);
        postElement.appendChild(userElement);

        postsContainer.appendChild(postElement);

        
    }

});