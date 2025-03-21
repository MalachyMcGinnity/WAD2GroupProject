document.addEventListener("DOMContentLoaded", function(){
    const threshold = 100; // character threshold for truncation
    const commentElements = document.querySelectorAll(".comment-text");
    
    commentElements.forEach(el => {
        const fullText = el.textContent.trim();
        if (fullText.length > threshold) {
            const truncated = fullText.slice(0, threshold) + "... ";
            // create a "Read more" link
            const readMoreLink = document.createElement("a");
            readMoreLink.href = "#";
            readMoreLink.textContent = "Read more";
            readMoreLink.style.color = "#007bff";
            readMoreLink.addEventListener("click", function(event){
                event.preventDefault();
                // if the text is truncated, expand the full text, otherwise collapse it back
                if (el.getAttribute("data-expanded") === "true") {
                    el.innerHTML = truncated;
                    el.appendChild(readMoreLink);
                    el.setAttribute("data-expanded", "false");
                } else {
                    el.textContent = fullText;
                    // create a "Read less" link for collapsing
                    const readLessLink = document.createElement("a");
                    readLessLink.href = "#";
                    readLessLink.textContent = " Read less";
                    readLessLink.style.color = "#007bff";
                    readLessLink.addEventListener("click", function(event){
                        event.preventDefault();
                        el.innerHTML = truncated;
                        el.appendChild(readMoreLink);
                        el.setAttribute("data-expanded", "false");
                    });
                    el.appendChild(readLessLink);
                    el.setAttribute("data-expanded", "true");
                }
            });
            el.innerHTML = truncated;
            el.appendChild(readMoreLink);
            el.setAttribute("data-expanded", "false");
        }
    });
});
