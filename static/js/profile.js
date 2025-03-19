document.addEventListener("DOMContentLoaded", function() {
    const createAlbumButton = document.getElementById("create_album_button");
    if (createAlbumButton) {
        createAlbumButton.addEventListener("click", function() {
            window.location.href = createAlbumButton.getAttribute("data-url");
        });
    }
});