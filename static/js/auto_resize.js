document.addEventListener("DOMContentLoaded", function() {
    var textarea = document.getElementById("text");
    var charCountElem = document.getElementById("charCount");
    if (textarea) {
        textarea.addEventListener("input", function() {
            // Automatic height change
            this.style.height = "auto";
            this.style.height = this.scrollHeight + "px";
            // Update character counter
            if (charCountElem) {
                charCountElem.textContent = this.value.length + "/1500 characters";
            }
        });
        // Initialization on page load
        textarea.style.height = textarea.scrollHeight + "px";
        if (charCountElem) {
            charCountElem.textContent = textarea.value.length + "/1500 characters";
        }
    }
});
