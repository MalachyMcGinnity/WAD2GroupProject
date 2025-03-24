document.addEventListener("DOMContentLoaded", function(){
    let ajaxCommentLoading = false;
    const commentForm = document.querySelector("#commentForm");

    // Function for displaying notifications
    function showAlert(message, type) {
        const alertDiv = document.createElement("div");
        alertDiv.className = "alert alert-" + type;
        alertDiv.textContent = message;
        commentForm.parentNode.insertBefore(alertDiv, commentForm);
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }

    if (commentForm) {
        commentForm.addEventListener("submit", function(event){
            event.preventDefault();
            if (ajaxCommentLoading) {
                return;
            }
            ajaxCommentLoading = true;
            // Get information about the pressed button, if available
            let submitterName = "";
            if (event.submitter && event.submitter.name) {
                submitterName = event.submitter.name;
            }
            const formData = new FormData(commentForm);
            // Add information about the pressed button to the form data
            if (submitterName) {
                formData.append(submitterName, event.submitter.value);
            }
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
                    // Update the comment input field
                    const textarea = commentForm.querySelector("textarea[name='text']");
                    if (textarea) {
                        textarea.value = data.comment_text;
                    }
                    // Update the main comment submit button
                    const submitButton = commentForm.querySelector("button[name='submit_comment']");
                    if (submitButton) {
                        submitButton.textContent = data.button_text;
                        submitButton.className = data.button_class;
                    }
                    // Update the main comment submit button
                    const deleteButton = commentForm.querySelector("button[name='delete_comment']");
                    if (deleteButton) {
                        if (data.show_delete_button === false) {
                            deleteButton.style.display = "none";
                        } else {
                            deleteButton.style.display = "";
                        }
                    }
                    // Update the average rating if available
                    const avgRatingElement = document.getElementById("avgRating");
                    if (avgRatingElement && data.average_rating !== undefined) {
                        avgRatingElement.textContent = data.average_rating;
                    }
                    showAlert(data.message, "success");
                } else {
                    showAlert(data.message, "danger");
                }
            })
            .catch(error => {
                console.error("Error submitting comment via AJAX:", error);
                showAlert("Error submitting comment, please try again.", "danger");
            })
            .finally(() => {
                ajaxCommentLoading = false;
            });
        });
    }
});
