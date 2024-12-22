document.addEventListener("DOMContentLoaded", function() {
    const editButtons = document.querySelectorAll(".edit_buttons");
    const saveButtons = document.querySelectorAll(".save_buttons");
    const likeButtons = document.querySelectorAll(".like_buttons");

    // When the "Edit" button is clicked
    editButtons.forEach(button => {
        button.addEventListener("click", function() {
            const postId = this.getAttribute("data-post-id");
            const contentView = document.getElementById(`content-view-${postId}`);
            const editView = document.getElementById(`edit-view-${postId}`);

            // Toggle between content and edit view
            contentView.style.display = "none";
            editView.style.display = "block";
        });
    });


    // When the "save" button is clicked
    saveButtons.forEach(button => {
        button.addEventListener("click", function() {
            // post_id from save button
            const postId = this.getAttribute("data-post-id");
            const text_area = document.getElementById(`text-area-${postId}`);
            const new_content = text_area.value

            fetch(`/edit/${postId}`, {
                method: 'PUT',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}",
                },
                body: JSON.stringify({
                    content: new_content
                })
              })
            .then(response => response.json())
            .then(data => {
            // ... do something else with emails ...
                if (data.success == true) {
                // Update the content view
                const contentView = document.getElementById(`content-view-${postId}`);
                const editView = document.getElementById(`edit-view-${postId}`);
                contentView.innerHTML =`<p>${new_content}</p>`;

                // Hide edit view and show content view                
                contentView.style.display = "block";
                editView.style.display = "none";
                }
            });            
        });
    });
    

    // When the "Edit" button is clicked
    likeButtons.forEach(button => {
        button.addEventListener("click", function() {
            const postId = this.getAttribute("data-post-id");

            // fetch call with put method?
            fetch(`/like/${postId}`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}",
                },
                body: JSON.stringify({
                    post_id: postId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success == true) {
                    // get elements: counter and like button
                    const counter_span = document.getElementById(`like-count-${postId}`);
                    
                    // could have used a dynamic id in html, trying a different method here for getting like button
                    const likeButton = document.querySelector(`.like_buttons[data-post-id="${postId}"]`);

                    // console.log(counter_span)
                    counter_span.innerText = `${data.count_likes} Likes`
                    
                    if (data.liked){
                        likeButton.innerText = "Unlike"
                    }
                    else {
                        likeButton.innerText = "Like"
                    }
                    
                }
            })
        })                        
    })
});


