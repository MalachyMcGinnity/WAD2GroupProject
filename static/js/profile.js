document.addEventListener("DOMContentLoaded", function() {
    const createAlbumButton = document.getElementById("create_album_button");
    const changePasswordButton = document.getElementById("change_password_button");
    const deleteAccountButton = document.getElementById("delete_account_button")
    if (createAlbumButton) {
        createAlbumButton.addEventListener("click", function() {
            window.location.href = createAlbumButton.getAttribute("data-url");
        });
    }
    if (changePasswordButton) {
        changePasswordButton.addEventListener("click", function() {
            window.location.href = changePasswordButton.getAttribute("data-url");
        });
    }
    if (deleteAccountButton) {
        deleteAccountButton.addEventListener("click", function() {
            window.location.href = deleteAccountButton.getAttribute("data-url");
        });
    }
});