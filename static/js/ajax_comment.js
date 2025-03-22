document.addEventListener("DOMContentLoaded", function(){
    const commentForm = document.querySelector("#commentForm");
    if (commentForm) {
        commentForm.addEventListener("submit", function(event){
            event.preventDefault();
            const formData = new FormData(commentForm);
            const url = commentForm.action;
            fetch(url, {
                method: "POST",
                headers: {"X-Requested-With": "XMLHttpRequest"},
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    // Update the comment container
                    const commentsContainer = document.getElementById("commentsContainer");
                    if (commentsContainer) {
                        commentsContainer.innerHTML = data.comments_html;
                        if (typeof applyReadMore === 'function') {
                            applyReadMore();
                        }
                    }
                    // Update the text in the comment field (textarea)
                    const textarea = commentForm.querySelector("textarea[name='text']");
                    if (textarea) {
                        textarea.value = data.comment_text;
                    }
                    // Update the button: change the name and class (color)
                    const submitButton = commentForm.querySelector("button[type='submit']");
                    if (submitButton) {
                        submitButton.textContent = data.button_text;
                        submitButton.className = data.button_class;
                    }
                    // Update the display of the average rating
                    const avgRatingElement = document.getElementById("avgRating");
                    if (avgRatingElement && data.average_rating !== undefined) {
                        avgRatingElement.textContent = data.average_rating;
                    }
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error("Error submitting comment via AJAX:", error));
        });
    }
});
