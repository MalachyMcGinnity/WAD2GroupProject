function applyReadMore() {
    const threshold = 200; // if the comment is longer than 200 characters - use readmore
    const commentElements = document.querySelectorAll('.comment-text');
    
    commentElements.forEach(function(el) {
        // If the element has already been processed, skip it
        if (el.dataset.readmoreApplied === "true") return;
        
        let fullText = el.textContent.trim();
        
        if (fullText.length > threshold) {
            let truncatedText = fullText.substring(0, threshold) + "... ";
            // Save full and truncated texts in data attributes
            el.dataset.full = fullText;
            el.dataset.truncated = truncatedText;
            el.dataset.expanded = "false";
            
            // Set truncated text
            el.textContent = truncatedText;
            
            // Create a "Read more" link
            const link = document.createElement('a');
            link.href = "#";
            link.className = "readmore-link";
            link.textContent = "Read more";
            
            // Add a link to the element
            el.appendChild(link);
            
            // Add a click handler
            link.addEventListener('click', function(e) {
                e.preventDefault();
                toggleReadMore(el);
            });
        }
        el.dataset.readmoreApplied = "true";
    });
}

function toggleReadMore(el) {
    if (el.dataset.expanded === "true") {
        // Show truncated text and "Read more" link
        el.textContent = el.dataset.truncated;
        const link = document.createElement('a');
        link.href = "#";
        link.className = "readmore-link";
        link.textContent = " Read more";
        el.appendChild(link);
        el.dataset.expanded = "false";
        link.addEventListener('click', function(e) {
            e.preventDefault();
            toggleReadMore(el);
        });
    } else {
        // Show full text and "Read less" link
        el.textContent = el.dataset.full;
        const link = document.createElement('a');
        link.href = "#";
        link.className = "readmore-link";
        link.textContent = " Read less";
        el.appendChild(link);
        el.dataset.expanded = "true";
        link.addEventListener('click', function(e) {
            e.preventDefault();
            toggleReadMore(el);
        });
    }
}

if (document.readyState !== 'loading') {
    applyReadMore();
} else {
    document.addEventListener('DOMContentLoaded', applyReadMore);
}
